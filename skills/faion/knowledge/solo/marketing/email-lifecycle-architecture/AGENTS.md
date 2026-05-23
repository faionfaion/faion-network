---
slug: email-lifecycle-architecture
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Maps every customer email to one of six lifecycle stages with global frequency caps, suppression rules, and consent records — the system layer atomic email programs miss.
content_id: "32ce79efa57844e1"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["email-lifecycle", "marketing", "deliverability", "consent", "gdpr", "solo"]
---
# Email Lifecycle Architecture

## Summary

**One-sentence:** Maps every customer email to one of six lifecycle stages with global frequency caps, suppression rules, and consent records — the system layer atomic email programs miss.

**One-paragraph:** Email Lifecycle Architecture produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder running ≥3 email programs who needs one map showing acquisition→churn lifecycle, global caps, and consent posture before deliverability tanks.

## Applies If (ALL must hold)

- ≥3 email programs running (welcome, newsletter, transactional, etc.)
- ≥1,000 subscribers OR ≥100 transactional emails/day
- Founder/owner has authority to consolidate sender + suppression list

## Skip If (ANY kills it)

- Single newsletter only — use growth-newsletter-growth instead
- Transactional-only product with no marketing emails
- Regulated industry (HIPAA) — requires regulated-email patterns

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| List of current email programs with sender + subscriber count | table | ESP exports |
| Current ESP(s) and segmentation capability | spec | ESP admin |
| Consent + GDPR/CASL/CAN-SPAM compliance baseline | doc | legal/ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `growth-email-marketing` | Peer methodology — produces individual program design that this consolidates. |
| `growth-newsletter-growth` | Peer methodology — newsletter is one stage in the lifecycle. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-six-lifecycle-stages, r2-frequency-cap-global, r3-suppression-cross-program, r4-consent-record-with-source, r5-quarterly-suppression-audit | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-email-lifecycle-architecture` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-email-lifecycle-architecture` | haiku | Schema check + threshold checks; deterministic. |
| `review-email-lifecycle-architecture` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/email-lifecycle-architecture.json` | JSON skeleton conforming to the output contract schema. |
| `templates/email-lifecycle-architecture.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-email-lifecycle-architecture.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[growth-email-marketing]]
- [[growth-newsletter-growth]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
