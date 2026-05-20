---
slug: vui-privacy-security
tier: pro
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Five privacy principles (transparency, control, minimization, security, deletion) and a split-agent architecture for sensitive VUI operations: a policy classifier decides "is this turn sensitive?" and an executor crafts the response — the executor never sees raw sensitive values.
content_id: "1aad2fef0065bca2"
tags: [voice, privacy, security, vui, pii]
---
# VUI Privacy and Security

## Summary

**One-sentence:** Five privacy principles (transparency, control, minimization, security, deletion) and a split-agent architecture for sensitive VUI operations: a policy classifier decides "is this turn sensitive?" and an executor crafts the response — the executor never sees raw sensitive values.

**One-paragraph:** Five privacy principles (transparency, control, minimization, security, deletion) and a split-agent architecture for sensitive VUI operations: a policy classifier decides "is this turn sensitive?" and an executor crafts the response — the executor never sees raw sensitive values. Redaction must happen pre-storage and pre-LLM-context, not post-hoc. Two-channel confirmation (voice initiates, SMS/push confirms) prevents voice-spoofing attacks on destructive operations.

## Applies If (ALL must hold)

- Designing voice features that handle PII, health, financial, or auth-sensitive data.
- Drafting privacy disclosures, consent flows, and data-retention copy for voice products.
- Auditing existing VUI for missing trust indicators (listening indicator, stop command, history access).
- Building agentic pipelines where ASR transcripts feed LLM calls and require redaction first.

## Skip If (ANY kills it)

- Pure text chatbots — covered by general data-privacy methodologies, not VUI specifics.
- One-off internal tools with no user voice capture (agent-only TTS announcements).
- Formal compliance scoping (GDPR DPIA, HIPAA controls) — VUI principles inform but do not replace formal assessment.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ux/ui-designer/`
