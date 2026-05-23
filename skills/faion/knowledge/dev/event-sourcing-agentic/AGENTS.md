# Event Sourcing — Agentic Workflow and Tooling

## Summary

**One-sentence:** Agentic workflow for event-sourcing scaffolding — 5-stage pipeline (design → code-gen → projection → tests → review) with model-specific gotchas, prompt patterns, and rejection criteria.

**One-paragraph:** When AI agents (Claude, GPT, Cursor) scaffold event-sourcing code unguided, they regress to CRUD-shaped events, mutate state outside `apply()`, omit `expected_version`, and invent event-store APIs. This methodology pins a 5-stage pipeline that constrains the agent at each step (aggregate design → event-class generation → projection → tests → antipattern review) and lists rejection criteria the reviewer must apply. Output: a spec describing the pipeline run, agent prompts used, and the rejected/accepted artefacts conforming to `02-output-contract.xml`.

**Ефективно для:**

- Scaffolding new event-sourced aggregates with AI assistance.
- Reviewing AI-generated ES code in PR review.
- Coaching teams adopting ES who use AI agents heavily.
- Catching the canonical regressions: CRUD events, lost expected_version, hallucinated APIs.
- SDD tasks where ES scaffolding is delegated to subagents.

## Applies If (ALL must hold)

- Event sourcing is the chosen persistence pattern for at least one aggregate.
- AI agents (LLM-driven) are scaffolding or modifying ES code.
- A reviewer (human or peer agent) gates the output before merge.
- The team has read `[[event-sourcing-fundamentals]]` and `[[event-sourcing-aggregate]]`.

## Skip If (ANY kills it)

- ES not yet adopted — start with the fundamentals methodology first.
- No AI involvement — apply the underlying ES methodologies directly.
- Hand-built ES kernel with custom DSL — review tools must be adapted; this pipeline assumes a standard event-store library.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Aggregate spec | Markdown | spec |
| Event-store library docs | URL | infra |
| Glossary (Ubiquitous Language) | Markdown | domain owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[event-sourcing-fundamentals]] | Core invariants this pipeline must protect. |
| [[event-sourcing-aggregate]] | Aggregate replay + apply rules. |
| [[event-sourcing-projections]] | Projection responsibilities the pipeline scaffolds. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: past-tense-event-names, apply-only-mutation, expected-version-enforced, no-invented-apis, projection-no-side-effects | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for pipeline-run spec | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: crud-events, mutate-in-command, hallucinated-event-store-api, projection-business-logic | ~900 |
| `content/04-procedure.xml` | essential | 5-stage agentic procedure | ~800 |
| `content/05-examples.xml` | essential | Worked example of a pipeline run for OrderPlaced + items projection | ~600 |
| `content/06-decision-tree.xml` | essential | Routing tree on agent-task shape → rule | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `aggregate-design` | sonnet | Domain judgment + small output. |
| `event-class-codegen` | sonnet | Constrained scaffold, easy to verify. |
| `projection-codegen` | sonnet | Same. |
| `tests-codegen` | haiku | Mechanical fixture generation. |
| `antipattern-review` | sonnet | Pattern-match against failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-prompts.md` | Prompt fragments per stage |
| `templates/review-checklist.md` | Reviewer rejection criteria |
| `templates/pipeline-run.json` | Empty pipeline-run record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-event-sourcing-agentic.py` | Validate pipeline-run record against schema | Pre-commit on artefact |

## Related

- [[event-sourcing-fundamentals]]
- [[event-sourcing-aggregate]]
- [[event-sourcing-projections]]
- [[event-sourcing-versioning]]
- parent skill: `pro/dev/software-developer/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps the current pipeline stage + observed agent output to a rule from `01-core-rules.xml` that either accepts or rejects the artefact. Use it whenever reviewing an AI-generated ES PR.
