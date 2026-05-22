<!--
purpose: 45-minute structured interview with SME to extract correctness rubric
consumes: per-intent 30-query sample, intent name
produces: spec (rubric block ready for contract)
depends-on: intents named in step 1 of procedure
token-budget-impact: 0 at runtime (template, not loaded)
-->

# SME Interview Guide — Acceptance Contract

Duration: 45 min per intent. Format: structured + adversarial.

## 0–5 min: Frame
- "I will not ship this feature until you sign off on what 'correct' means here. Your judgement is the ground truth."
- Show the intent name + 5 representative queries.

## 5–20 min: Walk pass → fail
- Read query #1. Ask: "Is this a passing answer? Why?"
- Capture verbatim reasoning. Tag each criterion (citation present, source-grounded, correct order, etc.).
- Repeat for borderline + fail examples.

## 20–35 min: Failure-mode probing
- Ask: "What is the worst answer this feature can give and still be acceptable?"
- Ask: "What is the worst answer that is NOT acceptable? Why?"
- Capture `acceptable_failure` line.

## 35–42 min: Threshold negotiation
- Show current-system baseline. Ask: "Would you ship at this number? At baseline × 1.1? × 1.2?"
- Anchor every threshold to a baseline.

## 42–45 min: Recontract trigger
- Ask: "What event would make you want to re-open this rubric?" Capture as recontract triggers.

## Output
- Filled `intent-rubric-card.md` per intent
- SME-quoted phrases verbatim (never paraphrase the SME)
