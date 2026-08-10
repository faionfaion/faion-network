# Feature 049 — Test Plan

Tests live in `tools/faion-cli/tests/sdd/`. Pytest, no async, golden-file fixtures.

## Test Structure

```
tests/sdd/
├── conftest.py                       # tmp_path-based .aidocs builder
├── fixtures/
│   ├── valid-feature/                # known-good delta + capability spec
│   ├── legacy-feature/               # pre-F049 layout
│   ├── conflict-feature/             # stale Last-updated
│   └── malformed-bdd/                # bad keywords
├── test_parser.py
├── test_linter.py
├── test_validator.py
├── test_differ.py
├── test_archiver.py
├── test_lister.py
└── test_cli.py                        # end-to-end via `runner.invoke`
```

## Coverage Per Requirement

### REQ-sdd-lifecycle-001 — living capability specs

| Test | Source scenario |
|------|-----------------|
| `test_archiver::test_creates_capability_spec_on_first_archive` | "Capability spec created on first archive" |
| `test_archiver::test_updates_existing_capability_spec` | "Capability spec updated on subsequent archive" |
| `test_archiver::test_history_section_appended` | (derived) |

### REQ-sdd-lifecycle-002 — delta-based contributions

| Test | Source scenario |
|------|-----------------|
| `test_archiver::test_multi_capability_delta_merges_independently` | "Delta with multiple capabilities" |
| `test_archiver::test_stale_delta_aborts_with_exit_2` | "Conflict on stale delta" |

### REQ-sdd-lifecycle-003 — backwards compat

| Test | Source scenario |
|------|-----------------|
| `test_lister::test_legacy_feature_listed_as_legacy` | "Legacy feature passes list" |
| `test_validator::test_legacy_feature_skips_validation` | (derived) |

### REQ-sdd-bdd-001 — scenario required

| Test | Source scenario |
|------|-----------------|
| `test_linter::test_valid_scenario_passes` | "Valid scenario passes lint" |
| `test_linter::test_missing_scenario_fails` | "Missing scenario fails lint" |

### REQ-sdd-bdd-002 — keyword strictness

| Test | Source scenario |
|------|-----------------|
| `test_linter::test_unknown_keyword_rejected` | "Unknown keyword rejected" |
| `test_linter::test_and_continuation_accepted` | "Valid AND continuation accepted" |

### REQ-sdd-cli-001 — validate

| Test | Source scenario |
|------|-----------------|
| `test_cli::test_validate_clean_feature_exit_0` | "Clean feature validates" |
| `test_cli::test_validate_missing_capability_exit_1` | "Missing capability spec for MODIFIED" |

### REQ-sdd-cli-002 — lint

| Test | Source scenario |
|------|-----------------|
| `test_cli::test_lint_single_delta` | "Lint a single delta" |

### REQ-sdd-cli-003 — diff

| Test | Source scenario |
|------|-----------------|
| `test_cli::test_diff_shows_pending_merge` | "Diff with one in-progress feature" |
| `test_cli::test_diff_empty_when_no_pending` | "Diff with no pending changes" |

### REQ-sdd-cli-004 — archive

| Test | Source scenario |
|------|-----------------|
| `test_cli::test_archive_full_flow` | "Successful archive" |
| `test_cli::test_archive_dry_run_no_changes` | "Dry run preview" |

### REQ-sdd-cli-005 — list

| Test | Source scenario |
|------|-----------------|
| `test_cli::test_list_mixed_legacy_and_new` | "List shows new and legacy features" |

## Manual / Acceptance Tests

1. **Self-validation:** `faion sdd validate feature-049-spec-deltas-bdd-cli` → exit 0
2. **Self-archive (dry run):** `faion sdd archive feature-049-spec-deltas-bdd-cli --dry-run` → prints planned merges into `sdd-lifecycle`, `sdd-bdd`, `sdd-cli` capability specs
3. **Self-archive (real):** archive the feature, verify three capability spec files appear and contain the requirements declared in `spec-delta.md`
4. **Round-trip:** create a small F050 stub delta that MODIFIES `REQ-sdd-cli-005`, run validate → exit 0, run archive → spec updated, history shows two entries

## Performance Targets

- `validate` on a single feature: < 200ms
- `list` over `.aidocs/` with 100 features: < 500ms
- `diff` for one capability: < 100ms

## Out-of-Scope for Tests

- Git commit signing
- Concurrent archive across multiple terminals
- Migrating legacy `done/feature-*/spec.md` content
