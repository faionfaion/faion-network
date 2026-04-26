# Trivy with Pinned-Version Supply-Chain Scan + SBOM

## Summary

Every container image, Helm chart, Terraform module, Kubernetes manifest, and release tarball passes through `trivy fs` (filesystem) plus `trivy image` (containers) in CI. The job fails on HIGH or CRITICAL CVEs and on misconfigurations, blocking merge. Each release tag also generates an SBOM in CycloneDX or SPDX and attaches it to the GitHub Release. Trivy itself is pinned by SHA — the action is referenced as `aquasecurity/trivy-action@<sha>` and the binary version in CI is set explicitly to a known-clean release, never `latest`.

## Summary continued

The pin is non-negotiable. In March 2026 the `aquasecurity/trivy-action` repository and a `trivy` 0.69.4 release were both supply-chain compromised (the "TeamPCP" incident), so any pipeline using floating refs in March 2026 silently shipped a tampered scanner. The hard rule is: SHA-pin the action, version-pin the binary, mirror the DB if practical, and verify the binary's cosign signature before the first run on any new runner image.

## Why

Trivy is the de-facto multi-purpose scanner in 2026 — vulns, misconfigs, secrets, SBOM — across containers, Kubernetes, IaC, code repos, cloud accounts and OS packages, with weekly DB updates. One scanner replacing four (Anchore + tfsec + dockle + grype) keeps the agent's mental model small and the CI minutes low. SBOMs are no longer optional: the EU Cyber Resilience Act mandates SBOM reporting from September 2026 with full enforcement from December 2027, and US Executive Order 14028 already requires SBOMs for federal procurement. A scan that produces SBOM-as-a-side-effect pays for the regulatory floor and the security gate at once. The pin discipline exists because the scanner is itself a piece of the supply chain — the lessons of the March 2026 compromise apply to every CI tool an agent reaches for.

## When To Use

- Any repo that produces a container image, IaC artifact, or release tarball.
- Any agent-driven dependency bump or base-image upgrade — agent runs `trivy image` on the candidate before opening the PR.
- Polyglot monorepos that need one scanner across `Dockerfile`, `terraform/`, `helm/`, `k8s/`, and `package-lock.json`.
- Release pipelines that must attach an SBOM for EU CRA or US EO 14028 compliance.

## When NOT To Use

- Pure documentation, asset, or static-blog repos with no container, IaC, or distributable binary — no supply-chain surface to scan.
- Highly air-gapped environments where Trivy's online DB updates are impossible — switch to a mirrored offline DB or substitute Anchore Enterprise with a private feed; do not run the scanner with stale signatures.
- Notebook-only research repos where dependency churn is constant and signal-to-noise is too low — use Snyk or Renovate-driven advisories instead and gate at deploy time.
- The exact tag `aquasecurity/trivy@v0.69.4` and `aquasecurity/trivy-action@v0.30.0` (compromised) — never use those refs anywhere.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pin-by-sha.xml` | The action SHA pin and binary version pin rules, with the March 2026 incident as anchor. |
| `content/02-fs-and-image-gate.xml` | The `trivy fs` + `trivy image` blocking-on-HIGH/CRITICAL contract for PRs. |
| `content/03-sbom-on-release.xml` | The SBOM-per-release-tag rule and the EU CRA / EO 14028 anchor. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trivy-action.yml` | GitHub Actions workflow with SHA-pinned action and explicit binary version. |
| `templates/.trivyignore` | Project-scoped CVE allowlist with sunset dates and review owners. |
| `templates/release-sbom.sh` | Script that runs `trivy sbom --format cyclonedx` and uploads to a release. |
