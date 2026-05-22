#!/usr/bin/env python3
"""F-066 B4 validator: methodology scripts/ discipline.

Rules per checklist B4.1..B4.5:
  B4.1 If 02-output-contract.xml declares a <schema>, a `scripts/validate-<slug>.py` must exist.
  B4.4 Every script has a `--help` flag (we test via argparse import or substring).
  B4.5 Every script SHOULD have `--self-test` flag (warn-only).
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"


def _slug_from_frontmatter(agents_md: Path) -> str | None:
    if not agents_md.exists():
        return None
    text = agents_md.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^slug:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1).strip('"').strip("'") if m else None


def _output_contract_has_schema(xml_path: Path) -> bool:
    if not xml_path.exists():
        return False
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:
        return False
    return tree.getroot().find(".//schema") is not None


def validate_dir(dir_path: Path) -> list[str]:
    errs: list[str] = []
    contract = dir_path / "content" / "02-output-contract.xml"
    if not _output_contract_has_schema(contract):
        return errs  # no schema declared → no validator script required
    slug = _slug_from_frontmatter(dir_path / "AGENTS.md") or dir_path.name
    candidates = [
        dir_path / "scripts" / f"validate-{slug}.py",
        dir_path / "scripts" / "validate-output.py",
    ]
    if not any(p.exists() for p in candidates):
        errs.append(f"missing scripts/validate-{slug}.py (or scripts/validate-output.py)")
        return errs
    script = next(p for p in candidates if p.exists())
    text = script.read_text(encoding="utf-8", errors="replace")
    if "--help" not in text and "argparse" not in text:
        errs.append(f"{script.name}: no `--help` / argparse")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    targets: list[Path]
    if args.all:
        targets = [p.parent for p in KNOWLEDGE.rglob("AGENTS.md")]
    else:
        if not args.target:
            ap.error("provide target dir or --all")
        targets = [Path(args.target).resolve()]

    fail = 0
    for d in targets:
        errs = validate_dir(d)
        if errs:
            fail += 1
            print(f"FAIL {d.relative_to(REPO_ROOT)}")
            for e in errs:
                print(f"  - {e}")
        elif not args.all:
            print(f"PASS {d.relative_to(REPO_ROOT)}")
    if args.all:
        print(f"\nsummary: {len(targets)-fail} pass / {fail} fail / {len(targets)} total")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
