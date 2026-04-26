#!/usr/bin/env bash
# audit-routes.sh — flag route handlers missing schema, auth, or error wiring.
# Usage: audit-routes.sh src/routes
# Exits 1 if any issues found; wire into pre-commit.
set -euo pipefail
dir="${1:-src/routes}"
node - <<'JS' "$dir"
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
const root = process.argv[1];
const issues = [];
const walk = (d) => readdirSync(d).flatMap(f => {
  const p = join(d, f);
  return statSync(p).isDirectory() ? walk(p) : [p];
});
for (const file of walk(root).filter(f => /\.routes?\.ts$/.test(f))) {
  const src = readFileSync(file, 'utf8');
  const verbs = [...src.matchAll(/\.(get|post|put|patch|delete)\(/g)];
  for (const m of verbs) {
    const idx = m.index;
    const window = src.slice(idx, idx + 600);
    if (!/schema\s*:/i.test(window))
      issues.push(`${file}: ${m[1].toUpperCase()} missing schema near offset ${idx}`);
    if (m[1] !== 'get' && !/(authenticate|preHandler)/.test(window))
      issues.push(`${file}: ${m[1].toUpperCase()} missing auth/preHandler near offset ${idx}`);
  }
  if (!/setErrorHandler|errorHandler|next\(/.test(src))
    issues.push(`${file}: no error wiring detected`);
}
if (issues.length) { for (const i of issues) console.error('-', i); process.exit(1); }
console.log('routes audit OK');
JS
