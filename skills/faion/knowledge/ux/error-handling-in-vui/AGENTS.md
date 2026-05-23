# Error Handling in VUI

## Summary

**One-sentence:** Produces a VUI error-recovery spec implementing a three-rung re-prompt ladder (brief re-ask → constructive re-ask with examples → escalation to visual/DTMF/human).

**One-paragraph:** Voice interface errors recover via a three-rung ladder. Rung 1: brief re-ask ('I didn't catch that — can you repeat?'). Rung 2: constructive re-ask with two examples ('You can say `play jazz` or `play classical`'). Rung 3: escalation — visual fallback on multimodal devices, DTMF tones on IVR, or live agent on supported channels. Verbatim repeat is forbidden; each rung varies prompt + adds scaffolding.

**Ефективно для:**

- Voice agents (Alexa/Google/LLM-native) — recovery без infinite loop.
- IVR з DTMF fallback на rung 3 для phone callers.
- Multimodal devices з screen — visual fallback на 3-й rung.
- Telephony контакт-центр — escalation до live agent на rung 3.

## Applies If (ALL must hold)

- Voice agent or IVR has at least 2 retry slots before fallback.
- Recovery latency budget allows 2-3 short re-asks.
- Multi-rung escalation infrastructure exists (visual / DTMF / human).

## Skip If (ANY kills it)

- Single-attempt command (e.g. 'pause') — no re-prompt needed.
- Push-to-talk with no automatic recovery — user retries on demand.
- Pure text chatbot — different error patterns apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Intent catalogue | list | voice agent spec |
| Example utterances per intent | ≥2 per intent | NLU corpus |
| Escalation channels | list (visual / DTMF / human) | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[core-vui-design-principles]] | Single-idea + barge-in baseline |
| [[vui-testing-best-practices]] | Recovery is regression-tested in tier-1 deterministic |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reprompt-lint.py` | Python lint: verify ladder prompts are distinct + rung 2 has examples + rung 3 escalates |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-error-handling-in-vui.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[core-vui-design-principles]]
- [[vui-conversation-design]]
- [[vui-testing-best-practices]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
