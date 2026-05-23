# Meta Ads Creative Strategy

## Summary

**One-sentence:** Produces a Meta creative brief + variant matrix: hook ≤3s, value-prop ≤8 words, CTA verb-led, native-feed-format, 3-5 variants per ad set rotated weekly to fight fatigue.

**One-paragraph:** Meta auction rewards thumb-stop in the first 3 seconds and punishes ads that look like ads. This methodology codifies the hook → value-prop → CTA structure, mandates native-feed format (1:1 / 4:5 / 9:16), and enforces creative-rotation cadence so frequency caps + creative fatigue don't tank CPM. Output is a creative brief + variant matrix (3-5 per ad set) and a refresh schedule.

**Ефективно для:**

- Ad-set creative brief з 3-5 варіантів на тиждень/ротацію.
- Frequency >2.5 і CTR падає — антифатига cycle.
- Production budget для UGC / video-hook тестів.
- Native-feed formats (1:1, 4:5, 9:16) на Reels/Stories/Feed.

## Applies If (ALL must hold)

- Active Meta campaign needing a creative brief for production.
- Frequency >2.5 or CTR dropping week-over-week.
- Launching 3-5 creative variants per ad set for matrix testing.
- Production budget available for at least UGC + static + video formats.

## Skip If (ANY kills it)

- Less than 3 creative variants planned — no matrix, single-point failure on creative fatigue.
- No production budget for native-feed format — landscape stock crops will fail.
- Awareness-only campaign with no conversion event — different brief structure (brand methodology).
- Existing ads with frequency ≤1.5 and CTR healthy — no need to refresh yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Audience + funnel stage | spec | ads-meta-campaign-setup |
| Past-performance creative dataset | JSON / dashboard | Ads Manager |
| Brand assets + voice guide | PDF / Figma | brand owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-meta-campaign-setup` | Creative brief consumes the audience + funnel stage chosen there. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-meta-creative | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hook-drafts` | sonnet | Creative judgement on pattern-interrupt language. |
| `format-mapping` | haiku | Mechanical: funnel stage → native format set. |
| `variant-matrix` | sonnet | Diversify hooks while preserving value-prop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/creative-brief.md` | Meta creative brief Markdown skeleton. |
| `templates/variant-matrix.csv` | Variant matrix CSV header for production hand-off. |
| `templates/creative-brief.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-meta-creative.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-campaign-setup]]
- [[ads-meta-targeting]]
- [[ads-meta-reporting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
