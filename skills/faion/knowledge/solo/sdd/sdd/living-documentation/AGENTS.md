---
slug: living-documentation
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a docs-as-code config (co-located docs + auto-generated API ref + CI link-validation + AUTO-GENERATED markers) so documentation stays synchronised with code and never silently rots."
content_id: "ba6dbabad947556c"
complexity: medium
produces: config
est_tokens: 3500
tags: [docs-as-code, documentation, ci-cd, devops, quality-gates]
---

# Living Documentation

## Summary

**One-sentence:** Produces a docs-as-code config (co-located docs + auto-generated API ref + CI link-validation + AUTO-GENERATED markers) so documentation stays synchronised with code and never silently rots.

**Ефективно для:** Solo devs whose README is 18 months out of date and whose API docs lie about endpoints that were renamed last sprint.

**One-paragraph:** Documentation rots when separated from code. This methodology pins docs-as-code: documentation lives in version control next to source, auto-generated where possible, validated in CI. Hand-authored docs (ADRs, design rationale) sit alongside auto-generated API references and changelogs. Every auto-generated section carries an AUTO-GENERATED marker so agents and humans know not to overwrite manually. Output is consumed by api-first-development and code-review-cycle.

## Applies If (ALL must hold)

- Repo has source + docs co-locatable.
- API surface exists with auto-generatable reference.
- CI pipeline available to enforce link validity.
- Documentation has ≥2 readers (devs, users, partners).

## Skip If (ANY kills it)

- Pre-product where no API exists yet.
- Throwaway scripts with no documentation need.
- Closed-source binary with PDF-only doc convention.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| source repo | git | engineer |
| docs framework | tool (Hugo, Docusaurus, MkDocs, etc.) | engineer |
| CI pipeline | yaml | engineer |
| link-validator + spec-diff tooling | tools | engineer |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/api-first-development` | Sibling — openapi.yaml drives auto-generated reference. |
| `solo/sdd/sdd/architecture-decision-records` | Sibling — ADRs are hand-authored alongside generated docs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/living-documentation.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/living-documentation.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-living-documentation.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[api-first-development]] — related methodology.
- [[architecture-decision-records]] — related methodology.
- [[design-docs-patterns]] — related methodology.
- [[code-review-cycle]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
