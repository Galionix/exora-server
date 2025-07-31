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

const ROOT_RESOURCES_PATH = './public/resources';
const BUCKET_NAME = process.env.AWS_S3_BUCKET;
const OUTPUT_RESOURCES_TS = './public/resources.ts';

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

async function uploadFileToS3(filePath, s3Key) {
  const fileData = await fs.readFile(filePath);
  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
    Body: fileData,
  });
  await s3.send(command);
  console.log(`Uploaded: ${s3Key}`);
}

async function deleteFileFromS3(s3Key) {
  const command = new DeleteObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
  });
  await s3.send(command);
  console.log(`Deleted: ${s3Key}`);
}

async function downloadManifestFromS3(s3Key) {
  try {
    const command = new GetObjectCommand({
      Bucket: BUCKET_NAME,
      Key: s3Key,
    });
    const response = await s3.send(command);
    if (!response.Body) throw new Error('Empty manifest body');
    const chunks = [];
    for await (const chunk of response.Body) {
      chunks.push(chunk);
    }
    return JSON.parse(Buffer.concat(chunks).toString('utf-8'));
  } catch (e) {
    console.warn(`No old manifest for ${s3Key} or error:`, e.message);
    return null;
  }
}

async function generateFolderMetadata(folderPath) {
  const entries = await fs.readdir(folderPath, { withFileTypes: true });
  const metadata = [];

  for (const entry of entries) {
    if (entry.isDirectory()) continue;
    if (entry.name === 'manifest.json') continue;

    const fileName = entry.name;
    const fullPath = path.join(folderPath, fileName);
    const stat = await fs.stat(fullPath);

    const hash = await getFileHash(fullPath);
    const ext = path.extname(fileName).slice(1);

    metadata.push({
      fileName,
      hash,
      size: stat.size,
      lastModified: stat.mtime.toISOString(),
      ext,
    });
  }

  return metadata;
}

function wrapManifest(files) {
  const manifestHash = crypto
    .createHash('sha256')
    .update(JSON.stringify(files))
    .digest('hex');
  return {
    generatedAt: new Date().toISOString(),
    manifestHash,
    files,
  };
}

async function uploadManifestToS3(manifest, s3Key) {
  const body = Buffer.from(JSON.stringify(manifest, null, 2), 'utf-8');
  const command = new PutObjectCommand({
    Bucket: BUCKET_NAME,
    Key: s3Key,
    Body: body,
    ContentType: 'application/json',
  });
  await s3.send(command);
  console.log(`Manifest uploaded: ${s3Key}`);
}

// Рекурсивный обход + наполнение registry
async function processResourceFolder(localPath, s3Prefix, registry, flatPaths) {
  console.log(`Processing: ${localPath}`);

  const remoteManifestKey = `${s3Prefix}manifest.json`;
  const oldManifest = await downloadManifestFromS3(remoteManifestKey);
  const oldFiles = oldManifest?.files || [];

  const filesMetadata = await generateFolderMetadata(localPath);
  const finalManifest = wrapManifest(filesMetadata);

  const localManifestPath = path.join(localPath, 'manifest.json');
  await fs.writeFile(
    localManifestPath,
    JSON.stringify(finalManifest, null, 2),
    'utf-8',
  );
  console.log(`Local manifest saved: ${localManifestPath}`);

  const newFilesMap = new Map(filesMetadata.map((f) => [f.fileName, f.hash]));
  const filesToDelete = oldFiles.filter((f) => {
    const newHash = newFilesMap.get(f.fileName);
    return !newHash || newHash !== f.hash;
  });

  for (const file of filesToDelete) {
    const key = `${s3Prefix}${file.fileName}`;
    await deleteFileFromS3(key);
  }

  for (const file of filesMetadata) {
    const relPath = path
      .relative(ROOT_RESOURCES_PATH, path.join(localPath, file.fileName))
      .replace(/\\/g, '/');

    flatPaths.push(relPath);
    const oldFile = oldFiles.find((f) => f.fileName === file.fileName);
    if (oldFile && oldFile.hash === file.hash) {
      console.log(`Skipped unchanged: ${file.fileName}`);
      continue;
    }
    const filePath = path.join(localPath, file.fileName);
    const key = `${s3Prefix}${file.fileName}`;
    await uploadFileToS3(filePath, key);
  }

  await uploadManifestToS3(finalManifest, remoteManifestKey);

  // === Добавляем файлы в registry ===
  for (const file of filesMetadata) {
    const parts = [file.fileName.replace(/\.[^/.]+$/, '')]; // имя файла без расширения

    let node = registry;
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      if (i === parts.length - 1) {
        // Финальный узел — пишем путь
        const relPath = path
          .relative(ROOT_RESOURCES_PATH, path.join(localPath, file.fileName))
          .replace(/\\/g, '/');
        node[part] = relPath;
      } else {
        if (!node[part]) node[part] = {};
        node = node[part];
      }
    }
  }
  // === Рекурсивно подпапки ===
  const entries = await fs.readdir(localPath, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      const subfolderPath = path.join(localPath, entry.name);
      const subfolderS3Prefix = `${s3Prefix}${entry.name}/`;

      if (!registry[entry.name]) registry[entry.name] = {};
      await processResourceFolder(
        subfolderPath,
        subfolderS3Prefix,
        registry[entry.name],
        flatPaths,
      );
    }
  }
}

async function main() {
  const registry = {};
  const flatPaths = [];
  await processResourceFolder(ROOT_RESOURCES_PATH, '', registry, flatPaths);

  const content = `
export const RESOURCES = ${JSON.stringify(registry, null, 2)};
export const RESOURCE_PATHS = ${JSON.stringify(flatPaths, null, 2)};
`;

  await fs.writeFile(OUTPUT_RESOURCES_TS, content, 'utf-8');
  console.log(`✅ resources.ts generated: ${OUTPUT_RESOURCES_TS}`);
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
