---
slug: generative-ui-design
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Spec for UIs whose layout / components are produced at request time by an LLM (v0-style runtime UI generation) — input model, safety guardrails, fallback layout, eval gate.
content_id: "505f4defdb6eaa58"
complexity: deep
produces: spec
est_tokens: 4900
tags: [generative-ui, v0, runtime-generation, llm-driven-ui, fallback-layout]
---

# Generative UI Design Spec

## Summary

**One-sentence:** Spec for UIs whose layout / components are produced at request time by an LLM (v0-style runtime UI generation) — input model, safety guardrails, fallback layout, eval gate.

**One-paragraph:** Spec for UIs whose layout / components are produced at request time by an LLM (v0-style runtime UI generation) — input model, safety guardrails, fallback layout, eval gate. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a spec produced by an agent applying generative ui design spec. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible spec for generative ui design spec across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- the UI is generated at request time by an LLM from user intent (not a fixed React tree)
- the team owns or controls the generator (prompt, schema, fallback) end-to-end
- a fallback layout for generation failure is part of the product spec, not aspirational

## Skip If (ANY kills it)

- UI is static or template-driven with parameter slots — use ordinary component spec
- the LLM only writes copy, not layout — use copy-generation methodology
- no production traffic plans — use a generative-ui prototype methodology instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| UI schema for generated tree | JSON Schema / component grammar | design-system team |
| Fallback layout (deterministic) | static React tree or Figma frame | designer |
| Eval suite for generated UIs | ≥30 cases with rubric | ml-engineering |
| Safety + brand rules | what the generator may never emit | design + brand |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[eval-driven-development-tdd-for-ai]] | Eval gate discipline |
| [[ai-generated-layout-review-checklist]] | Per-instance review pattern |

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
| `schema_design` | opus | UI grammar + safety constraints in schema form. |
| `fallback_layout_design` | sonnet | Static fallback that works for all inputs. |
| `eval_suite_construction` | opus | Cover happy + adversarial + minority strata. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ui-grammar.json` | JSON Schema skeleton for generated UI tree |
| `templates/generative-spec.md` | Spec document skeleton |
| `templates/_smoke-test.md` | Minimum viable filled-in generative-UI spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-generative-ui-design.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-generated-layout-review-checklist]]
- [[llm-powered-conversational-ai]]
- [[eval-driven-development-tdd-for-ai]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
