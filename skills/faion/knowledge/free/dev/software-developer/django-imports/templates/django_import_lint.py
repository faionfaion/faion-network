#!/usr/bin/env python3
# django_import_lint.py — flag cross-app imports without alias and wildcard imports.
# Usage: python django_import_lint.py path/to/repo
# Exits 1 if violations found. Wire into pre-commit and CI.
import ast
import pathlib
import sys

BAD: list[tuple[str, int, str]] = []


def check(path: pathlib.Path) -> None:
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        mod = node.module or ""
        # Cross-app: from apps.<other>.<module> import X (direct symbol import)
        if mod.startswith("apps.") and mod.count(".") >= 2:
            tail = mod.split(".", 2)[2]
            if tail in {"models", "services", "constants", "serializers"}:
                app = mod.split(".")[1]
                BAD.append((
                    str(path),
                    node.lineno,
                    f"use `from apps.{app} import {tail} as {app}_{tail}` "
                    f"instead of `from {mod} import ...`",
                ))
        # Wildcard imports
        for alias in node.names:
            if alias.name == "*":
                BAD.append((str(path), node.lineno, "wildcard import banned"))


root = pathlib.Path(sys.argv[1])
for py in root.rglob("*.py"):
    if "/migrations/" in str(py) or "/.venv/" in str(py) or "/node_modules/" in str(py):
        continue
    check(py)

for f, ln, msg in BAD:
    print(f"{f}:{ln}: {msg}")

sys.exit(1 if BAD else 0)
