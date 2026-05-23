#!/usr/bin/env python3
"""Static check for Django service functions.

Inputs:
    path to `services.py` (or directory).

Checks per function:
    * keyword-only signature (no positional args, no **kwargs)
    * if function contains > 1 write (.save/.create/.update/.delete/.bulk_*),
      function body must contain `transaction.atomic()` usage
    * if function contains `.delay(` it must be inside `transaction.on_commit(`
    * function must not import from `rest_framework.exceptions` or raise `Http404`

Outputs: stdout PASS or violation list. Exit 0/1/2.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

WRITE_NAMES = {"save", "delete", "create", "update", "bulk_create", "bulk_update"}


def collect_calls(node: ast.AST) -> list[ast.Call]:
    return [n for n in ast.walk(node) if isinstance(n, ast.Call)]


def check_function(node: ast.FunctionDef) -> list[str]:
    errors: list[str] = []
    args = node.args
    if args.args:
        errors.append(f"{node.name}: positional args present — expected keyword-only")
    if args.kwarg:
        errors.append(f"{node.name}: **kwargs passthrough — expected explicit params")
    # writes
    writes = [
        c for c in collect_calls(node)
        if isinstance(c.func, ast.Attribute) and c.func.attr in WRITE_NAMES
    ]
    if len(writes) > 1:
        body_src = ast.unparse(node)
        if "transaction.atomic" not in body_src:
            errors.append(
                f"{node.name}: multi-model writes without transaction.atomic()"
            )
    # delay outside on_commit
    src = ast.unparse(node)
    if ".delay(" in src:
        # naive proximity check: every .delay must be inside an on_commit lambda
        # we look for `on_commit(lambda` followed somewhere by `.delay(` — sloppy but catches the common case
        if "transaction.on_commit" not in src:
            errors.append(f"{node.name}: .delay() without transaction.on_commit wrap")
    # forbidden imports / raises
    for sub in ast.walk(node):
        if isinstance(sub, ast.Raise) and isinstance(sub.exc, ast.Call):
            target = ast.unparse(sub.exc.func)
            if "rest_framework" in target or "Http404" in target:
                errors.append(f"{node.name}: raises HTTP/DRF exception — use domain exception")
    return errors


def check_file(path: Path) -> list[str]:
    if path.name != "services.py":
        return [f"{path}: services must live in services.py"]
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as e:
        return [f"{path}: syntax error: {e}"]
    errors: list[str] = []
    src = path.read_text()
    if "from rest_framework.exceptions" in src or "from django.http import Http404" in src:
        errors.append(f"{path}: imports HTTP/DRF exceptions — services must stay HTTP-agnostic")
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            errors.extend(f"{path}:{node.lineno}: {m}" for m in check_function(node))
    return errors


def iter_targets(target: Path):
    if target.is_file():
        yield target
        return
    yield from target.rglob("services.py")


def self_test() -> int:
    import tempfile
    good = """
from django.db import transaction
from core.exceptions import ValidationError
def order_create(*, user, items):
    if not items:
        raise ValidationError("empty")
    with transaction.atomic():
        order.full_clean()
        order.save()
        OrderItem.objects.bulk_create([])
        transaction.on_commit(lambda: notify_user.delay(order_id=order.id))
    return order
"""
    bad = """
from rest_framework.exceptions import ValidationError
def order_create(user, items, **kwargs):
    Order.objects.create()
    OrderItem.objects.bulk_create([])
    notify_user.delay(order_id=1)
    raise ValidationError("x")
"""
    with tempfile.TemporaryDirectory() as d:
        gp = Path(d) / "services.py"
        gp.write_text(good)
        assert check_file(gp) == [], check_file(gp)
        bp = Path(d) / "services.py"
        bp.write_text(bad)
        assert check_file(bp), "expected violations"
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
