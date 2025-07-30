import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';

const FOLDER_PATH = './chunks'; // локальная папка с файлами
const OUTPUT_JSON = './chunks-manifest.json';

async function getFileHash(filePath) {
  const data = await fs.readFile(filePath);
  return crypto.createHash('sha256').update(data).digest('hex');
}

async function generateManifest() {
  const files = await fs.readdir(FOLDER_PATH);
  const manifest = [];

  for (const fileName of files) {
    const match = fileName.match(/^(x\d+y\d+)/);
    const chunkName = match ? match[1] : null;
    console.log('chunkName: ', chunkName);
    const fullPath = path.join(FOLDER_PATH, fileName);
    const stat = await fs.stat(fullPath);
    if (!stat.isFile()) continue;

    const hash = await getFileHash(fullPath);
    const ext = path.extname(fileName).slice(1); // убираем точку
    manifest.push({
      fileName,
      size: stat.size,
      lastModified: stat.mtime.toISOString(),
      hash,
      chunkName,
      ext
    });
  }

  await fs.writeFile(OUTPUT_JSON, JSON.stringify(manifest, null, 2), 'utf-8');
  console.log(
    `Manifest saved to ${OUTPUT_JSON}, total files: ${manifest.length}`,
  );
}

generateManifest().catch((err) => {
  console.error('Error generating manifest:', err);
  process.exit(1);
});
