# OpenSpec
**Layer:** 2 — Decomposition · **Verdict:** 🟡 take the idea not the tool — for a SOLOPRENEUR incl. non-technical · **Verified:** 2026-08-03

## What it is

OpenSpec is a Node/TypeScript CLI that adds a **change-proposal layer** in front of a living spec tree. Instead of rewriting a capability's spec every time you touch it, you write a *delta* — an explicit `ADDED` / `MODIFIED` / `REMOVED` / `RENAMED` block — review it before any code is written, implement against it, then `archive`, which merges the delta into the permanent spec and moves the change folder aside.

The whole surface is plain Markdown with three structural rules (`## Requirements`, `### Requirement:`, `#### Scenario:`) plus a normative keyword (`SHALL`/`MUST`). The CLI's real job is validation and merge, not authoring — the authoring is done by an AI agent through generated slash commands (`/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:archive`).

It is the closest thing in the 2026 landscape to what our `.aidocs/` lifecycle already does, which is why it is worth stealing from rather than adopting.

## Current state

| Fact | Value | As of |
|------|-------|-------|
| Repo | `Fission-AI/OpenSpec` | 2026-08-03 |
| Latest release | **v1.7.0** ("New tools, smarter updates"), tagged 2026-07-29 | 2026-08-03 (GitHub Releases API) |
| npm | `@fission-ai/openspec`, `latest` = 1.7.0 published 2026-07-29T01:31Z; `beta` = 1.6.0-beta.1; `next` = 0.3.0 | 2026-08-03 (npm registry API) |
| Stars | **63,637** | 2026-08-03 (GitHub API) |
| Forks | 4,402 | 2026-08-03 |
| Last push | **2026-08-03T21:18Z** — actively developed, daily commits | 2026-08-03 |
| Open issues | 313 | 2026-08-03 |
| Repo created | 2025-08-05; first npm publish 2025-09-06 | — |
| Maintainer | Fission AI (primary committer visible in recent CHANGELOG: `@clay-good`) | 2026-08-03 |
| License | **MIT** | 2026-08-03 |
| Price | **Free / OSS.** No paid tier in the repo or on openspec.dev. Site collects emails for a "Coming Soon — Workspaces" feature; "Stores" (cross-repo planning) shipped in v1.5.0 (2026-06-28) as a beta and is free | 2026-08-03 |
| Homepage | openspec.dev — marketing only, no docs, no benchmarks | 2026-08-03 |
| Runtime | Node.js. Installed via `npx`/`pnpm`. **No Go binary, no Python.** | 2026-08-03 |

Release cadence 2026: 1.0.2 (Jan 27) → 1.1.0 (Jan 30) → 1.2.0 (Feb 23) → 1.3.0 (Apr 11) → 1.4.0 (Jun 1) → 1.5.0 (Jun 28) → 1.6.0 (Jul 10) → 1.7.0 (Jul 29). Roughly monthly minors, still accelerating.

**Dogfooding scale** (from a shallow clone of `main` at commit `45cca5d`, 2026-07-30): the repo's own `openspec/` tree holds **36 capability specs** and **83 archived changes** in `openspec/changes/archive/`, oldest dated `2025-08-05`. This is not a demo project — the format has survived ~1 year and 83 merges.

## Mechanics

Everything below is read from the v1.7.0 source (`src/core/validation/validator.ts`, `src/core/specs-apply.ts`, `src/core/parsers/*`), not from docs. It is sufficient to reimplement in Go.

### Directory layout

```
openspec/
├── config.yaml
├── specs/<capability>/spec.md        ← the living spec (the "baseline")
├── changes/
│   ├── <change-id>/
│   │   ├── proposal.md               ← ## Why + ## What Changes
│   │   ├── design.md                 ← optional
│   │   ├── tasks.md                  ← implementation checklist
│   │   ├── .openspec.yaml            ← optional metadata, holds `skip_specs: true`
│   │   └── specs/<capability>/spec.md ← the DELTA
│   └── archive/YYYY-MM-DD-<change-id>/
```

Nested capability folders are supported (`specs/<area>/<capability>/spec.md`). A `spec.md` sitting directly at `changes/<id>/specs/spec.md` — no capability folder — is a **hard error**, because the merge path silently drops it (issue #1385).

Archive naming: the date prefix `YYYY-MM-DD-` is prepended unless the change name already matches `/^\d{4}-\d{2}-\d{2}-/`, so the prefix never stacks (issue #1309).

### Commands (v1.7.0)

`init [path]` · `update [path]` · `list` · `view` · `show [change]` · `validate [item]` · `archive [change]` · `new change <name>` · `spec …` · `change …` · `store …` · `workset …` · `doctor` · `context` · `status` · `instructions` · `templates` · `schemas` · `config` · `completion` · `feedback` · `experimental` (hidden).

**There is no `diff` verb.** It existed and was removed in **v0.2.0** with the changelog line: *"Remove the deprecated `openspec diff` command and direct users to `openspec show`."* — note the correction: users were pointed at `openspec show`, **not** at `git diff`. That's the tool's own answer to "what would the spec look like after merge": don't simulate it, read the delta.

### Baseline spec file format (`openspec/specs/<cap>/spec.md`)

```markdown
# <capability> Specification

## Purpose
<prose>

## Requirements
### Requirement: <name>
The system SHALL <normative statement>.

#### Scenario: <name>
- **WHEN** <trigger>
- **THEN** <outcome>
- **AND** <extra outcome>
```

Structural rules enforced on baseline specs (`src/core/parsers/spec-structure.ts`):

| Regex | Meaning |
|-------|---------|
| `/^##\s+Requirements\s*$/i` | the only section whose requirements are parsed |
| `/^###\s+Requirement:\s*(.+)\s*$/i` | canonical requirement header |
| `/^##\s+(ADDED\|MODIFIED\|REMOVED\|RENAMED)\s+Requirements\s*$/i` | **illegal in a baseline spec** |

Two hard errors, both reported with line numbers, both of which abort `archive`:
1. `delta-header` — a delta header found in a baseline spec (it truncates the parsed `## Requirements` section).
2. `requirement-outside-requirements` — a `### Requirement:` header outside `## Requirements` (invisible to validate/list/archive).

Fenced code blocks are masked out first (`buildCodeFenceMask`), so a `#### Scenario:` inside a ```` ``` ```` example does not count.

### Delta file format (`changes/<id>/specs/<cap>/spec.md`)

```markdown
## ADDED Requirements
### Requirement: <name>
... SHALL ...
#### Scenario: <name>
- **WHEN** …
- **THEN** …

## MODIFIED Requirements
### Requirement: <existing name>
<the COMPLETE new body, not a patch>
#### Scenario: … (must repeat every scenario you intend to keep)

## REMOVED Requirements
### Requirement: <existing name>          ← header form
- `### Requirement: <existing name>`      ← or bullet form

## RENAMED Requirements
- FROM: `### Requirement: <old name>`
- TO: `### Requirement: <new name>`
```

Parser regexes (`src/core/parsers/requirement-blocks.ts`):

| Purpose | Regex |
|---------|-------|
| Requirement header | `/^###\s*Requirement:\s*(.+)\s*$/i` |
| REMOVED bullet | `/^\s*-\s*` + backtick? + `###\s*Requirement:\s*(.+?)` + backtick? + `\s*$/` |
| RENAMED FROM | `/^\s*-?\s*FROM:\s*` + backtick? + `###\s*Requirement:\s*(.+?)` + backtick? + `\s*$/` |
| RENAMED TO | same with `TO:` |
| Scenario header (delta counter) | `/^####\s+/` — **any** level-4 header, deliberately not only `Scenario:` |
| Scenario header (name extraction) | `/^####\s*Scenario:\s*(.+)\s*$/` |
| Normative keyword | `/\b(SHALL\|MUST)\b/` |
| Requirement-body terminator | `/^#{1,6}\s/` (first header ends the body) |
| Metadata line, skipped from body unless nothing else | `/^\*\*[^*]+\*\*:/` |

Name matching: `normalizeRequirementName(n) = n.trim()` — **case-sensitive**. A separate `foldRequirementName(n) = n.trim().toLowerCase().replace(/\s+/g,' ')` exists **only for typo detection**: a name that differs from an existing one solely in case/whitespace is treated as a mistake, never as a second requirement.

### Validation rules — hard ERROR vs WARNING vs INFO

`ValidationLevel = 'ERROR' | 'WARNING' | 'INFO'`. The verdict (`src/core/validation/validator.ts`, `createReport`):

```
valid = strictMode ? (errors === 0 && warnings === 0)
                   : (errors === 0)
```

So **`validate --strict` requires zero errors AND zero warnings** — confirmed. Exit code is `report.valid ? 0 : 1`. INFO never fails, in either mode.

**ERRORS (delta validation, `validateChangeDeltaSpecs`)**

| # | Rule | Message |
|---|------|---------|
| E1 | Delta spec at `specs/spec.md` root (regular file, not a dir) | "Delta spec found at specs/spec.md. Delta specs must live in a capability folder…" |
| E2 | Zero deltas across all files and no `skip_specs` marker | `CHANGE_NO_DELTAS` + a long guidance block |
| E3 | Delta section headers present but zero requirement entries parsed | "Delta sections … were found, but no requirement entries parsed." |
| E4 | No delta section headers at all in a file under `specs/` | "No delta sections found. Add headers such as `## ADDED Requirements`…" |
| E5 | ADDED/MODIFIED requirement with no body text | `ADDED "<n>" is missing requirement text` |
| E6 | ADDED/MODIFIED body missing `SHALL` or `MUST` | `REQUIREMENT_NO_SHALL` variant, with a hint if the keyword is only in the header |
| E7 | ADDED/MODIFIED with zero `####` children | `ADDED "<n>" must include at least one scenario` |
| E8 | Duplicate name within ADDED / within MODIFIED / within REMOVED | `Duplicate requirement in <SECTION>` |
| E9 | Duplicate `FROM` or duplicate `TO` in RENAMED | `Duplicate FROM in RENAMED` / `Duplicate TO in RENAMED` |
| E10 | Cross-section conflict: name in MODIFIED ∧ REMOVED | `Requirement present in both MODIFIED and REMOVED` |
| E11 | name in MODIFIED ∧ ADDED | `…both MODIFIED and ADDED` |
| E12 | name in ADDED ∧ REMOVED | `…both ADDED and REMOVED` |
| E13 | RENAMED `FROM` also appears in MODIFIED | "MODIFIED references old name from RENAMED. Use new header for `<to>`" |
| E14 | RENAMED `TO` collides with an ADDED name | "RENAMED TO collides with ADDED" |
| E15 | RENAMED `FROM` also appears in REMOVED (**folded** comparison) | "Requirement present in both RENAMED and REMOVED" |
| E16 | **Scenario loss** — a MODIFIED block omits a `#### Scenario:` the baseline still carries (only when `--mainSpecsDir` is resolvable; issue #1477) | "current spec contains scenario(s) not present in the modified block … Refresh the change spec before archiving" |
| E17 | `skip_specs: true` in `.openspec.yaml` but **any** file exists under `specs/` | `CHANGE_SKIP_SPECS_CONFLICT` |
| E18 | `skip_specs` set but `.openspec.yaml` is not valid change metadata | `CHANGE_SKIP_SPECS_INVALID_METADATA` |
| E19 | Baseline spec structurally invalid (delta header inside it, or requirement outside `## Requirements`) | aborts archive with line numbers |
| E20 | Proposal `## Why` < 50 chars | `CHANGE_WHY_TOO_SHORT` |
| E21 | Proposal `## What Changes` empty; spec `## Purpose` empty; spec has zero requirements; requirement/scenario text empty | schema errors from Zod |

**WARNINGS** (fail only under `--strict`)

- `## Why` > 1000 chars.
- More than **10** deltas in one change (`MAX_DELTAS_PER_CHANGE`) — "Consider splitting".
- Requirement text > **500** chars — "Consider breaking it down."
- `## Purpose` < **50** chars — "too brief".
- Delta description too brief / delta missing requirements.
- At archive time: a REMOVED requirement already absent from the baseline (early-sync); a delta `## Purpose` ignored because the target spec already has a different one; REMOVED entries ignored for a brand-new spec; a foreign `#`/`##`/`###` heading absorbed into a requirement block and about to be dropped.

**INFO** (never fails)

- A non-canonical `### <something>` header inside a delta section that the reader skipped — reported with line number and the exact fix (`Use "### Requirement: <header>"`).
- `skip_specs` accepted with zero deltas.

Notably **relaxed** vs. what one would assume: the *keyword grammar inside a scenario is not validated at all*. `- **WHEN**` / `- **THEN**` are convention, enforced only by the prompt templates the CLI generates for the agent. `countScenarios` counts *any* `####` header. There is no GIVEN requirement, no keyword whitelist, no line/column on most errors.

### Archive merge algorithm (`src/core/specs-apply.ts`)

This is the piece worth reimplementing. Precise order:

**0. Pre-flight.** Re-run the full delta conflict set (E8–E15) as *throws*, not diagnostics — archive refuses on the same conditions validate reports. If total operations = 0, throw.

**1. Load baseline.** If `openspec/specs/<cap>/spec.md` does not exist:
- MODIFIED or RENAMED present → **abort**: "target spec does not exist; only ADDED requirements are allowed for new specs."
- REMOVED present → warn, ignore.
- Build a skeleton spec; carry the delta's `## Purpose` into it if present and the result is readable, else keep the placeholder and warn.
If it does exist and the delta has a `## Purpose` that differs from the baseline's → warn, **ignore the delta's Purpose** ("Edit the target directly").

**2. Structure gate.** `findMainSpecStructureIssues(baseline)` → any issue aborts.

**3. Index.** `extractRequirementsSection(baseline)` splits the file into `{before, headerLine, preamble, bodyBlocks, after}`; build `Map<normalizeRequirementName(name) → RequirementBlock>`. A block's `raw` runs from its header to the next *recognised* header.

**4. Apply in order: RENAMED → REMOVED → MODIFIED → ADDED.** (Confirmed; comment in source: `// Apply operations in order: RENAMED → REMOVED → MODIFIED → ADDED`.)

- **RENAMED**: `from` missing ∧ `to` present → treat as already-synced no-op, *unless* a case/whitespace near-miss of `from` still exists (≠ `to`) → abort as a typo. `from` missing ∧ `to` missing → abort. `to` already present → abort ("target already exists"). Otherwise: rewrite line 0 of the block to `### Requirement: <to>`, re-key the map, record `from→to`.
- **REMOVED**: name missing → if a case/whitespace near-miss exists, abort as typo; else warn "treating it as already removed" and continue. Name present → delete from map.
- **MODIFIED**: name missing → abort. Header line of the delta block must itself parse to the same normalized name → else abort ("header mismatch in content"). `findMissingCurrentScenarios(current, modified)` — any scenario in the baseline block absent from the delta block → **abort** ("Refresh the change spec before archiving to avoid dropping scenarios"). Then replace the block wholesale. Counted as applied only if `normalizeBlockRaw(old) !== normalizeBlockRaw(new)`.
- **ADDED**: name already present with *identical* normalized raw → no-op (early-sync). Present with *different* content → abort ("already exists"). Else insert.

Rename chains are walked, not looked up once (`A→B` then `B→C`), with a visited-set cycle guard.

**5. Recompose.** Iterate the *original* `bodyBlocks` order; emit the replacement for each surviving key (preserves original ordering); then append every map entry not seen, in insertion order (new requirements land at the end). Join with `\n\n`, reassemble `before + "## Requirements" + body + after`, collapse `\n{3,}` → `\n\n`.

**6. Write.** If every operation was already synced, skip the write entirely rather than churn normalization diffs into the file. Then move `changes/<id>/` → `changes/archive/YYYY-MM-DD-<id>/` (`fs.rename`, with a copy+rm fallback for Windows).

**7. Gates before the move.** Archive stops (unless `--no-validate --yes`) if: validation fails; `tasks.md` has unchecked items; the post-merge sync check fails — i.e. after writing, it re-reads every touched capability and confirms ADDED present, MODIFIED applied, REMOVED gone, RENAMED under the new name and not the old. If any capability doesn't match, **nothing moves** and it reports the difference (v1.7.0 fix; previously the sync ran in a background task and could report `Specs: ✓ Synced` for a sync that never landed).

## Primary docs collected

| # | Title | URL | What's in it | Fetched |
|---|-------|-----|--------------|---------|
| 1 | Fission-AI/OpenSpec repo + README | https://github.com/Fission-AI/OpenSpec | Pitch, workflow, delta example, `openspec/` layout, Stores | 2026-08-03 |
| 2 | GitHub REST API `/repos/Fission-AI/OpenSpec` | https://api.github.com/repos/Fission-AI/OpenSpec | 63,637 stars, MIT, pushed 2026-08-03T21:18Z, 313 open issues | 2026-08-03 |
| 3 | GitHub Releases API | https://api.github.com/repos/Fission-AI/OpenSpec/releases | v1.7.0 @ 2026-07-29, full tag history | 2026-08-03 |
| 4 | npm registry `@fission-ai/openspec` | https://registry.npmjs.org/@fission-ai/openspec | dist-tags, per-version publish timestamps, MIT | 2026-08-03 |
| 5 | Source: `src/core/validation/{constants,types,validator}.ts` @ `45cca5d` | (shallow clone of `main`) | Every threshold, every message, strict-mode semantics | 2026-08-03 |
| 6 | Source: `src/core/specs-apply.ts` @ `45cca5d` | (shallow clone) | The full merge algorithm above | 2026-08-03 |
| 7 | Source: `src/core/parsers/{requirement-blocks,requirement-text,spec-structure,code-fence}.ts` | (shallow clone) | Every regex, name normalization, fence masking | 2026-08-03 |
| 8 | Source: `src/core/schemas/change.schema.ts` | (shallow clone) | Zod schema: `why` 50–1000 chars, deltas 1–10, operation enum | 2026-08-03 |
| 9 | `CHANGELOG.md` @ `45cca5d` | (shallow clone) | `diff` removal in 0.2.0; the #1437 and #1475 archive fixes | 2026-08-03 |
| 10 | `openspec/` self-hosted tree @ `45cca5d` | (shallow clone) | 36 live capability specs, 83 archived changes since 2025-08-05 | 2026-08-03 |
| 11 | openspec.dev | https://openspec.dev/ | Marketing; no docs, no benchmark, no pricing; "Workspaces coming soon" | 2026-08-03 |
| 12 | Jamie Telin, *Is Your Safe Choice Burning Your Budget?* | https://medium.com/it-chronicles/is-your-safe-choice-burning-your-budget-1cfddf8782e4 | The only public OpenSpec-vs-Spec-Kit token benchmark — see `spec-delta-pattern.md` | 2026-08-03 (published **2026-03-18**) |

## What to borrow for faion

1. **The four-verb delta vocabulary — including RENAMED.** ADDED / MODIFIED / REMOVED / RENAMED is the minimum complete set. Our F049 draft has only three; without RENAMED, every rename becomes a REMOVE+ADD pair that loses the requirement's history and its scenarios. Cheap to add, expensive to retrofit.

2. **The merge order RENAMED → REMOVED → MODIFIED → ADDED, verbatim.** It is not arbitrary: renames must land before anything addresses the new name, removals before modifications so a remove+modify contradiction surfaces as "not found" rather than being silently applied, and additions last so a `RENAMED TO` collision is caught by an already-populated map. If we implement a merge engine in Go, copy this order and the near-miss guards.

3. **Scenario-loss detection (E16).** This is the single best idea in the codebase. Because MODIFIED replaces the whole requirement body, an agent that regenerates a requirement from memory will quietly drop scenarios it forgot. OpenSpec compares the delta block's scenarios against the baseline's and refuses to archive on loss. Our `spec.md`-is-delta rule has exactly this hole today and no detector.

4. **Idempotent / early-sync tolerance.** Applying a delta whose content is already in the baseline is a no-op, not a conflict — but a *near-miss* (differs only in case/whitespace) is a hard abort. That distinction is what makes the tool survivable when a human edits the baseline by hand mid-flight. Any Go implementation must reproduce both halves.

5. **The strict-mode contract.** `errors === 0 && warnings === 0` for `--strict`, plain `errors === 0` otherwise, INFO never failing. Three levels is the right number: it lets a linter nag about a 900-word requirement without blocking a release.

6. **Fence-masking before any structural parse.** Our SDD docs are full of fenced examples that contain `### Requirement:` and `#### Scenario:`. Any validator we write must mask fences first or it will parse its own documentation.

7. **The "no `diff` verb" decision.** They shipped it, deprecated it, and pointed users at `show`. A simulated post-merge view is a maintenance burden that duplicates the merge engine. Confirms killing `faion sdd diff` from F049.

8. **`skip_specs: true` as an explicit, loud escape hatch** for pure-refactor changes, with a hard error if any spec file exists alongside it. We already have the "no spec impact" line in `readiness.md` (per `project-spec-structure/content/03-delta-update.xml`); making it machine-checkable is a small step.

## What NOT to borrow — and why

1. **The `openspec/specs/<capability>/` tree.** We already have `.aidocs/project-spec/`, which is strictly richer (see Mapping). Adding a second living-spec tree — which is exactly what F049 proposes with `.aidocs/specs/<capability>/` — would give us two sources of truth that must be kept consistent by hand. That is the drift problem we adopted `project-spec/` to solve.

2. **Node.js runtime.** Non-negotiable for us: `faion-cli` is a Go single binary and ships no runtime interpreter. Adopting OpenSpec means telling a non-technical solopreneur to install Node. Its 63k stars do not change that.

3. **The generated slash-command / skill surface.** `openspec update` writes agent instructions into 20+ tool-specific directories (`.claude/skills`, `.cursor`, `.windsurf`, …). We already own that layer through `faion-network` skills; two systems writing agent instructions into the same directories is a collision, not a synergy.

4. **`## Why` length limits (50–1000 chars) as a hard error.** Character-count gates on prose are ceremony. A 40-character "Search is broken for tier=free users" is a perfectly good Why. Adopt the *idea* (Why must be non-empty) and drop the numbers.

5. **`MAX_DELTAS_PER_CHANGE = 10` as a warning that fails `--strict`.** Solo work regularly touches more than 10 capabilities in one sweep. Under strict mode this turns a valid change into a failure.

6. **The requirement-name-as-primary-key design.** OpenSpec keys requirements on their *title string*, case-sensitively, and then needs `foldRequirementName`, near-miss detection, and rename-chain walking to survive it. Our corpus already uses stable numeric IDs (`FR-NNN`, `REQ-NNN` — see `sdd/spec-requirements`). Keep the IDs; a rename then becomes a title edit, not a graph operation, and RENAMED collapses to a trivial case.

7. **`MODIFIED` = full block replacement.** It is what forces E16 (scenario loss) to exist at all. If our IDs are stable we can express MODIFIED as a scoped edit ("REQ-014 scenario 3 replaced") and never risk silent scenario loss. Borrow their *detector* as a safety net, but not the design that makes it necessary.

8. **`test-plan.md` in the validated set.** Not an OpenSpec concept (they use `tasks.md`), and F049 wants to validate it. Don't — scenarios in the spec already are the test contract; a second document to keep in sync is drift bait.

## Mapping to our corpus

Ground truth read for this section: `skills/faion/knowledge/sdd/INDEX.xml` (274 lines, 60+ methodologies), `skills/faion/knowledge/sdd/project-spec-structure/` (AGENTS.md + `content/01-folder-shape.xml` … `04-location-decision.xml`, `meta.json` v1.0.0, tier `solo`, last reviewed 2026-05-25), `skills/faion/knowledge/sdd/spec-requirements/AGENTS.md`.

**Where we already beat OpenSpec:**

| Dimension | OpenSpec | Us |
|-----------|----------|-----|
| Living source of truth | `specs/<cap>/spec.md` — requirements + scenarios only | `project-spec/` — 15+ artefact types: `mission.md`, `glossary.md`, `business-rules.md`, `data-model.md`, `auth.md`, `deploy.md`, `config-secrets.md`, `non-functional.md`, `observability.md`, `invariants.md`, plus `domain/`, `api/`, `integrations/`, `decisions/` subtrees |
| Acceptance bar | validator exit code | **rebuild test** (`02-rebuild-test.xml`): a mid-level dev rebuilds the project in two weeks from `project-spec/` + `ui-ux-design.md` + `constitution.md`. Runs at end-of-feature and pre-deploy after CR/BUG |
| Delta discipline | `archive` command | **same-PR rule** (`03-delta-update.xml`): spec delta lands in the PR that ships the code; reviewer must diff spec against code; `readiness.md` checkbox blocks merge; "no spec impact" requires a written one-line reason |
| Retrieval cost | agent reads the whole capability spec | `project-spec/` is 58 files, avg 432 words, each subdir carrying its own `AGENTS.md`+`CLAUDE.md` so an agent routes to 3–4 files (~2k tokens) instead of bulk-loading |
| Side streams | none | `crs/` and `bugs/` with their own lifecycles (`cr-bug-tracking`), and a rule that a BUG exposing a missing business rule MUST update `business-rules.md` in the same PR |
| Requirement identity | title string, case-sensitive | numbered `FR-NNN`/`NFR-NNN` with stable anchors across revisions (`spec-requirements`) |

**Where OpenSpec beats us — honestly, three things:**

1. **Machine-checkable delta structure.** Our same-PR rule is a *review* rule enforced by a human checkbox. OpenSpec's is a parser with 20+ hard errors and an exit code. Ours is stronger in intent and weaker in enforcement — and on a solo project the reviewer and the author are the same person, which is exactly the blind spot `03-delta-update.xml` names.

2. **Scenario-loss detection.** We have nothing equivalent. Our `spec.md` is *supposed* to be delta-only when `project-spec/` exists; in practice (measured below, in `spec-delta-pattern.md`) 36% of it is baseline restatement, and nothing detects when a restatement silently drops a rule.

3. **Explicit RENAMED.** Not present anywhere in our SDD knowledge. `sdd/INDEX.xml` has no methodology covering requirement renames or ID stability across a rename.

**Corpus gaps this research exposes** (candidate new methodologies for `knowledge/sdd/`):

- No `spec-delta-format` methodology. `spec-structure`, `spec-requirements`, `spec-advanced-guidelines`, `writing-specifications` all describe a *full* spec. The delta shape is documented only inside the uncommitted F049.
- **No EARS methodology anywhere in the corpus.** `grep -i ears skills/faion/knowledge/*/INDEX.xml` → zero hits. We teach "Given-When-Then AC" (`spec-structure`, `workflow-spec-phase`, `impl-plan-task-format`) but never the EARS requirement templates (ubiquitous / event-driven / state-driven / optional-feature / unwanted-behaviour / complex). That is a real hole in a corpus that sells 2,622 methodologies over 23 domains.
- No methodology on requirement-ID stability, renames, or supersession.

**Verdict rationale (🟡):** the format is worth copying line for line; the tool is a Node dependency that would fork our source of truth in two. Take the delta vocabulary, the merge order, the scenario-loss check and the three-level severity model into our own Go validator; do not install `openspec`.

## Open questions / staleness risk

- **Fast-moving.** Eight minor releases in 2026, last push the same day as this dossier. The validation rule *set* has been stable since ~1.3.0, but archive semantics changed materially in 1.7.0 (inline sync + post-merge verification, PRs #1437/#1475). Re-verify `specs-apply.ts` before writing any Go port. **Staleness horizon: ~6 weeks.**
- **Stores / Workspaces.** "Stores" (cross-repo planning, v1.5.0 beta, 2026-06-28) and the unreleased "Workspaces" are the obvious commercialization path. There is no paid tier today and no announced pricing; a free OSS core with a paid hosted layer is the likely 2027 shape. Not a risk for a format we copy, a risk for a tool we depend on.
- **Unresolved:** does `validate --strict` fail on the INFO-level "non-canonical header skipped" diagnostic? Source says no (only ERROR and WARNING count), but the guidance text reads like it expects to be acted on. Worth a live test before we mirror the semantics.
- **Not verified:** whether the 36 live capability specs in their own repo have ever been hand-edited outside the archive path. If yes, the early-sync tolerance is load-bearing in practice and not just defensive.
- **Prior-pass corrections recorded here:** (a) the `diff` verb was removed in **v0.2.0** pointing at **`openspec show`**, not `git diff`; (b) `MODIFIED` blocks additionally fail on *scenario loss*, a rule the prior pass did not list; (c) requirement matching is **case-sensitive** with a separate case-insensitive fold used only for typo detection — an implementation detail that changes the Go port materially.
