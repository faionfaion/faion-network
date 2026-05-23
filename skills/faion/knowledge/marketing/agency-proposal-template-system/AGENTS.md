# Agency Tiered-Proposal Template System

## Summary

**One-sentence:** Tiered (Good / Better / Best) anchored-pricing proposal template — sent within 48h of discovery, fixed scope per tier, 6-month minimum, designed to anchor on the middle tier.

**One-paragraph:** Tiered (Good / Better / Best) anchored-pricing proposal template — sent within 48h of discovery, fixed scope per tier, 6-month minimum, designed to anchor on the middle tier. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

**Ефективно для:**

- Мікро-агенції що конвертують inbound leads у signed retainers (4-6 тижневий цикл).
- Founders що відмовляються від custom-proposal-per-lead — це template system replacement.
- Якщо single-price proposals — close-rate < 25%, перейти на 3-tier.
- Перед щоквартальним sales-retrospective щоб тюнити anchoring.

## Applies If (ALL must hold)

- Agency / studio робить retainer / project-fee work з 4+ delivered engagements.
- Founder особисто handles proposal stage (or one named SDR).
- Average deal size > $3k/mo — нижче tiered pricing overhead не окуповується.

## Skip If (ANY kills it)

- Productized fixed-SKU без custom scope — single-price краще.
- Hourly billing only — це pricing problem, не proposal system.
- Enterprise > $50k/mo — потрібен MSA + custom SOW, не 3-tier template.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist` | Parent role context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `draft-rationale` | sonnet | Per-decision rationale + rejected alternatives. |
| `review-tradeoffs` | opus | Cross-decision synthesis + reversibility judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-skeleton.md` | Agency Tiered-Proposal Template System skeleton — fill per artefact, do not commit free-form output. |
| `templates/_smoke-test.md` | Minimum viable filled-in Agency Tiered-Proposal Template System. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-proposal-template-system.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[from-hourly-to-fixed-transition]]
- [[agency-niche-positioning]]
- [[agency-discovery-call-scorecard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
