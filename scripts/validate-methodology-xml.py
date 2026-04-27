#!/usr/bin/env python3
"""
Validate methodology.xml files against the closed schema.

Usage:
    python3 scripts/validate-methodology-xml.py <path1> [<path2> ...]
    python3 scripts/validate-methodology-xml.py --all     # walks skills/faion/knowledge/

Exit codes:
    0 — all files valid
    1 — one or more files failed validation

Prints a per-file PASS/FAIL summary and detailed errors. Designed to run as a
pre-commit hook and inside the migration agent's quality gate.

The closed tag vocabulary is loaded from docs/methodology-tag-glossary.xml.
The mandatory-fields list, length-parity threshold, and required-attribute
table are kept in code (this file) — single source of truth.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = REPO_ROOT / "docs" / "methodology-tag-glossary.xml"
KNOWLEDGE_ROOT = REPO_ROOT / "skills" / "faion" / "knowledge"

VALID_TIERS = {"free", "solo", "pro", "geek"}
VALID_GROUPS = {
    "dev", "ai", "marketing", "research", "product",
    "pm", "ba", "ux", "comms", "infra", "sdd", "sdlc-ai",
}
VALID_DIFFICULTY = {"beginner", "intermediate", "advanced"}
VALID_APPLIES_TO = {"agents", "humans", "both"}

REQUIRED_ATTRS = {
    "methodology": {"slug"},
    "section": {"name"},
    "reference": {"path"},
    "file": {"path"},
    "template": {"path"},
    "script": {"path"},
    "ref": {"slug"},
    "term": {"name"},
    "link": {"href"},
}

NON_EMPTY_CONTAINERS = {
    "rule", "rules", "example", "antipattern",
    "files", "templates", "scripts", "checklist", "verify",
    "list", "tags", "tools", "languages", "frameworks",
    "related", "requires", "superseded-by", "see-also",
    "metadata", "content",
}

LENGTH_PARITY_MIN = 0.80  # content text ≥ 80% of source markdown chars


@dataclass
class Issue:
    path: Path
    code: str
    message: str

    def render(self) -> str:
        return f"  [{self.code}] {self.message}"


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)

    def fail(self, path: Path, code: str, message: str) -> None:
        self.issues.append(Issue(path, code, message))

    @property
    def ok(self) -> bool:
        return not self.issues


def load_glossary() -> set[str]:
    if not GLOSSARY_PATH.exists():
        raise SystemExit(f"glossary missing: {GLOSSARY_PATH}")
    tree = ET.parse(GLOSSARY_PATH)
    names: set[str] = set()
    for tag in tree.iter("tag"):
        name = tag.get("name")
        if name:
            names.add(name)
    return names


def text_length(elem: ET.Element) -> int:
    """Total non-whitespace character count under elem."""
    parts: list[str] = []
    for chunk in elem.itertext():
        parts.append(chunk)
    return len(re.sub(r"\s+", " ", "".join(parts)).strip())


def find_source_markdown(folder: Path) -> int:
    """Sum char count of OLD-shape .md bodies as the comparison baseline."""
    total = 0
    for name in (
        "README.md",
        "agent-integration.md",
        "checklist.md",
        "examples.md",
        "llm-prompts.md",
        "templates.md",
        "AGENTS.md",
    ):
        f = folder / name
        if f.exists():
            total += len(re.sub(r"\s+", " ", f.read_text(encoding="utf-8")).strip())
    return total


def is_in_knowledge(path: Path) -> bool:
    """True iff the file lives under skills/faion/knowledge/<tier>/<group>/<domain>/<slug>/."""
    try:
        return path.is_relative_to(KNOWLEDGE_ROOT)
    except (AttributeError, ValueError):
        return False


def validate_file(path: Path, glossary: set[str], report: Report) -> None:
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        report.fail(path, "XML_PARSE", f"unparseable XML: {exc}")
        return

    root = tree.getroot()
    enforce_path = is_in_knowledge(path)

    # 1. root element + slug attribute
    if root.tag != "methodology":
        report.fail(path, "ROOT_TAG", f"root must be <methodology>, got <{root.tag}>")
        return
    slug = root.get("slug")
    if not slug:
        report.fail(path, "ROOT_SLUG", "<methodology> missing required slug attribute")
    elif enforce_path and slug != path.parent.name:
        report.fail(
            path, "SLUG_MISMATCH",
            f"slug='{slug}' != folder name '{path.parent.name}'",
        )

    # 2. metadata + content presence and order
    children = list(root)
    metadata = root.find("metadata")
    content = root.find("content")
    if metadata is None:
        report.fail(path, "NO_METADATA", "missing <metadata> child")
    if content is None:
        report.fail(path, "NO_CONTENT", "missing <content> child")
    if metadata is not None and content is not None:
        if children.index(metadata) > children.index(content):
            report.fail(path, "ORDER", "<metadata> must come before <content>")

    # 3. mandatory metadata fields
    if metadata is not None:
        validate_metadata(path, metadata, report, enforce_path=enforce_path)

    # 4. content title
    if content is not None:
        validate_content(path, content, report)

    # 5. closed tag vocabulary
    for elem in root.iter():
        if elem.tag not in glossary and elem.tag != "methodology":
            report.fail(path, "UNKNOWN_TAG", f"<{elem.tag}> not in glossary")

    # 6. required attributes
    for elem in root.iter():
        required = REQUIRED_ATTRS.get(elem.tag, set())
        for attr in required:
            if not elem.get(attr):
                report.fail(
                    path, "MISSING_ATTR",
                    f"<{elem.tag}> requires attribute '{attr}'",
                )

    # 7. non-empty containers
    for elem in root.iter():
        if elem.tag in NON_EMPTY_CONTAINERS:
            if len(elem) == 0 and not (elem.text and elem.text.strip()):
                report.fail(
                    path, "EMPTY_CONTAINER",
                    f"<{elem.tag}> must not be empty",
                )

    # 8. length parity (only if the migration source still exists alongside)
    if content is not None:
        baseline = find_source_markdown(path.parent)
        if baseline > 200:  # only meaningful for non-trivial sources
            current = text_length(content)
            ratio = current / baseline if baseline else 1.0
            if ratio < LENGTH_PARITY_MIN:
                report.fail(
                    path, "LENGTH_PARITY",
                    f"content text {current} chars is {ratio:.0%} of source markdown "
                    f"({baseline} chars); minimum {LENGTH_PARITY_MIN:.0%}. "
                    f"Detect accidental summarization.",
                )


def validate_metadata(path: Path, metadata: ET.Element, report: Report, enforce_path: bool = True) -> None:
    tier = metadata.findtext("tier", "").strip()
    group = metadata.findtext("group", "").strip()
    domain = metadata.findtext("domain", "").strip()
    summary = metadata.findtext("summary", "").strip()

    if tier not in VALID_TIERS:
        report.fail(path, "META_TIER", f"<tier>='{tier}' not in {sorted(VALID_TIERS)}")
    if group not in VALID_GROUPS:
        report.fail(path, "META_GROUP", f"<group>='{group}' not in {sorted(VALID_GROUPS)}")
    if not domain:
        report.fail(path, "META_DOMAIN", "<domain> missing or empty")
    if not summary:
        report.fail(path, "META_SUMMARY", "<summary> missing or empty")
    elif len(summary) > 200:
        report.fail(
            path, "META_SUMMARY_LEN",
            f"<summary> is {len(summary)} chars (max 200)",
        )

    # path-derived consistency check (skipped for examples / fixtures)
    parts = path.parent.relative_to(KNOWLEDGE_ROOT).parts if enforce_path else None
    if parts and len(parts) >= 4:
        path_tier, path_group, path_domain = parts[0], parts[1], parts[2]
        if tier and path_tier and tier != path_tier:
            report.fail(path, "META_TIER_PATH", f"<tier>='{tier}' != path tier '{path_tier}'")
        if group and path_group and group != path_group:
            report.fail(path, "META_GROUP_PATH", f"<group>='{group}' != path group '{path_group}'")
        if domain and path_domain and domain != path_domain:
            report.fail(path, "META_DOMAIN_PATH", f"<domain>='{domain}' != path domain '{path_domain}'")

    difficulty = metadata.findtext("difficulty")
    if difficulty and difficulty.strip() not in VALID_DIFFICULTY:
        report.fail(
            path, "META_DIFFICULTY",
            f"<difficulty>='{difficulty}' not in {sorted(VALID_DIFFICULTY)}",
        )

    applies_to = metadata.findtext("applies-to")
    if applies_to and applies_to.strip() not in VALID_APPLIES_TO:
        report.fail(
            path, "META_APPLIES_TO",
            f"<applies-to>='{applies_to}' not in {sorted(VALID_APPLIES_TO)}",
        )

    for date_tag in ("created", "updated"):
        val = metadata.findtext(date_tag)
        if val and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", val.strip()):
            report.fail(
                path, "META_DATE_FORMAT",
                f"<{date_tag}>='{val}' not ISO YYYY-MM-DD",
            )


def validate_content(path: Path, content: ET.Element, report: Report) -> None:
    children = list(content)
    if not children:
        report.fail(path, "CONTENT_EMPTY", "<content> has no children")
        return
    first = children[0]
    if first.tag != "title":
        report.fail(path, "CONTENT_TITLE_FIRST", f"first child of <content> must be <title>, got <{first.tag}>")
    title_text = (first.text or "").strip() if first.tag == "title" else ""
    if first.tag == "title" and not title_text:
        report.fail(path, "CONTENT_TITLE_EMPTY", "<title> is empty")


def collect_files(targets: list[str], scan_all: bool) -> list[Path]:
    paths: list[Path] = []
    if scan_all:
        if not KNOWLEDGE_ROOT.exists():
            raise SystemExit(f"knowledge root not found: {KNOWLEDGE_ROOT}")
        paths.extend(sorted(KNOWLEDGE_ROOT.rglob("methodology.xml")))
        return paths
    for arg in targets:
        p = Path(arg).resolve()
        if p.is_dir():
            paths.extend(sorted(p.rglob("methodology.xml")))
        elif p.is_file():
            paths.append(p)
        else:
            raise SystemExit(f"not found: {p}")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate methodology.xml files")
    parser.add_argument(
        "targets", nargs="*",
        help="paths to methodology.xml files or folders",
    )
    parser.add_argument(
        "--all", dest="scan_all", action="store_true",
        help="walk skills/faion/knowledge for every methodology.xml",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="only print failures",
    )
    ns = parser.parse_args()

    if not ns.scan_all and not ns.targets:
        parser.error("provide paths or --all")

    glossary = load_glossary()

    paths = collect_files(ns.targets, ns.scan_all)
    if not paths:
        print("no methodology.xml files found")
        return 0

    failed: list[Path] = []
    for path in paths:
        report = Report()
        validate_file(path, glossary, report)
        if report.ok:
            if not ns.quiet:
                print(f"PASS {path.relative_to(REPO_ROOT)}")
        else:
            failed.append(path)
            print(f"FAIL {path.relative_to(REPO_ROOT)}")
            for issue in report.issues:
                print(issue.render())

    print()
    total = len(paths)
    ok = total - len(failed)
    print(f"summary: {ok}/{total} passed, {len(failed)} failed")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
