---
slug: uv-lockfile-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a pyproject.toml + uv.lock floor + AGENTS.md snippet enforcing `uv run` for every Python tool call so the agent fleet shares one virtualenv + one Python version + one resolution.
content_id: "f1f8001bf9d64098"
complexity: medium
produces: config
est_tokens: 4200
tags: [uv, python, lockfile, dependency-management, reproducible-builds]
---
# uv as the Python Lockfile Floor

## Summary

**One-sentence:** Standardize every Python project on Astral's uv (env + resolver + lockfile + Python install); the committed uv.lock is the single source of truth and AI agents invoke commands via `uv run <cmd>`, never bare `pytest` / `python`.

**One-paragraph:** Standardize every Python project on Astral's `uv` for environment management, dependency resolution, lockfile, and Python version installation. The committed `uv.lock` is the single source of truth for reproducible installs; AI coding agents must invoke commands through `uv run <cmd>` (never bare `pytest` / `python`) so the right virtualenv and the right Python version are guaranteed for every tool call.

**Ефективно для:**

- Python project, де agents (Claude / Devin / Cursor) бігають commands.
- Multi-version Python labs: uv pins the version too.
- CI reproducibility: lockfile flow без `pip install` surprises.
- Cold-start onboarding: `uv sync` — single command для setup.

## Applies If (ALL must hold)

- Project is Python (3.10+).
- AI coding agents run shell commands against the project.
- Reproducible installs are a requirement (CI, deploy, multi-dev team).

## Skip If (ANY kills it)

- Project is pinned to legacy pip + requirements.txt with no migration budget.
- Single throwaway script with no dependencies.
- Org policy mandates a different resolver (e.g., conda-only).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Python project with pyproject.toml | TOML | repo |
| uv installed (≥ 0.6) | binary | developer machine |
| AGENTS.md or equivalent context file | Markdown | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pyproject.toml` | pyproject.toml skeleton with [project] + [tool.uv] sections. |
| `templates/agents-md-snippet.md` | Markdown snippet enforcing `uv run` for all Python tool calls in AGENTS.md. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-uv-lockfile-floor.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[ts-strict-isolated]]
- [[task-worktree-runtime-isolation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
