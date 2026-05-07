# Faion Workflows

End-to-end orchestration patterns for multi-step delivery inside one agent session. Each workflow is a self-contained methodology folder following the skill-authoring spec (`docs/skill-authoring.md`): `AGENTS.md` for routing, `content/*.xml` for the executable rules, `templates/` for reusable artifacts.

## How to Use

1. **Match by trigger.** Read `catalog.json` for the machine-readable trigger map (`triggers` field per workflow). Or scan the Index table below.
2. Read `adapters/AGENTS.md`, then the active platform adapter (`adapters/claude-code.md` or `adapters/codex.md`).
3. Read the workflow's `AGENTS.md` (≤80 lines) to confirm fit.
4. Load the specific `content/*.xml` files relevant to the current phase.
5. Use templates verbatim where the workflow references them.

A workflow is **the orchestration shape**, not a script. The orchestrator is the active agent in the current session; subagents are spawned via the platform subagent-dispatch primitive with paths to versioned prompt files.

## Catalog

`catalog.json` (this folder) is the machine-readable index — slug → metadata (status, version, summary, triggers, phases, content_files, agents_lines, notes). Use it for routing decisions instead of free-text search.

## Index

| Workflow | When to use |
|----------|-------------|
| `brainstorm/` | Multi-agent diverge-converge-review (10 research + 8 reviewers). Triggers: "brainstorm", "10 ideas", "audit X", "give me options". **Phase 0 consent gate** runs first if user did not explicitly ask for brainstorming. |
| `sdd-batch-orchestrator/` | Batch of ≥3 related SDD features delivered through study → clarify → plan → wave-execute → verify → review → fix → visual-deliver → close, fronted by versioned prompt files. Also single-feature SDD work. |
| `improver/` | Session-based continuous improvement: extract patterns + mistakes from current session (Phase 0, always) → optional system audit → propose fixes → apply with explicit approval → log → commit → skill creation. Triggers: "що зробили", "audit my server", "find issues", "improve system". |
| `media-ops/` | Build a complete AI media publishing pipeline from scratch (TG channel + site + automation). 7 phases: interview → propose → scaffold → infrastructure → seed content → register in media-manager → iterate. |
| `poll-agents/` | Self-replenishing background-agent pool for long queues of independent task batches (≥30). Parent does only orchestration; subagents work in isolated worktrees. Driven by cron tick + completion handler. |
| `idea-to-prod/` | Single-prompt autonomous build: idea → production via cron-driven loop, file-ref subagent dispatch, /faion-knowledge consultation, SDD phases. Triggers: "ідея до прод", "автономний білд", "запусти проект сам", "build this end-to-end". |

## Conventions Inherited from the Repo

- **SDD lifecycle:** features and tasks travel `backlog/ → todo/ → in-progress/ → done/` inside `.aidocs/<project>/`.
- **Monorepo + nested repos:** primary tree is `faionfaion/faion-net`; `faion-net-fe/`, `faion-net-be/`, `faion-net-e2e/`, `faion-network/`, `faion-network-storybook/` are separate git repos.
- **Commits:** 50-char title, `type: short`, no Co-Authored-By, no emojis, **CHANGELOG.md entry under `## [Unreleased]` required by pre-commit**.
- **Pre-commit:** never `--no-verify`; fix the underlying issue and re-commit.
- **Subagents:** dispatched through the active platform adapter; use worktree isolation where the workflow requires it.
- **Quota gate:** read `platform quota-state source` between spawns; pause on threshold.
- **Language:** user-facing strings Ukrainian; code, commits, prompt files, reference docs English.

## Adding a New Workflow

1. Create `workflows/<workflow-slug>/` mirroring the methodology folder shape (`AGENTS.md` + `content/` + optional `templates/` and `scripts/`).
2. Validate every `content/*.xml` against the closed tag glossary at `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml`.
3. Run `python3 scripts/validate-methodology-xml.py skills/faion/workflows/<slug>/methodology.xml` if the workflow ships a `methodology.xml`; otherwise validate each content file individually.
4. Add a row to the Index table above with one-line trigger phrasing.
5. Add a CHANGELOG entry under `## [Unreleased]`.

## Related

- `docs/skill-authoring.md` — folder shape, token budgets, anti-patterns.
- `adapters/AGENTS.md` — Claude Code and Codex runtime mappings.
- `skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/` — semantic XML convention.
- `skills/faion/` — quality gates and review loop primitives.
- `skills/faion/` — sequential SDD task execution baseline.
