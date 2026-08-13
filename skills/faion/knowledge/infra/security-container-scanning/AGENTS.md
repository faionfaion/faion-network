# Container Security Scanning and Image Signing

## Summary

**One-sentence:** Produces a CI config (workflow YAML + trivy.yaml + .trivyignore + cosign signing job) that scans every image build, generates an SBOM, and signs the image with Sigstore keyless OIDC.

**One-paragraph:** 87 % of production container images carry at least one major CVE (CNCF 2024). This methodology wires the scan + SBOM + sign triad into CI: Trivy (or Grype) on the built image, fail on CRITICAL+HIGH; CycloneDX SBOM via Syft attached to the release; Sigstore cosign keyless OIDC signature with the CI's id-token. The output is a CI config artefact (GitHub Actions / GitLab CI / Jenkinsfile) plus the trivy.yaml + .trivyignore policy files. The scanner is pinned to a release tag, ignore-unfixed is on, and the registry push step depends on scan exit-code 0.

**Ефективно для:**

- Every project that builds and pushes container images — pre-registry-push gate.
- SBOM generation для SOC2 / NIST SSDF / FedRAMP audit.
- Image signing для admission control verification (Kyverno verifyImages / Cosign policy).
- Same-pipeline IaC misconfig scanning (Dockerfile + K8s manifests + Terraform).

## Applies If (ALL must hold)

- Pipeline builds and pushes a container image to a registry.
- Compliance scope OR security baseline requires CVE scan + SBOM + signing.
- CI provider issues OIDC id-tokens (GitHub Actions, GitLab CI, CircleCI, Buildkite).

## Skip If (ANY kills it)

- Project ships no containers — apply filesystem SAST / SCA instead.
- Using container scanning as a substitute for SAST — it catches CVEs in packages, not app code flaws.
- Trying to block on every MEDIUM finding at start — alert fatigue collapses the gate.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dockerfile + image tag plan | file + tag scheme | repo |
| Registry credentials | OIDC role (GHCR / ECR / GAR) — no static keys | CI provider |
| Severity policy | block list (e.g. CRITICAL+HIGH) + ignore policy | security team |
| Admission verifier | Kyverno verifyImages / Cosign policy controller (optional) | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[security-sast]] | SAST + container scanning are complementary; defence in depth |
| [[security-policy-as-code]] | Cosign signatures verified at admission via Kyverno |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: scan-before-push, block-critical-high, sbom-immutable, keyless-cosign, pin-scanner-version, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for CI scan config + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: floating-master-tag, sbom-format-mix, key-in-secrets, no-fail-on-critical | 800 |
| `content/04-procedure.xml` | essential | 6 steps: pin tool → build → trivy → SBOM → sign → push | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on scanner choice + signing model → rule | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-scanner` | haiku | Trivy vs Grype vs Clair — deterministic on registry / SBOM-centric / CI-centric. |
| `compose-workflow` | sonnet | Assemble the CI YAML with correct OIDC permissions. |
| `triage-findings` | sonnet | Reduce false-positive noise + write .trivyignore entries with rationale. |

## Templates

| File | Purpose |
|------|---------|
| `templates/github-actions-trivy.yml` | GitHub Actions workflow: build → trivy → SBOM → cosign keyless sign → push |
| `templates/trivy.yaml` | Trivy scanner config: severity gate + ignore-unfixed + DB cache |
| `templates/.trivyignore` | Trivy ignore policy with mandatory expiry dates |
| `templates/_smoke-test.json` | Minimum scan-config artefact used by validate-security-container-scanning.py --self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-container-scanning.py` | Validate the config artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[security-sast]]
- [[security-policy-as-code]]
- [[security-dast]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it when scoping the supply-chain security gate for a new repo.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/github-actions-trivy.yml`

```yaml
name: container-scan-and-sign
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write
  id-token: write   # required for keyless cosign
  security-events: write

jobs:
  scan-and-sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - name: Login GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build
        id: build
        uses: docker/build-push-action@v5
        with:
          push: false
          load: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
      - name: Trivy scan (fail on CRITICAL/HIGH)
        uses: aquasecurity/trivy-action@0.20.0
        with:
          image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: sarif
          output: trivy.sarif
          severity: CRITICAL,HIGH
          exit-code: '1'
          ignore-unfixed: true
      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with: { sarif_file: trivy.sarif }
      - name: SBOM (CycloneDX)
        uses: anchore/sbom-action@v0
        with:
          image: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: cyclonedx-json
          output-file: sbom.cdx.json
      - name: Push image
        uses: docker/build-push-action@v5
        id: push
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
      - name: Cosign install
        uses: sigstore/cosign-installer@v3
      - name: Cosign keyless sign
        env:
          COSIGN_EXPERIMENTAL: "1"
        run: cosign sign --yes ghcr.io/${{ github.repository }}@${{ steps.push.outputs.digest }}
```

### `templates/trivy.yaml`

```yaml
severity:
  - CRITICAL
  - HIGH
exit-code: 1
ignore-unfixed: true
ignorefile: .trivyignore
cache-dir: .trivy-cache
db:
  skip-update: false
vulnerability:
  type:
    - os
    - library
```

### `templates/.trivyignore`

```text
# Each entry MUST have a reason + an expiry date (exp:YYYY-MM-DD).
# Permanent ignores require security-team approval.

# Example: upstream not yet shipped
CVE-2024-11111 exp:2026-09-01
# Example: false positive in unused codepath (reachability-confirmed)
CVE-2024-22222 exp:2026-12-31
```

### `templates/_smoke-test.json`

```json
{
  "scanner": "trivy",
  "scanner_version": "0.50.0",
  "severity_block": [
    "CRITICAL",
    "HIGH"
  ],
  "ignore_unfixed": true,
  "sbom_format": "cyclonedx",
  "signing": {
    "tool": "cosign",
    "mode": "keyless-oidc",
    "key_in_repo": false
  },
  "scan_before_push": true
}
```
