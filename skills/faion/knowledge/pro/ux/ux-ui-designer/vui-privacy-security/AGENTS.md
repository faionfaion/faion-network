# VUI Privacy and Security

## Summary

A design methodology for voice interfaces that handle sensitive user data. Requires explicit consent disclosure before capture, visual and audio trust indicators during listening, step-up authentication for sensitive actions, and PII redaction at transcript boundaries. Voice data is sensitive and persistent; privacy must be designed in from the first dialog turn.

## Why

Voice capture is legally regulated (GDPR, HIPAA, CCPA, BIPA) and technically leaky: cloud transcripts persist on third-party infrastructure, LLM context crosses turns, and "private mode" UI cannot prevent model-level logging. Privacy-by-design prevents post-launch regulatory exposure and user trust failures that are expensive to remediate.

## When To Use

- Designing a voice agent that handles personal data (banking, health, identity, child profiles).
- Submitting an Alexa/Google Action for certification — privacy disclosures are mandatory.
- Operating in regulated jurisdictions: GDPR, HIPAA, CCPA/CPRA, Illinois BIPA, EU AI Act (voice biometrics).
- Building voice flows in customer support that may capture card numbers, OTPs, or account secrets.

## When NOT To Use

- Internal-only voice prototypes with synthetic data — full disclosure flows can be deferred until external pilot.
- Non-voice UI forms — apply standard data-minimisation principles instead; voice-specific patterns don't apply.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Core privacy principles, trust indicators, sensitive-operation rules |
| `content/02-agent-patterns.xml` | Agentic audit workflow, subagent prompts, gotchas, regulatory references |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui_privacy.py` | Disclosure emitter + PII redactor (regex patterns for card, email, phone, SSN) |

## Scripts

none
