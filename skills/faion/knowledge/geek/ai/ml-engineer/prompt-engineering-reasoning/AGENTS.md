---
slug: prompt-engineering-reasoning
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Designs prompts for reasoning-first models (o1, Claude extended thinking, Gemini Thinking): minimal CoT instructions, target-output framing, and step-budget tuning.
content_id: "a05106ed8085f961"
complexity: medium
produces: playbook-step
est_tokens: 4300
tags: [prompt-engineering, reasoning, chain-of-thought, o1, extended-thinking]
---
# Prompt Engineering — Reasoning Patterns

## Summary

**One-sentence:** Designs prompts for reasoning-first models (o1, Claude extended thinking, Gemini Thinking): minimal CoT instructions, target-output framing, and step-budget tuning.

**One-paragraph:** Designs prompts for reasoning-first models (o1, Claude extended thinking, Gemini Thinking): minimal CoT instructions, target-output framing, and step-budget tuning. The methodology assumes the inputs in Prerequisites and produces a `playbook-step` artefact validated by `scripts/validate-prompt-engineering-reasoning.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML engineers using reasoning-class models where verbose chain-of-thought prompting hurts rather than helps.

## Applies If (ALL must hold)

- Math, calculation, or multi-step logic where intermediate steps matter.
- Decision analysis with multiple options and trade-offs.
- Code review or debugging where cause-and-effect reasoning is needed.
- Tasks where you need verifiable, auditable reasoning (legal, medical, financial).
- High-stakes outputs where reliability matters more than latency or cost.

## Skip If (ANY kills it)

- Simple, well-defined tasks — CoT adds tokens and latency without quality gain.
- Latency-sensitive real-time pipelines — CoT scratchpads can double or triple response time.
- Self-consistency in production — multiple samples are expensive; reserve for offline evaluation.
- Tasks where chain-of-thought is already embedded in the model via RLHF (modern instruction-tuned models often reason internally without explicit CoT prompting).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-fundamentals]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `expand-step` | sonnet | Inline judgment per step. |
| `integrate-with-upstream` | opus | Cross-step consistency. |
| `lint-output` | haiku | Format check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/playbook-step.md.tmpl` | Markdown playbook-step skeleton: trigger, action, verification, rollback. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-engineering-reasoning.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[prompt-engineering-fundamentals]]
- [[reasoning-first-architectures]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `prompt-engineering-reasoning` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
