#!/usr/bin/env bash
# purpose: turn a one-line stakeholder ask into 3 framing questions + strawman outcome
# consumes: one-line stakeholder ask as $1..$n, MODEL env var (default claude-opus-4-7)
# produces: JSON object matching stance-review-schema.json shape
# depends-on: content/01-core-rules.xml (positioning rule), llm CLI
# token-budget-impact: ~150 tokens of header + variable LLM output
# Usage: ba-frame "add a CSV export to the dashboard"
# Requires: llm CLI (pip install llm llm-anthropic) and MODEL env var or default.
set -euo pipefail
: "${MODEL:=claude-opus-4-7}"
ASK="${*:?usage: ba-frame <one-line stakeholder ask>}"
llm -m "$MODEL" --no-stream <<EOF
You are a strategic BA. The stakeholder said: "$ASK".
Refuse to design a solution. Output strict JSON:
{
  "problem_hypothesis": "...",
  "framing_questions": ["q1","q2","q3"],
  "strawman_outcome": {"kpi":"...","delta":"...","horizon_months":0}
}
Rules: no solution proposals, no feature descriptions,
  each framing question must be open-ended,
  KPI must reference a real metric category (revenue, cost, NPS, time, error rate).
EOF
