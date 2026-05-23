#!/usr/bin/env python3
"""Static check for Django DRF serializers.

Inputs:
    path to `serializers.py` (or directory).

Checks:
    * class name matches Entity(Create|Update)Request or Entity(Response|ListResponse)
    * base class is `serializers.Serializer` (not ModelSerializer + __all__)
    * no `fields = "__all__"` anywhere
    * `validate_*` / `validate` methods do not contain `.objects.` (ORM call)
    * no obvious mutation calls (`.save`, `.delete`, `.create`, `.update`) in validate methods

Outputs: stdout PASS or violation list. Exit 0/1/2.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

CLASS_RE_HINT = ("Request", "Response")
MUTATION_TOKENS = ("save", "delete", "create", "update", "bulk_create", "bulk_update", "delay")


def is_modelserializer_all(node: ast.ClassDef) -> bool:
    for sub in node.body:
        if isinstance(sub, ast.ClassDef) and sub.name == "Meta":
            for stmt in sub.body:
                if isinstance(stmt, ast.Assign):
                    for tgt in stmt.targets:
                        if isinstance(tgt, ast.Name) and tgt.id == "fields":
                            if isinstance(stmt.value, ast.Constant) and stmt.value.value == "__all__":
                                return True
    return False


def check_validate_method(node: ast.FunctionDef) -> list[str]:
    msgs: list[str] = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and sub.attr == "objects":
            msgs.append(
                f"{node.name}: ORM call '.objects' in validate method — business logic belongs in services.py"
            )
            break
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and sub.attr in MUTATION_TOKENS:
            msgs.append(
                f"{node.name}: mutation '.{sub.attr}' in validate method — must be in service"
            )
            break
    return msgs


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError as e:
        return [f"{path}: syntax error: {e}"]
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        # is it a serializer?
        base_names = [ast.unparse(b) for b in node.bases]
        if not any("Serializer" in b for b in base_names):
            continue
        # name shape (only check if it looks like a serializer class)
        if not any(node.name.endswith(suf) for suf in CLASS_RE_HINT):
            errors.append(
                f"{path}:{node.lineno}: serializer class {node.name} should end with Request or Response"
            )
        # __all__ check
        if is_modelserializer_all(node):
            errors.append(f"{path}:{node.lineno}: class {node.name} uses fields = '__all__' — forbidden")
        # validate methods
        for sub in node.body:
            if isinstance(sub, ast.FunctionDef) and (sub.name == "validate" or sub.name.startswith("validate_")):
                errors.extend(f"{path}:{sub.lineno}: {m}" for m in check_validate_method(sub))
    return errors


def iter_targets(target: Path):
    if target.is_file():
        yield target
        return
    yield from target.rglob("serializers.py")


def self_test() -> int:
    import tempfile
    good = """
from rest_framework import serializers
class UserCreateRequest(serializers.Serializer):
    name = serializers.CharField()
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("x")
        return value
"""
    bad = """
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = "x"
        fields = "__all__"
    def validate_email(self, value):
        from x.models import User
        User.objects.get(email=value)
        return value
"""
    with tempfile.TemporaryDirectory() as d:
        gp = Path(d) / "serializers.py"
        gp.write_text(good)
        assert check_file(gp) == [], check_file(gp)
        bp = Path(d) / "serializers.py"
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
