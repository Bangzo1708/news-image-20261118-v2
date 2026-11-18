// news-image-20261118, round 2 — "The world in one day: 18 November 2026".
//
// The entry image is entry.png beside this file: a newspaper front page
// composed offline from six editorial illustrations of the day's top
// stories (Gulf strikes, Crimea bridge, Shenzhen summit, Alaska Senate,
// Ebola in DR Congo, Cyclone Xavier), with the date WEDNESDAY 18 NOVEMBER
// 2026 across the top. This program does nothing creative at run time: it
// copies that finished PNG into the grader's output directory.
//
// It runs with no network and no randomness, so two runs write byte-identical
// files. Node 22, standard library only.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { closeSync, copyFileSync, mkdirSync, openSync, readSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The PNG magic bytes every valid PNG starts with.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576; // the gate's 1 MiB limit

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

// Check the header only (8 bytes), without loading the whole image.
const fd = openSync(source, 'r');
try {
  const head = Buffer.alloc(8);
  if (readSync(fd, head, 0, 8, 0) !== 8 || !head.equals(PNG_SIGNATURE)) {
    throw new Error('entry.png is not a PNG file');
  }
} finally {
  closeSync(fd);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const bytes = statSync(target).size;
if (bytes > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB limit`);
}

console.log(`wrote ${target} (${bytes} bytes)`);
