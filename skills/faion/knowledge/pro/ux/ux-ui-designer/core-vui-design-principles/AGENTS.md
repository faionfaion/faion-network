# Core VUI Design Principles

## Summary

Three foundational principles for voice user interfaces — simplicity (short, single-idea responses),
natural conversation (follow-up awareness, human turn-taking), and context awareness (remembering
prior turns, adapting to preferences) — that apply to all voice runtimes from Alexa Skills to
LLM-powered Realtime API agents.

## Why

Voice interfaces fail when designed like visual interfaces: verbose confirmations inflate latency
past the 1.5 s tolerance threshold, robotic phrasing triggers negative user affect, and lack of
context forces repetition that users associate with IVR hell. These three principles are the
minimal contract any VUI must satisfy before adding features; violating any one is the primary
cause of abandoned voice experiences.

## When To Use

- Designing a new voice agent or LLM-powered voice interface (Alexa, Google Action, OpenAI Realtime).
- Auditing transcripts of an existing voice product for verbosity or missing context handling.
- Writing the system prompt and dialog policy for a Realtime API or Vapi voice agent.
- Defining acceptance criteria for voice flows in a spec or design doc.

## When NOT To Use

- Visual UI or chat — these principles produce over-terse copy when applied to text interfaces.
- IVR with regulatory scripts (banking disclosures, healthcare consent) — mandatory verbosity overrides.
- Rapid voice prototype before basic ASR is confirmed working — premature optimization.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Three principles with good/bad dialogue examples and the reasoning behind each. |
| `content/02-rules.xml` | Testable rules derived from the principles; known failure modes; LLM-specific gotchas. |

## Templates

none
