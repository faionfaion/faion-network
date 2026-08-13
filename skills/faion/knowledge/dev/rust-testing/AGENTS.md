# Rust Testing

## Summary

**One-sentence:** Configures Rust's three test layers (inline `#[cfg(test)]` unit, `tests/*.rs` integration, `///` doctests) plus cargo-llvm-cov coverage gate and a proptest budget.

**One-paragraph:** Rust testing has three orthogonal layers and most projects use only one. Unit tests inside `#[cfg(test)] mod tests` cover private functions cheaply. Integration tests in `tests/` exercise the public API like a downstream consumer. Doctests verify documented examples still compile and pass. This methodology forces all three to be present (gated by `cargo test --doc` + `cargo test --tests` in CI), wires `cargo-llvm-cov` for branch coverage with diff-cover on PR (target ≥85% on changed lines), reserves `proptest` for invariants on data structures and parsers, and forbids `.unwrap()` outside `#[cfg(test)]` (paired with [[rust-error-handling]]).

**Ефективно для:**

- Нова Rust бібліотека: doctests документуються та валідуються одночасно.
- Парсери, кодеки, structures: proptest з shrinking ловить edge cases unit-tests пропускають.
- Refactor публічного API: integration tests у `tests/` ловлять breaking change.
- Switching mock framework: built-in `#[cfg(test)]` модуль + `mockall` крихітніший за external test harnesses.

## Applies If (ALL must hold)

- Rust crate with `Cargo.toml`.
- Public API or invariant-rich data structures present (anything beyond hello-world).
- CI runs on every PR and can execute `cargo test --all-targets`.

## Skip If (ANY kills it)

- Build scripts and procedural macros — different testing harness; out of scope.
- `#![no_std]` with limited test infrastructure (use `defmt-test` or `embedded-test` instead).
- Spike code or experiment branches where coverage gate slows iteration.
- Pure binary crate with no library extract — integration tests less applicable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `Cargo.toml` | TOML | crate root |
| CI workflow | YAML | `.github/workflows/` |
| Critical-path manifest | path list | `Cargo.toml [package.metadata.faion]` or AGENTS.md |
| Coverage tool | binary | `cargo install cargo-llvm-cov` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-error-handling]] | Tests are allowed to `.unwrap()`; non-test code is not — clippy gate config shared. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: three-layers-mandatory, llvm-cov-gate, doctest-not-rustdoc-only, proptest-on-parsers, no-test-in-pub-namespace, integration-tests-folder | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for test-strategy config + coverage gate | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: only-unit-tests, doctest-without-runs, proptest-no-shrink, shared-mutable-state-tests | 700 |
| `content/04-procedure.xml` | essential | 5-step setup: detect crate type → install llvm-cov → wire CI → add doctests → set proptest budget | 700 |
| `content/06-decision-tree.xml` | essential | Routing: feature type → unit/integration/doctest/proptest mix | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_crate_layout` | haiku | `cargo metadata` parse. |
| `propose_test_layer` | sonnet | Decide which layer per feature. |
| `write_doctest` | sonnet | Tied to documentation prose. |
| `proptest_strategy_design` | opus | Invariant identification is cross-cutting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rust-coverage-gate.sh` | CI script running `cargo llvm-cov` + diff-cover against base branch |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing.py` | Validate test-strategy config JSON against schema | After config generation |

## Related

- [[rust-error-handling]] — test code escapes the `.unwrap()` gate via `#[cfg(test)]`.
- [[code-coverage]] — language-agnostic coverage discipline; this methodology specialises to Rust.

## Decision tree

See `content/06-decision-tree.xml`. Branches on test scope: private invariant → unit; public API behavior → integration; documentation example → doctest; data-structure / parser invariant → proptest. All leaves reference rules from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rust-coverage-gate.sh`

```bash
#!/usr/bin/env bash
# rust-coverage-gate.sh — enforce line + branch coverage thresholds.
# Usage: rust-coverage-gate.sh LINE_PCT BRANCH_PCT
# Example: rust-coverage-gate.sh 70 60
set -euo pipefail
LINE="${1:-70}"
BRANCH="${2:-60}"

cargo llvm-cov --workspace --lcov --output-path lcov.info >/dev/null

python3 - "$LINE" "$BRANCH" <<'PY'
import re, sys
line_t, branch_t = float(sys.argv[1]), float(sys.argv[2])
with open("lcov.info") as f:
    data = f.read()
lf = sum(int(x) for x in re.findall(r"^LF:(\d+)", data, re.M))
lh = sum(int(x) for x in re.findall(r"^LH:(\d+)", data, re.M))
bf = sum(int(x) for x in re.findall(r"^BRF:(\d+)", data, re.M))
bh = sum(int(x) for x in re.findall(r"^BRH:(\d+)", data, re.M))
line = (lh / lf * 100) if lf else 100.0
branch = (bh / bf * 100) if bf else 100.0
print(f"line={line:.1f}% branch={branch:.1f}%")
fails = []
if line < line_t:   fails.append(f"line {line:.1f}% < {line_t}%")
if branch < branch_t: fails.append(f"branch {branch:.1f}% < {branch_t}%")
if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)
print("OK")
PY
```
