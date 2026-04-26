# Voice UI Design Basics

## Summary

A process for designing voice user interfaces (VUI): write sample dialogues first, then extract intent/slot schemas, design prompts under 20 words, build a 3-attempt error recovery chain, and validate with Wizard of Oz testing before any NLU training begins.

## Why

Voice interfaces fail when designed like visual ones — unnatural prompts, missing error recovery, and idealized utterance sets that do not match real speech cause high abandonment. Writing dialogues before building schemas grounds the design in natural language and exposes confirmation strategy and context-tracking gaps before they become production bugs.

## When To Use

- Designing a new voice feature for a mobile app, smart speaker skill, or IVR system
- Writing and reviewing dialogue scripts for conversational AI products
- Defining intent/slot schemas for NLU training (Alexa, Dialogflow, Rasa)
- Auditing existing voice flows for error handling gaps and confirmation strategy mismatches
- Generating utterance variations for NLU training data

## When NOT To Use

- Complex data entry, browsing, or detailed comparison tasks — voice is the wrong modality
- Noisy environments or contexts requiring private information (credit card numbers, passwords)
- First-version MVP features where basic screen UI is not yet validated
- Platforms without microphone access or TTS output capability

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Six-step VUI design process: define use cases, write dialogues, define intents/slots, design prompts, handle errors, test with users |
| `content/02-examples.xml` | Worked examples (food ordering, smart home) and antipatterns (hollow apologies, long prompts, missing fallbacks) |

## Templates

| File | Purpose |
|------|---------|
| `templates/voice-flow.md` | Full voice flow document: user context, happy path, intent definitions, error handling, confirmation strategy, edge cases, fallbacks |
| `templates/prompt-writing.md` | Prompt design template with primary, variations, reprompts (3 levels), and A/B test variants |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/vui-lint.py` | Python linter for VUI dialogue scripts: checks prompt length, detects hollow apologies, URLs, and long numbers |
