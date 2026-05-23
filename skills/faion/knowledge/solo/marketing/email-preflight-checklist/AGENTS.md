---
slug: email-preflight-checklist
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a 12-item pre-send checklist artefact every marketing or lifecycle send must pass — subject, preheader, links, suppression, render, throttle, owner sign-off — before the send button activates.
content_id: "cbc55dda36460837"
complexity: light
produces: checklist
est_tokens: 2900
tags: ["email", "preflight", "checklist", "marketing", "solo"]
---
# Email Preflight Checklist

## Summary

**One-sentence:** Produces a 12-item pre-send checklist artefact every marketing or lifecycle send must pass — subject, preheader, links, suppression, render, throttle, owner sign-off — before the send button activates.

**One-paragraph:** Email Preflight Checklist produces a checklist artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated checklist ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo marketer on send-day who needs a single auditable artefact that stops the four classic preflight bugs (broken link, wrong segment, missing unsub, untracked utm) before deploy.

## Applies If (ALL must hold)

- Marketing or lifecycle email send is queued in an ESP
- Audience segment is defined and exported
- There is a named owner accountable for the send

## Skip If (ANY kills it)

- Transactional emails handled by application code — different gate
- Drip campaign already in steady state with no template change (use audit only)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Final HTML/MJML template | file | ESP draft or git |
| Segment definition | query or list ID | ESP segmentation |
| UTM tagging convention | doc | marketing-ops handbook |
| Suppression / global unsubscribe list | list ID | ESP suppression UI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `email-lifecycle-architecture` | Provides global frequency cap + suppression that preflight must respect. |
| `growth-email-marketing` | Parent methodology — preflight is the gate before send. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-12-items-mandatory, r2-each-item-has-source, r3-named-owner-not-team, r4-time-box-30-min, r5-block-if-any-red, r6-evidence-link-per-item | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-email-preflight-checklist` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-email-preflight-checklist` | haiku | Schema check + threshold checks; deterministic. |
| `review-email-preflight-checklist` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/email-preflight-checklist.json` | JSON skeleton conforming to the output contract schema. |
| `templates/email-preflight-checklist.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-email-preflight-checklist.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[email-lifecycle-architecture]]
- [[growth-email-marketing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
