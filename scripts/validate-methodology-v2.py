#!/usr/bin/env python3
"""
Validate methodology v2 directory shape (F-059).

A v2 methodology is a directory containing:

  <dir>/
  ├── AGENTS.md              (frontmatter + 9 required H2 sections)
  ├── content/
  │   ├── 01-core-rules.xml      (required)
  │   ├── 02-output-contract.xml (optional)
  │   └── 03-failure-modes.xml   (optional)
  ├── templates/             (optional)
  └── scripts/               (optional)

Usage:

    python3 scripts/validate-methodology-v2.py <dir>

Exit codes:

    0 — directory passes all v2 checks
    1 — one or more violations found

The validator is intentionally strict: it is a gate for the new template, not a
soft linter. All violations are printed with absolute paths so editors can
jump directly to the failure site.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_FRONTMATTER_KEYS = (
    "slug",
    "tier",
    "group",
    "domain",
    "version",
    "status",
    "last_reviewed",
    "maintainers",
    "summary",
    "content_id",
)

REQUIRED_SECTIONS = (
    "Summary",
    "Applies If",
    "Skip If",
    "Prerequisites",
    "Assumes Loaded",
    "Content",
    "Task Routing",
    "Templates",
    "Scripts",
    "Related",
)

CONTENT_FILES_KNOWN = {
    "01-core-rules.xml": "01-core-rules",
    "02-output-contract.xml": "02-output-contract",
    "03-failure-modes.xml": "03-failure-modes",
}

CONTENT_ID_RE = re.compile(r"^[0-9a-f]{16}$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Violation:
    path: Path
    code: str
    message: str

    def render(self) -> str:
        return f"  [{self.code}] {self.path}: {self.message}"


@dataclass
class Report:
    violations: list[Violation] = field(default_factory=list)

    def fail(self, path: Path, code: str, message: str) -> None:
        self.violations.append(Violation(path, code, message))

    @property
    def ok(self) -> bool:
        return not self.violations


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse a minimal YAML-ish frontmatter block. Returns None on missing block."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    block = m.group(1)
    out: dict[str, str] = {}
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        # collect top-level "key: value" pairs only; nested YAML lists / maps
        # are kept verbatim under the parent key for presence-checks.
        if not line.startswith(" ") and ":" in line:
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip()
    return out


def frontmatter_body(text: str) -> str:
    m = FRONTMATTER_RE.match(text)
    return m.group(2) if m else text


def validate_agents_md(agents_path: Path, report: Report) -> None:
    if not agents_path.exists():
        report.fail(agents_path, "AGENTS_MISSING", "AGENTS.md not found")
        return

    text = agents_path.read_text(encoding="utf-8")

    fm = parse_frontmatter(text)
    if fm is None:
        report.fail(agents_path, "FRONTMATTER_MISSING",
                    "AGENTS.md must start with --- YAML frontmatter --- block")
    else:
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in fm or not fm[key]:
                report.fail(agents_path, "FRONTMATTER_KEY",
                            f"required frontmatter key missing or empty: '{key}'")
        cid = fm.get("content_id", "").strip().strip('"').strip("'")
        if cid and not CONTENT_ID_RE.fullmatch(cid):
            report.fail(agents_path, "CONTENT_ID_FORMAT",
                        f"content_id='{cid}' must be 16 lowercase hex chars")

    body = frontmatter_body(text)
    headings = {h.strip() for h in HEADING_RE.findall(body)}
    # Section names may include optional parenthetical qualifiers, e.g.
    # "Applies If (ALL must hold)". Match by prefix to be tolerant.
    for required in REQUIRED_SECTIONS:
        if not any(h == required or h.startswith(required + " ") or
                   h.startswith(required + "(") for h in headings):
            report.fail(agents_path, "SECTION_MISSING",
                        f"required H2 section missing: '## {required}'")


def validate_xml_text(content_path: Path, expected_id: str, report: Report) -> None:
    """Parse content_path and ensure root is <text id=expected_id ...>."""
    try:
        tree = ET.parse(content_path)
    except ET.ParseError as exc:
        report.fail(content_path, "XML_PARSE", f"unparseable XML: {exc}")
        return
    root = tree.getroot()
    if root.tag != "text":
        report.fail(content_path, "XML_ROOT_TAG",
                    f"root must be <text>, got <{root.tag}>")
        return
    rid = root.get("id", "")
    if rid != expected_id:
        report.fail(content_path, "XML_ROOT_ID",
                    f'<text> id="{rid}" — expected id="{expected_id}"')


def count_testable_rules(content_dir: Path) -> int:
    """Count <rule testable="true"> across every content/*.xml present."""
    total = 0
    if not content_dir.is_dir():
        return 0
    for xml_file in sorted(content_dir.glob("*.xml")):
        try:
            tree = ET.parse(xml_file)
        except ET.ParseError:
            continue
        for elem in tree.getroot().iter("rule"):
            if (elem.get("testable") or "").lower() == "true":
                total += 1
    return total


def validate_methodology_dir(root: Path, report: Report) -> None:
    if not root.exists():
        report.fail(root, "DIR_MISSING", "methodology directory does not exist")
        return
    if not root.is_dir():
        report.fail(root, "NOT_A_DIR", "path is not a directory")
        return

    validate_agents_md(root / "AGENTS.md", report)

    content_dir = root / "content"
    if not content_dir.is_dir():
        report.fail(content_dir, "CONTENT_DIR_MISSING",
                    "content/ subdirectory must exist")
    else:
        # Require ≥1 content/01-*.xml (the "core" position). Canonical is
        # 01-core-rules.xml but domain-specific filenames are accepted as long
        # as they follow the \d{2}-[a-z0-9-]+ pattern. Each \d{2}- file has its
        # <text id> validated against its filename stem.
        core_candidates = sorted(content_dir.glob("01-*.xml"))
        if not core_candidates:
            report.fail(content_dir / "01-*.xml", "CORE_RULES_MISSING",
                        "at least one content/01-*.xml is REQUIRED")

        for fpath in sorted(content_dir.glob("*.xml")):
            stem = fpath.stem
            if re.fullmatch(r"\d{2}-[a-z0-9-]+", stem):
                validate_xml_text(fpath, stem, report)

        total_rules = count_testable_rules(content_dir)
        if total_rules < 1:
            report.fail(content_dir, "NO_TESTABLE_RULES",
                        "at least one <rule testable=\"true\"> required across "
                        "content/*.xml files (none found)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate methodology v2 directory layout",
    )
    parser.add_argument("target", help="path to methodology directory")
    ns = parser.parse_args()

    root = Path(ns.target).resolve()
    report = Report()
    validate_methodology_dir(root, report)

    if report.ok:
        print(f"PASS {root}")
        print("summary: 1/1 passed, 0 failed")
        return 0

    print(f"FAIL {root}")
    for v in report.violations:
        print(v.render())
    print()
    print(f"summary: 0/1 passed, {len(report.violations)} violations")
    return 1


if __name__ == "__main__":
    sys.exit(main())
