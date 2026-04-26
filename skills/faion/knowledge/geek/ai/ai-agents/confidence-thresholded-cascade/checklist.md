# Checklist — Confidence-Thresholded Cascade

## Design

- [ ] Picked cheap and strong model from same family or proven pair
- [ ] Schema for cheap model includes `confidence: float` (0.0 to 1.0)
- [ ] Confidence field comes AFTER the answer field (post-answer self-assessment)
- [ ] Threshold chosen — usually 0.80-0.90 to start

## Calibration

- [ ] Ran 100+ eval tasks through cheap model only
- [ ] Bucketed actual accuracy by confidence (0-0.5, 0.5-0.7, 0.7-0.85, 0.85-0.95, 0.95-1.0)
- [ ] Verified accuracy increases with confidence (calibration is real)
- [ ] If poorly calibrated, switched to logprob-based or different model

## Production

- [ ] Escalation rate logged per request
- [ ] Cost per task tracked: cascade vs always-strong
- [ ] Quality metric tracked: accuracy compared to always-strong on a sample
- [ ] Drift alerts: escalation rate suddenly spiking or dropping → investigate

## Anti-pattern checks

- [ ] Threshold not arbitrary
- [ ] Not always escalating (defeats the cascade)
- [ ] Cascade depth ≤ 3 levels
- [ ] No infinite escalation loops

## Composition

- [ ] cheap-model output schema follows schema-field-order rule
- [ ] OTel spans capture which level handled the request
- [ ] If cheap model says "I don't know" explicitly, escalate without checking confidence
