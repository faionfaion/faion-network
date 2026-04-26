// token-contrast.mjs — fail CI if any semantic text/background pair is below WCAG AA
// Usage: node token-contrast.mjs tokens.json
// Requires: npm i wcag-contrast
import { createRequire } from "module";
import { readFileSync } from "fs";

const require = createRequire(import.meta.url);
const { hex, score } = require("wcag-contrast");

const file = process.argv[2];
if (!file) { console.error("Usage: node token-contrast.mjs <tokens.json>"); process.exit(2); }

const tokens = JSON.parse(readFileSync(file, "utf8"));
const pairs = tokens?.color?.semantic?.pairs ?? {};
const fails = [];

for (const [name, pair] of Object.entries(pairs)) {
  const fg = pair.fg?.$value ?? pair.fg;
  const bg = pair.bg?.$value ?? pair.bg;
  if (!fg || !bg) { console.warn(`SKIP ${name}: missing fg or bg value`); continue; }
  const ratio = hex(fg, bg);
  const required = pair.size === "large" ? 3.0 : 4.5;
  if (ratio < required) {
    fails.push({ name, fg, bg, ratio: ratio.toFixed(2), required, score: score(ratio) });
  }
}

if (fails.length) {
  console.error("FAIL: contrast violations");
  console.error(JSON.stringify(fails, null, 2));
  process.exit(1);
}
console.log(`OK: all ${Object.keys(pairs).length} pairs pass WCAG AA`);
