#!/usr/bin/env python3
"""
F-065 phase 3 validator: enforce the new playbook layout

    <dir>/AGENTS.md             — frontmatter envelope + body
    <dir>/content/01-playbook.xml — structured stages/gaps

Usage:
    python3 scripts/validate-playbook-v3.py <path/to/playbook-dir> [more ...]
    python3 scripts/validate-playbook-v3.py --all
    python3 scripts/validate-playbook-v3.py --self-test

Exit codes:
    0 - all input dirs valid
    1 - one or more dirs failed validation

Rules:
- AGENTS.md MUST start with a YAML `---` frontmatter block containing every
  required key: slug, tier, group, persona, goal, complexity, version, status,
  last_reviewed, maintainers, summary, content_id, methodology_refs.
- content/01-playbook.xml MUST parse, root tag MUST be <playbook>,
  attrs id/slug/goal/complexity MUST exist and be non-empty.
- complexity attr MUST be one of {light, medium, deep}.
- At least 1 <stage> under <stages>.
- <success-criteria> MUST contain >= 3 <criterion> entries.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAYBOOKS_ROOT = REPO_ROOT / "skills" / "faion" / "playbooks"

VALID_COMPLEXITY = {"light", "medium", "deep"}
VALID_TIER = {"free", "solo", "pro", "geek"}
VALID_STATUS = {"draft", "active", "review", "published", "deprecated"}

REQUIRED_FRONTMATTER_KEYS = [
    "slug",
    "tier",
    "group",
    "persona",
    "goal",
    "complexity",
    "version",
    "status",
    "last_reviewed",
    "maintainers",
    "summary",
    "content_id",
    "methodology_refs",
]


@dataclass
class Result:
    path: Path
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    if not text.startswith("---"):
        return None, "AGENTS.md does not start with frontmatter `---`"
    # find closing ---
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "AGENTS.md does not start with frontmatter `---`"
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, "frontmatter `---` not closed"
    block = "\n".join(lines[1:end_idx])
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        return None, f"frontmatter yaml parse error: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def validate_dir(dir_path: Path) -> Result:
    res = Result(path=dir_path)
    if not dir_path.is_dir():
        res.errors.append(f"not a directory: {dir_path}")
        return res

    agents_md = dir_path / "AGENTS.md"
    xml_path = dir_path / "content" / "01-playbook.xml"

    # AGENTS.md
    if not agents_md.exists():
        res.errors.append("missing AGENTS.md")
    else:
        text = agents_md.read_text(encoding="utf-8")
        fm, err = parse_frontmatter(text)
        if err:
            res.errors.append(err)
        else:
            missing = [k for k in REQUIRED_FRONTMATTER_KEYS if k not in fm]
            if missing:
                res.errors.append(f"frontmatter missing keys: {missing}")
            tier = fm.get("tier")
            if tier is not None and tier not in VALID_TIER:
                res.errors.append(f"invalid tier: {tier!r}")
            status = fm.get("status")
            if status is not None and status not in VALID_STATUS:
                res.errors.append(f"invalid status: {status!r}")
            complexity = fm.get("complexity")
            if complexity is not None and complexity not in VALID_COMPLEXITY:
                res.errors.append(f"invalid frontmatter complexity: {complexity!r}")
            mrefs = fm.get("methodology_refs")
            if mrefs is not None and not isinstance(mrefs, list):
                res.errors.append("methodology_refs must be a list")
            maint = fm.get("maintainers")
            if maint is not None and not isinstance(maint, list):
                res.errors.append("maintainers must be a list")
            summary = fm.get("summary")
            if isinstance(summary, str) and len(summary) > 200:
                res.errors.append(f"summary > 200 chars (len={len(summary)})")
            cid = fm.get("content_id")
            if cid is not None and (not isinstance(cid, str) or len(cid) != 16
                                    or not all(c in "0123456789abcdef" for c in cid.lower())):
                res.errors.append(f"content_id must be 16 hex chars: {cid!r}")

    # XML
    if not xml_path.exists():
        res.errors.append("missing content/01-playbook.xml")
    else:
        try:
            tree = ET.parse(xml_path)
        except ET.ParseError as exc:
            res.errors.append(f"xml parse error: {exc}")
            return res
        root = tree.getroot()
        if root.tag != "playbook":
            res.errors.append(f"root tag must be <playbook>, got <{root.tag}>")
            return res
        for attr in ("id", "slug", "goal", "complexity"):
            v = root.get(attr)
            if not v:
                res.errors.append(f"<playbook> missing attribute: {attr}")
        cattr = root.get("complexity")
        if cattr and cattr not in VALID_COMPLEXITY:
            res.errors.append(f"<playbook> invalid complexity attr: {cattr!r}")

        # success-criteria
        sc = root.find("success-criteria")
        if sc is None:
            res.errors.append("<success-criteria> missing")
        else:
            criteria = sc.findall("criterion")
            if len(criteria) < 3:
                res.errors.append(
                    f"<success-criteria> needs >= 3 entries, got {len(criteria)}"
                )

        # stages
        stages_elem = root.find("stages")
        if stages_elem is None:
            res.errors.append("<stages> missing")
        else:
            stages = stages_elem.findall("stage")
            if not stages:
                res.errors.append("<stages> needs >= 1 entry")

    return res


def self_test() -> int:
    fail = 0
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        pb_dir = td_p / "pb"
        pb_dir.mkdir()
        (pb_dir / "content").mkdir()
        agents_md = pb_dir / "AGENTS.md"
        xml_path = pb_dir / "content" / "01-playbook.xml"

        valid_fm = """---
slug: test
tier: pro
group: delivery-ops
persona: P5
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: One-liner.
content_id: 0123456789abcdef
methodology_refs:
  - foo
  - bar
---
# Test
body
"""
        valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<playbook id="01-playbook" slug="test" goal="TBD" complexity="light">
  <intent>i</intent>
  <scope>s</scope>
  <success-criteria>
    <criterion>a</criterion>
    <criterion>b</criterion>
    <criterion>c</criterion>
  </success-criteria>
  <stages>
    <stage n="1" name="x"><intent>i</intent><tasks><task>t</task></tasks><methodologies/><outputs/><decision-gate>g</decision-gate></stage>
  </stages>
  <gaps/>
</playbook>
"""
        # 1: valid
        agents_md.write_text(valid_fm)
        xml_path.write_text(valid_xml)
        r = validate_dir(pb_dir)
        if not r.ok:
            print(f"[FAIL] expected pass, got: {r.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] valid dir passes")

        # 2: missing AGENTS.md
        agents_md.unlink()
        r = validate_dir(pb_dir)
        if not any("missing AGENTS.md" in e for e in r.errors):
            print(f"[FAIL] expected missing AGENTS.md, got: {r.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] catches missing AGENTS.md")
        agents_md.write_text(valid_fm)

        # 3: only 2 criteria
        bad_xml = valid_xml.replace("<criterion>c</criterion>", "")
        xml_path.write_text(bad_xml)
        r = validate_dir(pb_dir)
        if not any("success-criteria" in e for e in r.errors):
            print(f"[FAIL] expected criterion-count error, got: {r.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] catches < 3 criteria")
        xml_path.write_text(valid_xml)

        # 4: missing key in frontmatter
        bad_fm = valid_fm.replace("persona: P5\n", "")
        agents_md.write_text(bad_fm)
        r = validate_dir(pb_dir)
        if not any("frontmatter missing keys" in e for e in r.errors):
            print(f"[FAIL] expected missing-key error, got: {r.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] catches missing persona")
        agents_md.write_text(valid_fm)

        # 5: zero stages
        zero_stages = valid_xml.replace(
            '<stage n="1" name="x"><intent>i</intent><tasks><task>t</task></tasks>'
            '<methodologies/><outputs/><decision-gate>g</decision-gate></stage>',
            "",
        )
        xml_path.write_text(zero_stages)
        r = validate_dir(pb_dir)
        if not any("stages" in e.lower() and ">= 1" in e for e in r.errors):
            print(f"[FAIL] expected zero-stages error, got: {r.errors}", file=sys.stderr)
            fail += 1
        else:
            print("[ OK ] catches zero stages")

    return 1 if fail else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if args.all:
        if not PLAYBOOKS_ROOT.exists():
            sys.stderr.write("playbooks root missing\n")
            return 0
        # Each leaf dir containing content/01-playbook.xml — the playbook dir
        # is the grandparent of the xml file (xml is inside content/).
        paths = sorted({p.parent.parent for p in PLAYBOOKS_ROOT.rglob("content/01-playbook.xml")})
    else:
        paths = [p for p in args.paths]

    if not paths:
        parser.error("no paths given (use --all or --self-test)")

    fail = 0
    for p in paths:
        r = validate_dir(p)
        if r.ok:
            sys.stdout.write(f"PASS {p}\n")
        else:
            fail += 1
            sys.stdout.write(f"FAIL {p}\n")
            for e in r.errors:
                sys.stdout.write(f"  - {e}\n")
    sys.stdout.write(f"\n{len(paths) - fail} pass / {fail} fail / {len(paths)} total\n")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
