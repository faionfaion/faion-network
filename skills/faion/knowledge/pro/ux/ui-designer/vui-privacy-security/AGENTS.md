# VUI Privacy and Security

## Summary

Five privacy principles (transparency, control, minimization, security, deletion) and a split-agent architecture for sensitive VUI operations: a policy classifier decides "is this turn sensitive?" and an executor crafts the response — the executor never sees raw sensitive values. Redaction must happen pre-storage and pre-LLM-context, not post-hoc. Two-channel confirmation (voice initiates, SMS/push confirms) prevents voice-spoofing attacks on destructive operations.

## Why

Voice data is ambient and persistent. ASR transcripts may contain PII, health, or financial data that flows silently into LLM context, observability logs, and training pipelines. A single-agent design that both classifies sensitivity and generates responses creates a path for PII leakage in rationale fields. Splitting into classifier + executor with structured outputs (no free-text echo of user data) blocks the leak at the architecture level.

## When To Use

- Designing voice features that handle PII, health, financial, or auth-sensitive data.
- Drafting privacy disclosures, consent flows, and data-retention copy for voice products.
- Auditing existing VUI for missing trust indicators (listening indicator, stop command, history access).
- Building agentic pipelines where ASR transcripts feed LLM calls and require redaction first.

## When NOT To Use

- Pure text chatbots — covered by general data-privacy methodologies, not VUI specifics.
- One-off internal tools with no user voice capture (agent-only TTS announcements).
- Formal compliance scoping (GDPR DPIA, HIPAA controls) — VUI principles inform but do not replace formal assessment.

## Content

| File | What's inside |
|------|---------------|
| `content/01-privacy-principles.xml` | Five principles with implementation rules, trust indicator requirements, sensitive-operation patterns. |
| `content/02-agent-architecture.xml` | Split-agent design, redaction pipeline, two-channel confirmation, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/redact-slots.py` | Regex + slot-map redactor that strips PII from transcripts before LLM or log ingestion. |
| `templates/privacy-classifier-prompt.txt` | Structured-output prompt for a vui-privacy-classifier subagent. |

## Scripts

none
