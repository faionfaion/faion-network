# Faion Workflows

End-to-end orchestration patterns for multi-step delivery inside one Claude Code session. Each workflow is a self-contained methodology folder following the skill-authoring spec (`docs/skill-authoring.md`): `AGENTS.md` for routing, `content/*.xml` for the executable rules, `templates/` for reusable artifacts.

## How to Use

1. Read this file to pick the workflow that matches the user's ask.
2. Read the workflow's `AGENTS.md` (under 80 lines) to confirm fit.
3. Load the specific `content/*.xml` files relevant to the current phase.
4. Use templates verbatim where the workflow references them.

A workflow is **the orchestration shape**, not a script. The orchestrator is always Claude in the active session; subagents are spawned via the `Agent` tool with paths to versioned prompt files.

## Index

| Workflow | When to use |
|----------|-------------|
| `sdd-batch-orchestrator/` | Batch of ≥3 related SDD features delivered through study → clarify → plan → wave-execute → verify → review → fix → visual-deliver → close, fronted by versioned prompt files. |

## Conventions Inherited from the Repo

- **SDD lifecycle:** features and tasks travel `backlog/ → todo/ → in-progress/ → done/` inside `.aidocs/<project>/`.
- **Monorepo + nested repos:** primary tree is `faionfaion/faion-net`; `faion-net-fe/`, `faion-net-be/`, `faion-net-e2e/`, `faion-network/`, `faion-network-storybook/` are separate git repos.
- **Commits:** 50-char title, `type: short`, no Co-Authored-By, no emojis, **CHANGELOG.md entry under `## [Unreleased]` required by pre-commit**.
- **Pre-commit:** never `--no-verify`; fix the underlying issue and re-commit.
- **Subagents:** dispatched with `Agent` (`subagent_type`, `model`, `isolation: "worktree"`, `run_in_background`).
- **Quota gate:** read `/tmp/claude-session-state.json` between spawns; pause on threshold.
- **Language:** user-facing strings Ukrainian; code, commits, prompt files, reference docs English.

## Adding a New Workflow

1. Create `workflows/<workflow-slug>/` mirroring the methodology folder shape (`AGENTS.md` + `content/` + optional `templates/` and `scripts/`).
2. Validate every `content/*.xml` against the closed tag glossary at `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`.
3. Run `python3 scripts/validate-methodology-xml.py skills/faion/workflows/<slug>/methodology.xml` if the workflow ships a `methodology.xml`; otherwise validate each content file individually.
4. Add a row to the Index table above with one-line trigger phrasing.
5. Add a CHANGELOG entry under `## [Unreleased]`.

## Related

- `docs/skill-authoring.md` — folder shape, token budgets, anti-patterns.
- `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/` — semantic XML convention.
- `skills/faion/` — quality gates and review loop primitives.
- `skills/faion/` — sequential SDD task execution baseline.
