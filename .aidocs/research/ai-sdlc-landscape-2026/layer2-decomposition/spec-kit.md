# GitHub Spec Kit
**Layer:** 2 — Decomposition · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
Spec Kit is a GitHub-maintained toolkit that installs a fixed sequence of slash-command prompt files into an AI coding agent's config directory, so the agent produces `spec.md` → `plan.md` → `tasks.md` before it writes code. The Python CLI is called `specify`; the on-disk marker directory it creates is `.specify/`. It ships no runtime, no model, and no server — the "product" is a set of markdown prompt templates plus five shell/PowerShell/Python helper scripts that resolve paths and assert file existence. Since v0.12 it has grown an extension/preset/bundle system that lets third parties override or add commands. It is agent-agnostic by design: the same templates are compiled into `.claude/commands/`, `.github/prompts/`, `.cursor/`, and ~30 other integration targets.

## Current state
| Fact | Value | Dated |
|---|---|---|
| Latest release | **v0.15.2** | published 2026-08-03T19:07:13Z (GitHub Releases API) |
| Previous releases | v0.15.1 (2026-07-31), v0.15.0 (2026-07-30), v0.14.4 (2026-07-29) | release cadence ≈ every 1-3 days |
| Stars | **125,171** | GitHub API, 2026-08-03 |
| Last push | 2026-08-03T19:32:10Z | GitHub API, 2026-08-03 |
| Repo created | 2025-08-21T22:54:31Z | GitHub API |
| Maintainer | `github` org (GitHub, Inc.); primary language Python | 2026-08-03 |
| License | **MIT** | GitHub API, 2026-08-03 |
| Price | **Free**. `uv tool install specify-cli` (PyPI) or `--from git+…@vX.Y.Z` | README, 2026-08-03 |
| Supported agents | "**30+ AI coding agents**" per README §Supported AI Coding Agent Integrations | README, 2026-08-03 |
| Repo size | 15,914 KB | GitHub API, 2026-08-03 |

Release velocity is extremely high — 6 minor versions (0.11 → 0.15) between 2026-06-26 and 2026-08-03. Anything you pin against will be stale within weeks.

### Claims adjudicated
| # | Claim (landscape doc, 2026-08-03) | Verdict | Dated evidence |
|---|---|---|---|
| 1 | "Spec Kit v0.11 (June 2026)" | **WRONG — stale by 6 minor versions** | v0.11.9 was 2026-06-26 and v0.11.2 was 2026-06-18, so "v0.11 ≈ June 2026" was true *then*. Current is **v0.15.2, published 2026-08-03T19:07:13Z** (Releases API, 2026-08-03). |
| 1b | "agent-agnostic, 30+ supported agents" | **CORRECT** | README §"Supported AI Coding Agent Integrations": "Spec Kit works with 30+ AI coding agents — both CLI tools and IDE-based assistants" (fetched 2026-08-03). |
| 1c | Prior pass: "v0.15.2, 125,169 stars, pushed 2026-08-03, 10 `/speckit.*` commands incl. `converge`" | **CORRECT** (star count now 125,171 — it moves hourly) | GitHub API 2026-08-03: `stargazers_count: 125171`, `pushed_at: 2026-08-03T19:32:10Z`. README lists exactly 10 commands: 7 core + 3 optional. `templates/commands/` contains exactly 10 `.md` files. |
| 1d | `converge` "added in 2026" | **CORRECT, and datable precisely** | CHANGELOG: `feat: add /speckit.converge command (#3001)` under `## [0.11.2] - 2026-06-18`; `Docs: Document /speckit.converge command (#3181)` under 0.11.10. |
| 2 | "Built for greenfield 0→1; rigidity hurts on a mature product" | **REFUTED as stated — half-true in practice** | README L317-327 (2026-08-03) has a three-row Development Phases table naming **"0-to-1 Development (Greenfield)"**, **"Creative Exploration"**, and **"Iterative Enhancement (Brownfield) — brownfield modernization: add features iteratively, modernize legacy systems"**, and points at `docs/guides/evolving-specs.md` as "the recommended brownfield loop". Brownfield is an explicitly supported, documented mode, not an afterthought. The *rigidity* half stands on its own evidence: `/speckit.converge` exists precisely because running the full chain against existing code kept leaving gaps. Rewrite the claim as "the artifact chain assumes a feature is authored before it exists; brownfield is supported but via a separate documented loop." |
| 3 | "Enforces nothing about content — only file existence and phase sequencing; `scripts/bash/check-prerequisites.sh` exits 1 without plan.md/tasks.md" | **CONFIRMED, verbatim** | Source read 2026-08-03: three `exit 1` branches — missing `$FEATURE_DIR`, missing `$IMPL_PLAN` (plan.md), and missing `$TASKS` (tasks.md, only when `--require-tasks`). `AVAILABLE_DOCS` is built purely from `[[ -f ]]` / `[[ -d ]]` tests. No parser, linter, or schema check anywhere in `scripts/`. Everything substantive lives in LLM-obeyed prose. |
| 4 | "`constitution.md` is the single most stealable idea, independent of the tool" | **CONFIRMED** | See `constitution-md-pattern.md` in this folder for the full adjudication. Short form: it is the only Spec Kit artifact that is (a) tool-independent, (b) versioned with a defined amendment procedure, and (c) treated as authority by a *different* command (`converge.md`: "The project constitution is **non-negotiable**… code that violates a MUST principle is the highest-severity finding"). |

## Mechanics

### Install and init
```bash
uv tool install specify-cli                                  # from PyPI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
specify init my-project --integration copilot
specify init my-project --integration claude --integration-options="--skills"   # skills mode
specify integration list
specify self check | specify self upgrade [--dry-run] [--tag vX.Y.Z]
specify extension add <name> | specify preset add <name>
```
`specify init` writes `.specify/` at the project root. `SPECIFY_INIT_DIR` (env) overrides which directory is treated as the project root; `resolve_specify_init_dir()` in `scripts/bash/common.sh` hard-fails if that path lacks `.specify/` — deliberately no silent fallback to cwd.

### The 10 commands (README, 2026-08-03)
Core: `/speckit.constitution`, `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.taskstoissues`, `/speckit.implement`, `/speckit.converge`.
Optional: `/speckit.clarify` (formerly `/quizme`), `/speckit.analyze`, `/speckit.checklist`.
Codex CLI in skills mode addresses them as `$speckit-*`; agent-skill ids are `speckit-constitution`, `speckit-converge`, etc.

### Artifacts on disk
```
.specify/
  memory/constitution.md      # the always-loaded governing document
  feature.json                # {"feature_directory": "specs/001-slug"} — persisted feature pointer
  extensions.yml              # optional hooks: hooks.before_converge, etc.
  templates/overrides/        # priority-1 project-local template overrides
scripts/bash/                 # + scripts/powershell/ + scripts/python/ — three parity implementations
  check-prerequisites.sh  common.sh  create-new-feature.sh  setup-plan.sh  setup-tasks.sh
templates/
  spec-template.md  plan-template.md  tasks-template.md  checklist-template.md
  constitution-template.md
  commands/{analyze,checklist,clarify,constitution,converge,implement,plan,specify,tasks,taskstoissues}.md
specs/<NNN>-<slug>/           # per-feature: spec.md, plan.md, tasks.md
                              # optional: research.md, data-model.md, contracts/, quickstart.md
```
Feature state resolution order (`get_feature_paths()` in `common.sh`): `SPECIFY_FEATURE_DIRECTORY` env → `.specify/feature.json` `feature_directory` key → hard error. Git branch names are **no longer** the feature identifier by default; `.specify/feature.json` is. `check-prerequisites.sh --paths-only` passes `--no-persist` so pure path resolution does not dirty the tree (issue #3025).

### What is actually enforced
`scripts/bash/check-prerequisites.sh` (and its PS/Python twins) is the whole enforcement surface. Flags: `--json`, `--require-tasks`, `--include-tasks`, `--paths-only`, `--help`. It does exactly three `exit 1` checks:
```bash
if [[ ! -d "$FEATURE_DIR" ]]; then  ... exit 1   # "Run /speckit.specify first"
if [[ ! -f "$IMPL_PLAN" ]];  then  ... exit 1   # "Run /speckit.plan first"
if $REQUIRE_TASKS && [[ ! -f "$TASKS" ]]; then ... exit 1   # "Run /speckit.tasks first"
```
Then it emits `{"FEATURE_DIR": "...", "AVAILABLE_DOCS": [...]}` where `AVAILABLE_DOCS` is a pure `[[ -f ]]` / `[[ -d ]]` presence list over `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md`. **No content is parsed, validated, linted, or schema-checked anywhere in the script layer.** Everything else — "resolve all `[NEEDS CLARIFICATION]` markers", "cite the Constitution Gate", "tag `[P]` only when truly parallel" — is prose inside a markdown prompt that an LLM may or may not obey.

### `/speckit.converge` (the drift-check)
Added in **v0.11.2, 2026-06-18** (PR #3001); documented in v0.11.10 (PR #3181). Frontmatter runs `check-prerequisites.sh --json --require-tasks --include-tasks`. Contract from `templates/commands/converge.md`:
- Reads `spec.md`, `plan.md`, `tasks.md` as the **sole source of intent**, plus `/memory/constitution.md` as governing constraints.
- Assesses the **present state of the code** — explicitly "not a diff tool… no git, no branch comparison, no history".
- **APPEND-ONLY**: its only write is a new `## Phase N: Convergence` section at the bottom of `tasks.md`. It MUST NOT touch `spec.md`, `plan.md`, existing task numbering, or application code.
- If the codebase already satisfies everything, `tasks.md` must be left **byte-for-byte unchanged**.
- Constitution violations of a MUST principle are the highest-severity finding; if the constitution is still an unfilled template, constitution checks are skipped gracefully rather than failing.
- Must run only *after* `/speckit.implement` has run on the current `tasks.md`.
Loads spec.md selectively (FR-###, SC-### excluding post-launch KPIs, user stories + acceptance scenarios, edge cases) — an explicit progressive-disclosure budget.

### `/speckit.constitution` amendment mechanics
From `templates/commands/constitution.md`: semver on the constitution itself — **MAJOR** = backward-incompatible principle removal/redefinition, **MINOR** = new principle or materially expanded guidance, **PATCH** = clarification/wording. Ambiguous bumps must be reasoned about before finalizing. The command must produce a **Sync Impact Report** prepended as an HTML comment at the top of the file (version change old→new, renamed principles, added/removed sections, deferred TODOs). Missing facts become `TODO(<FIELD_NAME>): explanation`. It always edits the existing `.specify/memory/constitution.md` — never creates a new template.

### Extension/preset priority
`.specify/templates/overrides/` (priority 1) > presets > extensions > core. Extensions add capability (new commands/phases); presets override how existing artifacts are shaped. `.specify/extensions.yml` declares `hooks.before_converge` etc., each with `enabled`, `optional`, and an uninterpreted `condition` field the prompt is told **not** to evaluate itself.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | spec-kit repo metadata (API) | https://api.github.com/repos/github/spec-kit | stars 125,171; pushed 2026-08-03T19:32:10Z; MIT; Python | 2026-08-03 |
| 2 | Releases (API) | https://api.github.com/repos/github/spec-kit/releases | v0.15.2 published 2026-08-03T19:07:13Z + 7 prior | 2026-08-03 |
| 3 | README.md | https://raw.githubusercontent.com/github/spec-kit/main/README.md | 10-command tables; "30+ AI coding agents"; Greenfield/Brownfield phase table (L319-327); install + `specify self upgrade` | 2026-08-03 |
| 4 | CHANGELOG.md | https://raw.githubusercontent.com/github/spec-kit/main/CHANGELOG.md | `converge` added #3001 under [0.11.2] 2026-06-18; docs #3181 | 2026-08-03 |
| 5 | scripts/bash/check-prerequisites.sh | https://raw.githubusercontent.com/github/spec-kit/main/scripts/bash/check-prerequisites.sh | the entire enforcement surface; 3 exit-1 existence checks | 2026-08-03 |
| 6 | scripts/bash/common.sh | https://raw.githubusercontent.com/github/spec-kit/main/scripts/bash/common.sh | `.specify/feature.json` resolution, `SPECIFY_INIT_DIR`, `--no-persist` | 2026-08-03 |
| 7 | templates/commands/converge.md | https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/converge.md | append-only contract; byte-for-byte-unchanged rule; constitution authority | 2026-08-03 |
| 8 | templates/commands/constitution.md | https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/constitution.md | semver bump rules; Sync Impact Report | 2026-08-03 |
| 9 | templates/constitution-template.md | https://raw.githubusercontent.com/github/spec-kit/main/templates/constitution-template.md | 5 principle slots + 2 free sections + Governance + version footer | 2026-08-03 |
| 10 | .specify/memory/constitution.md (their own) | https://raw.githubusercontent.com/github/spec-kit/main/.specify/memory/constitution.md | real 13,252-byte / 1,743-word / 214-line example; v1.0.0 ratified 2026-06-19 | 2026-08-03 |
| 11 | Evolving Specs guide (brownfield loop) | https://github.github.io/spec-kit/ (linked `docs/guides/evolving-specs.md`) | referenced from README L323-327 as the brownfield loop | 2026-08-03 |

## What to borrow for faion
1. **`converge` as a methodology, not a tool.** The append-only, no-git, present-state-vs-intent drift check is the single best idea in the repo and we have nothing like it. Our `readiness.md` is a human checklist; `converge` is an automatable re-derivation of remaining work. The "byte-for-byte unchanged when clean" rule is what makes it safe to run on a loop.
2. **Progressive-disclosure loading contracts inside prompts.** `converge.md` names exactly which sections of `spec.md` to load (FR-###, SC-### minus business KPIs, acceptance scenarios, edge cases). We should specify per-document load budgets the same way instead of "read spec.md".
3. **Semver + Sync Impact Report on governing documents.** MAJOR/MINOR/PATCH definitions for a *prose* document, plus a machine-readable diff header. Directly applicable to our `constitution.md` and `project-spec/`.
4. **Three-language script parity (bash/PowerShell/Python).** Our CLI is Go single-binary, but the principle — never let the workflow depend on a shell a Windows solopreneur lacks — is exactly our cross-platform USP.
5. **`.specify/feature.json` instead of branch names.** Decoupling "which feature am I on" from git branch is right for a solopreneur who works on `main`. Our SDD lifecycle currently infers state from directory position; an explicit pointer file is more robust.
6. **The overrides > presets > extensions > core priority ladder.** A clean answer to "how does a customer customize a methodology without forking it" — relevant to the faion tier/manifest design.

## What NOT to borrow — and why
1. **The 10-command chain itself.** For a solopreneur, `constitution → specify → clarify → plan → tasks → analyze → checklist → implement → converge` is 9 ceremony steps before a line of code. Our lifecycle already collapses this: `plan.md` merges design + execution plan into two H2s, which is strictly better than separate `plan.md` + `tasks.md`. Adopting Spec Kit's split would re-inflate what we deliberately deflated (as we did when we removed `test-plan.md`).
2. **`.specify/` as another root directory.** We already have `.product/`, `.aidocs/`, `.agents/`. A fourth agent-owned root is a documentation-convention violation and a discoverability tax.
3. **Non-technical users must never run `uv tool install specify-cli --from git+…@vX.Y.Z`.** That single line disqualifies the tool for half our audience. It also demands the user manually track release tags — the README literally tells you to go read the Releases page and substitute.
4. **The release cadence.** 6 minor versions in 5 weeks. Anything we document about Spec Kit rots. Do not ship a methodology that instructs a customer to run a specific `speckit` command sequence.
5. **`tasks.md` with `[P]` parallel tags.** Their own methodology admits mis-tagging is a hard failure with silent merge conflicts, and nothing checks it. A solopreneur with one agent gains nothing from parallel-task annotation.
6. **`taskstoissues`.** GitHub-issue coupling is org-scale ceremony; a solopreneur's tracker is the `todo/ → in-progress/ → done/` directory.

## Mapping to our corpus
Verified against `skills/faion/knowledge/sdd/INDEX.xml` (v3.0, `count="90"`, generated 2026-05-25) and `skills/faion/knowledge/sdlc-ai/INDEX.xml`, plus `skills/tier-manifest.json` (v8, 3070 entries, updated 2026-05-07).

**Direct overlap — already covered:**
- `sdlc-ai/task-spec-kit-three-step` (geek, v1.1.0, last_reviewed 2026-05-23) — this *is* our Spec Kit methodology. It encodes 6 rules: `artifact-order-fixed`, `clarification-markers-honored`, `constitution-gate-evidence`, `tasks-drive-agent-only`, `parallel-tag-meaning`, `skip-this-methodology`; ships a JSON-Schema output contract, a validator (`scripts/validate-task-spec-kit-three-step.py`), and `templates/{spec,tasks}-skeleton.md`.
  **It is STALE as of 2026-08-03.** It documents a *three*-step pipeline. Spec Kit now has ten commands, and `converge` (2026-06-18) post-dates the methodology's `last_reviewed` of 2026-05-23. Its `constitution-gate-evidence` rule cites "GitHub spec-kit /plan template" — still valid, but the surrounding chain is not.
- `sdd/sdd-workflow-overview` (solo), `sdd/workflow-spec-phase` (solo), `sdd/workflow-design-phase` (solo) — our own equivalent of the phase chain.
- `sdd/spec-requirements`, `sdd/spec-structure`, `sdd/writing-specifications`, `sdd/template-spec` (all solo) — cover `spec.md`.
- `sdd/impl-plan-components`, `sdd/impl-plan-task-format`, `sdd/impl-plan-100k-rule`, `sdd/writing-implementation-plans` (solo) — cover `plan.md` + `tasks.md`.
- `sdd/task-creation-principles`, `sdd/task-creation-parallelization` (solo) — cover `[P]` semantics.
- `sdd/quality-gates-confidence` (solo) — nearest thing to `/speckit.analyze` + `/speckit.checklist`.

**Proposed new methodology:**
- **slug:** `spec-drift-convergence-loop` · **domain:** `sdd` · **tier:** `pro`
  The append-only convergence check generalized off Spec Kit: read intent artifacts + constitution, assess present code state (explicitly not a git diff), append only unbuilt work as new tasks, leave the file untouched when clean, and refuse to run before implementation has run at least once. Nothing in `sdd/` or `sdlc-ai/` covers post-implementation drift detection — `sdd/quality-gates-confidence` gates *before* done, `sdd/readiness-checklist` gates the move to `done/`. Neither re-derives remaining work.
- **Update, not new:** bump `sdlc-ai/task-spec-kit-three-step` to v2.0.0 — rename the concept from "three-step" to the current command chain, or explicitly scope it as "the three artifact layers, tool-independent" and drop the `spec-kit` framing from the slug.

**Corpus defect found while verifying (unrelated to Spec Kit but blocking):**
`skills/faion/knowledge/sdd/` contains **99** directories but `INDEX.xml` lists **90**. These seven exist on disk yet appear in **neither** `INDEX.xml` **nor** `tier-manifest.json`, so the retriever cannot find them and no tier gates them:
`project-spec-structure`, `plan-md-structure`, `quality-gates`, `readiness-checklist`, `user-flows-template`, `ui-ux-design-template`, `cr-bug-tracking`.
Every one of these is referenced by name in the repo root `AGENTS.md` as the authority for a lifecycle document. They are invisible to the product that sells them.

## Open questions / staleness risk
- **Staleness: severe.** v0.15.2 shipped the same day this dossier was written; v0.11 → v0.15 took 5 weeks. Treat every command name here as valid only for 2026-08-03. Re-verify before any customer-facing citation.
- `docs/guides/evolving-specs.md` (the brownfield loop) was referenced from the README but not fetched in full — worth a follow-up read before writing `spec-drift-convergence-loop`.
- Unknown how often `/speckit.converge` produces false "already satisfied" clean results on a large codebase; the prompt gives the model no budget for how much code to read before concluding.
- The extension/preset/bundle catalog is community-submitted (README mentions adrkit, ContextForge MCP). Supply-chain surface for anyone installing them; not audited here.
- "30+ agents" is a README marketing count; the authoritative list is `specify integration list` against an installed version, which was not run.
