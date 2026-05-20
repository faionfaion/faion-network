---
slug: sow-template-with-traced-assumptions
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: SoW template where every scope clause, exclusion, and price assumption traces by ID to a discovery artefact (interview note, doc reference, decision memo), so the BA can defend scope post-signature.
content_id: "e5fb9e20d36f27d5"
tags: [business-analyst, sow, pre-bid, fixed-price, p4-outsource, traceability]
---
# SoW Template with Traced Assumptions

## Summary

**One-sentence:** A fixed-price SoW template where every scope clause, exclusion, and pricing assumption carries an inline `[A-NN]` ID that traces to a discovery artefact, so any later "but we thought..." dispute lands on a documented source.

**One-paragraph:** P4 outsource shops lose margin to assumption-creep on fixed-price engagements: clients challenge scope post-signature ("we assumed X was included"), and the BA cannot point to *which* discovery interaction set the assumption. This methodology fixes the SoW shape: every in-scope item, exclusion, and dependency clause has an `[A-NN]` assumption ID, and the SoW ships with an `assumptions.md` appendix mapping each ID to a concrete artefact (interview note timestamp, requirement doc line, decision memo paragraph). Scope changes post-signature must cite an assumption ID to be considered — no ID, no change. Closes the gap between BA discovery output and the legal/commercial SoW.

## Applies If (ALL must hold)

- Engagement model is fixed-price (or fixed-price-per-phase), not pure T&M.
- A pre-bid discovery phase has produced at least one interview note, requirements doc, or signed decision memo.
- The BA owns or co-owns the SoW content (not pure legal hand-off).
- Client is willing to sign an SoW that includes an explicit assumptions appendix.

## Skip If (ANY kills it)

- Pure T&M engagement — assumptions are managed via change orders, not the SoW body.
- Discovery phase did not produce written artefacts — trace targets do not exist; fix discovery first.
- Standing MSA with the client already defines all scope language — use the MSA's change protocol instead.
- Engagement under 2 weeks total — overhead exceeds dispute risk.

## Prerequisites

- Discovery artefact folder with stable URLs/paths (interview notes, requirement docs, decision memos).
- Draft scope list and exclusion list from the pre-bid workshop.
- Pricing model worksheet (so assumption IDs can attach to pricing lines).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/` | Baseline elicitation + documentation conventions are assumed. |
| `pro/pm/freelancer-proposal-template-fixed-vs-tm` | Pricing-model framing the SoW must align with. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules for assumption-ID traceability across the SoW body and appendix. | ~900 |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer: `freelance-proposal-template`, `cr-impact-memo-template`, `decision-rationale-capture`
- external: PMI Practice Standard for Project Estimating §4.4 (estimating assumptions documentation)
