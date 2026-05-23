# AI Design Assistant Patterns

## Summary

**One-sentence:** Produces a decision record selecting one of four AI-assistant patterns (sidebar / modal / inline / review-mode) for a design-tool integration and locks the pattern for the product.

**One-paragraph:** Mixing assistant patterns inside a single design tool creates UX confusion — users learn one mental model, get jarred when context shifts to another. This methodology picks ONE pattern per tool, justified by task duration + context window + agent-vs-human trigger. Review-mode is the most agent-native: the agent receives a design artifact, applies a rubric, returns structured JSON feedback a human acts on. Output: a one-page decision record with chosen pattern, rationale, fallback behaviour, telemetry plan.

**Ефективно для:** PM / staff designer, що додає AI assistant у Figma plugin / design tool і потребує заморозити pattern перед розробкою.

## Applies If (ALL must hold)

- Embedding AI assistance inside a design tool (Figma plugin, internal canvas, web design app).
- Decision is being made BEFORE implementation begins.
- ≥2 candidate patterns are seriously considered (sidebar / modal / inline / review).

## Skip If (ANY kills it)

- Pattern already in production for >6 months — too costly to re-pattern.
- Single-shot prompt UX with no follow-up — no pattern needed.
- Tool is non-design (IDE, terminal) — use a different decision framework.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task description (what the assistant does) | markdown | PM |
| Expected interaction frequency | JSON (per session) | research |
| Trigger source (human-action vs agent-poll) | string | engineering |
| Context-window budget | tokens | engineering |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-enhanced-design-systems]] | DS instrumentation context. |
| [[figma-ai-ecosystem]] | Figma plugin sandbox boundaries. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
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
| `templates/decision-record.md` | Markdown skeleton: pattern + rationale + trigger + telemetry + fallback. |
| `templates/score-table.json` | Scoring rubric for sidebar / modal / inline / review. |
| `templates/_smoke-test.md` | Filled review-mode decision record example. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-design-assistant-patterns.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-enhanced-design-systems]]
- [[figma-ai-ecosystem]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the decision-record; mis-routing leads to producing the wrong artefact shape.
