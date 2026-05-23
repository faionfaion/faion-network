# Experiment Hypothesis Scoring

## Summary

**One-sentence:** ICE/PIE/RICE rubric for CRO experiment intake — explicit thresholds (min projected lift × confidence), behavioural anchors, ≥2 raters, frozen-during-cycle, evidence-required.

**One-paragraph:** `growth-conversion-optimization` treats CRO as a "do testing" verb without an upstream scoring framework. This rubric adapts ICE/PIE/RICE to CRO with explicit thresholds (minimum projected_lift × confidence to enter the queue) + behavioural anchors per band + ≥2-rater calibration + frozen-during-cycle discipline. Core rules: behavioural anchors per band (no "high impact" without observable signal); evidence-required (every score cites a quote / ticket / dashboard row); ≥2 raters with discrepancy escalation; frozen rubric during the review window; minimum entry threshold (queue cannot accept low-lift × low-confidence ideas). Output: a versioned, sortable hypothesis backlog.

**Ефективно для:**

- Weekly CRO cadence — landing-page-team-of-one needs intake discipline.
- A/B test ICE/PIE/RICE rubric — choose one + freeze.
- Quarterly experiment portfolio audit — re-score backlog against fresh data.
- Agency / freelance CRO retainer — shared scoring with client.

## Applies If (ALL must hold)

- Weekly or biweekly experiment cadence with a queue of ≥3 hypotheses.
- Access to landing-page analytics (sessions, conversions, segment data).
- ≥2 raters available for calibration (founder + designer, or 2 freelancers).
- Authority to push a hypothesis to test (no further sign-off needed for top of queue).

## Skip If (ANY kills it)

- No traffic / no data — score-based prioritization is meaningless without funnel signal.
- Pre-PMF where the metric to optimize is unclear — fix PMF discovery first.
- Single-shot test (one campaign launch) — overhead exceeds value.
- Single-rater org with no second voice — rule r3 cannot be met.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hypothesis backlog | spreadsheet / Notion table | growth team |
| Page analytics (sessions, conv rate per segment) | dashboard | analytics tool |
| Frozen rubric file (this cycle) | YAML / JSON | growth lead |
| Prior cycle's verdicts (for carry-forward) | report | experiment-verdict-template |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ab-testing-basics]] | Statistical foundations of the lift × confidence threshold. |
| [[experiment-ledger-discipline]] | The ledger that consumes scored hypotheses. |
| [[experiment-verdict-template]] | Closes the loop after a hypothesis ships. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: behavioural-anchor-per-band, evidence-required, two-rater-calibration, frozen-rubric, min-entry-threshold | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one scored hypothesis + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick rubric → score with 2 raters → calibrate → publish → freeze | 600 |
| `content/06-decision-tree.xml` | essential | Tree mapping discrepancy + threshold signals to action | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-hypothesis` | sonnet | Bounded judgment per axis. |
| `calibrate-raters` | sonnet | Discrepancy resolution. |
| `lint-evidence` | haiku | Token-level evidence presence check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scored-hypothesis.json` | JSON example of one scored hypothesis |
| `templates/rubric.yaml` | Frozen rubric with behavioural anchors per band |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-experiment-hypothesis-scoring.py` | Validate the scored-hypothesis JSON against the schema | After scoring, before adding to ledger |

## Related

- [[ab-testing-basics]]
- [[experiment-ledger-discipline]]
- [[experiment-verdict-template]]
- [[icp-message-mining-from-ai-conversations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from discrepancy-between-raters + threshold signals to the next action (re-score / kill / promote / freeze) and pins the rule from `01-core-rules.xml`. Use it during the calibration step — bypassing it produces drift between cycles.
