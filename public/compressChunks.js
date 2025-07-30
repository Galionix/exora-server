import fs from 'fs';
import path from 'path';
import * as tar from 'tar';

import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CHUNKS_DIR = path.join(__dirname, 'chunks');

async function run() {
  const files = await fs.promises.readdir(CHUNKS_DIR);

  // Только несжатые файлы
  const filesToCompress = files.filter(name => !name.endsWith('.gz') && !name.endsWith('.tar.gz'));

  // Извлекаем ключ xNyN
  const chunkKeys = filesToCompress.map(name => {
    const match = name.match(/^(x\d+y\d+)/);
    return match ? match[1] : null;
  }).filter(Boolean);

  const uniqueKeys = Array.from(new Set(chunkKeys));

  for (const key of uniqueKeys) {
    const groupFiles = filesToCompress.filter(name => name.startsWith(key));

    if (groupFiles.length === 0) continue;

    const outputTarGz = path.join(CHUNKS_DIR, `${key}.tar.gz`);

    if (fs.existsSync(outputTarGz)) {
      await fs.promises.unlink(outputTarGz);
    }

    // Создаём tar.gz
    await tar.c(
      {
        gzip: true,
        file: outputTarGz,
        cwd: CHUNKS_DIR,

      },
      groupFiles
    );

    // Удаляем исходники
    for (const file of groupFiles) {
      const filePath = path.join(CHUNKS_DIR, file);
      await fs.promises.unlink(filePath);
    }

    console.log(`Created: ${key}.tar.gz`);
  }

  console.log('✅ Done!');
}

run().catch(console.error);
