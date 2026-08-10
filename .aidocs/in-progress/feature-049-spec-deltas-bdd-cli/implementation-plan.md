# Feature 049 — Implementation Plan

## Wave Structure

Four waves, each independently mergeable. Token estimates per task. No time estimates.

---

## Wave 1 — Parser & Grammar (foundation)

Goal: turn Markdown delta/spec files into an AST we can reason about. No CLI yet.

| Task | Description | Est. tokens | Depends on |
|------|-------------|-------------|------------|
| T-049-001 | Add `markdown-it-py` to `tools/faion-cli/pyproject.toml`; create `faion_cli/sdd/__init__.py` skeleton | ~3k | — |
| T-049-002 | Implement `grammar.py`: keyword sets, regex constants for headings, REQ-IDs, scenario steps | ~6k | T-049-001 |
| T-049-003 | Implement `parser.py`: walk markdown-it tokens → typed dataclasses (`Capability`, `Requirement`, `Scenario`, `Step`) | ~12k | T-049-002 |
| T-049-004 | Tests for parser: golden fixtures in `tests/sdd/fixtures/`, parametrized cases | ~10k | T-049-003 |

**Wave 1 exit:** parser ingests F049's own `spec-delta.md` without errors, dataclass roundtrip stable.

---

## Wave 2 — Linter & Validator

Goal: catch malformed deltas and cross-file inconsistencies.

| Task | Description | Est. tokens | Depends on |
|------|-------------|-------------|------------|
| T-049-005 | Implement `linter.py`: structural checks per REQ-sdd-bdd-001/002 — missing scenarios, bad keywords, duplicate REQ-IDs | ~8k | T-049-003 |
| T-049-006 | Implement `validator.py`: cross-file REQ-ID resolution against `.aidocs/specs/` capability specs | ~10k | T-049-005 |
| T-049-007 | Tests for linter and validator covering all REQ-sdd-bdd and REQ-sdd-cli-001/002 scenarios | ~12k | T-049-006 |

**Wave 2 exit:** `linter.lint(path)` and `validator.validate(feature)` work programmatically; tests green.

---

## Wave 3 — CLI Surface

Goal: expose Wave 1+2 plus diff/archive/list via `faion sdd ...`.

| Task | Description | Est. tokens | Depends on |
|------|-------------|-------------|------------|
| T-049-008 | Implement `cli.py` Typer app: register `sdd` group, wire `validate` and `lint` subcommands | ~5k | T-049-006 |
| T-049-009 | Implement `differ.py` + wire `diff` subcommand: simulate merge, emit unified diff via `difflib` | ~8k | T-049-008 |
| T-049-010 | Implement `lister.py` + wire `list` subcommand: walk `.aidocs/` states, render Rich table, detect legacy features | ~7k | T-049-008 |
| T-049-011 | Implement `archiver.py` + wire `archive` subcommand (with `--dry-run`): merge, move dirs, append history, stage git commit | ~14k | T-049-009 |
| T-049-012 | End-to-end CLI tests via Typer's `CliRunner` covering all REQ-sdd-cli scenarios | ~12k | T-049-011 |

**Wave 3 exit:** `faion sdd --help` shows five subcommands; all CLI tests green.

---

## Wave 4 — Self-archive & Documentation

Goal: F049 dogfoods its own toolchain, docs are updated.

| Task | Description | Est. tokens | Depends on |
|------|-------------|-------------|------------|
| T-049-013 | Run `faion sdd validate feature-049-spec-deltas-bdd-cli` → fix any issues until exit 0 | ~3k | T-049-011 |
| T-049-014 | Run `faion sdd archive feature-049-spec-deltas-bdd-cli --dry-run`, inspect output | ~2k | T-049-013 |
| T-049-015 | Write `.aidocs/conventions/spec-deltas.md` — format reference, examples, rebase recipe | ~6k | T-049-013 |
| T-049-016 | Update `.aidocs/AGENTS.md` and root `AGENTS.md` to reference new format and CLI | ~4k | T-049-015 |
| T-049-017 | CHANGELOG.md `## [Unreleased]` entry; commit per granular-commits feedback | ~1k | T-049-016 |
| T-049-018 | Real archive: `faion sdd archive feature-049-spec-deltas-bdd-cli` → verify capability specs created at `.aidocs/specs/{sdd-lifecycle,sdd-bdd,sdd-cli}/spec.md` | ~3k | T-049-016 |

**Wave 4 exit:** F049 in `done/`, capability specs live, docs reference them.

---

## Dependencies Diagram

```
W1 (parser)
  ↓
W2 (linter, validator)
  ↓
W3 (cli: validate, lint, diff, list, archive)
  ↓
W4 (self-archive + docs)
```

Within each wave, tasks marked with the same prerequisite can run in parallel.

## Total Estimate

~126k tokens across 18 tasks. Complexity: **Medium** — well-bounded, no networked dependencies, deterministic file I/O.

## Open Questions Tracked

1. **REQ-ID allocator implementation** — lock file vs. parsing existing IDs at archive time. Resolve in T-049-011 design pass.
2. **Git author/committer** — use repo default; do not skip hooks. Pre-commit hook will require CHANGELOG.md update (T-049-017 covers this).
3. **Should `archive` push to remote?** No. User runs `git push` manually after reviewing the staged commit.

## Success Definition

- All 18 tasks `done`
- Test suite green (`pytest tools/faion-cli/tests/sdd/`)
- F049 archived using its own CLI
- `.aidocs/specs/sdd-lifecycle/spec.md`, `.aidocs/specs/sdd-bdd/spec.md`, `.aidocs/specs/sdd-cli/spec.md` exist with correct content
- Docs updated; CHANGELOG entry committed; no `--no-verify` used
