---
slug: freelancer-niche-positioning
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Single-person service positioning — 'I do X for Y so they Z' one-liner validated against 3 external signals (search-find, peer recall, buyer paraphrase) before any other change.
content_id: "freelancer-niche-1"
complexity: medium
produces: spec
est_tokens: 3200
tags: [freelance, positioning, niche, ICP, solo-consultant]
---
# Freelancer Niche Positioning

## Summary

**One-sentence:** Single-person service positioning — 'I do X for Y so they Z' one-liner validated against 3 external signals (search-find, peer recall, buyer paraphrase) before any other change.

**One-paragraph:** Single-person service businesses fail or stall when positioning is fuzzy. This methodology pins the format 'I do X for Y so they Z' (specific verb X, named buyer segment Y, measurable outcome Z) and the 3-signal validation that must pass before anything else changes: search-find (typing the X+Y phrase finds you in &lt;5 results), peer recall (3 of 5 peers paraphrase your one-liner back without prompting), buyer paraphrase (≥1 buyer in last 30 days repeats the outcome Z back). Core rules: format strict; numeric outcome Z; 3-of-3 signals must pass; review monthly; redo if any signal degrades.

**Ефективно для:**

- Solo consultant / freelancer — first or 2nd positioning attempt.
- Niche pivot — validating the new positioning lands.
- Pre-launch — positioning before any other GTM spend.
- Quarterly positioning health-check.

## Applies If (ALL must hold)

- Single-person service business (solo or 1-2 person micro-agency).
- Authority to change positioning unilaterally.
- Access to ≥5 peers + ≥1 recent buyer for the validation signals.
- Capacity to wait 2-4 weeks for signals to land.

## Skip If (ANY kills it)

- 10+ person agency with multiple offerings — different methodology applies.
- Pre-discovery (don't know what you can deliver) — discover first.
- Single anchor client that defines the work — positioning is downstream.
- Fewer than 5 peers reachable for the recall test.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Capability list (what you can deliver) | doc | self-audit |
| Buyer interviews (≥2 in target segment) | transcripts | own ops |
| Peer list (≥5 reachable) | list | network |
| Recent buyer (last 30 days) | named contact | CRM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[freelance-pilot-pricing]] | Pilot pricing follows positioning. |
| [[freelance-rate-jump-tactics]] | Rate jump follows established positioning. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: format-x-y-z, numeric-outcome, search-find-test, peer-recall-test, buyer-paraphrase-test | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-positioning` | sonnet | Light judgment on specificity. |
| `lint-format` | haiku | Check unit/direction/magnitude presence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/positioning-spec.json` | JSON example of positioning spec |
| `templates/validation-log.md` | Markdown skeleton for the 3-signal validation log |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-niche-positioning.py` | Validate one spec JSON against the schema | After draft, before publish |

## Related

- [[freelance-pilot-pricing]]
- [[freelance-rate-jump-tactics]]
- [[icp-message-mining-from-ai-conversations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
