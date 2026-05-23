---
slug: single-channel-bet-selector
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Single Channel Bet Selector — a decision rubric that picks ONE primary growth channel by intersecting founder strengths, ICP behaviour, and proof-of-traction signal, instead of trying four poorly.
content_id: "39d04cdaa5452d44"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: [single-channel-bet-selector, marketing, pro]
---
# Single Channel Bet Selector

## Summary

**One-sentence:** A scoring rubric that intersects founder DNA (what you'll execute weekly without dropping), ICP behaviour (where they already hang out and search), and traction signal (where you've already had one real lead) to pick a single channel to bet on for 90 days.

**One-paragraph:** Solo founders fail by trying four channels poorly. Existing growth methodologies enumerate channels and tactics but do not help pick which one fits this founder + this ICP right now. This selector forces a written rubric across three axes — founder fit (1-5), ICP density (1-5), early traction (1-5) — and refuses to let the founder pick a channel that scores below 12/15. The output is a single committed 90-day plan; channels 2 and 3 go in a parking lot for review after the bet is graded.

**Ефективно для:**

- Solo founder обирає ОДИН канал на 90 днів — не чотири паралельно.
- Three-axis scoring (founder fit / ICP density / early traction).
- Pre-committed kill criterion на week 12 без emotional re-negotiation.
- Команд, які 'пробують всі канали' і не виходять з $0 traction.

## Applies If (ALL must hold)

- the founder is currently doing 0–4 channels with no single one above $0 → real-revenue traction
- the founder has at least 5 paying customers (or 50 qualified conversations) to read ICP behaviour from
- the founder can commit to one channel for 90 days without re-deciding
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- one channel is already producing measurable revenue — keep going, don't re-pick
- founder has zero direct ICP signal (no customers, no interviews) — run discovery first
- the product is pre-launch with no audience to observe — defer

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operating-trigger event | log / calendar / ticket | upstream observability |
| Methodology preconditions checklist | YAML | this methodology's `templates/single-channel-bet-selector.md` |
| Named owner contact | string | team RACI / org chart |
| Write-access to artefact store | URL | team's knowledge space |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream artefact template that anchors this methodology's recurring loop. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)
| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: written rubric, three-axis scoring, minimum threshold, 90-day commitment, kill criterion |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/single-channel-bet-selector.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/single-channel-bet-selector.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-single-channel-bet-selector.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- upstream playbook: `p1-solo-saas-builder/$0 → $4K MRR bootstrap journey`
- parent skill: `pro/marketing/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

