#!/usr/bin/env python3
"""validate-python.py — check pyproject.toml for python >=3.11 + ruff + mypy strict, no black/flake8.

Usage:
    validate-python.py --root /path/to/repo
    validate-python.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_toml(text: str) -> dict:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore
    return tomllib.loads(text)


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    pp = root / "pyproject.toml"
    if not pp.exists():
        v.append({"rule": "schema", "message": "pyproject.toml missing"})
        return v
    data = parse_toml(pp.read_text(encoding="utf-8"))
    poetry = data.get("tool", {}).get("poetry", {})
    py = poetry.get("dependencies", {}).get("python") or data.get("project", {}).get("requires-python", "")
    if not re.search(r"3\.(1[1-9]|[2-9][0-9])", str(py)):
        v.append({"rule": "rule:r5", "message": f"python version constraint {py!r} does not require >=3.11"})
    tool = data.get("tool", {})
    if "ruff" not in tool:
        v.append({"rule": "rule:r4", "message": "[tool.ruff] not configured"})
    mypy = tool.get("mypy", {})
    if not mypy.get("strict"):
        v.append({"rule": "rule:r3", "message": "[tool.mypy] strict is not true"})
    deps = poetry.get("dev-dependencies", {}) or poetry.get("group", {}).get("dev", {}).get("dependencies", {}) or {}
    for forbidden in ("black", "isort", "flake8"):
        if forbidden in deps:
            v.append({"rule": "rule:r4", "message": f"{forbidden} present in deps alongside ruff"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pyproject.toml").write_text(
            '[tool.poetry]\nname="x"\n[tool.poetry.dependencies]\npython="^3.11"\n'
            '[tool.ruff]\ntarget-version="py311"\n[tool.mypy]\nstrict=true\n',
            encoding="utf-8"
        )
        assert not scan(root), scan(root)
        (root / "pyproject.toml").write_text(
            '[tool.poetry]\nname="x"\n[tool.poetry.dependencies]\npython="^3.10"\n[tool.mypy]\nstrict=false\n',
            encoding="utf-8"
        )
        v = scan(root)
        assert any(x["rule"] == "rule:r5" for x in v), v
        assert any(x["rule"] == "rule:r3" for x in v), v
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.root:
        ap.error("--root required")
        return 2
    v = scan(args.root)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
