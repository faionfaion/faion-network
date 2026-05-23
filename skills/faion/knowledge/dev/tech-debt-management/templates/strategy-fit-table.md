<!--
purpose: Per-strategy fit profile + exit criteria; reference table consumed during plan drafting.
consumes: nothing — used as authoring guide.
produces: strategy choice anchored to fit profile.
depends-on: scored debt register present.
token-budget-impact: ~220 tokens when copied.
-->

# Strategy fit table

| Strategy | When it fits | Exit criterion | Cadence |
|----------|--------------|-----------------|---------|
| boy-scout         | Score &lt; threshold/2; small localized debt; "tidy as you pass through" | File LoC ≤ cap; debt label removed | Continuous, attached to any PR touching the file |
| feature-attached  | Score threshold..2× threshold; localized to a single area; a feature touches the same area | Feature ships + debt items closed | Per-sprint, attached to the feature ticket |
| dedicated-sprint  | Score &gt; 2× threshold; localized but too large to chunk into features | All items in epic closed | One full sprint dedicated |
| strangler-fig     | Score &gt; 2× threshold; broad impact (cross-service); old system must keep running | 100% traffic switched, old system removed after 2-week stability | Multi-sprint epic |

## Picking

Start from score band. If band is unambiguous, the strategy follows. If the item spans multiple areas, lean Strangler Fig. If the team's sprint cadence is too tight for dedicated, fall back to feature-attached with explicit budget.

## Gate examples

- boy-scout: LoC cap CI check (file fails if &gt; 200 lines).
- feature-attached: lint rule covering the category (e.g. ruff T201 for print-statements).
- dedicated-sprint: complexity-cap (cyclomatic &lt; threshold) on the area.
- strangler-fig: traffic-routing gate; old endpoint disabled after switch.
