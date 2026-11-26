import { copyFileSync, mkdirSync, statSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point: copy entry.png next to this file to $MAKEFUN_OUTPUT_DIR.
// The source is resolved relative to the script directory, never the
// process working directory: MAKEFUN_BOT_DIR when set, otherwise the
// directory containing main.ts itself. That keeps grader runs from a
// foreign working directory working.
const MAX_BYTES = 1048576;

function fail(message) {
  console.error(message);
  process.exit(1);
}

const botDir = (process.env.MAKEFUN_BOT_DIR || "").trim();
const scriptDir = botDir ? resolve(botDir) : dirname(fileURLToPath(import.meta.url));

const source = join(scriptDir, "entry.png");
const outDir = (process.env.MAKEFUN_OUTPUT_DIR || "").trim()
  ? resolve(process.env.MAKEFUN_OUTPUT_DIR)
  : "/output";
const dest = join(outDir, "entry.png");

let data;
try {
  data = readFileSync(source);
} catch {
  fail("entry.png not found next to main.ts");
}

const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const jpegMagic = Buffer.from([0xff, 0xd8, 0xff]);
if (data.length < 3) {
  fail("entry.png is too short to be an image file");
}
if (!data.subarray(0, 8).equals(pngMagic) && !data.subarray(0, 3).equals(jpegMagic)) {
  fail("entry.png is not a PNG or JPEG file");
}
if (data.length > MAX_BYTES) {
  fail("entry.png is larger than 1 MiB: " + data.length + " bytes");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
const copied = statSync(dest).size;
if (copied !== data.length) {
  fail("copied size mismatch: " + copied + " vs " + data.length);
}
console.log("Wrote " + dest + " (" + copied + " bytes)");
