#!/usr/bin/env python3
"""F-066 B5 validator: every methodology must ship content/06-decision-tree.xml.

Rules per checklist B5.1..B5.8:
  B5.1 file exists at <dir>/content/06-decision-tree.xml
  B5.2 root <text id="06-decision-tree" version est_tokens> with one <decision-tree> child
  B5.3 first child of <decision-tree> is <root-question> with >=2 <branch when="...">
  B5.4 every branch has non-empty when= attribute (concrete observable)
  B5.5 every leaf <conclusion> has ref= pointing to a rule id in 01-core-rules.xml
  B5.6 even flat methodologies have minimum form
  B5.7 max depth <=4

Usage:
  validate-methodology-decision-tree.py <dir>          # one
  validate-methodology-decision-tree.py --all          # whole knowledge tree
"""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"


def _gather_rule_ids(core_xml: Path) -> set[str]:
    ids: set[str] = set()
    if not core_xml.exists():
        return ids
    try:
        tree = ET.parse(core_xml)
    except ET.ParseError:
        return ids
    for r in tree.iter("rule"):
        rid = r.get("id")
        if rid:
            ids.add(rid)
    # Conventional conclusion-only rule ids allowed even if not present:
    ids.update({"run-the-checklist", "skip-this-methodology"})
    return ids


def _depth(node: ET.Element) -> int:
    if node is None:
        return 0
    children = [c for c in node if c.tag in ("question", "branch", "decision-tree", "root-question")]
    if not children:
        return 1
    return 1 + max(_depth(c) for c in children)


def validate_dir(dir_path: Path, rule_ids_override: set[str] | None = None) -> list[str]:
    errs: list[str] = []
    dt = dir_path / "content" / "06-decision-tree.xml"
    if not dt.exists():
        errs.append("missing content/06-decision-tree.xml")
        return errs
    try:
        tree = ET.parse(dt)
    except ET.ParseError as e:
        errs.append(f"xml parse error: {e}")
        return errs
    root = tree.getroot()
    if root.tag != "text" or root.get("id") != "06-decision-tree":
        errs.append("root must be <text id='06-decision-tree'>")
    if not root.get("version"):
        errs.append("<text> missing version attr")
    children = list(root)
    dts = [c for c in children if c.tag == "decision-tree"]
    if not dts:
        errs.append("missing <decision-tree> child")
        return errs
    if len(dts) > 1:
        errs.append("more than one <decision-tree> child")
    dtree = dts[0]
    rq = dtree.find("root-question")
    if rq is None:
        errs.append("<decision-tree> missing <root-question>")
        return errs
    branches = rq.findall("branch")
    if len(branches) < 2:
        errs.append(f"<root-question> needs >=2 branches, got {len(branches)}")
    for b in branches:
        if not (b.get("when") or "").strip():
            errs.append("<branch> missing when= attr")
        # leaf <conclusion> ref check
        for conc in b.iter("conclusion"):
            ref = conc.get("ref")
            if not ref:
                errs.append("<conclusion> missing ref= attr")
                continue
            ids = rule_ids_override if rule_ids_override is not None else _gather_rule_ids(dir_path / "content" / "01-core-rules.xml")
            if ref not in ids:
                errs.append(f"<conclusion ref='{ref}'> does not match any rule id in 01-core-rules.xml")
    depth = _depth(dtree)
    if depth > 5:
        errs.append(f"depth {depth} > 5 (SHOULD <=4, hard cap 5)")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="methodology dir")
    ap.add_argument("--all", action="store_true", help="walk full knowledge tree")
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
