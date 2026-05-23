# AI Design Assistant Patterns (UX/UI)

## Summary

**One-sentence:** Produces a decision record for AI assistants embedded in UX/UI design tools — sidebar (long tasks) vs modal (single-shot) vs inline (micro-suggestions) — with trigger rules and fallback states.

**One-paragraph:** Distinct from the ui-designer counterpart by emphasis on UX research integration (where the assistant lives in the broader workflow, not just the canvas). This methodology produces a decision record selecting ONE pattern per assistant with explicit trigger rules (when the assistant invokes itself), context-disclosure spec (what data it reads), fallback states (offline / rate-limited / low-confidence), and human-in-loop checkpoints.

**Ефективно для:** UX/UI lead, що додає AI assistant у research + design workflow і потребує human-in-loop checkpoints + fallback states.

## Applies If (ALL must hold)

- Embedding AI assistance in a UX/UI workflow (research + design + handoff).
- Decision frozen BEFORE implementation; ≥2 patterns considered.
- Human-in-loop checkpoints required (auditable, replayable).

## Skip If (ANY kills it)

- Pattern already in production >6 months.
- Single-shot prompt UX with no follow-up.
- Workflow is engineering-only — see ui-designer counterpart.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workflow description (research → design → handoff stages) | markdown | PM |
| Trigger sources (designer click / agent poll / scheduled) | JSON | engineering |
| Context-disclosure inventory (data the assistant reads) | JSON | privacy |
| Fallback policy | YAML | ops |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-enhanced-design-systems]] | DS instrumentation context. |
| [[ai-design-assistant-patterns]] (ui-designer) | Sibling under ui-designer; mainly canvas-focused. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-decision-record` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/decision-record.json` | JSON skeleton: assistant + pattern + triggers + disclosure + fallbacks + checkpoints. |
| `templates/trigger-rules.yaml` | Trigger rule library template. |
| `templates/_smoke-test.json` | Filled design-review-bot decision record. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-design-assistant-patterns.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-enhanced-design-systems]]
- [[ai-assisted-accessibility]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the decision-record; mis-routing leads to producing the wrong artefact shape.
