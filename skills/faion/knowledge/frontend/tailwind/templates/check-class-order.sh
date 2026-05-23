#!/usr/bin/env bash
# check-class-order.sh
# Enforce canonical Tailwind class order via Prettier and ESLint.
# Add to .husky/pre-commit or GitHub Actions.
#
# Prerequisites:
#   npm i -D prettier prettier-plugin-tailwindcss eslint eslint-plugin-tailwindcss
#
# .prettierrc must include:
#   { "plugins": ["prettier-plugin-tailwindcss"] }
set -euo pipefail

echo "Checking Tailwind class order..."

# 1. Prettier: check class sort in all TS/TSX/JSX/HTML files
npx prettier \
  --check \
  --plugin prettier-plugin-tailwindcss \
  'src/**/*.{ts,tsx,jsx,js,html}' \
  'components/**/*.{ts,tsx,jsx}'

# 2. ESLint: enforce class order rule
npx eslint \
  --rule '{"tailwindcss/classnames-order": "error"}' \
  'src/**/*.{ts,tsx,jsx}' \
  'components/**/*.{ts,tsx,jsx}'

echo "Class order OK."
