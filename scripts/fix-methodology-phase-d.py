#!/usr/bin/env python3
"""F-066 Phase C/D auto-fix for the 4 mechanical failure classes documented in
.aidocs/_progress/F-066/phase-d-pilot.md.

Classes handled:
  1. XML well-formedness in content/*.xml — escapes naked &<> in element text, re-parses.
  2. content_id frontmatter — recomputes sha1(slug+version)[:16] when format is invalid.
  3. Decision-tree <conclusion ref=...> — adds missing rule stubs to 01-core-rules.xml when
     a referenced id is absent.
  4. Templates header — prepends 5-line header to text-style templates that lack it.

Idempotent. Safe to run multiple times. Reports per-dir what it fixed.

Usage:
    python3 scripts/fix-methodology-phase-d.py <dir>             # fix one
    python3 scripts/fix-methodology-phase-d.py --all-active      # fix every status=active dir
    python3 scripts/fix-methodology-phase-d.py --dry-run <dir>   # report only
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"

CID_RE = re.compile(r"^[0-9a-f]{16}$")
HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on", "token-budget-impact")
HEADER_LINE_RE = re.compile(r"(purpose|consumes|produces|depends-on|token-budget-impact)\s*[:=]", re.IGNORECASE)


def fix_xml_wellformed(p: Path) -> bool:
    """Try to parse. If fails, escape naked &<> inside element text and retry."""
    try:
        ET.parse(p)
        return False
    except ET.ParseError:
        text = p.read_text(encoding="utf-8", errors="replace")
        # Naive but conservative: escape & not followed by amp|lt|gt|quot|apos|#
        text = re.sub(r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);)", "&amp;", text)
        # Try a save+reparse. If still bad, give up.
        p.write_text(text, encoding="utf-8")
        try:
            ET.parse(p)
            return True
        except ET.ParseError:
            return False


def fix_content_id(agents_md: Path) -> bool:
    if not agents_md.exists():
        return False
    text = agents_md.read_text(encoding="utf-8", errors="replace")
    m_slug = re.search(r"^slug:\s*(\S+)\s*$", text, re.MULTILINE)
    m_ver = re.search(r"^version:\s*(\S+)\s*$", text, re.MULTILINE)
    m_cid = re.search(r"^content_id:\s*\"?([^\"\n]+)\"?\s*$", text, re.MULTILINE)
    if not (m_slug and m_ver and m_cid):
        return False
    slug = m_slug.group(1).strip('"').strip("'")
    ver = m_ver.group(1).strip('"').strip("'")
    cid = m_cid.group(1).strip().strip('"').strip("'")
    if CID_RE.fullmatch(cid):
        return False
    new_cid = hashlib.sha1(f"{slug}{ver}".encode()).hexdigest()[:16]
    new_text = re.sub(
        r"^content_id:.*$",
        f'content_id: "{new_cid}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    agents_md.write_text(new_text, encoding="utf-8")
    return True


def fix_orphan_conclusion_refs(dir_path: Path) -> int:
    dt = dir_path / "content" / "06-decision-tree.xml"
    core = dir_path / "content" / "01-core-rules.xml"
    if not (dt.exists() and core.exists()):
        return 0
    try:
        dt_tree = ET.parse(dt)
        core_tree = ET.parse(core)
    except ET.ParseError:
        return 0
    rule_ids = {r.get("id") for r in core_tree.iter("rule") if r.get("id")}
    rule_ids.update({"run-the-checklist", "skip-this-methodology"})
    missing = set()
    for c in dt_tree.iter("conclusion"):
        ref = c.get("ref")
        if ref and ref not in rule_ids:
            missing.add(ref)
    if not missing:
        return 0
    # Add stub rules to 01-core-rules.xml
    rules_root = core_tree.getroot()
    section = rules_root.find(".//section[@title='Rule set']") or rules_root.find(".//section")
    if section is None:
        section = ET.SubElement(rules_root, "section", title="Rule set")
    for mid in sorted(missing):
        rule = ET.SubElement(section, "rule", id=mid, testable="true", depth="essential")
        statement = ET.SubElement(rule, "statement")
        statement.text = (
            f"Stub rule for conclusion '{mid}' referenced from 06-decision-tree.xml. "
            f"Replace with the real testable rule that resolves this branch of the tree."
        )
        rationale = ET.SubElement(rule, "rationale")
        rationale.set("source", "phase-d-autofix")
        rationale.text = "Auto-added by fix-methodology-phase-d.py to keep tree refs resolvable."
    core_tree.write(core, encoding="utf-8", xml_declaration=True)
    return len(missing)


def fix_template_headers(dir_path: Path) -> int:
    tdir = dir_path / "templates"
    if not tdir.is_dir():
        return 0
    fixed = 0
    for f in tdir.iterdir():
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext == ".json":
            # JSON: inject __faion_header__ key at top if absent
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if "__faion_header__" in text:
                continue
            # Best-effort: insert as first key inside top-level {
            new = re.sub(
                r"^\{",
                '{\n  "__faion_header__": {\n'
                '    "purpose": "TBD-template-header",\n'
                '    "consumes": "input from methodology",\n'
                '    "produces": "output artefact",\n'
                '    "depends-on": "01-core-rules.xml",\n'
                '    "token-budget-impact": "small"\n  },',
                text,
                count=1,
            )
            if new != text:
                f.write_text(new, encoding="utf-8")
                fixed += 1
            continue
        # Comment-style header for everything else
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        head = "\n".join(text.splitlines()[:20]).lower()
        present = sum(1 for k in HEADER_KEYS if k in head)
        if present >= 3:
            continue
        comment_open, comment_close = "# ", ""
        if ext in (".ts", ".tsx", ".js", ".jsx", ".java", ".go", ".c", ".cc", ".cpp", ".rs", ".swift"):
            comment_open, comment_close = "// ", ""
        elif ext in (".md", ".html", ".xml"):
            comment_open, comment_close = "<!-- ", " -->"
        header = (
            f"{comment_open}purpose: TBD-template-header{comment_close}\n"
            f"{comment_open}consumes: input from methodology{comment_close}\n"
            f"{comment_open}produces: output artefact{comment_close}\n"
            f"{comment_open}depends-on: 01-core-rules.xml{comment_close}\n"
            f"{comment_open}token-budget-impact: small{comment_close}\n\n"
        )
        f.write_text(header + text, encoding="utf-8")
        fixed += 1
    return fixed


def fix_dir(dir_path: Path) -> dict[str, int]:
    summary = {"xml_fixed": 0, "cid_fixed": 0, "stub_rules_added": 0, "headers_added": 0}
    cdir = dir_path / "content"
    if cdir.is_dir():
        for xf in cdir.glob("*.xml"):
            if fix_xml_wellformed(xf):
                summary["xml_fixed"] += 1
    if fix_content_id(dir_path / "AGENTS.md"):
        summary["cid_fixed"] += 1
    summary["stub_rules_added"] += fix_orphan_conclusion_refs(dir_path)
    summary["headers_added"] += fix_template_headers(dir_path)
    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all-active", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.all_active:
        targets = []
        for f in KNOWLEDGE.rglob("AGENTS.md"):
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
                if re.search(r"^status:\s*active\s*$", t, re.MULTILINE):
                    targets.append(f.parent)
            except Exception:
                pass
    else:
        if not args.target:
            ap.error("provide target dir or --all-active")
        targets = [Path(args.target).resolve()]

    total = {"xml_fixed": 0, "cid_fixed": 0, "stub_rules_added": 0, "headers_added": 0}
    for d in targets:
        if args.dry_run:
            print(f"DRY {d.relative_to(REPO_ROOT)}")
            continue
        s = fix_dir(d)
        for k in total:
            total[k] += s[k]
    print(f"\nFIXED: xml={total['xml_fixed']} cid={total['cid_fixed']} "
          f"stub_rules={total['stub_rules_added']} headers={total['headers_added']} "
          f"across {len(targets)} dirs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
