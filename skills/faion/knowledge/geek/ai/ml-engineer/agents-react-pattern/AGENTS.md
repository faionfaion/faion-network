---
slug: agents-react-pattern
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Single-agent ReAct loop: Thought → Action → Observation, with bounded iterations, typed tool registry, audit log, and termination guard.
content_id: "ffaea0fd7318b363"
complexity: medium
produces: code
est_tokens: 4200
tags: [agents, react, tool-use, llm, autonomous-agents]
---
# Agents ReAct Pattern

## Summary

**One-sentence:** Single-agent ReAct loop: Thought → Action → Observation, with bounded iterations, typed tool registry, audit log, and termination guard.

**One-paragraph:** ReAct is the canonical single-agent loop. The LLM thinks, calls a tool, observes the result, and repeats until the task is done or an iteration cap is hit. This methodology codifies the loop into a small Python class with a typed tool registry, a termination guard (final answer detection), an iteration cap, and audit logging. Foundation for all higher-order agent patterns.

**Ефективно для:** Девів, що будують перший справжній агентний цикл, не хочуть LangGraph і хочуть зрозуміти, що там всередині насправді.

## Applies If (ALL must hold)

- single agent (no multi-agent coordination yet)
- tools are well-defined and bounded
- iteration cap ≤ 15 acceptable
- you can detect a «final answer» from the LLM output
- audit log is required

## Skip If (ANY kills it)

- task is single-shot — no loop needed
- multi-agent coordination is required — use a graph framework
- tools have non-deterministic side-effects requiring human gate
- iteration cap is too restrictive — pick plan-execute instead

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-agents-react-pattern.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/react-loop.py` | ReAct loop class skeleton |
| `templates/react-prompt.txt` | Prompt template requiring Thought + Action JSON |
| `templates/final-answer-tool.py` | FinalAnswer typed tool |
| `templates/audit-row.py` | Structured audit row schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents-react-pattern.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-thought-action-observation`, `r2-typed-action`, `r3-bounded-iter`, `r4-termination-guard`, `r5-audit-log` from `content/01-core-rules.xml`.
