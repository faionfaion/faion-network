---
slug: gdpr-dsar-runbook-product-dev-team
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "f7d6d5527e2cfcca"
summary: "Gdpr Dsar Runbook Product Dev Team — testable methodology for platform, k8s, networking, cost models. DSAR (Data Subject Access Request) execution is a recurring legal obligation with no concrete runbook in faion: data discovery query patterns, redaction rules, response packaging."
tags: [infra, geek, methodology]
---
# Gdpr Dsar Runbook Product Dev Team

## Summary

**One-sentence:** Gdpr Dsar Runbook Product Dev Team — testable methodology for platform, k8s, networking, cost models. DSAR (Data Subject Access Request) execution is a recurring legal obligation with no concrete runbook in faion: data discovery query patterns, redaction rules, response packaging.

**One-paragraph:** Gdpr Dsar Runbook Product Dev Team closes a known gap in infra practice: DSAR (Data Subject Access Request) execution is a recurring legal obligation with no concrete runbook in faion: data discovery query patterns, redaction rules, response packaging. The methodology is anchored to the recurring activity 'SOC2 / GDPR audit prep (annual) (role: p6-product-dev-team)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'SOC2 / GDPR audit prep (annual) (role: p6-product-dev-team)' shows up in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems, dashboards, or transcripts that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/infra/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `geek/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gdpr_dsar_runbook_product_dev_team_template_fill` | haiku | Template fill, no judgement |
| `gdpr_dsar_runbook_product_dev_team_evidence_check` | sonnet | Bounded comparison + judgement |
| `gdpr_dsar_runbook_product_dev_team_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/infra/` (see neighbouring methodologies)
- triggering activity: `SOC2 / GDPR audit prep (annual) (role: p6-product-dev-team)`
- external: industry references cited inline in `content/01-core-rules.xml`
