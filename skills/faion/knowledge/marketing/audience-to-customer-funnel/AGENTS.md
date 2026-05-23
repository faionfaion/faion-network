# Audience to Customer Funnel

## Summary

**One-sentence:** Generates a 4-stage solo-marketer funnel artefact — awareness, interest, consideration, conversion — with per-stage KPI + drop-off thresholds — gated by named stage owners.

**One-paragraph:** Solo marketers track 'subscribers' or 'visits' without knowing which stage leaks. This methodology pins a 4-stage funnel (Awareness → Interest → Consideration → Conversion) with one named KPI per stage, a drop-off threshold that triggers intervention, and a single owner accountable. Output: a FunnelArtefact + per-stage diagnostic.

**Ефективно для:**

- Solo founder with traffic but no understanding of where it dies.
- Newsletter operator who watches subscribers but ignores click-to-paid.
- Pre-monetisation product needing the first funnel definition.
- Audit of an existing funnel against minimum standards.

## Applies If (ALL must hold)

- Operator runs ≥1 content / acquisition channel.
- Tracking surface exists (Plausible / GA / Mixpanel / spreadsheet).
- There IS a paid conversion goal (not pure awareness play).
- Operator has ≥30 days of data OR is launching new and needs the definition.

## Skip If (ANY kills it)

- Pre-product hobby project with no monetisation goal.
- B2B enterprise sale handled via outbound only — funnel is different.
- Existing well-instrumented funnel already meeting these standards.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Channel inventory + cost per channel | list | operator marketing log |
| Conversion event definition | tracked event name | analytics config |
| 30 days of channel data | CSV per channel | Plausible / GA / Mixpanel |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| audience-to-paid-conversion-loop | Conversion stage shares definitions with the paid-loop methodology. |
| brand-voice-consistency-system | Content quality at awareness/interest depends on voice consistency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-four-stages-fixed, r2-one-kpi-per-stage, r3-named-stage-owner, r4-drop-off-threshold, r5-30day-baseline | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Audience to Customer Funnel artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: vanity-metrics-only, funnel-of-fifteen-stages, no-drop-off-threshold, single-source-baseline | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-funnel` | sonnet | Per-business stage definition. |
| `diagnose-drop-off` | sonnet | Reads stage data + names the leak. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audience-to-customer-funnel.json` | FunnelArtefact JSON skeleton. |
| `templates/audience-to-customer-funnel.md` | Per-stage definitions + diagnostic. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audience-to-customer-funnel.py` | Validate FunnelArtefact JSON against the schema. | Monthly review + after KPI redefinition. |

## Related

- [[audience-to-paid-conversion-loop]]
- [[brand-voice-consistency-system]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
