# Feature Prioritization (RICE)

## Summary

Score each candidate feature as `(Reach × Impact × Confidence) / Effort`. Reach = users affected per quarter (cite an analytics query or proxy metric). Impact = {3, 2, 1, 0.5, 0.25} only — do not add intermediate values. Confidence = 100%/80%/50% only — drop one tier for each unknown. Effort = person-months including design, dev, QA, and a 30% buffer for unknowns; engineers must own this column. Sort highest-to-lowest, sanity-check, then apply strategic veto for one bet that may rank lower but is the only path to differentiation.

## Why

Feature prioritization driven by gut or loudest voice (HiPPO) produces inconsistent decisions and scope creep. RICE forces stakeholders to debate quantified inputs rather than opinions, and the division by Effort surfaces effort-adjusted ROI that verbal discussion consistently misses. The fixed impact and confidence scales prevent score inflation and keep cross-feature comparison valid over time. Tracking post-ship actuals against estimates is the only mechanism that improves future confidence scores.

## When To Use

- Comparing 5+ candidate features in a single quarter where reach and effort vary widely.
- Killing pet features: a numeric score forces debate on inputs, not opinions.
- Triaging a backlog after a discovery sprint produced more validated problems than capacity.
- Deciding between two features that both look "obviously valuable" — RICE exposes effort-adjusted ROI.

## When NOT To Use

- Solo founder with fewer than 3 candidates — overhead exceeds signal; pick by gut and ship.
- Hard-deadline regulatory or compliance work — there is no score; you ship or get fined.
- Discovery phase before reach and impact data exist — confidence will be 50% across the board and ranking is noise.
- Strategic bets / 0-to-1 features — RICE punishes high-effort items even when they are the only path to a moat.

## Content

| File | What's inside |
|------|---------------|
| `content/01-formula.xml` | RICE formula, factor definitions, fixed scales, calculation example, and score-inflation antipatterns. |
| `content/02-process.xml` | Six-step scoring process, sanity check, strategic veto rule, and quarterly re-scoring cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rice-scorecard.md` | RICE scoring table with notes per feature and rank. |
| `templates/rice-decision-record.md` | Per-feature decision record: inputs, rationale, rank, and decision. |
| `templates/rice-rank.sh` | Bash script: reads a CSV (name, reach, impact, confidence, effort) and outputs sorted RICE scores. |
