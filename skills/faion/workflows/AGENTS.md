# Faion Workflows

End-to-end orchestration patterns for multi-step delivery inside one agent session. Each workflow is a self-contained methodology folder following the skill-authoring spec (`docs/skill-authoring.md`): `AGENTS.md` for routing, `content/*.xml` for the executable rules, `templates/` for reusable artifacts.

## How to Use

1. **Match by trigger.** Read `catalog.json` for the machine-readable trigger map (`triggers` field per workflow). Or scan the Index table below.
2. Read exactly one platform adapter — `adapters/claude-code.md` or `adapters/codex.md`. Workflow content names platform-neutral primitives (`platform user-choice primitive`, `platform subagent-dispatch primitive`, `platform quota-state source`, `platform wakeup primitive`, `platform cross-session memory store`, `platform worktree isolation path`); the adapter is what maps them onto the running runtime.
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

## Orchestration rules (workflow-specific; repo-wide conventions are in the root `AGENTS.md`)

- **Subagents** are dispatched through the active platform adapter; use worktree isolation where the workflow requires it.
- **Quota gate:** read `platform quota-state source` between spawns; pause on threshold.
- SDD phases inside a workflow follow the repo lifecycle `backlog/ → todo/ → in-progress/ → done/` under `.aidocs/<project>/`.

## Adding a New Workflow

1. Create `workflows/<workflow-slug>/` mirroring the methodology folder shape (`AGENTS.md` + `content/` + optional `templates/` and `scripts/`).
2. Validate every `content/*.xml` against the closed tag glossary at `skills/faion/knowledge/llm-integration/semantic-xml-content/templates/tag-glossary.xml`.
3. Run `python3 scripts/validate-workflow-v2.py` — it is validator 6 of `f066-validate-all.sh` and covers the workflow shape. **Do not run `validate-methodology-xml.py`**; it is superseded and listed as do-not-run in `scripts/AGENTS.md`.
4. Add a row to the Index table above and to `catalog.json`, with one-line trigger phrasing.
5. Add a CHANGELOG entry under `## [Unreleased]`.

## Related

- `../../../workflows/article-pipeline.js` — **runnable** Workflow-tool script (invoked by name via `Workflow({name: "article-pipeline"})`): universal longform article production + translation; content-only, no coding. Projects supply paths/languages/gates/prompt-overrides via `args`. Its role prompts are also distilled into the corpus fragment library at `../fragments/article/` (tier pro; `corpus:article-outliner` et al.), which the F027 workflow composer in `faion-cli` composes into emitted artifacts.
- `../fragments/sdd/` — SDD role fragment library (tier solo; `corpus:sdd-intake-analyzer`, `sdd-planner`, `sdd-task-executor`, `sdd-wave-coordinator` + verdict schema, `sdd-code-reviewer` + verdict schema, `sdd-fix-applier`), distilled from `sdd-batch-orchestrator/`'s role contracts for the F027 workflow composer.
- `docs/skill-authoring.md` — folder shape, token budgets, anti-patterns.
- `adapters/claude-code.md` · `adapters/codex.md` — the two runtime mappings.
- `skills/faion/knowledge/llm-integration/semantic-xml-content/` — semantic XML convention.
