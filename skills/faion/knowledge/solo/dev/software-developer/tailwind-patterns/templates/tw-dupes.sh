#!/usr/bin/env bash
# tw-dupes.sh — find Tailwind className strings duplicated across 3+ components.
# Usage: bash tw-dupes.sh [src-dir]
# Exit 1 if duplicates found.
set -euo pipefail
ROOT="${1:-src}"
node - "$ROOT" <<'JS'
const fs = require('fs'), path = require('path');
const root = process.argv[2];
const re = /className\s*=\s*["'`]([^"'`]+)["'`]/g;
const map = new Map();
function walk(d) {
  for (const f of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, f.name);
    if (f.isDirectory()) walk(p);
    else if (/\.(tsx|jsx|astro|svelte|vue)$/.test(f.name)) {
      const src = fs.readFileSync(p, 'utf8');
      let m;
      while ((m = re.exec(src))) {
        const norm = m[1].split(/\s+/).filter(Boolean).sort().join(' ');
        if (norm.split(' ').length < 3) continue;
        if (!map.has(norm)) map.set(norm, []);
        map.get(norm).push(p);
      }
    }
  }
}
walk(root);
const dupes = [...map.entries()].filter(([, v]) => new Set(v).size >= 3);
dupes.sort((a, b) => b[1].length - a[1].length);
for (const [cls, files] of dupes.slice(0, 30)) {
  console.log(`# ${files.length}x  ${cls}`);
  for (const f of [...new Set(files)]) console.log(`  ${f}`);
}
process.exit(dupes.length ? 1 : 0);
JS
