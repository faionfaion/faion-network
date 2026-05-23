---
slug: objection-bank
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a living objection-bank artefact: every recurring buyer objection from outreach, landing-page bounces, and sales calls into a single ranked list with response template, evidence link, and last-seen date — feeds landing copy + FAQ.
content_id: "08e9f01b912345b7"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["objection-handling", "sales-ops", "faq", "landing-pages", "solo"]
---
# Objection Bank

## Summary

**One-sentence:** Generates a living objection-bank artefact: every recurring buyer objection from outreach, landing-page bounces, and sales calls into a single ranked list with response template, evidence link, and last-seen date — feeds landing copy + FAQ.

**One-paragraph:** Objection Bank produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder who fields repeating buyer objections across outreach, landing bounces, and calls and needs ONE ranked source-of-truth feeding FAQ + landing copy — before the same objection kills the third deal in a row.

## Applies If (ALL must hold)

- Has fielded ≥10 sales conversations / inbound replies / landing bounces
- Maintains FAQ or landing copy that can be updated continuously
- Founder commits to weekly capture cadence

## Skip If (ANY kills it)

- Pre-revenue with <10 conversations — wait for signal first
- Enterprise sale with 1 deal in flight — different objection-handling style
- No FAQ surface to update — fix that first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent sales call recordings or notes | audio / doc | Gong / Loom / notes |
| Outreach reply archive | thread / CSV | ESP / Hunter |
| Landing-page bounce + exit-intent transcripts | session-replay | PostHog / Hotjar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `positioning-diff-log` | Pulls positioning shifts driven by objections. |
| `growth-cold-outreach` | Replies feed the bank. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-capture-evidence-link, r2-ranked-by-frequency, r3-response-template-per-entry, r4-feeds-faq-and-landing, r5-named-owner-and-weekly-review, r6-no-personally-attacking-objections | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-objection-bank` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-objection-bank` | haiku | Schema check + threshold checks; deterministic. |
| `review-objection-bank` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/objection-bank.json` | JSON skeleton conforming to the output contract schema. |
| `templates/objection-bank.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-objection-bank.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[positioning-diff-log]]
- [[growth-cold-outreach]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
