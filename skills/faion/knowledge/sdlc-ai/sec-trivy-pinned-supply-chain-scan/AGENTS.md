# Trivy with Pinned-Version Supply-Chain Scan + SBOM

## Summary

**One-sentence:** Run `trivy fs` (filesystem) + `trivy image` (containers) in CI on every PR; fail on HIGH/CRITICAL CVEs + misconfig; attach CycloneDX SBOM to each Release; pin trivy itself by SHA.

**One-paragraph:** Container, IaC, and release-tarball pipelines ship vulnerable transitive deps and base-image CVEs silently. This methodology produces a Trivy-pinned CI workflow that runs `trivy fs` over the repo (Dockerfile, terraform/, helm/, k8s/, package-lock.json) and `trivy image` on built images; fails the job on HIGH/CRITICAL CVEs and misconfigurations; emits SBOM per release for EU CRA / US EO 14028 compliance. The Trivy action and binary are pinned by SHA — never `@latest`, never compromised tag.

**Ефективно для:**

- Repo, що випускає container image, Helm chart, Terraform module, k8s manifest, release tarball.
- Agent-driven base-image upgrade — agent запускає trivy image на candidate перед PR.
- Polyglot monorepo з Dockerfile + terraform + helm + k8s + package-lock.json.
- Release pipeline, що mustcomply з EU CRA / US EO 14028 (SBOM required).

## Applies If (ALL must hold)

- Repo produces a container image, IaC artifact, or release tarball.
- CI has outbound network egress (Trivy DB updates).
- Team accepts blocking merge on HIGH/CRITICAL CVE or misconfig.
- Release pipeline can attach an SBOM artefact.

## Skip If (ANY kills it)

- Pure docs/asset/static-blog repo with no container, IaC, or distributable binary.
- Air-gapped environment without offline-DB mirror.
- Notebook-only research repo with constant dep churn — gate at deploy time via different tooling.
- The exact compromised tags `aquasecurity/trivy@v0.69.4` and `aquasecurity/trivy-action@v0.30.0` MUST NEVER be referenced.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| GitHub workflow | .github/workflows/trivy.yml | platform |
| Trivy action SHA pin | known-clean SHA | sec |
| SBOM tool | trivy fs --format cyclonedx OR syft | platform |
| Release pipeline | gh release upload | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[sec-codeql-autofix-on-pr]] | Complementary SAST layer. |
| [[sec-secrets-defense-in-depth]] | Complementary secret-scan layer. |
| [[mr-renovate-ai-handoff]] | Renovate handles deps Trivy flags as breaking. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 500 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workflow_draft` | haiku | Boilerplate Trivy YAML. |
| `sha_pin` | haiku | Mechanical lookup. |
| `cve_triage` | sonnet | HIGH/CRITICAL triage requires judgement (exploitable in our context?). |

## Templates

| File | Purpose |
|------|---------|
| `templates/trivy-action.yml` | Trivy fs + image workflow with SHA-pinned action. |
| `templates/release-sbom.sh` | Release-time script that emits CycloneDX SBOM and attaches to gh release. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sec-trivy-pinned-supply-chain-scan.py` | Validate workflow + SBOM emission config against schema. | Pre-merge of trivy.yml |

## Related

- [[sec-codeql-autofix-on-pr]]
- [[sec-secrets-defense-in-depth]]
- [[mr-renovate-ai-handoff]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (produces container/IaC/release? egress? compliance need?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to enable Trivy — the tree terminates either on the active rule or on `skip-this-methodology`.
