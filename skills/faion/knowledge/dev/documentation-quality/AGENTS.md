# Documentation

## Summary

**One-sentence:** Defines the AGENTS.md + CLAUDE.md per-dir doc convention so agents can navigate any code dir under ~80 lines of context.

**One-paragraph:** Agents that lack a routing doc fall back to guessing file paths; the guesses go stale and the agent edits the wrong place. This methodology mandates one AGENTS.md per code directory (20-80 lines, structured: purpose + key files + commands + gotchas) and one CLAUDE.md that just contains `@AGENTS.md`. The pair fits in any agent's auto-load budget and answers four questions: what is this dir, what files matter, how do I build/test, what are the pitfalls. Output is a spec artefact listing every dir + its required headers + a smoke-test that verifies the pair exists.

**Ефективно для:**

- Repos з 50+ subdirs: agent-navigation collapse без routing-doc.
- Multi-agent workflows (faion/poll-agents): кожен субагент стартує в незнайомому dir — потрібен 20-line context.
- Onboarding new dev: AGENTS.md = живий orientation tour без 50-page handbook.
- Migration: old README.md → AGENTS.md як частина refactor PR.

## Applies If (ALL must hold)

- Repo has ≥10 code directories (below that, root AGENTS.md suffices).
- Agents are routinely launched in subdirectories (cwd-scoped sessions).
- Team treats docs as code (PR-reviewed, versioned).

## Skip If (ANY kills it)

- Single-file repo or one-shot script.
- Pure data repo (no code modules).
- Vendored / generated subdirs — exempted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo root | path | git rev-parse --show-toplevel |
| Existing AGENTS.md inventory | list | find . -name AGENTS.md |
| Code-dir inventory | list | find . -type d with source files |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pair-required, 20-80-lines, structured-sections, no-readme-shadowing, refresh-on-edit | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for doc-spec artefact | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: drift-from-code, stretch-past-80, readme-shadow | 600 |
| `content/04-procedure.xml` | essential | 5-step rollout procedure | 700 |
| `content/05-examples.xml` | reference | Example AGENTS.md for a python module | 500 |
| `content/06-decision-tree.xml` | essential | Dir-shape tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_dirs` | haiku | find + filter; deterministic. |
| `draft_agents_md` | sonnet | Per-dir custom content; needs source skim. |
| `verify_pair` | haiku | File-exists checks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agents-md-universal.md` | Universal AGENTS.md skeleton with placeholders |
| `templates/doc-outline.sh` | Shell that scans a dir and prints draft AGENTS.md sections |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-documentation.py` | Validate the doc-spec artefact + per-dir pair existence | After draft, before landing the docs PR |

## Related

- - [[code-review-process]] — docs PRs use the same review template.
- - [[code-decomposition-patterns]] — decomposition PRs MUST update / create AGENTS.md per moved dir.

## Decision tree

See `content/06-decision-tree.xml`. Branches: dir has source code? → pair required. Dir is tests-only / generated / vendored? → exempt. Repo-root vs sub-dir → root carries top-level map, sub-dir carries local map.
