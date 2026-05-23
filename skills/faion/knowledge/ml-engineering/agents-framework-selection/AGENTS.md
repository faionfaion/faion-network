# Agents Framework Selection

## Summary

**One-sentence:** Decision rubric to pick among LangGraph / CrewAI / AutoGen / Anthropic Agent SDK / OpenAI Swarm / no-framework for a new agent project.

**One-paragraph:** The 2025-2026 Python agent ecosystem has consolidated around six frameworks. Each is best at a different shape of problem. This methodology produces a decision record naming the chosen framework + the 3 axes that drove the choice (graph vs role, observability stack, deployment target) + the 2 explicitly rejected alternatives with reasons.

**Ефективно для:** Tech lead, що стоїть перед «який agent-фреймворк брати» і хоче не вгадувати, а зробити decision record за один захід.

## Applies If (ALL must hold)

- you are starting a new agent project from scratch
- team has ≥1 Python dev with LLM experience
- monthly compute budget is known
- deployment target (serverless, kube, on-prem) is decided
- observability requirements are documented

## Skip If (ANY kills it)

- existing codebase already uses a framework — migration is a separate methodology
- single-agent + 3-tool tasks — raw provider SDK is enough; no framework needed
- research / experimental prototype — pick whatever the team knows
- framework choice is mandated by org policy

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
| `content/02-output-contract.xml` | essential | JSON Schema for produces=decision-record + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=decision-record`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-agents-framework-selection.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Framework selection decision record skeleton |
| `templates/axis-scoring.md` | 3-axis scoring rubric (graph-vs-role, observability, deployment) |
| `templates/rejected-alternatives.md` | Rejected alternatives section template |
| `templates/review-memo.md` | 6-month review memo template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents-framework-selection.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-three-axes`, `r2-two-rejected`, `r3-no-framework-allowed`, `r4-named-owner`, `r5-deployment-fit` from `content/01-core-rules.xml`.
