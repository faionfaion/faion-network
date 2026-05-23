# AI Convention Anchoring

## Summary

**One-sentence:** Three-layer convention anchoring (CONVENTIONS.md + CLAUDE.md/AGENTS.md context pyramid + lint gates) that stops AI from generating compilable code which silently violates the team's conventions.

**One-paragraph:** Three-layer convention anchoring (CONVENTIONS.md + CLAUDE.md/AGENTS.md context pyramid + lint gates) that stops AI from generating compilable code which silently violates the team's conventions. The methodology pins the artefact: a single CONVENTIONS.md as policy, a per-dir AGENTS.md as local context, and a lint config that mechanically rejects violations the AI keeps repeating.

**Ефективно для:**

- Codebases where 'works on my machine' diverges from team style.
- AI coding agents that compile correct code which fails review on style/convention grounds.
- Reviewers tired of repeating the same comment.
- Audit surface: convention drift shows up as lint failures, not chat threads.

## Applies If (ALL must hold)

- Repo has explicit code conventions (style, naming, structure).
- AI agents contribute code regularly.
- There is a lint or static-analysis toolchain available.

## Skip If (ANY kills it)

- Repo has no documented conventions — write them first.
- Lint tooling unavailable or disabled.
- Single-author scratchpad with no convention surface.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CONVENTIONS.md | markdown | Repo root |
| AGENTS.md per module | markdown | Per-dir |
| Lint config | yaml | Repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdlc-ai/agents-md-per-module-bootstrap` | Provides the AGENTS.md context layer this methodology anchors against. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ai-convention-anchoring` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-ai-convention-anchoring` | haiku | Schema check + threshold checks; deterministic. |
| `review-ai-convention-anchoring` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-convention-anchoring.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ai-convention-anchoring.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-convention-anchoring.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[agents-md-per-module-bootstrap]]
- [[ai-coding-agent-handoff-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
