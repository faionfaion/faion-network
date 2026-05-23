---
slug: interview-recording-redaction-pipeline
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pipeline configuration for BA interview recordings: transcript generation, automated PII redaction, manual review checkpoint, retention policy, access log.
content_id: "94393615aed2e994"
complexity: deep
produces: config
est_tokens: 4700
tags: [ba, pro, interview, recording, redaction, pii, pipeline]
---
# Interview Recording Redaction Pipeline

## Summary

**One-sentence:** Pipeline configuration for BA interview recordings: transcript generation, automated PII redaction, manual review checkpoint, retention policy, access log.

**One-paragraph:** Interview Recording Redaction Pipeline pins a recurring BA decision into an auditable artefact. It enforces a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. Inputs and triggers come from the engagement context; outputs feed a named downstream consumer (human or agent) without re-deriving the reasoning. The decision tree at `content/06-decision-tree.xml` routes every application to either an applicable rule or `skip-this-methodology`.

**Ефективно для:**

- User research engagements with HIPAA / GDPR scope.
- Whistleblower / sensitive-source interviews.
- Multi-client recording archives where one leak could end the engagement.
- M&A / due-diligence interviews subject to NDAs.

## Applies If (ALL must hold)

- BA records interviews / user research sessions (audio or video).
- Recordings contain PII / PHI / commercially sensitive data.
- Recordings are shared with team members or stored beyond the immediate session.
- Regulatory regime applies (GDPR, HIPAA, CCPA, or contractual NDA).

## Skip If (ANY kills it)

- Sessions are not recorded — no pipeline needed.
- Recordings are deleted immediately post-session — no retention to manage.
- Recording is governed entirely by the client's own pipeline — you have no custody.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recording storage location | url / path | Project infra |
| Transcript tooling (Whisper / vendor) | config | BA toolkit |
| Redaction allowlist / denylist | yaml | Project legal review |
| Retention policy | yaml | Engagement governance |
| Access log destination | url / path | Audit infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-interview-recording-redaction-pipeline` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-recording-redaction-pipeline.yaml` | YAML config skeleton with required keys |
| `templates/interview-recording-redaction-pipeline.schema.json` | JSON Schema for the config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interview-recording-redaction-pipeline.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ba/AGENTS.md`
- [[requirement-quality-scorecard]]
- [[discovery-to-delivery-handover-protocol]]
- [[demo-recap-email-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, scope, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
