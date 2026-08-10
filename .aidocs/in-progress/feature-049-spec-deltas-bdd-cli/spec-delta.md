# Spec Delta — feature-049-spec-deltas-bdd-cli

> Self-referential: this delta is the first artifact authored in the new format. After F049 archives, the merge engine writes the resulting capability specs to `.aidocs/specs/{sdd-lifecycle,sdd-cli,sdd-bdd}/spec.md`.

## Capability: sdd-lifecycle

### ADDED Requirements

#### REQ-sdd-lifecycle-001: Living capability specs

The system SHALL maintain `.aidocs/specs/<capability>/spec.md` per capability as the single source of truth for that capability's accepted state.

#### Scenario: Capability spec created on first archive

- **GIVEN** capability `<cap>` has no spec file
- **AND** an in-progress feature has a delta with `## Capability: <cap>` and `### ADDED Requirements`
- **WHEN** the feature is archived
- **THEN** `.aidocs/specs/<cap>/spec.md` is created with the added requirements and a `## History` entry

#### Scenario: Capability spec updated on subsequent archive

- **GIVEN** `.aidocs/specs/<cap>/spec.md` exists
- **AND** a feature delta MODIFIES one existing REQ and ADDS one new REQ
- **WHEN** the feature is archived
- **THEN** the existing REQ is replaced, the new REQ appended, and history gains an entry

#### REQ-sdd-lifecycle-002: Delta-based feature contributions

A feature folder MAY contain `spec-delta.md` declaring `ADDED`, `MODIFIED`, `REMOVED` requirements scoped per capability.

#### Scenario: Delta with multiple capabilities

- **GIVEN** a feature touches capabilities `A` and `B`
- **WHEN** the delta declares two `## Capability:` blocks
- **THEN** archive merges each block into its respective spec independently

#### Scenario: Conflict on stale delta

- **GIVEN** a delta was authored against `<cap>` `Last updated: 2026-05-01`
- **AND** the capability has since advanced to `Last updated: 2026-05-10`
- **WHEN** the user runs `faion sdd archive <feature>`
- **THEN** the command exits with code 2 and prints rebase instructions

#### REQ-sdd-lifecycle-003: Backwards compatibility for legacy features

Features authored before F049 SHALL remain valid without modification.

#### Scenario: Legacy feature passes list

- **GIVEN** a feature folder lacks `spec-delta.md`
- **WHEN** `faion sdd list` runs
- **THEN** the feature is listed with capability column `(legacy)` and no validation is attempted

## Capability: sdd-bdd

### ADDED Requirements

#### REQ-sdd-bdd-001: BDD scenario grammar

Every Requirement SHALL include at least one `#### Scenario:` block using the keyword set `{GIVEN, AND, WHEN, THEN}`.

#### Scenario: Valid scenario passes lint

- **GIVEN** a Requirement contains exactly one Scenario with one GIVEN, one WHEN, one THEN
- **WHEN** `faion sdd lint` runs on the file
- **THEN** lint exits 0

#### Scenario: Missing scenario fails lint

- **GIVEN** a Requirement has no Scenario block
- **WHEN** lint runs
- **THEN** lint exits 1 with message `<REQ-ID>: missing scenario`

#### REQ-sdd-bdd-002: Step keyword strictness

Scenario steps SHALL use only the four keywords `GIVEN`, `AND`, `WHEN`, `THEN` formatted as `- **<KEYWORD>** <text>`.

#### Scenario: Unknown keyword rejected

- **GIVEN** a step uses `WHENEVER`
- **WHEN** lint runs
- **THEN** lint reports the line with expected keyword set

#### Scenario: Valid AND continuation accepted

- **GIVEN** a step `- **AND** ...` follows a `GIVEN` or `WHEN`
- **WHEN** lint runs
- **THEN** lint exits 0

## Capability: sdd-cli

### ADDED Requirements

#### REQ-sdd-cli-001: `faion sdd validate <feature>`

Validate cross-file consistency: required files present, delta well-formed, REQ-IDs in MODIFIED/REMOVED resolve in target capability spec.

#### Scenario: Clean feature validates

- **GIVEN** feature has spec, design, test-plan, spec-delta, implementation-plan
- **AND** all MODIFIED REQ-IDs exist in target capability specs
- **WHEN** user runs `faion sdd validate <feature>`
- **THEN** exit code is 0 and a success summary is printed

#### Scenario: Missing capability spec for MODIFIED

- **GIVEN** delta MODIFIES `REQ-foo-001` but `.aidocs/specs/foo/spec.md` does not exist
- **WHEN** validate runs
- **THEN** exit code is 1 with message naming the missing capability

#### REQ-sdd-cli-002: `faion sdd lint <path>`

Single-file structural lint that does NOT resolve cross-file REQ-IDs.

#### Scenario: Lint a single delta

- **GIVEN** path points to `spec-delta.md`
- **WHEN** lint runs
- **THEN** the parser walks the file, reports any keyword/structure violations, and exits accordingly

#### REQ-sdd-cli-003: `faion sdd diff <capability>`

Print a unified diff showing the capability's spec before vs. after merging all in-progress deltas that touch it.

#### Scenario: Diff with one in-progress feature

- **GIVEN** capability `cap-x` has a current spec
- **AND** exactly one in-progress feature has a delta touching `cap-x`
- **WHEN** user runs `faion sdd diff cap-x`
- **THEN** unified diff is printed showing additions, modifications, removals

#### Scenario: Diff with no pending changes

- **GIVEN** no in-progress features touch `cap-x`
- **WHEN** diff runs
- **THEN** output is empty and exit code is 0

#### REQ-sdd-cli-004: `faion sdd archive <feature>`

Merge deltas into target capability specs, move the feature to `done/`, stage a single git commit.

#### Scenario: Successful archive

- **GIVEN** feature validates clean and has no delta conflicts
- **WHEN** user runs `faion sdd archive <feature>`
- **THEN** capability specs are updated, feature is moved to `done/`, history entry is appended, and `git status` shows a staged commit `sdd: archive <feature>`

#### Scenario: Dry run preview

- **GIVEN** the feature is valid
- **WHEN** user runs `faion sdd archive <feature> --dry-run`
- **THEN** no files are changed; the command prints the actions it would take

#### REQ-sdd-cli-005: `faion sdd list`

Tabular report of all features across `backlog/`, `todo/`, `in-progress/`, `done/` with capabilities and REQ counts.

#### Scenario: List shows new and legacy features

- **GIVEN** `done/` contains a mix of legacy features and new-format features
- **WHEN** user runs `faion sdd list`
- **THEN** output is a table with columns: `id`, `state`, `capabilities`, `+/~/-` counts; legacy features show `(legacy)` and `n/a`
