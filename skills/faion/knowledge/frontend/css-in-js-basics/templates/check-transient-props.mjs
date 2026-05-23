#!/usr/bin/env node
// check-transient-props.mjs
// Flag styled.X<{Props}> where prop names don't start with $
// Usage: node check-transient-props.mjs [src-dir]
import { execSync } from 'node:child_process';

const src = process.argv[2] ?? 'src';

// Match styled.X<{ nonDollarProp: ... }> patterns
const grep = `grep -rEn 'styled\\.[a-zA-Z]+<\\{[^$\\}]*[^,$\\s}][a-zA-Z]+[^$]' ${src} --include='*.tsx' || true`;
const out = execSync(grep, { encoding: 'utf8' });

if (out.trim()) {
  console.error('Non-transient props detected (should use $prefix):');
  console.error(out);
  process.exit(1);
}
console.log('OK: all styled-components props use $prefix convention');
