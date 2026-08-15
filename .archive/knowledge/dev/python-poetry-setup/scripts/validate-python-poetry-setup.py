#!/usr/bin/env python3
"""validate-python-poetry-setup.py — verify lockfile + tight Python pin + no Poetry in final Docker stage.

Usage:
    validate-python-poetry-setup.py --root /path/to/repo
    validate-python-poetry-setup.py --self-test

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
    if not (root / "poetry.lock").exists():
        v.append({"rule": "rule:r1", "message": "poetry.lock missing — must be committed"})
    pp = root / "pyproject.toml"
    if pp.exists():
        try:
            data = parse_toml(pp.read_text(encoding="utf-8"))
            py = data.get("tool", {}).get("poetry", {}).get("dependencies", {}).get("python", "")
            if not re.match(r"^\^?3\.(1[1-9]|[2-9][0-9])", str(py)):
                v.append({"rule": "rule:r5", "message": f"python constraint {py!r} not tight (>=3.11)"})
        except Exception as e:
            v.append({"rule": "schema", "message": f"pyproject.toml parse: {e}"})
    for df in root.rglob("Dockerfile*"):
        text = df.read_text(encoding="utf-8")
        stages = re.findall(r"^FROM\s+\S+(?:\s+AS\s+(\S+))?", text, re.MULTILINE | re.IGNORECASE)
        if len(stages) >= 2:
            last_stage_start = text.rfind("FROM ")
            tail = text[last_stage_start:]
            if "poetry install" in tail:
                v.append({"rule": "rule:r7", "file": str(df), "message": "poetry install appears in final Docker stage"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "poetry.lock").touch()
        (root / "pyproject.toml").write_text(
            '[tool.poetry]\nname="x"\n[tool.poetry.dependencies]\npython="^3.11"\n', encoding="utf-8"
        )
        assert not scan(root)
        (root / "Dockerfile").write_text(
            "FROM python:3.11 AS builder\nRUN pip install poetry\n"
            "FROM python:3.11\nRUN pip install poetry && poetry install\n",
            encoding="utf-8"
        )
        v = scan(root)
        assert any(x["rule"] == "rule:r7" for x in v), v
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
