#!/usr/bin/env python3
# purpose: AST lint rejecting bare cross-app symbol imports and wildcard imports.
# consumes: a repo root path; the apps/<app>/<module> layout from the imports spec.
# produces: one violation line per offence on stdout; exit 1 when any is found.
# depends-on: content/01-core-rules.xml rules r4-alias-convention and r11-no-star-imports.
# token-budget-impact: zero — local-only template; pre-commit time is the only cost.

# django_import_lint.py — flag cross-app imports without an alias, and wildcard imports.
# Usage: python django_import_lint.py path/to/repo
# Exits 1 if violations are found. Wire into pre-commit and CI.
# This is the rule ruff cannot express: ruff sorts imports, it does not know that
# `from apps.users.models import User` is the shape that shadows a name.
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
            if tail in {"models", "services", "selectors", "constants", "serializers"}:
                app = mod.split(".")[1]
                BAD.append((
                    str(path),
                    node.lineno,
                    f"use `from apps.{app} import {tail} as {app}_{tail}` "
                    f"instead of `from {mod} import ...`",
                ))
        # Multi-dot relative imports
        if node.level and node.level > 1:
            BAD.append((str(path), node.lineno,
                        "multi-dot relative import banned; use the absolute apps.<app> path"))
        # Wildcard imports
        for alias in node.names:
            if alias.name == "*":
                BAD.append((str(path), node.lineno, "wildcard import banned"))


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print(__doc__ or "usage: django_import_lint.py <repo-root>")
        return 0 if argv[1:2] in ([], ["-h"], ["--help"]) else 2
    root = pathlib.Path(argv[1])
    for py in root.rglob("*.py"):
        s = str(py)
        if "/migrations/" in s or "/.venv/" in s or "/node_modules/" in s:
            continue
        check(py)
    for f, ln, msg in BAD:
        print(f"{f}:{ln}: {msg}")
    return 1 if BAD else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
