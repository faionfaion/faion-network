# Mocking Strategies

## Summary

**One-sentence:** Produces a mocking-spec (per-dependency double type + boundary + tool) for a Python/JS/Go test suite, plus an over-mock lint report.

**One-paragraph:** Over-mocking is a silent suite killer: tests pass but production breaks because the mocked contract drifts. Under-mocking makes tests slow and non-deterministic. This methodology classifies every collaborator into a test-double type (Dummy/Stub/Spy/Mock/Fake), pins the mocking boundary (I/O, time, randomness, externals), prescribes autospec/spec discipline, and runs an over-mock lint pass against the existing suite.

**Ефективно для:** team whose Python/JS suite has accumulated MagicMock() noise and whose typo bugs slip past tests because mocks silently absorb attribute errors.

## Applies If (ALL must hold)

- Deciding whether to mock a dependency or use a real one.
- Writing Python mocks with unittest.mock / pytest-mock.
- Writing JavaScript mocks with Vitest vi.mock or Jest.
- Writing Go mocks via interface substitution or mockery.
- Auditing an existing suite for over-mocking.

## Skip If (ANY kills it)

- E2E tests where no mocking is desired → e2e-testing.
- Database isolation (use real DB with rollback) → integration-testing.
- Pure fixture design without mocking concerns → test-fixtures.
- Throwaway script with no test suite.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `dependency-graph.yaml` | list of {dep_name, boundary, mutability, third_party} | operator |
| `language` | python / typescript / go | repo |
| `runner` | pytest / vitest / jest / go-test | repo |
| `existing_test_dir` | path | repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[testing-pytest]] or [[testing-javascript]] | Runner-specific scoping. |
| [[test-fixtures]] | Fake objects are a fixture-design problem. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: mock at boundaries, autospec mandatory, patch where used, no mocking what you don't own, vi.clearAllMocks each test, time mock via freezegun, prefer Fake to Mock for stateful deps. | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the mocking-spec artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: MagicMock no spec, wrong-target patch, mocking value objects, missing clearAllMocks, mocking own code. | ~800 |
| `content/04-procedure.xml` | recommended | 5-step procedure: enumerate deps → classify boundary → pick double → emit spec → lint suite. | ~700 |
| `content/05-examples.xml` | recommended | Python autospec example + Vitest module mock + Go interface mock end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks Stub vs Mock vs Fake; full vs partial; mock vs leave-real. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_dependency_graph` | haiku | Mechanical YAML→typed list. |
| `classify_doubles` | sonnet | Tradeoff between stub simplicity and fake fidelity. |
| `audit_over_mocking` | opus | Cross-suite pattern detection — needs synthesis. |
| `emit_mocking_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/over-mock-lint.py` | Script detecting over-mocked Python test files. |
| `templates/mocking-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/mocking-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/mocking-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.yaml` | Minimum dependency graph (one HTTP client, one time call). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[testing-pytest]]
- [[integration-testing]]
- [[test-fixtures]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `is_own_code` (yes → leave real; no → continue), then on `is_io_or_time_or_random` (yes → mock at boundary; no → fake/stub by state), then on `verify_calls_needed` (yes → Mock with autospec; no → Stub/Fake). Each leaf cites a rule id.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/over-mock-lint.py`

```python
"""
over-mock-lint.py — detect over-mocked test files in a Python project.

A test file is considered "over-mocked" when the ratio of mock/patch calls
to assertions is too high, or when internal modules (not third-party) are mocked.

Usage:
    python over-mock-lint.py tests/
    python over-mock-lint.py tests/ --threshold 3 --own-package myapp

Exit codes:
    0 — no issues found
    1 — one or more files exceed the mock:assert ratio threshold
"""
import argparse
import ast
import sys
from pathlib import Path


MOCK_NAMES = {"Mock", "MagicMock", "patch", "mocker.patch", "create_autospec", "AsyncMock"}


def count_mocks(tree: ast.AST) -> int:
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Direct calls: Mock(), MagicMock()
            if isinstance(node.func, ast.Name) and node.func.id in MOCK_NAMES:
                count += 1
            # Attribute calls: mocker.patch(), unittest.mock.patch()
            elif isinstance(node.func, ast.Attribute) and node.func.attr in {"patch", "patch_object", "patch_dict"}:
                count += 1
    return count


def count_asserts(tree: ast.AST) -> int:
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            count += 1
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr.startswith("assert_"):
                count += 1
    return count


def analyze_file(path: Path, threshold: int, own_package: str | None) -> list[str]:
    issues = []
    try:
        source = path.read_text()
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return []

    mocks = count_mocks(tree)
    asserts = count_asserts(tree)

    if asserts == 0 and mocks > 0:
        issues.append(f"{path}: {mocks} mocks, 0 assertions — tests may be vacuous")
    elif asserts > 0 and (mocks / asserts) > threshold:
        issues.append(
            f"{path}: mock:assert ratio {mocks}/{asserts} = {mocks/asserts:.1f} "
            f"(threshold {threshold}) — possible over-mocking"
        )

    if own_package:
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Look for mocker.patch("myapp.internal.something")
                if isinstance(node.func, ast.Attribute) and node.func.attr == "patch":
                    if node.args and isinstance(node.args[0], ast.Constant):
                        target = node.args[0].value
                        if isinstance(target, str) and target.startswith(own_package):
                            # Internal patch — potentially over-mocking own code
                            parts = target.split(".")
                            if len(parts) > 3:  # deep internal path
                                issues.append(
                                    f"{path}:{node.lineno}: patching internal "
                                    f"'{target}' — consider using a real or fake implementation"
                                )

    return issues


def main():
    parser = argparse.ArgumentParser(description="Detect over-mocked test files")
    parser.add_argument("paths", nargs="+", type=Path, help="Test directories or files")
    parser.add_argument("--threshold", type=float, default=3.0,
                        help="Max mock:assert ratio before warning (default: 3.0)")
    parser.add_argument("--own-package", default=None,
                        help="Your package name to detect internal mocking (e.g. myapp)")
    args = parser.parse_args()

    all_issues: list[str] = []
    for path in args.paths:
        if path.is_file():
            files = [path]
        else:
            files = list(path.rglob("test_*.py")) + list(path.rglob("*_test.py"))

        for f in files:
            all_issues.extend(analyze_file(f, args.threshold, args.own_package))

    if all_issues:
        print("over-mock-lint: issues found\n")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("over-mock-lint: no issues found")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

### `templates/_smoke-test.yaml`

```yaml
language: python
runner: pytest

dependencies:
  - {dep_name: requests.post, boundary: io-network, mutability: stateless, third_party: true, reuse_count: 2}
  - {dep_name: datetime.now, boundary: time, mutability: stateless, third_party: true, reuse_count: 4}
  - {dep_name: UserRepository, boundary: own-code, mutability: stateful, third_party: false, reuse_count: 5}

drivers:
  is_own_code: false
  is_io_or_time_or_random: true
  verify_calls_needed: true
  stateful_reuse_count: 5
```
