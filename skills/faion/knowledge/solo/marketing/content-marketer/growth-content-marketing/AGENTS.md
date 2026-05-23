---
slug: growth-content-marketing
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a content-marketing spec — pillars, keyword clusters, brief, calendar, distribution checklist — gated by the 50%-on-distribution rule.
content_id: "20f7c4443a616111"
complexity: medium
produces: spec
est_tokens: 5000
tags: ["content-marketing", "seo", "keyword-research", "distribution", "organic-traffic"]
---
# Growth Content Marketing

## Summary

**One-sentence:** Generates a content-marketing spec — pillars, keyword clusters, brief, calendar, distribution checklist — gated by the 50%-on-distribution rule.

**One-paragraph:** Generates a content-marketing spec — pillars, keyword clusters, brief, calendar, distribution checklist — gated by the 50%-on-distribution rule.

**Ефективно для:**

- Solo founder running a content engine on organic SEO.
- Pre-launch keyword research consolidating topic clusters.
- Pillar-content rollout where distribution often gets cut.

## Applies If (ALL must hold)

- Topic cluster is named and the ICP is declared.
- Distribution time budget is ≥50% of production time.
- Content calendar covers ≥3 months.
- Brand voice is documented.

## Skip If (ANY kills it)

- Defining content pillars from scratch — requires ICP interviews first.
- Original-data content (interviews, proprietary research) — different methodology.
- Publishing without human review — never.
- Predicting SERP performance — agents cannot query live search engines.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ICP description | md | ICP doc |
| Topic cluster | yaml | pillar + cluster keywords |
| Brand voice doc | path | brand-voice-consistency-system output |
| Distribution channels | list | active channels + audience |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice doc gates tone. |
| growth-copywriting-fundamentals | Headline + CTA craft. |
| ai-content-quality-review | Pre-publish rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-pillar-and-cluster, r2-fifty-percent-distribution, r3-calendar-quarterly, r4-named-owner, r5-derivative-formats | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Growth Content Marketing artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: publish-and-pray, month-by-month, no-derivative | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-content-marketing` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-growth-content-marketing` | sonnet | Bounded structural check against the output contract. |
| `review-growth-content-marketing` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-content-marketing.json` | JSON skeleton matching the output contract. |
| `templates/growth-content-marketing.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-content-marketing.py` | Validate Growth Content Marketing output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[brand-voice-consistency-system]]
- [[growth-copywriting-fundamentals]]
- [[ai-content-quality-review]]
- [[content-atomization-engine]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
