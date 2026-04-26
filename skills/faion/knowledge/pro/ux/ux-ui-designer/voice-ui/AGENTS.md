# Voice UI Design

## Summary

A methodology for designing speech-controlled interfaces — voice assistants, app voice commands,
IVR systems — by writing sample dialogues first, then defining intents/slots, authoring prompts,
and designing a 3-tier error-recovery ladder before any NLU training begins.

## Why

Voice interfaces fail when copied from visual UI patterns: users do not know what to say, prompts
are robotic, errors are dead ends. Writing dialogues before code forces natural language and exposes
missing intents early. Error ladders (rephrase → examples → fallback) reduce abandonment; explicit
confirmation strategy prevents irreversible actions without user awareness.

## When To Use

- Designing a voice assistant, Alexa/Google skill, or IVR flow end-to-end.
- Adding voice commands to an existing app for hands-free or accessibility use.
- Migrating a legacy NLU bot (Dialogflow, Lex) to an LLM-powered runtime.
- Defining acceptance criteria for a voice feature in a spec or design doc.
- Auditing transcripts of an existing voice product for verbosity or missing error paths.

## When NOT To Use

- Visual UI work where voice is cosmetic — invest in the core visual flow first.
- Highly private data entry (financial account numbers, medical detail) without strong auth design.
- Noisy or shared environments where ASR reliability cannot be guaranteed.
- Browsing or exploratory tasks — visual lists outperform voice for discovery.
- Rapid prototype stage before basic ASR integration is confirmed working.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | VUI components (wake word, intent, slot, utterance, confirmation); voice-suitability matrix. |
| `content/02-process.xml` | Six-step VUI design process: use cases → dialogues → intents/slots → prompts → error handling → testing. |
| `content/03-rules.xml` | Prompt writing rules, error-ladder rule, confirmation strategy, ASR/LLM gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/voice-flow.md` | Voice flow doc: overview, happy-path dialogue, intent definitions, error handling, fallbacks. |
| `templates/prompt-spec.md` | Per-prompt spec: primary text, short/long variants, reprompts 1-3, A/B variants. |
