#!/usr/bin/env python3
"""Static check for Django selector functions.

Inputs:
    path to a `selectors.py` module (or directory containing such files).

Checks:
    * every top-level function uses keyword-only args (signature contains `*`)
    * return-type annotation is `QuerySet[...]` or a single class name
    * function body contains no obvious write operation (.save, .update,
      .create, .delete, .delay) — covers rule r4
    * file path ends with `selectors.py` (otherwise the selector belongs
      somewhere else)

Outputs:
    stdout: PASS or per-violation list.
    exit 0 on pass, 1 on any violation, 2 on bad CLI.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

WRITE_TOKENS = ("save", "update", "create", "bulk_create", "bulk_update", "delete", "delay", "apply_async")


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    if path.name != "selectors.py":
        errors.append(f"{path}: selectors must live in selectors.py")
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as e:
        return [f"{path}: syntax error: {e}"]
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        # kwarg-only: args.args must be empty (everything after *)
        if node.args.args:
            errors.append(f"{path}:{node.lineno}: {node.name} uses positional args; expected keyword-only")
        # return annotation present
        if node.returns is None:
            errors.append(f"{path}:{node.lineno}: {node.name} missing return type annotation")
        else:
            annotation = ast.unparse(node.returns)
            if "QuerySet" not in annotation and not annotation[:1].isupper():
                errors.append(
                    f"{path}:{node.lineno}: {node.name} return type {annotation!r} not QuerySet[...] or a Model"
                )
        # forbid write tokens
        for sub in ast.walk(node):
            if isinstance(sub, ast.Attribute) and sub.attr in WRITE_TOKENS:
                # tolerate `.save` on non-DB objects is rare in selectors; flag for review
                errors.append(
                    f"{path}:{sub.lineno}: {node.name} contains write-like call '.{sub.attr}' — move to services.py"
                )
                break
    return errors


def iter_targets(target: Path):
    if target.is_file():
        yield target
        return
    yield from target.rglob("selectors.py")


def self_test() -> int:
    import tempfile
    good = """
from django.db.models import QuerySet
def order_list(*, user) -> QuerySet:
    return None  # placeholder
"""
    bad = """
def order_list(user):
    Order.objects.filter(user=user).update(status='x')
    return list(Order.objects.all())
"""
    with tempfile.TemporaryDirectory() as d:
        gp = Path(d) / "selectors.py"
        gp.write_text(good)
        assert check_file(gp) == [], check_file(gp)
        bp = Path(d) / "selectors.py"
        bp.write_text(bad)
        assert check_file(bp), "expected violations on positional + update"
    sys.stdout.write("self-test: PASS\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.path:
        parser.print_usage()
        return 2
    target = Path(args.path)
    if not target.exists():
        sys.stderr.write(f"not found: {target}\n")
        return 1
    all_errors: list[str] = []
    for f in iter_targets(target):
        all_errors.extend(check_file(f))
    if all_errors:
        sys.stdout.write("FAIL\n")
        for e in all_errors:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
