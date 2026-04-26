# VUI Testing Best Practices

## Summary

A four-layer VUI test strategy: unit (intent accuracy), integration (dialog flow completion), user (moderated session with 5+ real users), stress (noise, accents, interruptions). Bucket accuracy by accent/age/gender — overall percentage hides subgroup failures of 15–30 points. Track "completion at attempt N" not just "completion" — N=2 is acceptable, N=4 is a failure. Lock LLM voice agent seeds for deterministic regression.

## Why

Synthetic test utterances from internal teams correlate poorly with real-world speech distributions; 100% accuracy on a clean test set still hides field failures. Short studies miss long-context retention bugs (5+ turns). Auto-graded scoring underweights tone and empathy, which are the primary drivers of user satisfaction scores in voice products.

## When To Use

- Pre-launch validation of an Alexa skill, Google Action, custom IVR, or LLM voice agent.
- Regression testing after NLU model updates or prompt changes.
- Measuring intent accuracy, task completion, and error rate against a baseline.
- Stress-testing under realistic noise and accent diversity before scaling.

## When NOT To Use

- TTS-only output (read-aloud, screen readers) — that is a11y testing, not VUI testing.
- Pure copy review without runtime testing — covered by content design heuristics.
- Latency or load tuning of the speech stack — use load testing tooling instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-test-layers.xml` | Four test layers, key metrics, real-world testing checklist, subgroup accuracy rule. |
| `content/02-agentic-workflow.xml` | Batch runner workflow, adversarial utterance generation, gotchas, human-in-loop gates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui-batch-runner.py` | Batch intent-accuracy runner against Alexa ask-cli simulate; outputs per-intent accuracy table. |
