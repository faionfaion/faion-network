# Code Review Cycle

## Summary

**One-sentence:** Produces a unified code-review report (AI pre-screen + parallel BLOCK/WARN/NOTE finding lists + deduplicated merge + reflexion writeback) so human-AI review catches the right things and the team learns from each PR.

**Ефективно для:** Solo devs who either skip review entirely or get drowned in noisy AI nit-picks that don't catch the real bug.

**One-paragraph:** Code review collapses to either no review or noisy AI lint. This methodology pins a 3-step pipeline: AI pre-screen flags style / anti-patterns / missing tests; parallel review agents (Claude + cross-model) emit structured BLOCK/WARN/NOTE findings; a merge step deduplicates and produces a unified report. Reflexion feeds findings back to patterns.md and mistakes.md. Output is consumed by reflexion-learning and mistake-memory.

## Applies If (ALL must hold)

- PRs touch production code with paying users.
- Operator wants human-AI collaboration, not AI replacement.
- Repo has a tests/ suite that runs in CI.
- Reflexion memory layer exists (patterns.md + mistakes.md).

## Skip If (ANY kills it)

- Throwaway scripts in research/ folders.
- Documentation-only changes (rely on docs CI).
- Single-person hobby project with no users.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| PR diff | git diff | developer |
| AI review agent config | yaml | engineer |
| BLOCK/WARN/NOTE rubric | spec | team |
| .aidocs/memory/ directory | folder | repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/pattern-memory` | Sibling — review findings feed pattern memory. |
| `solo/sdd/sdd/mistake-memory` | Sibling — BLOCK findings feed mistake memory. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/code-review-cycle.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/code-review-cycle.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-code-review-cycle.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[pattern-memory]] — related methodology.
- [[mistake-memory]] — related methodology.
- [[design-docs-patterns]] — related methodology.
- [[living-documentation]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
