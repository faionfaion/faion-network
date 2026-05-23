#!/usr/bin/env bash
# purpose: generate CycloneDX SBOM, sign with cosign, attach to GitHub Release
# consumes: $TAG + $GITHUB_TOKEN environment + repo content
# produces: config (sbom.cdx.json + signature uploaded to gh release)
# depends-on: content/01-core-rules.xml (sbom-per-release)
# token-budget-impact: low — ~150 tokens when loaded as context
# Invoked from a tag-triggered workflow.
set -euo pipefail

: "${TAG:?TAG must be set to the release tag (e.g. v1.2.3)}"
: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set}"

OUT_SBOM="sbom-${TAG}.cdx.json"
OUT_SIG="${OUT_SBOM}.sig"

trivy sbom --format cyclonedx --output "${OUT_SBOM}" .
cosign sign-blob --yes "${OUT_SBOM}" --output-signature "${OUT_SIG}"
gh release upload "${TAG}" "${OUT_SBOM}" "${OUT_SIG}" --clobber

echo "ok: SBOM and signature uploaded to release ${TAG}"
