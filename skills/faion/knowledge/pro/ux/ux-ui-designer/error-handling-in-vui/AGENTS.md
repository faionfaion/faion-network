# Error Handling in VUI

## Summary

A three-rung re-prompt ladder for voice interface error recovery: rung 1 — brief re-ask; rung 2 — constructive re-ask with two example phrases; rung 3 — escalation to visual fallback, DTMF, or human agent. Cap at three rungs; escalate on rung 4 input instead of looping. Never use blame language ("you said wrong", "invalid"). Every example phrase on rung 2 must exist in the NLU training data.

## Why

Voice recognition errors are inevitable; the user experience of recovery determines abandonment rate. Users who hear the same "I didn't catch that" three times in a row perceive the system as broken, not themselves. The rung-2 example-phrase rule prevents the most common failure: users parroting a phrase that isn't in the recognizer, masking the true no-match cause.

## When To Use

- Designing fallback dialogs for ASR no-input, no-match, and ambiguous-intent failures.
- Drafting re-prompt copy with example phrases for second/third failure passes.
- Auditing existing Alexa/Google Action/Dialogflow intents for unhandled utterances.
- Building help or transfer-to-agent escalation paths for IVR or LLM-backed voice bots.

## When NOT To Use

- Pure speech-to-text quality issues — model retraining or acoustic tuning, not dialog design.
- Silent or visual-only UIs where confirmation can be shown on screen.
- One-shot transactional commands with no multi-turn state (no recovery path needed).

## Content

| File | What's inside |
|------|---------------|
| `content/01-error-ladder.xml` | Error taxonomy (no-input, no-match, ambiguous, system error), three-rung ladder rules, escalation triggers. |
| `content/02-antipatterns-and-workflow.xml` | Blame-language antipatterns, LLM-agent gotchas, SSML rules, lint script reference. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reprompt-lint.py` | CI lint: flag missing rung 3 escalation, missing rung 2 examples, banned blame phrases. |
