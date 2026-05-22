#!/usr/bin/env python3
"""F-066 A2 validator: per-domain INDEX.xml shape.

Rules per checklist A2.1..A2.10:
  A2.1 root <index domain count>
  A2.2 <description> present, refines L1 scope
  A2.3 every <methodology> has slug+tier+path+<summary>
  A2.4 summary <=200 chars, ideally output-first (we only enforce length)
  A2.5 SHOULD: <groups> partition (3-8 sub-clusters) — flagged when missing
  A2.6 SHOULD: complexity attr (light|medium|deep)
  A2.7 SHOULD: produces attr (one of 8 values)
  A2.8 entries sorted alphabetically by slug within each group (or globally if no groups)
  A2.9 count attr equals number of <methodology> entries

Usage:
  validate-domain-index.py skills/faion/knowledge/<domain>/INDEX.xml
  validate-domain-index.py --all
"""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"

VALID_TIER = {"free", "solo", "pro", "geek"}
VALID_COMPLEXITY = {"light", "medium", "deep"}
VALID_PRODUCES = {
    "checklist", "rubric", "spec", "report",
    "code", "config", "playbook-step", "decision-record",
}


def validate(index_xml: Path) -> list[str]:
    errs: list[str] = []
    warns: list[str] = []
    if not index_xml.exists():
        errs.append(f"missing {index_xml}")
        return errs
    try:
        tree = ET.parse(index_xml)
    except ET.ParseError as e:
        errs.append(f"xml parse error: {e}")
        return errs
    root = tree.getroot()
    if root.tag != "index":
        errs.append(f"root must be <index>, got <{root.tag}>")
    if not root.get("domain"):
        errs.append("<index> missing domain= attr")
    count_attr = root.get("count")
    if count_attr is None:
        errs.append("<index> missing count= attr")

    desc = root.find("description")
    if desc is None or not (desc.text or "").strip():
        warns.append("missing or empty <description>")

    methods = root.findall(".//methodology")
    if count_attr is not None:
        try:
            if int(count_attr) != len(methods):
                errs.append(f"count attr ({count_attr}) != methodology entries ({len(methods)})")
        except ValueError:
            errs.append(f"count attr not int: {count_attr!r}")

    seen_slugs: set[str] = set()
    slugs_seq: list[str] = []
    for m in methods:
        slug = m.get("slug") or ""
        tier = m.get("tier") or ""
        path = m.get("path") or ""
        if not slug:
            errs.append("<methodology> missing slug= attr")
            continue
        if slug in seen_slugs:
            errs.append(f"duplicate slug: {slug}")
        seen_slugs.add(slug)
        slugs_seq.append(slug)
        if tier and tier not in VALID_TIER:
            errs.append(f"{slug}: invalid tier {tier!r}")
        if not path:
            warns.append(f"{slug}: missing path= attr")
        summary = m.find("summary")
        if summary is None or not (summary.text or "").strip():
            errs.append(f"{slug}: missing or empty <summary>")
        elif len(summary.text) > 200:
            warns.append(f"{slug}: summary > 200 chars (len={len(summary.text)})")
        # A2.6/A2.7
        cx = m.get("complexity")
        if cx and cx not in VALID_COMPLEXITY:
            errs.append(f"{slug}: invalid complexity {cx!r}")
        pr = m.get("produces")
        if pr and pr not in VALID_PRODUCES:
            errs.append(f"{slug}: invalid produces {pr!r}")

    # A2.5
    groups = root.findall("groups/group")
    if not groups:
        warns.append("no <groups> partition (SHOULD, A2.5)")

    # A2.8 — sorted check (within groups if present, else globally)
    if groups:
        for g in groups:
            gs = [m.get("slug") or "" for m in g.findall("methodology")]
            if gs != sorted(gs):
                warns.append(f"group '{g.get('id') or g.get('name') or '?'}' not sorted by slug")
    else:
        if slugs_seq != sorted(slugs_seq):
            warns.append("methodology entries not sorted alphabetically by slug")

    if warns and not errs:
        for w in warns:
            print(f"  WARN: {w}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="path to INDEX.xml")
    ap.add_argument("--all", action="store_true", help="walk all per-domain INDEX.xml under knowledge/")
    args = ap.parse_args()

    if args.all:
        # Walk every domain dir directly under knowledge/ (depth 1)
        targets = sorted([
            d / "INDEX.xml" for d in KNOWLEDGE.iterdir() if d.is_dir() and (d / "INDEX.xml").exists()
        ])
    else:
        if not args.target:
            ap.error("provide target INDEX.xml or --all")
        targets = [Path(args.target).resolve()]

    fail = 0
    for t in targets:
        errs = validate(t)
        rel = t.relative_to(REPO_ROOT) if t.is_relative_to(REPO_ROOT) else t
        if errs:
            fail += 1
            print(f"FAIL {rel}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {rel}")
    if args.all:
        print(f"\nsummary: {len(targets)-fail} pass / {fail} fail / {len(targets)} total")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
