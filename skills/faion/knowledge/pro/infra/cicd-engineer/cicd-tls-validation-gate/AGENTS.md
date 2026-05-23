---
slug: cicd-tls-validation-gate
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Adds a CI gate that runs testssl.sh + sslyze + (optional) SSL Labs against staging and blocks promotion to production unless A+ grade, cipher policy, and certificate chain validity all pass.
content_id: "bb212e274cff36e9"
complexity: medium
produces: config
est_tokens: 4200
tags: ["tls", "ci-gate", "security-scanning", "testssl", "ssl-labs"]
---
# TLS Validation CI Gate

## Summary

**One-sentence:** Adds a CI gate that runs testssl.sh + sslyze + (optional) SSL Labs against staging and blocks promotion to production unless A+ grade, cipher policy, and certificate chain validity all pass.

**One-paragraph:** TLS Validation CI Gate — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Public-facing TLS endpoint promotion pipeline (staging → production).
- Compliance regime requires demonstrable TLS posture (PCI-DSS, SOC2).
- Team is willing to fail builds on TLS regression.

## Applies If (ALL must hold)

- Public-facing TLS endpoint promotion pipeline (staging → production).
- Compliance regime requires demonstrable TLS posture (PCI-DSS, SOC2).
- Team is willing to fail builds on TLS regression.

## Skip If (ANY kills it)

- Internal-only services without public TLS exposure.
- Pre-prod environment without a staging URL to scan.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cicd-tls-renewal-automation]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (a-plus-required, cipher-policy-mozilla-intermediate, hsts-min-1-year, ocsp-stapling-enabled, scan-blocks-promotion, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-cicd-tls-validation-gate` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tls-scan.gha.yml` | GitHub Actions workflow step running testssl.sh + parsing grade |
| `templates/testssl-policy.json` | testssl.sh policy file enforcing A+ + Mozilla intermediate |
| `templates/backup-config.example.json` | Filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cicd-tls-validation-gate.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/`
- [[cicd-tls-renewal-automation]]
- [[cicd-cert-rotation-pipeline]]
- [[cicd-mtls-deployment]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
