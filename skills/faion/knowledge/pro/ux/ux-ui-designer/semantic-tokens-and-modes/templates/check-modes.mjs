// check-modes.mjs — CI gate for semantic token mode coverage
// Fails the build if any semantic token is missing a value in any required mode
// Input: tokens/semantic.json (W3C DTCG format with $value per mode as object)
// Usage: node check-modes.mjs [tokens/semantic.json] [light,dark,hc]
import { readFileSync } from 'node:fs';

const tokenFile = process.argv[2] ?? 'tokens/semantic.json';
const REQUIRED_MODES = (process.argv[3] ?? 'light,dark,hc').split(',').map(m => m.trim());

let tokens;
try {
  tokens = JSON.parse(readFileSync(tokenFile, 'utf8'));
} catch (e) {
  console.error(`Cannot read ${tokenFile}: ${e.message}`);
  process.exit(1);
}

const missing = [];

function walk(node, path = []) {
  if (!node || typeof node !== 'object') return;
  if ('$value' in node) {
    const v = node.$value;
    // DTCG per-mode value: { light: '#fff', dark: '#000', hc: '#000' }
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      const definedModes = Object.keys(v);
      const lacking = REQUIRED_MODES.filter(m => !definedModes.includes(m));
      if (lacking.length) missing.push({ token: path.join('.'), missing: lacking });
    }
    return;
  }
  for (const [k, child] of Object.entries(node)) {
    if (!k.startsWith('$')) walk(child, [...path, k]);
  }
}

walk(tokens);

if (missing.length) {
  console.error(`\nToken mode coverage failures (${missing.length}):\n`);
  console.error(JSON.stringify(missing, null, 2));
  process.exit(1);
}

console.log(`All semantic tokens have values for modes: ${REQUIRED_MODES.join(', ')}`);
