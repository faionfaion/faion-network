# Feature 049 — Design

## Architecture Overview

```
faion-cli (Python)
└── faion_cli/sdd/
    ├── __init__.py
    ├── cli.py                  # Click/Typer entrypoint: faion sdd ...
    ├── parser.py               # Markdown → AST (capabilities, requirements, scenarios)
    ├── delta.py                # Delta document model + merge engine
    ├── validator.py            # Cross-file validation (REQ-ID refs, capability targets)
    ├── linter.py               # Single-file structural lint
    ├── archiver.py             # archive command: merge + move + git
    ├── differ.py               # diff command: simulated post-merge view
    ├── lister.py               # list command: tabular state report
    └── grammar.py              # BDD keyword sets, regex constants

.aidocs/
├── specs/                      # NEW: living capability specs
│   └── <capability>/
│       └── spec.md             # current state of capability
├── backlog/                    # unchanged
├── todo/                       # unchanged
├── in-progress/                # unchanged
│   └── feature-NNN-<slug>/
│       ├── spec.md             # feature-level requirements (unchanged role)
│       ├── spec-delta.md       # NEW: capability deltas
│       ├── design.md           # unchanged
│       ├── test-plan.md        # unchanged (BDD references mirror spec scenarios)
│       └── implementation-plan.md
└── done/                       # unchanged location, but archived features keep spec-delta.md
```

## Document Models

### Capability spec (`.aidocs/specs/<cap>/spec.md`)

```markdown
# Capability: <cap>

**Status:** active
**Last updated:** YYYY-MM-DD by feature-NNN

## Purpose

<one paragraph>

## Requirements

### REQ-<cap>-001: <title>

<requirement body>

#### Scenario: <name>
- **GIVEN** ...
- **WHEN** ...
- **THEN** ...

### REQ-<cap>-002: ...

## History

- 2026-05-02 — feature-049-spec-deltas-bdd-cli — added REQ-001..005
- 2026-05-15 — feature-051-foo — modified REQ-002, added REQ-006
```

REQ-IDs are **capability-scoped** (`REQ-<cap>-NNN`), not feature-scoped. Decision rationale:
- Capability-scoped IDs survive across features and remain stable in cross-references.
- Renumbering risk addressed by allocator: `archive` reserves IDs in lock file `.aidocs/specs/<cap>/.next-id`.

### Spec-delta (`spec-delta.md`)

```markdown
# Spec Delta — feature-NNN

## Capability: <cap>

### ADDED Requirements

#### REQ-<cap>-NNN: <title>

<body + scenarios>

### MODIFIED Requirements

#### REQ-<cap>-MMM: <title>

<full new body — replaces existing entry; changelog notes optional>

### REMOVED Requirements

- REQ-<cap>-XXX (reason: superseded by REQ-<cap>-NNN)

## Capability: <other-cap>

...
```

A delta MAY target multiple capabilities. Each `## Capability:` block resolves to one merge target.

## Parser

Markdown-only, no YAML frontmatter on requirements. Parser uses `markdown-it-py` AST, then walks for:

- `h1` → document title
- `h2` matching `^Capability: (.+)$` → capability scope
- `h3` matching `^(ADDED|MODIFIED|REMOVED) Requirements$` → operation
- `h4` matching `^REQ-([a-z0-9-]+)-(\d{3}): (.+)$` → requirement
- `h4` matching `^Scenario: (.+)$` → scenario, child of preceding requirement
- list items matching `^- \*\*(GIVEN|AND|WHEN|THEN)\*\* (.+)$` → scenario step

Strict mode: any unrecognized `h2/h3/h4` near a Requirement is a lint error.

## Merge Engine (`delta.py` + `archiver.py`)

```
def merge(capability_spec, deltas):
    for delta in deltas:
        for req in delta.added:
            if req.id in capability_spec.requirements:
                raise Conflict(f"ADDED {req.id} already exists")
            capability_spec.add(req)
        for req in delta.modified:
            if req.id not in capability_spec.requirements:
                raise Conflict(f"MODIFIED {req.id} not found")
            capability_spec.replace(req)
        for req_id in delta.removed:
            capability_spec.remove(req_id)
    capability_spec.append_history(delta.feature_id, today())
    return capability_spec
```

### Concurrency / rebase

Deltas reference the capability `Last updated` line they were authored against. If `archive` finds the capability has a newer `Last updated` than the delta declares, it aborts with rebase instructions: re-read current spec, regenerate REQ-IDs from the lock file, update `MODIFIED` blocks to match current text.

## CLI Surface (Typer)

```python
@app.command()
def validate(feature: str): ...
@app.command()
def lint(path: Path): ...
@app.command()
def diff(capability: str): ...
@app.command("list")
def list_features(): ...
@app.command()
def archive(feature: str, dry_run: bool = False): ...
```

Exit codes:
- 0 — success
- 1 — lint/validation failure
- 2 — conflict / rebase needed
- 3 — IO / git error

## File Locations

| Item | Path |
|------|------|
| CLI module | `tools/faion-cli/faion_cli/sdd/` |
| Tests | `tools/faion-cli/tests/sdd/` |
| Capability specs | `.aidocs/specs/<cap>/spec.md` |
| ID lock files | `.aidocs/specs/<cap>/.next-id` |
| Migration doc | `.aidocs/conventions/spec-deltas.md` |
| AGENTS update | `.aidocs/AGENTS.md` |
| Root AGENTS update | `~/workspace/projects/faion-net/faion-network/AGENTS.md` |

## Dependencies

- `typer` (already in faion-cli)
- `markdown-it-py` (NEW — small, MIT)
- `rich` (already in faion-cli) for `list` table output
- No async, no DB, no network — pure file I/O + git via `subprocess`

## Migration Strategy

1. F049 itself uses the new format — exercises the toolchain end-to-end.
2. After F049 ships, `.aidocs/conventions/spec-deltas.md` documents the format and links from root AGENTS.md.
3. Old features in `done/` are NOT migrated. `faion sdd list` shows them as legacy.
4. Future features (F050+) author `spec-delta.md` alongside `spec.md`. The feature-level `spec.md` stays as the human-readable proposal narrative; `spec-delta.md` is the machine-mergeable artifact.

## Trade-offs

| Choice | Alternative | Why chosen |
|--------|-------------|------------|
| Markdown-embedded BDD | Separate `.feature` Gherkin files | Keeps SDD docs single-file readable; lint can still enforce grammar |
| Capability-scoped REQ-IDs | Feature-scoped | Stable cross-references, predictable history |
| Explicit `archive` command | Auto-merge on `done/` move | Reviewability; conflict detection |
| Living specs in `.aidocs/specs/` | Living specs in `.product/specs/` | `.aidocs/` is workspace-level; `.product/` is per-project — capabilities here are workspace-wide |
| Pure Python CLI | Bash script wrapping markdown | Testability, maintainability, error messages |
