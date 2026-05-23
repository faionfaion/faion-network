# Meta Audience Targeting (Granular)

## Summary

**One-sentence:** Produces an audience-by-audience targeting spec: interest stacks, behavioral filters, custom segments, dynamic creative + Advantage+ Audience gate, exclusion matrix for all funnel stages.

**One-paragraph:** Granular complement to ads-meta-targeting (tier strategy). This methodology focuses on the interest + behavior + demo composition INSIDE each tier: what interest stacks size correctly, which behavioral filters survive iOS attribution loss, how Advantage+ Audience interacts with manual audiences, and the full exclusion matrix per funnel stage (TOFU excludes converters; MOFU excludes purchasers within 30d; BOFU excludes converters within 7d).

**Ефективно для:**

- Deep audience composition після tier strategy.
- Interest stacks 2-3 broad themes (no AND-stacking).
- Advantage+ Audience коли ≥$100/day + broad-appeal product.
- Exclusion matrix по funnel stages (TOFU/MOFU/BOFU).

## Applies If (ALL must hold)

- Existing campaign needs granular audience composition (after tier strategy).
- Iterating on broad audiences that under-deliver.
- Advantage+ Audience experiments with measurable lift hypothesis.
- Funnel-wide exclusion-matrix cleanup.

## Skip If (ANY kills it)

- First-time campaign with no tier strategy — use ads-meta-targeting first.
- Cold start without a measurable hypothesis — random interest stacks waste money.
- Pixel insufficient for behavioral filters — fix pixel first.
- Audience size <500K — no granularity worth it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tier audience spec | JSON | ads-meta-targeting |
| Pixel + CAPI live | dashboard | ads-conversion-tracking |
| Exclusion lists per funnel stage | CRM lists | RevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-meta-targeting` | Tier strategy provides the parent structure. |
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Pixel events seed behavioral filters. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for meta-audience-targeting | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interest-stack-design` | sonnet | Theme composition + sizing. |
| `exclusion-matrix-fill` | haiku | Apply per-stage exclusion rules. |
| `advantage-plus-gate` | haiku | Apply broad / budget gate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/targeting-spec.md` | Granular targeting spec Markdown skeleton. |
| `templates/exclusion-matrix.csv` | Per-stage exclusion matrix seed. |
| `templates/targeting-spec.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-meta-audience-targeting.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-targeting]]
- [[ads-meta-campaign-setup]]
- [[ads-meta-creative]]
- [[ads-retargeting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
