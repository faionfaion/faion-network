# Examples — Confidence-Thresholded Cascade

## Example 1: Customer-support classifier

10K tickets/day. Pure-Sonnet: $40/day. Cascade Haiku→Sonnet at 0.88: 78% handled by Haiku at $0.0005/each, 22% escalated to Sonnet at $0.01/each. Total: $11/day. ~75% saved with no quality regression on monthly evals.

## Example 2: FAQ chatbot

Most questions are repeats with strong priors. Haiku confidence calibrated: 91% at threshold 0.85 stay with Haiku. Cascade serves 12K/day at $5 vs $90 single-Sonnet — 94% saved.

## Example 3: Code-review triage

Cheap model decides "trivial PR" vs "needs review". 60% of PRs are dependency bumps and trivial → handled by Haiku with confidence > 0.90. The 40% that aren't get escalated to Opus for deep review.

## Example 4: Anti-example — uncalibrated threshold

Team set threshold at 0.5 because "halfway seems reasonable." Production accuracy dropped 8 points. Calibration revealed: at confidence 0.5, Haiku was right only 58% of the time. Threshold 0.85 (where it was 92% accurate) restored quality.

## Example 5: When cascade fails — creative writing

A team tried cascade for blog-post generation. "Confidence" was meaningless for creative output — Haiku confidently produced low-quality drafts, and nothing escalated to Sonnet. Result: cascade made quality WORSE.

Lesson: cascade fits classification/extraction, not generation.

## Example 6: Drift detection

Escalation rate stable at 22% for months. Suddenly jumps to 67% after a prompt update. Root cause: the new prompt confused Haiku, which started rating its own confidence lower. Reverted prompt; rate normalized.

This is why instrumenting escalation rate matters.

## Example 7: Three-level production cascade

```
Haiku  → 70% handled at $0.0005
Sonnet → 25% handled at $0.005
Opus   →  5% handled at $0.05
weighted avg ≈ $0.0035 vs $0.05 single-Opus → 92% saved
```

Three levels work when the task has a real difficulty distribution.

## Example 8: Confidence with explicit IDK

```python
class CheapAnswer(BaseModel):
    answer: str | None
    confidence: float
    flag_unclear: bool
```

A question about a deprecated feature that the cheap model has never seen → it sets `flag_unclear=True` and escalates regardless of confidence. This catches blind-spot failures that confidence alone misses.
