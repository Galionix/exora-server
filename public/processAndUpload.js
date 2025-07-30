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

// valid for launching with npm
// const OUTPUT_JSON = './public/chunks-manifest.json';
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
    return [];
  }
}

async function generateManifest() {
  const files = await fs.readdir(FOLDER_PATH);
  const manifest = [];

  for (const fileName of files) {
    const fullPath = path.join(FOLDER_PATH, fileName);
    const stat = await fs.stat(fullPath);
    if (!stat.isFile()) continue;

    const hash = await getFileHash(fullPath);
    const match = fileName.match(/^(x\d+y\d+)/);
    const chunkName = match ? match[1] : null;
    const ext = path.extname(fileName).slice(1); // убираем точку

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
  // Скачиваем старый манифест из S3
  const oldManifest = await downloadManifestFromS3();

  // Генерируем новый локальный манифест
  const newManifest = await generateManifest();

  // Сравниваем и удаляем устаревшие файлы из S3
  const newFilesMap = new Map(newManifest.map((f) => [`${f.chunkName}-${f.ext}`,f.hash
  ]));
  const newFilesNames = newManifest.map((f) => f.fileName);
  const filesToDelete = oldManifest.filter(
    (f) =>
    {
      if (!newFilesNames.includes(f.fileName)) {
        console.log('there is no file in new with such name, need to delete: ', `${f.fileName} ${f.chunkName}-${f.ext}`);
        return true
      }
      /*
      короче тут нужно написать логику которая будет смотреть
      есть ли у нас такой же чанк на сервере с таким же форматом но с другим хешем
      если есть то мы его удаляем
      */
      const oldFileExists = newFilesMap.has(`${f.chunkName}-${f.ext}`)

      if (oldFileExists) {
        if (f.hash !== newFilesMap.get(`${f.chunkName}-${f.ext}`)) {
          // hash changed, need to delete
          console.log('hash changed, need to delete: ', `${f.fileName} ${f.chunkName}-${f.ext}`);
          return true
        }
      }
    },
  );

  console.log('filesToDelete: ', filesToDelete);
  for (const file of filesToDelete) {
    const key = S3_PREFIX + file.fileName;
    await deleteFileFromS3(key);
  }

  // Загружаем новые и изменённые файлы
  for (const file of newManifest) {
    const oldFile = oldManifest.find((f) => f.fileName === file.fileName);
    if (oldFile && oldFile.hash === file.hash) {
      console.log(`Skipped upload (unchanged): ${file.fileName}`);
      continue;
    }
    const filePath = path.join(FOLDER_PATH, file.fileName);
    const key = S3_PREFIX + file.fileName;
    await uploadFileToS3(filePath, key);
  }

  // Сохраняем локальный манифест (опционально)
  await fs.writeFile(
    LOCAL_MANIFEST_PATH,
    JSON.stringify(newManifest, null, 2),
    'utf-8',
  );
  console.log(`Local manifest saved to ${LOCAL_MANIFEST_PATH}`);

  // Загружаем новый манифест в S3
  await uploadManifestToS3(newManifest);
}
main().catch((err) => {
  console.error('Error in upload process:', err);
  process.exit(1);
});
