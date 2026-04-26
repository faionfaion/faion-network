#!/usr/bin/env bash
# release-sbom.sh — generate, sign, and attach a CycloneDX SBOM to a GitHub Release.
# Invoked from a tag-triggered workflow with $TAG and $GITHUB_TOKEN exported.
set -euo pipefail

: "${TAG:?TAG must be set to the release tag (e.g. v1.2.3)}"
: "${GITHUB_TOKEN:?GITHUB_TOKEN must be set}"

OUT_SBOM="sbom-${TAG}.cdx.json"
OUT_SIG="${OUT_SBOM}.sig"

trivy sbom --format cyclonedx --output "${OUT_SBOM}" .
cosign sign-blob --yes "${OUT_SBOM}" --output-signature "${OUT_SIG}"
gh release upload "${TAG}" "${OUT_SBOM}" "${OUT_SIG}" --clobber

echo "ok: SBOM and signature uploaded to release ${TAG}"
