# Feature 049 — Spec Deltas + BDD + CLI

**Status:** in-progress
**Owner:** Ruslan
**Created:** 2026-05-02
**Inspiration:** OpenSpec (spec-deltas), Gherkin/BDD, openspec CLI

## Why

Current SDD rewrites entire `spec.md` per feature → drift, no living single-source-of-truth, no machine-checkable validation. Borrow three OpenSpec primitives without abandoning NERO's 4-state lifecycle, constitution, roadmap, or memory layer.

## Goals

1. **Living capability specs** — `.aidocs/specs/<capability>/spec.md` updated atomically when a feature merges, instead of being scattered across `done/feature-*/spec.md` snapshots.
2. **Spec deltas per feature** — feature folders carry `spec-delta.md` with `## ADDED`, `## MODIFIED`, `## REMOVED` blocks instead of full rewrites.
3. **BDD scenarios** — every Requirement carries `WHEN/THEN` (and optional `GIVEN/AND`) scenarios that double as test contracts.
4. **CLI validator** — `faion sdd` subcommands validate structure, lint deltas, diff capabilities, archive features.

## Non-Goals

- Replacing `constitution.md`, `roadmap.md`, or `.aidocs/memory/` (kept as-is).
- Replacing the 4-state lifecycle `backlog/ → todo/ → in-progress/ → done/`.
- Migrating closed features in `done/` retroactively (only F049+ uses new format).
- Replacing existing `test-plan.md` — BDD scenarios live alongside, not instead.

## Scope

### IN

- New `.aidocs/specs/` capability tree
- `spec-delta.md` format spec
- BDD scenario grammar (Markdown-embedded, no separate `.feature` files)
- `faion sdd` CLI (5 subcommands: `validate`, `diff`, `archive`, `list`, `lint`)
- Migration plan: F049 itself uses new format; existing `done/*` left alone
- Updated AGENTS.md / docs

### OUT

- Auto-generation of `spec.md` from code
- IDE plugins, web viewer
- Schema enforcement beyond Markdown structure

## Capabilities Affected

- **sdd-lifecycle** — adds delta-based merge step (NEW capability)
- **sdd-cli** — adds `faion sdd` subcommand group (NEW capability)
- **sdd-bdd** — adds BDD scenario grammar (NEW capability)

## Requirements

### REQ-049-001: Living capability specs

The system SHALL maintain a `.aidocs/specs/<capability>/spec.md` per capability that reflects the current accepted state of that capability.

#### Scenario: New capability spec is created on first feature merge

- **GIVEN** capability `<cap>` has no `.aidocs/specs/<cap>/spec.md`
- **AND** feature F has `spec-delta.md` with `## ADDED Requirements` for `<cap>`
- **WHEN** F is archived (moved `in-progress/ → done/`)
- **THEN** `.aidocs/specs/<cap>/spec.md` is created with the ADDED requirements
- **AND** the feature's `spec-delta.md` is preserved in `done/F/`

#### Scenario: Existing capability spec is updated by delta merge

- **GIVEN** `.aidocs/specs/<cap>/spec.md` exists with REQ-A, REQ-B
- **AND** feature F's delta has `## MODIFIED REQ-A` and `## ADDED REQ-C`
- **WHEN** F is archived
- **THEN** the spec contains the modified REQ-A, original REQ-B, and new REQ-C
- **AND** a `## History` section in the spec gains an entry referencing F

### REQ-049-002: Spec-delta document format

A feature folder MAY contain a `spec-delta.md` declaring changes to one or more capabilities.

#### Scenario: Valid delta with all three operations

- **GIVEN** `spec-delta.md` contains:
  - `## Capability: <cap>`
  - `### ADDED Requirements` with one or more `#### REQ-<id>` blocks
  - `### MODIFIED Requirements` with `#### REQ-<id>` blocks (existing IDs)
  - `### REMOVED Requirements` with `#### REQ-<id>` references
- **WHEN** `faion sdd validate` runs on the feature
- **THEN** validation passes
- **AND** referenced REQ-IDs in MODIFIED/REMOVED exist in the target capability spec

#### Scenario: Invalid delta references nonexistent requirement

- **GIVEN** delta MODIFIES `REQ-X` that does not exist in `<cap>/spec.md`
- **WHEN** `faion sdd validate` runs
- **THEN** validator exits non-zero
- **AND** error names the missing REQ-ID and capability

### REQ-049-003: BDD scenario grammar

Every Requirement in a spec or delta SHALL include at least one `#### Scenario:` block using `GIVEN/AND/WHEN/THEN` keywords.

#### Scenario: Requirement without scenario fails lint

- **GIVEN** a Requirement block has no `#### Scenario:`
- **WHEN** `faion sdd lint` runs
- **THEN** lint reports `REQ-<id>: missing scenario`

#### Scenario: Scenario with malformed keywords fails lint

- **GIVEN** a scenario uses `WHENEVER` instead of `WHEN`
- **WHEN** `faion sdd lint` runs
- **THEN** lint reports the offending line and expected keyword set

### REQ-049-004: CLI surface — `faion sdd`

The `faion-cli` SHALL expose a `sdd` subcommand group with five operations.

#### Scenario: `faion sdd validate <feature>`

- **GIVEN** feature directory exists in `in-progress/` or `done/`
- **WHEN** user runs `faion sdd validate feature-049-spec-deltas-bdd-cli`
- **THEN** command checks: required files, delta syntax, REQ-ID references, scenario structure
- **AND** exits 0 on success, prints summary; exits 1+ on first failure with line:col

#### Scenario: `faion sdd diff <capability>`

- **GIVEN** a capability has spec at `.aidocs/specs/<cap>/spec.md`
- **AND** an in-progress feature has a delta touching `<cap>`
- **WHEN** user runs `faion sdd diff <cap>`
- **THEN** unified diff is printed showing what the spec WOULD look like after merging all in-progress deltas

#### Scenario: `faion sdd archive <feature>`

- **GIVEN** feature is in `in-progress/` and validates clean
- **WHEN** user runs `faion sdd archive <feature>`
- **THEN** deltas are merged into target capability specs
- **AND** feature folder is moved `in-progress/ → done/`
- **AND** capability `## History` is updated with feature ID and date
- **AND** a single git commit is staged with message `sdd: archive <feature>`

#### Scenario: `faion sdd list`

- **GIVEN** any state in `.aidocs/`
- **WHEN** user runs `faion sdd list`
- **THEN** output is a table: feature ID, state, capabilities touched, REQ counts (added/modified/removed)

#### Scenario: `faion sdd lint <path>`

- **GIVEN** path is a spec or delta file (or directory)
- **WHEN** user runs `faion sdd lint <path>`
- **THEN** structural lint runs without REQ-ID resolution (faster than `validate`)
- **AND** exits 0 if all scenarios well-formed and REQ-IDs unique within the file

### REQ-049-005: Backwards compatibility

Existing features in `done/` and `in-progress/` (F048 and earlier) SHALL remain valid without migration.

#### Scenario: Old-format feature still works

- **GIVEN** F048 has only `spec.md` + `design.md` + `test-plan.md` (no delta)
- **WHEN** `faion sdd list` runs
- **THEN** F048 appears with state `done`, capabilities `(legacy)`, REQ counts `(n/a)`
- **AND** validate/lint do not error on legacy features

## Success Criteria

- [ ] `.aidocs/specs/sdd-lifecycle/spec.md`, `.aidocs/specs/sdd-cli/spec.md`, `.aidocs/specs/sdd-bdd/spec.md` exist after F049 archive
- [ ] `faion sdd validate feature-049-spec-deltas-bdd-cli` exits 0
- [ ] `faion sdd diff sdd-cli` shows the to-be-added requirements before archive
- [ ] `faion sdd archive feature-049-spec-deltas-bdd-cli` succeeds on a worktree
- [ ] AGENTS.md (root + `.aidocs/`) documents the new format
- [ ] CHANGELOG.md `## [Unreleased]` lists the feature
- [ ] All BDD scenarios in this spec have matching test cases in `test-plan.md`

## Risks

| Risk | Mitigation |
|------|------------|
| Conflicting deltas from parallel features | `archive` aborts if target spec changed since delta was written; user must rebase delta |
| Markdown-embedded BDD harder to parse than `.feature` | Use a strict regex grammar; provide `lint` to catch drift early |
| `faion-cli` Python codebase grows | Implement as separate `faion_cli/sdd/` module, not monolith additions |

## Open Questions

- Should delta IDs follow `REQ-<feature>-<n>` (current draft) or `REQ-<capability>-<n>`? Draft favors feature-scoped to avoid renumbering on merge; resolve in design.md.
- Auto-merge or PR-style review for delta → spec promotion? Default: explicit `archive` command, no auto.
