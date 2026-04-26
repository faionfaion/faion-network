#!/usr/bin/env bash
# extract-push.sh — i18next extract + Lokalise push/pull for TS/React projects
# Requires: LOKALISE_TOKEN and LOKALISE_PROJECT_ID env vars
set -euo pipefail

: "${LOKALISE_TOKEN:?Set LOKALISE_TOKEN}"
: "${LOKALISE_PROJECT_ID:?Set LOKALISE_PROJECT_ID}"

echo "Extracting strings..."
npx i18next-parser --config i18next-parser.config.js

echo "Pushing EN catalogue to Lokalise..."
lokalise2 file upload \
  --token "$LOKALISE_TOKEN" \
  --project-id "$LOKALISE_PROJECT_ID" \
  --file 'locales/en/*.json' \
  --lang-iso en \
  --replace-modified \
  --apply-tm

echo "Pulling translations from Lokalise..."
lokalise2 file download \
  --token "$LOKALISE_TOKEN" \
  --project-id "$LOKALISE_PROJECT_ID" \
  --format json \
  --unzip-to ./locales \
  --original-filenames true \
  --export-sort-order a_z

echo "Done. Run check-i18n.sh to verify key alignment."
