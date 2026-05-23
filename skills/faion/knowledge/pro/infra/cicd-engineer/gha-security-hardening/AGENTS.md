---
slug: gha-security-hardening
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a security-hardened workflow config (SHA-pinned actions + OIDC for cloud auth + per-job token permissions + pull_request_target audit + actionlint gate).
content_id: "14d56d69e9045214"
complexity: deep
produces: config
est_tokens: 4300
tags: [github-actions, security, oidc, supply-chain, permissions]
---
# GitHub Actions — Security Hardening

## Summary

**One-sentence:** Generates a security-hardened workflow config (SHA-pinned actions + OIDC for cloud auth + per-job token permissions + pull_request_target audit + actionlint gate).

**One-paragraph:** Generates a security-hardened workflow config (SHA-pinned actions + OIDC for cloud auth + per-job token permissions + pull_request_target audit + actionlint gate). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Public + open-source repos де PR з fork може зловживати CI.
- Enterprise repos з access до cloud (AWS/GCP/Azure) через CI.
- Supply-chain audit: SHA-pin замість @v3 для third-party actions.
- Compliance (SOC2 / ISO27001) — workflow audit-trail обов'язковий.

## Applies If (ALL must hold)

- Workflow runs untrusted code (PR from fork, downloaded artefacts, npm/pip installs).
- Workflow has access to secrets or cloud credentials.
- Repo is public OR has external contributors.
- Compliance / supply-chain controls apply to the codebase.

## Skip If (ANY kills it)

- Internal repo with no external contributors AND no secrets in workflows AND no cloud-auth.
- Throwaway prototype repo with no production deploy path.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current workflow files | yaml | Repo |
| Cloud account list with OIDC trust policies | JSON | Cloud Platform |
| Third-party action inventory | list of `uses:` strings | audit script |
| actionlint binary | v1+ | CI team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gha-security-hardening` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gha-security-hardening.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
