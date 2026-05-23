# AGENTS.md Per-Module Bootstrap

## Summary

**One-sentence:** Bootstrap an AGENTS.md (+ CLAUDE.md symlink) inside every module / subpackage so AI coding agents always read essential local context (what this dir IS + commands + gotchas) at directory entry instead of hallucinating it.

**One-paragraph:** Bootstrap an AGENTS.md (+ CLAUDE.md symlink) inside every module / subpackage so AI coding agents always read essential local context (what this dir IS + commands + gotchas) at directory entry instead of hallucinating it. The methodology pins the artefact: 20–80 lines of essential context, a file table, key types, and a pointer to detailed reference docs under `.agents/`.

**Ефективно для:**

- Polyrepo or multi-package codebases where agents jump between dirs.
- Onboarding new agents/contributors to large unfamiliar trees.
- Reviewers verifying that every module has a doc front-door.
- Audit surface: a script can find dirs missing AGENTS.md.

## Applies If (ALL must hold)

- Codebase has ≥3 modules / subpackages.
- AI coding agents operate inside the codebase.
- Repo follows the CLAUDE.md → @AGENTS.md convention.

## Skip If (ANY kills it)

- Single-file project; AGENTS.md at root is enough.
- Dir contains only an empty __init__.py with no logic.
- Repo does not run AI coding agents.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo root | directory | Workspace |
| Module list | list | Project layout |
| Doc convention | markdown | AGENTS.md spec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdlc-ai/ai-convention-anchoring` | Provides the convention pyramid AGENTS.md sits inside. |

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
| `draft-agents-md-per-module-bootstrap` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-agents-md-per-module-bootstrap` | haiku | Schema check + threshold checks; deterministic. |
| `review-agents-md-per-module-bootstrap` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agents-md-per-module-bootstrap.json` | JSON skeleton conforming to the output contract schema. |
| `templates/agents-md-per-module-bootstrap.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agents-md-per-module-bootstrap.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[ai-convention-anchoring]]
- [[ai-coding-agent-handoff-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
