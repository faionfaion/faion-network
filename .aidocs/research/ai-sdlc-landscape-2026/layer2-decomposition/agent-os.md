# Agent OS (Builder Methods)
**Layer:** 2 — Decomposition · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is
Agent OS is a set of markdown command files plus three bash install scripts, by Brian Casel (Builder Methods), that put a project's coding *standards* into a place an AI agent will actually read. It began (2025) as a full spec-driven pipeline — plan product, create spec, create tasks, execute tasks, verify — and in v3 (2026-01-20) deliberately deleted most of that, keeping only standards discovery, standards injection, product planning, and a plan-mode wrapper. Today the entire repo is 424 KB and five command files. It is not a CLI, not a runtime, and not agent-agnostic in any deep sense: it targets Claude Code's Plan Mode, AskUserQuestion tool, and Skills format directly, and works with others only insofar as they have a plan mode.

## Current state
| Fact | Value | Dated |
|---|---|---|
| Latest release | **v3.0.0 "Agent OS 3.0"** | published 2026-01-20T17:26:20Z (Releases API) |
| Prior releases | v2.1.1 (2025-10-28), v2.1.0 (2025-10-21), v2.0.0 (2025-10-07), v1.4.1 (2025-08-19) | Releases API, 2026-08-03 |
| Last code push | **2026-05-05T05:07:51Z** — ~3 months stale | GitHub API, 2026-08-03 |
| Commits since v3.0.0 | **4**, all on 2026-05-05, all install-script bug fixes (PR #327 `tac`→POSIX `awk` for macOS; PR #328 `((var++))` under `set -e`) | Commits API, 2026-08-03 |
| Stars | **5,160** | GitHub API, 2026-08-03 |
| Forks / watchers / open issues | 814 / 109 / **2** | GitHub API, 2026-08-03 |
| Repo created | 2025-07-16T21:28:59Z | GitHub API |
| Maintainer | `buildermethods` org — effectively one person, Brian Casel | 2026-08-03 |
| License | **MIT** | GitHub API, 2026-08-03 |
| Price | **Free & open source** (buildermethods.com/agent-os, fetched 2026-08-03). Paid adjacent: "Builder Methods Pro" community + courses; price not published on that page. |
| Repo size | 424 KB · primary language Shell | GitHub API, 2026-08-03 |

**Is it still maintained?** Barely, and it is not dead. Signals for: MIT, `archived: false`, only 2 open issues (the author closes or declines), two community PRs merged 2026-05-05. Signals against: zero feature work in the 6.5 months since v3.0.0; the entire repo is 5 command files; the project's own v3 release notes are an argument for *doing less*, which caps how much future work there is to do. Treat it as **feature-complete-by-retreat, low-activity, single-maintainer** — fine to read, wrong to depend on.

### Claims adjudicated
| # | Claim (landscape doc / prior pass, 2026-08-03) | Verdict | Dated evidence |
|---|---|---|---|
| 5a | "Three context layers Standards → Product → Specs, each injected at its own moment" | **CORRECT for v1/v2; only partly true in v3** | The three folders still exist (`agent-os/standards/`, `agent-os/product/`, `agent-os/specs/` — confirmed in v3 `plan-product.md` and `shape-spec.md`, fetched 2026-08-03). But "each injected at its own moment" described a pipeline v3 dismantled: the Specs layer is no longer *authored* by Agent OS, and injection is now one on-demand command (`/inject-standards`) rather than a per-phase automatic step. State the claim as "three context *folders*", not "three injection moments". |
| 5b | "v3 can auto-extract standards from an existing codebase" | **CONFIRMED** | `/discover-standards` (`commands/agent-os/discover-standards.md`, fetched 2026-08-03): "Extract tribal knowledge from your codebase into concise, documented standards." Reads 5-10 representative files per area, surfaces patterns that are *unusual / opinionated / tribal / consistent*, then asks the user which to keep. Semi-automatic — it never writes a standard without an AskUserQuestion confirmation. |
| 5c | Prior pass: "v3.0.0 (2026-01-20) surrendered spec authoring to Claude Code Plan Mode" | **CONFIRMED, in the maintainer's own words** | CHANGELOG `## [3.0] - 2026-01-20`: "Spec writing — Now best handled using Plan mode"; "Spec creation now defers to **Plan Mode**…the industry-standard approach to spec-driven development in 2026+"; "Implementation/orchestration phases retired—frontier models handle this well on their own now." `shape-spec.md` hard-stops if not in plan mode. |
| 5d | Prior pass: "dropped `decisions.md` for post-ship 'Recaps'" | **WRONG on both halves** | (a) No `decisions.md` exists in **any** tagged version. Trees for v1.2.0, v1.3.0, v1.4.1, v2.1.1 and `main` contain zero paths matching `decision`; v1.4.1 `instructions/core/plan-product.md` L56-59 lists the product file set as exactly `mission.md`, `mission-lite.md`, `tech-stack.md`, `roadmap.md`. Nothing was dropped because nothing was there. (b) Recaps were **not** a v3 replacement — they were introduced in **v1.4.1 (2025-08-19)**, whose release title is literally "Recaps, Project Manager subagent & task execution improvements", implemented in `instructions/core/complete-tasks.md` step 5 (`document_recap` → `.agent-os/recaps/[SPEC_FOLDER_NAME].md`) via the `project-manager` subagent. v3 **removed** recaps along with the whole implementation phase; there is no recap machinery in `main` as of 2026-08-03. |
| 5e | Prior pass: "5,160 stars, last push 2026-05-05" | **CORRECT** | GitHub API, 2026-08-03: `stargazers_count: 5160`, `pushed_at: 2026-05-05T05:07:51Z`. (Note `updated_at: 2026-08-03T19:10:04Z` is metadata churn — stars/watches — not code.) |

## Mechanics

### Install
Three bash scripts, no package manager, no CLI binary:
```
scripts/project-install.sh     # install into a project
scripts/sync-to-profile.sh     # push a project's standards back up into a base profile
scripts/common-functions.sh
```
`config.yml` at repo root is the entire configuration in v3:
```yaml
version: 3.0
default_profile: default
# profiles:
#   profile-a:
#     inherits_from: default
```
Profile inheritance moved from separate files into this one file in v3.

### The five commands (v3, `commands/agent-os/`)
`discover-standards.md`, `index-standards.md`, `inject-standards.md`, `plan-product.md`, `shape-spec.md`.
That is the complete list — verified against the `main` git tree, 2026-08-03. **Gone since v2.1.1:** `write-spec`, `create-tasks`, `implement-tasks`, `orchestrate-tasks`, `improve-skills`, and the entire `multi-agent/` vs `single-agent/` command duplication.

### Folder layout it produces
```
agent-os/
  standards/            # layer 1 — the durable "how we build" corpus
    index.yml           # slug → one-line description; the retrieval index
    <root>.md           # files directly in standards/ are addressed as `root/<name>`
    api/response-format.md, api/error-handling.md
    database/migrations.md, frontend/components.md, …
  product/              # layer 2 — the durable "what this product is"
    mission.md  roadmap.md  tech-stack.md
  specs/                # layer 3 — per-feature, now written by Plan Mode, saved here
profiles/default/global/tech-stack.md   # shipped default: React 18 + TS, Tailwind v4, Vite, Node/Express, PostgreSQL
```
`root` is a **reserved keyword** meaning "`.md` files directly in `agent-os/standards/`, not in a subfolder"; the docs explicitly warn against creating an actual folder named `root`.

### `/discover-standards` — the mechanism worth studying
1. If no area given: analyze folder structure and file types, identify **3-5 major areas** (frontend: components/styling/state/forms/routing; backend: API routes/DB/auth/jobs; cross-cutting: error handling, validation, testing, naming, file structure). Present them via **AskUserQuestion**. Wait.
2. Read **5-10 representative files** in the chosen area. Surface only patterns that are **unusual or unconventional** (not stock framework behavior), **opinionated** (could plausibly have gone the other way), **tribal** (a new dev wouldn't know without being told), and **consistent** (repeated across files).
3. Present candidates; user picks ("Yes, all of them" / "Just 1 and 3" / "Add: …" / "Skip this area"). Wait.
4. **"Ask Why, Then Draft Each Standard"** — for every accepted standard the user is asked *why* before it is written. The rationale is part of the artifact.
Standing instruction across all v3 commands: *"Write concise standards — use minimal words. Standards must be scannable by AI agents without bloating context windows."*

### `/inject-standards` — context-shaped retrieval
Two modes:
```
/inject-standards                                  # auto-suggest from the index
/inject-standards api                              # whole folder
/inject-standards api/response-format              # one file
/inject-standards api/response-format api/auth     # several
/inject-standards root                             # loose .md files in standards/
```
Step 1 detects one of three **scenarios** and formats output differently for each:
1. **Conversation** — read the standards' full text into chat (implementation work needs the content).
2. **Creating a Skill** — emit *file references* to paste into a `.claude/skills/` file.
3. **Shaping/Planning** — in plan mode: emit *file references* into the plan/spec.
Detection: plan mode OR the words "spec"/"plan"/"shape" → Shaping; mentions of `.claude/skills/` → Skill; otherwise **ask, never assume**. This full-text-vs-reference distinction is the single sharpest idea in the tool.

### `/index-standards`
Rebuilds `agent-os/standards/index.yml` so `/inject-standards` can suggest without reading every file. Scans `.md` files, diffs against the existing index (new / deleted / unchanged), and for each new file reads it and proposes a description via AskUserQuestion. This is a hand-rolled two-level retrieval — exactly the L1-index → L2-leaf shape our own `domains.xml` → `INDEX.xml` → leaf uses.

### `/plan-product` and `/shape-spec`
`plan-product` is a lightweight interview producing `mission.md`, `roadmap.md`, `tech-stack.md`. It checks for existing files first and offers *Start fresh / Update specific files / Cancel*. Standing rules: **always use AskUserQuestion**, **one question at a time**, **keep it lightweight — don't over-document**.
`shape-spec` **hard-stops** unless the agent is in plan mode: *"Shape-spec must be run in plan mode. Please enter plan mode first, then run /shape-spec again."* Its steps: (1) clarify scope + 1-2 follow-ups, (2) gather visuals (mockups/wireframes/screenshots), (3) identify **reference implementations** in the existing codebase ("The comments feature is similar to what we're building"), (4) read `agent-os/product/` if present and confirm alignment. It never writes the spec — Plan Mode does, and the resulting plan is saved into the Agent OS spec folder.

### What is enforced vs suggested
**Nothing is enforced by code.** There is no equivalent of Spec Kit's `check-prerequisites.sh` — the three bash scripts only install and sync files. The only hard gate is a *prose* precondition in `shape-spec.md` ("stop immediately if not in plan mode") that an obedient model honors. Everything else is a suggestion inside a markdown prompt. Agent OS is a **content** system, not a control system.

## Primary docs collected
| # | Title | URL | What's in it | Fetched |
|---|---|---|---|---|
| 1 | agent-os repo metadata (API) | https://api.github.com/repos/buildermethods/agent-os | 5,160 stars; pushed 2026-05-05T05:07:51Z; MIT; Shell; 2 open issues; not archived | 2026-08-03 |
| 2 | Releases (API) | https://api.github.com/repos/buildermethods/agent-os/releases | v3.0.0 = 2026-01-20T17:26:20Z; v1.4.1 = 2025-08-19 titled "Recaps, Project Manager subagent…" | 2026-08-03 |
| 3 | Commits (API) | https://api.github.com/repos/buildermethods/agent-os/commits | only 4 commits since v3.0.0, all 2026-05-05, all install-script fixes | 2026-08-03 |
| 4 | CHANGELOG.md | https://raw.githubusercontent.com/buildermethods/agent-os/main/CHANGELOG.md | full v3.0 rationale; v2.1.0 history; "Implementation/orchestration phases retired" | 2026-08-03 |
| 5 | commands/agent-os/discover-standards.md | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/discover-standards.md | 3-5 areas, 5-10 files, unusual/opinionated/tribal/consistent filter, "ask why" | 2026-08-03 |
| 6 | commands/agent-os/inject-standards.md | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/inject-standards.md | 3 scenarios; full-text vs file-reference formatting; `root` keyword | 2026-08-03 |
| 7 | commands/agent-os/index-standards.md | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/index-standards.md | `index.yml` rebuild + new/deleted diff | 2026-08-03 |
| 8 | commands/agent-os/shape-spec.md | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/shape-spec.md | plan-mode hard precondition; visuals; reference implementations | 2026-08-03 |
| 9 | commands/agent-os/plan-product.md | https://raw.githubusercontent.com/buildermethods/agent-os/main/commands/agent-os/plan-product.md | mission/roadmap/tech-stack interview; one-question-at-a-time | 2026-08-03 |
| 10 | config.yml | https://raw.githubusercontent.com/buildermethods/agent-os/main/config.yml | `version: 3.0`, `default_profile`, `inherits_from` | 2026-08-03 |
| 11 | v1.4.1 `instructions/core/complete-tasks.md` | https://raw.githubusercontent.com/buildermethods/agent-os/v1.4.1/instructions/core/complete-tasks.md | step 5 `document_recap` → `.agent-os/recaps/`; proves Recaps = v1.4.1, not v3 | 2026-08-03 |
| 12 | v1.4.1 `instructions/core/plan-product.md` | https://raw.githubusercontent.com/buildermethods/agent-os/v1.4.1/instructions/core/plan-product.md | L56-59 product file set — **no** `decisions.md` | 2026-08-03 |
| 13 | Official docs / landing | https://buildermethods.com/agent-os | "v3"; "Free & Open Source"; Builder Methods Pro is the paid adjacent product | 2026-08-03 |

## What to borrow for faion
1. **The three formatting scenarios of `/inject-standards`.** Full text into a conversation, *file references* into a Skill, *file references* into a plan. Our `faion` skill retrieval currently returns methodology content one way. Emitting a reference when the consumer is a durable artifact (a Skill, a `plan.md`) and full text only when the consumer is an ephemeral conversation is a direct token win and prevents copies of methodology text rotting inside customer plans.
2. **The `discover-standards` extraction filter.** *Unusual · opinionated · tribal · consistent* is a four-word test for "is this worth writing down". It is the best answer I have seen to the brownfield-onboarding problem, and it is what turns a mature codebase into a `project-spec/` without the owner typing it. Directly reusable as a `project-spec/` bootstrapper.
3. **"Ask why, then draft."** Every standard carries the rationale that justified it. Same rule the user proposes for `constitution.md` items. Agent OS makes it a *procedure*, not a template field — the model must obtain the "why" from the human before the artifact exists.
4. **`index.yml` as a retrieval index over prose standards.** Independent convergent evolution of our `domains.xml` → `INDEX.xml` → leaf pyramid, at project scale rather than corpus scale. Worth stealing *downward*: customers should have a project-local index of their own standards, generated the same way we generate ours.
5. **`shape-spec`'s "identify reference implementations" step.** Asking "is there similar code in this codebase I should reference?" before planning. Cheap, high-yield, and absent from our lifecycle.
6. **The v3 retreat itself, as a design lesson.** The maintainer publicly deleted spec-writing, task breakdown, and orchestration because the host agent got good enough. That is a direct warning about which parts of *our* SDD are commoditizing: task breakdown and implementation orchestration are the parts a frontier model now does unaided. Our durable value is the corpus and the invariants, not the pipeline choreography.

## What NOT to borrow — and why
1. **The tool.** Five markdown files, one maintainer, no feature commits in 6.5 months, no CLI, bash-only install. There is nothing to depend on and nothing that would survive us depending on it.
2. **Deferring spec authoring to Plan Mode.** Correct for Agent OS's business (it sells standards, not process), wrong for ours. Plan Mode output is ephemeral, unversioned, Claude-Code-specific, and invisible to a non-technical user. Our `spec.md` / `plan.md` being files under `todo/ → in-progress/ → done/` is precisely the thing a solopreneur can hand to someone else, diff, and revisit. Do not surrender the artifact.
3. **Retiring the implementation/orchestration phase.** Agent OS's justification ("frontier models manage task delegation on their own") assumes a single interactive session with a human watching. Our pool/subagent orchestration exists for unattended batch runs where nobody is watching. Different problem.
4. **Losing Recaps with nothing in their place.** v1.4.1 wrote a dated `.agent-os/recaps/<spec>.md` after completion; v3 has no post-ship artifact at all. Our `readiness.md` + `done/` archive covers this — keep it, and note this as an argument *for* our gate, not against.
5. **The shipped `profiles/default/global/tech-stack.md`** (React 18 + Tailwind v4 + Vite + Node/Express + PostgreSQL). A default stack opinion baked into a framework is exactly the thing our `constitution.md`-declares-`project-spec/` design avoids. Ship an empty template, never a stack.
6. **AskUserQuestion-per-step as the only interaction model.** `plan-product` asks one question at a time across ~8 steps. For a non-technical solopreneur that is better than a wall of form fields, but it is also Claude-Code-tool-specific and does not survive into a Go CLI. Borrow the *interview shape*, not the tool binding.

## Mapping to our corpus
Verified against `skills/faion/knowledge/sdd/INDEX.xml` (v3.0, `count="90"`, generated 2026-05-25), `skills/faion/knowledge/sdlc-ai/INDEX.xml`, and `skills/tier-manifest.json` (v8, 3070 entries, updated 2026-05-07).

**Overlaps — already covered:**
- `sdlc-ai/task-plan-mode-locked-execution` (geek) — the Agent OS v3 thesis (plan mode as the authoring surface, execution locked to the approved plan). Closest existing match to `shape-spec`.
- `sdlc-ai/ai-convention-anchoring` (solo) — the "inject standards so the agent writes in your style" idea.
- `sdlc-ai/agents-md-per-module-bootstrap` (solo) and `sdlc-ai/kb-agents-md-context-pyramid` (geek) — our layered always-on context; functionally the Standards layer plus the retrieval pyramid `index.yml` imitates.
- `sdlc-ai/kb-versioned-agent-memory-files` (geek) — durable agent-readable memory.
- `sdlc-ai/kb-codebase-rag-symbol-chunked` (geek) and `sdlc-ai/kb-symbol-index-fresh-tags` (geek) — mechanical codebase indexing; adjacent to but *not* the same as `discover-standards`, which extracts **judgement**, not symbols.
- `sdd/sdd-workflow-overview` (solo), `sdd/workflow-spec-phase` (solo) — the phase chain v3 abandoned.
- `sdd/pattern-memory` (solo), `sdd/mistake-memory` (solo), `sdd/engagement-pattern-memory` (solo), `sdd/living-documentation` (solo), `sdd/client-conventions-as-code` (pro), `sdd/client-style-guide-importer` (pro) — the standards-as-durable-artifact family. `client-style-guide-importer` is the nearest neighbour to `discover-standards` but is scoped to importing a *given* style guide, not deriving one from code.
- `sdd/dark-knowledge-extraction-protocol` (pro) — closest existing slug to "extract tribal knowledge". Read this before writing anything new; it may already cover 60% of `discover-standards`.
- `sdd/project-spec-structure` — the intended home for the Standards+Product layers. **Exists on disk but is absent from both `INDEX.xml` and `tier-manifest.json`** (see defect note below).

**Proposed new methodology:**
- **slug:** `standards-extraction-from-codebase` · **domain:** `sdd` · **tier:** `pro`
  Derive a project's `project-spec/` invariants and conventions from an existing repo: pick 3-5 areas, sample 5-10 representative files each, keep only patterns that are unusual / opinionated / tribal / consistent, obtain the *why* from the owner before writing, and emit one short scannable file per standard plus an index entry. Justified as new only if `sdd/dark-knowledge-extraction-protocol` and `sdd/client-style-guide-importer` are read first and confirmed not to cover code→standard derivation. **If they do, this is "none — covered by `sdd/dark-knowledge-extraction-protocol`" plus a scope extension to that slug.**
- **slug:** `context-injection-by-consumer-shape` · **domain:** `sdlc-ai` · **tier:** `pro`
  The full-text-vs-file-reference rule: emit knowledge inline when the consumer is an ephemeral conversation, emit a path reference when the consumer is a durable artifact (a Skill, a plan, a spec). Nothing in `sdlc-ai/` covers this; `kb-agents-md-context-pyramid` covers *what* to load, not *in which form*. Directly relevant to how `faion get-content` should behave.

**Corpus defect (same as noted in `spec-kit.md`, repeated because it blocks this mapping):**
`skills/faion/knowledge/sdd/` holds **99** directories; `INDEX.xml` declares **90**. Missing from both `INDEX.xml` and `tier-manifest.json`: `project-spec-structure`, `plan-md-structure`, `quality-gates`, `readiness-checklist`, `user-flows-template`, `ui-ux-design-template`, `cr-bug-tracking`. All seven are cited by name in the repo root `AGENTS.md` as the authority for a lifecycle document, and all seven are unreachable by the retriever and ungated by tier.

## Open questions / staleness risk
- **Staleness: moderate but of a different kind than Spec Kit.** The risk is not that the docs move — nothing has moved since 2026-05-05 — it is that the project goes dormant and the ideas stop being maintained against changing agent capabilities. Re-check `pushed_at` before any customer-facing citation; if it is still 2026-05-05 in three months, downgrade to 🔴 as a *tool* while keeping the ideas.
- Builder Methods Pro pricing was not obtainable from the public landing page (2026-08-03). If a "price" figure is needed for a comparison table, it must be sourced separately.
- v3 docs and video walkthrough live behind buildermethods.com, not in the repo. The README delegates everything to that site, so the on-repo mechanics documented here may be incomplete relative to the site's guidance.
- Unresolved: whether `/discover-standards` produces standards a *non-technical* owner can evaluate. Every example in the command file is code-shaped ("API Response Envelope", "cursor-based pagination"). The extraction filter may not transfer to a non-technical solopreneur's product without a different question set.
- `index.yml`'s schema is never specified in the repo — only described. Anyone reimplementing must invent it.
