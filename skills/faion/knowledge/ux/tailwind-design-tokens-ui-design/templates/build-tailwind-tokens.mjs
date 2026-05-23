// build-tailwind-tokens.mjs — generate tailwind-theme.js + tokens.css from tokens.json
// Reads: tokens/tokens.json (W3C DTCG format)
// Outputs: dist/tailwind-theme.js, dist/tokens.css
// Usage: node build-tailwind-tokens.mjs
//
// Color tokens use RGB channel pattern for Tailwind opacity modifier compatibility:
//   --color-primary-rgb: 59 130 246;
//   config: 'rgb(var(--color-primary-rgb) / <alpha-value>)'
//   usage: bg-primary/50

import { readFileSync, writeFileSync, mkdirSync } from 'fs';

const tokens = JSON.parse(readFileSync('tokens/tokens.json', 'utf8'));
const cssVars = [];
const twColors = {};
const twSpacing = {};

function hexToRgb(hex) {
  const h = hex.replace('#', '');
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ].join(' ');
}

function setNestedKey(obj, keys, value) {
  keys.reduce((acc, key, i) => {
    if (i === keys.length - 1) { acc[key] = value; return acc; }
    acc[key] = acc[key] || {};
    return acc[key];
  }, obj);
}

function processTokens(obj, prefix = '') {
  for (const [key, val] of Object.entries(obj)) {
    if (key.startsWith('comment')) continue;
    const path = prefix ? `${prefix}-${key}` : key;
    if (val && val.value !== undefined) {
      const cssKey = `--${path}`;
      if (val.type === 'color' && val.value.startsWith('#')) {
        const rgb = hexToRgb(val.value);
        cssVars.push(`  ${cssKey}-rgb: ${rgb};`);
        cssVars.push(`  ${cssKey}: ${val.value};`);
        const colorPath = path.replace(/^color-/, '').split('-');
        setNestedKey(twColors, colorPath, `rgb(var(${cssKey}-rgb) / <alpha-value>)`);
      } else if (val.type === 'dimension') {
        cssVars.push(`  ${cssKey}: ${val.value};`);
        if (path.startsWith('spacing-')) {
          const name = path.replace('spacing-', '');
          twSpacing[name] = `var(${cssKey})`;
        }
      }
    } else if (val && typeof val === 'object') {
      processTokens(val, path);
    }
  }
}

processTokens(tokens);
mkdirSync('dist', { recursive: true });

writeFileSync('dist/tokens.css',
  `@layer base {\n  :root {\n${cssVars.map(v => '  ' + v).join('\n')}\n  }\n}\n`);

writeFileSync('dist/tailwind-theme.js',
  `module.exports = ${JSON.stringify({ colors: twColors, spacing: twSpacing }, null, 2)};\n`);

console.log(`Generated: ${cssVars.length} CSS variables`);
console.log('Output: dist/tokens.css, dist/tailwind-theme.js');
