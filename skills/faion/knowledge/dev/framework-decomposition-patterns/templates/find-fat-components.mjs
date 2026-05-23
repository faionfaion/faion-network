#!/usr/bin/env node
// purpose: list React components over 150 LOC for hook extraction.
// consumes: src-dir (default ./src).
// produces: stdout LOC + path of fat components, sorted descending.
// depends-on: node >= 18 (fs/promises, glob).
// token-budget-impact: ~80 tokens (helper only).

// find-fat-components.mjs — list React components over 150 LOC for hook extraction
// Usage: node find-fat-components.mjs [src-dir]
// Output: LOC and file path, sorted descending

import { readFileSync } from 'node:fs';
import { globSync } from 'glob';

const srcDir = process.argv[2] || 'src';
const threshold = 150;

const results = [];
for (const f of globSync(`${srcDir}/**/*.{tsx,jsx}`)) {
  const loc = readFileSync(f, 'utf8').split('\n').length;
  if (loc > threshold) results.push({ loc, file: f });
}
results.sort((a, b) => b.loc - a.loc);
for (const { loc, file } of results) console.log(loc, file);
