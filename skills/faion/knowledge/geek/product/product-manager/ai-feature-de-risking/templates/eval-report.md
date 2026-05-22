<!--
purpose: Versioned eval report skeleton for AI feature de-risking.
consumes: kill-criteria + frozen eval set + judge scores + cost log.
produces: A reproducible eval report with n + mean + CI + verdict.
depends-on: ../scripts/validate-ai-feature-de-risking.py.
token-budget-impact: ~300 tokens when filled.
-->

---
kill_criteria_committed_at: "2026-04-10"
set: "golden-v3-frozen-2026-05-15"
set_n: 247
model: "claude-opus-4.6"
prompt_sha: "a3f1c"
judge_calibrated_at: "2026-04-20"
cost_per_run: "$<x>"
cost_ceiling: "$<2x-daily-prod>"
---

# Eval report — <feature>

## Kill criteria (pre-registered)

- Pass: <e.g. pass-rate ≥ 0.80>
- Fail: <e.g. pass-rate < 0.70>
- Freeze: <e.g. 0.70-0.80>

## Result

- pass-rate: <0.XX> ± <0.XX> (95% CI)
- n = <n>
- verdict: PASS | FAIL | FREEZE

## Cost

- Per-example: $<x>
- Total run: $<x>
- Ceiling: $<x>  (status: under | over)

## Judge calibration

- Last recalibration: <ISO date>
- Agreement vs human labels: <%>

## Decisions / Actions / Next review

- <decision 1>
- Next review: <ISO date>
