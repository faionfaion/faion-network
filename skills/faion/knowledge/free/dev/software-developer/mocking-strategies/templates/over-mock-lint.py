#!/usr/bin/env python3
# purpose: lint script — flags test functions with >5 lines of mock setup.
# consumes: pytest test files via Path arguments.
# produces: stderr report; exit 1 on findings.
# depends-on: stdlib only (ast).
# token-budget-impact: 0 — pre-commit script.
"""
Over-mock detector: flags test functions with too many assert_called* calls.
Input:  tests/ directory (recursive scan of test_*.py files)
Output: stdout listing offenders; exits 1 if any found
Usage:  python over-mock-lint.py [threshold]
"""
import ast
import pathlib
import sys

THRESHOLD = int(sys.argv[1]) if len(sys.argv) > 1 else 4
issues = 0

for path in pathlib.Path("tests").rglob("test_*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            asserts = sum(
                1
                for child in ast.walk(node)
                if isinstance(child, ast.Attribute)
                and child.attr.startswith("assert_called")
            )
            if asserts > THRESHOLD:
                print(
                    f"{path}:{node.lineno} {node.name} "
                    f"has {asserts} call assertions (threshold {THRESHOLD})"
                )
                issues += 1

sys.exit(1 if issues else 0)
