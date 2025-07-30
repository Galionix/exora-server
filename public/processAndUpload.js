import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

import {
  S3Client,
  PutObjectCommand,
  DeleteObjectCommand,
  GetObjectCommand,
} from '@aws-sdk/client-s3';

import dotenv from 'dotenv';
dotenv.config();

const FOLDER_PATH = './public/chunks';
const LOCAL_MANIFEST_PATH = './public/chunks-manifest.json';
const REMOTE_MANIFEST_KEY = 'chunks-manifest.json';

const BUCKET_NAME = process.env.AWS_S3_BUCKET;
const S3_PREFIX = 'chunks/';

const s3 = new S3Client({
  region: process.env.NEXT_PUBLIC_AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

async function getFileHash(filePath) {
  const data = await fs.readFile(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

async function uploadFileToS3(filePath, key) {
  const fileData = await fs.readFile(filePath);
  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
    Body: fileData,
  });
  await s3.send(command);
  console.log(`Uploaded: ${key}`);
}

async function deleteFileFromS3(key) {
  const command = new DeleteObjectCommand({
    Bucket: BUCKET_NAME,
    Key: key,
  });
  await s3.send(command);
  console.log(`Deleted: ${key}`);
}

async function downloadManifestFromS3() {
  try {
    const command = new GetObjectCommand({
      Bucket: BUCKET_NAME,
      Key: REMOTE_MANIFEST_KEY,
    });
    const response = await s3.send(command);

    if (!response.Body) throw new Error('Empty manifest body from S3');

    const stream = response.Body;

    const chunks = [];
    for await (const chunk of stream) {
      chunks.push(chunk);
    }
    const buffer = Buffer.concat(chunks);
    const jsonString = buffer.toString('utf-8');
    const manifest = JSON.parse(jsonString);

    console.log('Old manifest downloaded from S3');
    return manifest;
  } catch (e) {
    console.warn('Old manifest not found in S3 or error:', e.message);
    return null;
  }
}

async function generateChunksMetadata() {
  const files = await fs.readdir(FOLDER_PATH);
  const manifest = [];

  for (const fileName of files) {
    const fullPath = path.join(FOLDER_PATH, fileName);
    const stat = await fs.stat(fullPath);
    if (!stat.isFile()) continue;

    const hash = await getFileHash(fullPath);
    const match = fileName.match(/^(x\d+y\d+)/);
    const chunkName = match ? match[1] : null;
    const ext = path.extname(fileName).slice(1);

    manifest.push({
      fileName,
      size: stat.size,
      lastModified: stat.mtime.toISOString(),
      hash,
      chunkName,
      ext,
    });
  }

  return manifest;
}

function generateManifestWrapper(chunksMetadata) {
  const tempString = JSON.stringify(chunksMetadata);
  const manifestHash = crypto.createHash('sha256').update(tempString).digest('hex');

  return {
    generatedAt: new Date().toISOString(),
    manifestHash,
    chunksMetadata,
  };
}

async function uploadManifestToS3(manifest) {
  const manifestBuffer = Buffer.from(
    JSON.stringify(manifest, null, 2),
    'utf-8',
  );
  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: REMOTE_MANIFEST_KEY,
    Body: manifestBuffer,
    ContentType: 'application/json',
  });
  await s3.send(command);
  console.log(`Manifest uploaded to S3 as ${REMOTE_MANIFEST_KEY}`);
}

async function main() {
  const oldManifest = await downloadManifestFromS3();
  const oldChunks = oldManifest?.chunksMetadata || [];

  const chunksMetadata = await generateChunksMetadata();
  const finalManifest = generateManifestWrapper(chunksMetadata);

  // Логика удаления устаревших файлов:
  const newFilesMap = new Map(chunksMetadata.map((f) => [`${f.chunkName}-${f.ext}`, f.hash]));
  const newFilesNames = chunksMetadata.map((f) => f.fileName);

  const filesToDelete = oldChunks.filter((f) => {
    if (!newFilesNames.includes(f.fileName)) {
      console.log('File missing, need to delete:', f.fileName);
      return true;
    }
    const exists = newFilesMap.has(`${f.chunkName}-${f.ext}`);
    if (exists && newFilesMap.get(`${f.chunkName}-${f.ext}`) !== f.hash) {
      console.log('Hash changed, need to delete:', f.fileName);
      return true;
    }
    return false;
  });

  console.log('Files to delete:', filesToDelete.map(f => f.fileName));

  for (const file of filesToDelete) {
    const key = S3_PREFIX + file.fileName;
    await deleteFileFromS3(key);
  }

  for (const file of chunksMetadata) {
    const oldFile = oldChunks.find((f) => f.fileName === file.fileName);
    if (oldFile && oldFile.hash === file.hash) {
      console.log(`Skipped upload (unchanged): ${file.fileName}`);
      continue;
    }
    const filePath = path.join(FOLDER_PATH, file.fileName);
    const key = S3_PREFIX + file.fileName;
    await uploadFileToS3(filePath, key);
  }

  await fs.writeFile(
    LOCAL_MANIFEST_PATH,
    JSON.stringify(finalManifest, null, 2),
    'utf-8',
  );
  console.log(`Local manifest saved to ${LOCAL_MANIFEST_PATH}`);

  await uploadManifestToS3(finalManifest);
}

main().catch((err) => {
  console.error('Error in upload process:', err);
  process.exit(1);
});
