# Meta Ads Reporting and Diagnosis

## Summary

**One-sentence:** Generates a Meta weekly report + action queue: column preset (CPM/CTR/CPC/CVR/CPA/ROAS), breakdowns by age/placement/device, symptom→root-cause map (creative fatigue / audience fatigue / LP fail).

**One-paragraph:** Structured analyze-decide-act cycle for Meta Ads. Pull column preset (CPM, CTR, CPC, CVR, CPA, ROAS, Frequency), run breakdowns by age, placement, device, country. Map each symptom (high CPA, low CTR, high frequency, low ROAS) to a root cause (creative fatigue, audience saturation, landing-page drop-off, attribution shift) and a concrete lever. Every report must end in a ranked action queue.

**Ефективно для:**

- Тижневий performance review активних Meta-кампейнів.
- CPA spike або CTR drop — діагностика через breakdown.
- Frequency >2.5 — anti-fatigue rotation.
- Stakeholder summary з actionable рекомендаціями.

## Applies If (ALL must hold)

- Weekly performance review for any active Meta campaign with ≥50 conv/wk.
- Diagnosing a CPA spike, CTR decline, or frequency creep.
- Stakeholder report covering executive summary + creative + audience.
- Deciding which campaigns to scale, hold, or pause.

## Skip If (ANY kills it)

- Daily micro-optimization — too noisy; weekly cadence only.
- Campaigns still in learning phase (<50 conv/wk) — data not representative.
- Cross-platform attribution decisions — use a dedicated MMM/attribution tool.
- Brand-only awareness campaigns with no conversion event — different KPI set.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Ads Manager + CAPI | OAuth + dashboard | platform owner |
| KPI target table | JSON | stakeholder |
| Last 30-day creative + audience inventory | CSV | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-meta-campaign-setup` | Campaign structure / naming convention required to interpret report rows. |
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Pixel + CAPI events define what CPA / ROAS measure. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-meta-reporting | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pull-and-breakdown` | haiku | Mechanical data assembly. |
| `diagnose-symptoms` | sonnet | Map symptom→root-cause requires judgement. |
| `prioritize-actions` | sonnet | Rank top-5 by expected impact × owner availability. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-report.md` | Meta weekly report Markdown skeleton with column preset + breakdowns + actions. |
| `templates/breakdown-checklist.md` | Breakdown checklist for the weekly cadence. |
| `templates/report-artefact.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-meta-reporting.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-meta-campaign-setup]]
- [[ads-meta-creative]]
- [[ads-meta-targeting]]
- [[ads-conversion-tracking]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
