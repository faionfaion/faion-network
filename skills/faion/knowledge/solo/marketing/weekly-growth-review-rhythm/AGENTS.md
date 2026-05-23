---
slug: weekly-growth-review-rhythm
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Solo growth review ritual: 5-7 metrics, hypothesis log, decision template — operational backbone connecting channel methodologies to compounding outcomes.
content_id: "28f001a090ba46eb"
complexity: medium
produces: spec
est_tokens: 4400
tags: ["weekly-growth-review-rhythm", "marketing", "solo", "rituals"]
---
# Weekly Growth Review Rhythm

## Summary

**One-sentence:** Solo growth review ritual: 5-7 metrics, hypothesis log, decision template — operational backbone connecting channel methodologies to compounding outcomes.

**One-paragraph:** Pins a weekly cadence where the founder picks 5-7 metrics, logs ≥3 active hypotheses, and forces ≥1 decision per cycle. Produces a versioned, owner-signed spec the agent can replay every week so growth channels compound instead of drifting.

**Ефективно для:**

- Solo founder running ≥1 active growth experiment who keeps skipping reviews and watching the dashboard grow without decisions — needs a 60-min rhythm that ends with kill / continue / double-down.

## Applies If (ALL must hold)

- Solo founder OR small team running growth channels
- ≥1 active growth experiment at any time
- Founder commits ≥1 hour/week to review

## Skip If (ANY kills it)

- Pre-product phase with no metrics to review
- Team has weekly growth standup running already
- Single-channel maintenance mode (no experiments)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 5-7 chosen growth metrics with definitions | table | ops doc |
| Experimentation log (URL/path) | URL | Notion / Linear |
| Calendar block for the review | calendar event | calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/seo-manager` | Peer methodology — feeds channel-level metrics into the review. |
| `solo/marketing/content-marketer` | Peer methodology — content programs that the review evaluates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules incl. skip-this-methodology + run-the-checklist | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-weekly-growth-review-rhythm` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-weekly-growth-review-rhythm` | haiku | Schema check + threshold checks; deterministic. |
| `review-weekly-growth-review-rhythm` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-growth-review-rhythm.json` | JSON skeleton conforming to the output contract schema. |
| `templates/weekly-growth-review-rhythm.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-growth-review-rhythm.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[growth-newsletter-growth]]
- [[email-lifecycle-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
