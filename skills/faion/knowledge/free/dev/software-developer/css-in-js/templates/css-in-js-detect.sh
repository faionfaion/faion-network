#!/usr/bin/env bash
# css-in-js-detect.sh — recommend a CSS-in-JS strategy for a JS/TS repo.
# Usage: css-in-js-detect.sh [path/to/repo]
# Outputs JSON with recommendations and risks. Use as input for agent lib selection.
set -euo pipefail
root="${1:-.}"
[ -f "$root/package.json" ] || { echo "no package.json in $root"; exit 1; }
node - <<'JS' "$root"
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const root = process.argv[1];
const pkg = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
const dep = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
const has = (n) => n in dep;

const rsc = (has('next') && /1[345]|^>=?13/.test(dep.next || ''))
  || existsSync(join(root, 'app/layout.tsx'))
  || existsSync(join(root, 'app/layout.jsx'));
const rn   = has('react-native');
const vite = has('vite');

const recs = [];
if (rn)        recs.push('react-native StyleSheet or @shopify/restyle (RN-safe)');
else if (rsc)  recs.push('vanilla-extract OR panda-css OR Tailwind (RSC-safe). Avoid styled-components/Emotion runtime.');
else if (vite) recs.push('styled-components v6 or @emotion/react are fine for client-only SPA.');
else           recs.push('CSS Modules + Tailwind unless dynamic styling is required.');

const risks = [];
if (rsc && (has('styled-components') || has('@emotion/styled')))
  risks.push('runtime CSS-in-JS detected with App Router — likely RSC breakage or hydration mismatch');
if (has('styled-components') && has('@emotion/styled'))
  risks.push('two CSS-in-JS engines installed — pick one to avoid css() import conflicts');
if (!rsc && has('styled-components') && !dep['styled-components'].includes('6'))
  risks.push('styled-components v5 detected — upgrade to v6 for React 18 compatibility');

console.log(JSON.stringify({ recommendations: recs, risks }, null, 2));
JS
