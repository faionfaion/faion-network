<!--
purpose: Single discovery experiment report — hypothesis, setup, success/kill thresholds, results and validated/invalidated decision.
consumes: the assumption + severity from the discovery kickoff's risk assessment
produces: an experiment report
depends-on: content/01-core-rules.xml (r3-kill-threshold, r4-cheap-to-fail)
token-budget-impact: ~350 tokens when filled
-->

# Experiment: <name>

## Hypothesis
We believe <assumption>.
We will test by [method].
We will know we're right when <specific_metric_threshold>.

## Setup
- **Method:** [Interview / Prototype test / Fake door / A/B / Survey / Spike]
- **Audience:** [Segment and how recruited]
- **Sample size:** [N] — justified by: [power calculation or published rule of thumb]
- **Duration:** <x_days>

## Thresholds
- **Success:** <metric> >= <threshold>
- **Kill:** <metric> < <kill_threshold>
  (kill threshold must differ from success threshold)

## Results

| Metric | Target | Actual | Pass/Fail |
|--------|--------|--------|-----------|
| <metric_1> | [X] | [Y] | Pass/Fail |
| <metric_2> | [X] | [Y] | Pass/Fail |

## Observations
- <observation_1>
- <observation_2>

## Learnings
- <key_insight_1>
- [Null result if any — still record it]

## Decision
- [ ] Validated — proceed to delivery
- [ ] Invalidated — pivot (describe pivot)
- [ ] Unclear — more discovery needed (specify what and timebox)

## Next Steps
- [Action 1 with owner]
- [Action 2 with owner]
