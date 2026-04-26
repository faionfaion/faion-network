# RICE Prioritization: [Feature Set]

**Date:** [Date]
**Analyst:** [Name]
**Reach baseline source:** [URL or dataset]
**Confidence default:** 0.8 (override to 1.0 requires primary-source URL)

## Scoring Criteria

| Factor | Scale | Rule |
|--------|-------|------|
| Reach | Users per quarter | Must cite source URL; tag "reach_estimated_no_baseline" if none |
| Impact | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal | Calibrate by quartile rank first |
| Confidence | 1.0=high (primary source required), 0.8=medium (default), 0.5=low | Default 0.8; reject 1.0 without link |
| Effort | Person-weeks | Must come from delivery team; kick back if missing |

## Scores

| REQ-ID | Requirement | Reach | Impact | Conf | Effort | RICE | Rank | Data Quality Flags |
|--------|-------------|-------|--------|------|--------|------|------|--------------------|
| [ID] | [Name] | [X] | [X] | [0.8] | [X] | [Score] | [#] | [flags] |

RICE Score = (Reach × Impact × Confidence) / Effort

## Data Quality Flag Legend

- `reach_estimated_no_baseline` — Reach has no source URL
- `confidence_at_100_unjustified` — Confidence = 1.0 without primary source
- `impact_clustered_at_median` — >70% of items have same impact value; recalibrate
- `effort_missing` — row is null until delivery estimates

## Sensitivity Check

Top item rank changes when Confidence perturbed ±20%:
- Low confidence rank items (rank shifts > 5): [list]
