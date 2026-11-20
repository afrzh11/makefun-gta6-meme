// Entry point for the gta6-meme-x-01 submission.
//
// The whole entry lives in one small file, POST.json, which points at the
// meme post on X. This program's single job is to carry that file from the
// bot directory into the output directory so the grader can pick it up.
//
// Before copying, the file is sanity-checked: it has to be a JSON object
// whose "url" field holds an X (or Twitter) status link. A malformed
// pointer would sink the entry at the gate, so it is cheaper to fail loudly
// here than to hand over garbage. The copy itself is byte-for-byte — the
// grader compares the output against the original, so nothing is
// reformatted along the way.
//
// Locations come from the environment:
//   MAKEFUN_BOT_DIR    where POST.json is read from   (default: /bot)
//   MAKEFUN_OUTPUT_DIR where POST.json is written to  (default: /output)
// On success the program prints nothing. On any failure it explains itself
// on stderr and exits with a non-zero status.

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const SOURCE_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const TARGET_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const FILE_NAME = 'POST.json';

// An X status address looks like:
//   https://x.com/<handle>/status/<numeric id>
// The older twitter.com host names the same thing and is accepted too.
const STATUS_LINK = /^https?:\/\/(?:www\.)?(?:x\.com|twitter\.com)\/[^/?#]+\/status\/\d+\/?$/;

function loadPointer(path: string): Buffer {
  let raw: Buffer;
  try {
    raw = readFileSync(path);
  } catch (err) {
    throw new Error(`cannot read ${path}: ${(err as Error).message}`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw.toString('utf8'));
  } catch (err) {
    throw new Error(`${FILE_NAME} is not valid JSON: ${(err as Error).message}`);
  }

  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    throw new Error(`${FILE_NAME} must hold a JSON object, not ${Array.isArray(parsed) ? 'an array' : typeof parsed}`);
  }

  const link = (parsed as Record<string, unknown>).url;
  if (typeof link !== 'string' || !STATUS_LINK.test(link)) {
    throw new Error(
      `${FILE_NAME} field "url" must be an X status link (https://x.com/<handle>/status/<id>); got ${JSON.stringify(link)}`,
    );
  }

  return raw;
}

function run(): void {
  const bytes = loadPointer(join(SOURCE_DIR, FILE_NAME));
  mkdirSync(TARGET_DIR, { recursive: true });
  writeFileSync(join(TARGET_DIR, FILE_NAME), bytes);
}

try {
  run();
} catch (err) {
  console.error(`main: ${(err as Error).message}`);
  process.exit(1);
}
