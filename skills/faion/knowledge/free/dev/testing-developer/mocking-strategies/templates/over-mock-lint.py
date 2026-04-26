#!/usr/bin/env python3
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
