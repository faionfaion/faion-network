---
slug: gitlab-cicd
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "GitLab CI configuration: staged pipelines, child pipelines for monorepos, OIDC auth to cloud, protected variables and required Merge-Request approvals."
content_id: "3ab348b096a5739b"
complexity: medium
produces: config
est_tokens: 4000
tags: [gitlab, cicd, merge-request, oidc, supply-chain]
---
# GitLab CI/CD Pipeline Design

## Summary

**One-sentence:** GitLab CI configuration: staged pipelines, child pipelines for monorepos, OIDC auth to cloud, protected variables and required Merge-Request approvals.

**One-paragraph:** GitLab CI configuration: staged pipelines, child pipelines for monorepos, OIDC auth to cloud, protected variables and required Merge-Request approvals. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `config` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-gitlab-cicd.py` before publication.

**Ефективно для:**

- Розбиття monorepo pipeline через child pipelines + rules:changes.
- Перехід CI/CD на OIDC до AWS / GCP / Azure.
- Налаштування MR-approval gate з code-owners.

## Applies If (ALL must hold)

- Input matches the methodology scope (gitlab-cicd) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `config` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Project structure | monorepo or multi-repo + service list | platform team |
| Runner topology | shared vs group vs project runners + tag taxonomy | ci team |
| Cloud OIDC trust | JWT audience + role mapping per cloud | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[github-actions-cicd]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-config-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.gitlab-ci.yml` | Annotated configuration skeleton with required keys + comments per knob |
| `templates/_smoke-test.json` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitlab-cicd.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[github-actions-cicd]]
- [[jenkins-pipelines]]
- [[iac-pr-review-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `staged-pipeline-shape` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
