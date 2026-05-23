---
slug: growth-cold-outreach
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a cold outreach campaign spec: focused prospect list (≤200), personalisation rule, ≤5-sentence email body, 4-5 step sequence, throttle and stop conditions — turns strangers into qualified replies without spam blowback.
content_id: "9f43951d988e807f"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["cold-email", "outreach", "sales", "b2b", "solo"]
---
# Cold Outreach

## Summary

**One-sentence:** Generates a cold outreach campaign spec: focused prospect list (≤200), personalisation rule, ≤5-sentence email body, 4-5 step sequence, throttle and stop conditions — turns strangers into qualified replies without spam blowback.

**One-paragraph:** Cold Outreach produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Solo founder running outbound to ≤200 prospects per cycle who needs a campaign spec with personalisation rule, sequence depth, and stop conditions before sending land hits spam-trap reputation.

## Applies If (ALL must hold)

- ICP is defined enough to source ≤200 prospects
- Sender domain has DKIM/SPF/DMARC + warmup history
- Founder commits to manual personalisation step per prospect

## Skip If (ANY kills it)

- Untargeted blast >500 contacts — different (spam-grade) methodology
- Domain not warmed up — fix deliverability first
- Email sender on Gmail personal account with no domain — switch domain first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ICP definition + qualifiers | doc | positioning artefact |
| Prospect list (≤200, with name + role + signal) | CSV | Apollo / LinkedIn Sales Nav / manual |
| Sender warmup health | score | Mailwarm / Lemwarm |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `growth-indiehackers-strategy` | Adjacent channel — community + content > pure cold. |
| `objection-bank` | Captures replies and feeds future outreach. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-list-size-leq-200, r2-personalisation-rule-explicit, r3-body-5-sentences-max, r4-sequence-4-to-5-steps, r5-stop-on-reply-or-bounce, r6-throttle-and-warmup | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-cold-outreach` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-growth-cold-outreach` | haiku | Schema check + threshold checks; deterministic. |
| `review-growth-cold-outreach` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-cold-outreach.json` | JSON skeleton conforming to the output contract schema. |
| `templates/growth-cold-outreach.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-cold-outreach.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[growth-indiehackers-strategy]]
- [[objection-bank]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
