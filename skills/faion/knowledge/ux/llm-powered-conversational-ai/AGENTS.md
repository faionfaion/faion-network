# LLM-Powered Conversational UI Spec

## Summary

**One-sentence:** Spec for text-or-voice conversational UI backed by an LLM — turn structure, tool surfaces, fallback policy, refusal model, conversational a11y.

**One-paragraph:** Spec for text-or-voice conversational UI backed by an LLM — turn structure, tool surfaces, fallback policy, refusal model, conversational a11y. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying llm-powered conversational ui spec. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for llm-powered conversational ui spec across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- primary interaction is a multi-turn conversation backed by an LLM (chat, voice, hybrid)
- the LLM has access to tools (functions, APIs) that can change state
- the team owns the prompt, tool schema, and refusal policy end-to-end

## Skip If (ANY kills it)

- single-turn Q&A with no state mutation — use simpler prompt-only methodology
- scripted bot (decision tree, no LLM) — use traditional chatbot design methodology
- the LLM is consumed by another system, not by a human user — use API integration methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Turn structure spec | user/assistant/tool format | ml-engineering |
| Tool schema catalog | tools available to the LLM with side-effects mapped | engineering |
| Refusal policy | what the LLM must refuse + how | trust & safety |
| Conversational a11y baseline | screen-reader-friendly turn rendering, voice-first parity | a11y team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[multimodal-vui-design]] | Voice-side parity |
| [[eval-driven-development-tdd-for-ai]] | Eval gate for conversational quality |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `turn_structure_design` | sonnet | Schema for user/assistant/tool turns + rendering rules. |
| `refusal_policy_design` | opus | Cross-cutting refusal patterns and rendering. |
| `a11y_review` | sonnet | Screen-reader + voice parity check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/conversational-spec.md` | Spec skeleton for conversational UI |
| `templates/turn-schema.json` | Turn schema (user/assistant/tool) skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in conversational-UI spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-powered-conversational-ai.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[multimodal-vui-design]]
- [[generative-ui-design]]
- [[ai-spatial-computing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
