#!/usr/bin/env python3
"""
Migrate a v1 methodology.xml to the v2 directory layout (F-059).

Input:  path to an existing v1 methodology.xml file
Output: side-by-side v2 structure written into the SAME directory:

    <slug>/
    ├── methodology-v1.xml.bak     (renamed from methodology.xml)
    ├── AGENTS.md                  (frontmatter + 9 required H2 sections)
    └── content/
        ├── 01-core-rules.xml      (all <rule testable="true"> elements)
        ├── 02-output-contract.xml (stub schema skeleton)
        └── 03-failure-modes.xml   (all <antipattern> elements)

The migration is deliberately mechanical: anything that cannot be auto-derived
from v1 metadata is stubbed with the required minimum so the v2 validator
passes — humans then fill the stubs.

Usage:

    python3 scripts/migrate-methodology-to-v2.py path/to/methodology.xml [--force]
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

DEFAULT_VERSION = "1.0.0"
DEFAULT_STATUS = "draft"
DEFAULT_MAINTAINER = "faion-net"


def compute_content_id(slug: str, version: str) -> str:
    """SHA-1 of slug + version, truncated to 16 hex chars."""
    h = hashlib.sha1(f"{slug}{version}".encode("utf-8"))
    return h.hexdigest()[:16]


def text_or_empty(elem: ET.Element | None, tag: str) -> str:
    if elem is None:
        return ""
    found = elem.find(tag)
    if found is None or found.text is None:
        return ""
    return found.text.strip()


def collect_list_items(parent: ET.Element | None, container: str) -> list[str]:
    """Return text from <container><list><item>...</item></list></container>."""
    if parent is None:
        return []
    block = parent.find(container)
    if block is None:
        return []
    items: list[str] = []
    for item in block.iter("item"):
        if item.text and item.text.strip():
            items.append(" ".join(item.text.split()))
    return items


def collect_tags(metadata: ET.Element | None) -> list[str]:
    if metadata is None:
        return []
    tags_block = metadata.find("tags")
    if tags_block is None:
        return []
    return [t.text.strip() for t in tags_block.iter("tag")
            if t.text and t.text.strip()]


def render_agents_md(
    slug: str,
    tier: str,
    group: str,
    domain: str,
    version: str,
    status: str,
    last_reviewed: str,
    content_id: str,
    summary_para: str,
    title: str,
    tags: list[str],
    applies_items: list[str],
    skip_items: list[str],
    content_files: list[Path],
    parent_skill_link: str,
) -> str:
    one_sentence = summary_para.split(".")[0].strip()
    if one_sentence:
        one_sentence += "."

    def bullets(items: list[str], fallback: str) -> str:
        if not items:
            return f"- {fallback}\n"
        return "".join(f"- {line}\n" for line in items)

    content_rows = []
    for cf in content_files:
        if cf.name == "01-core-rules.xml":
            depth, desc = "essential", "Testable rules migrated from v1 methodology"
        elif cf.name == "02-output-contract.xml":
            depth, desc = "essential", "Output schema (stub — fill from v1 patterns)"
        elif cf.name == "03-failure-modes.xml":
            depth, desc = "essential", "Antipatterns migrated from v1 methodology"
        else:
            depth, desc = "essential", "Migrated content"
        content_rows.append(
            f"| `content/{cf.name}` | {depth} | {desc} | ~800 |"
        )
    content_table = "\n".join(content_rows) if content_rows else (
        "| `content/01-core-rules.xml` | essential | TBD | ~800 |"
    )

    tags_line = ", ".join(tags) if tags else "[]"

    fm_lines = [
        "---",
        f"slug: {slug}",
        f"tier: {tier}",
        f"group: {group}",
        f"domain: {domain}",
        f"version: {version}",
        f"status: {status}",
        f"last_reviewed: {last_reviewed}",
        f"maintainers: [{DEFAULT_MAINTAINER}]",
        f"summary: {one_sentence or 'TBD — fill from v1 source'}",
        f'content_id: "{content_id}"',
        f"tags: [{tags_line}]",
        "---",
        "",
    ]

    sections = [
        f"# {title or slug}",
        "",
        "## Summary",
        "",
        f"**One-sentence:** {one_sentence or 'TBD'}",
        "",
        f"**One-paragraph:** {summary_para or 'TBD — migrated from v1; please rewrite.'}",
        "",
        "## Applies If (ALL must hold)",
        "",
        bullets(applies_items, "TBD — populate from v1 when-to-use list").rstrip(),
        "",
        "## Skip If (ANY kills it)",
        "",
        bullets(skip_items, "TBD — populate from v1 when-not-to-use list").rstrip(),
        "",
        "## Prerequisites",
        "",
        "- TBD — list concrete input artifacts and where they come from",
        "",
        "## Assumes Loaded",
        "",
        "| Methodology | Why |",
        "|-------------|-----|",
        "| `TBD/path` | TBD — what upstream output this consumes |",
        "",
        "## Content (load on demand)",
        "",
        "| File | Depth | What's inside | Est. tokens |",
        "|------|-------|---------------|-------------|",
        content_table,
        "",
        "## Task Routing",
        "",
        "| Sub-task | Model | Rationale |",
        "|----------|-------|-----------|",
        "| TBD | sonnet | TBD |",
        "",
        "## Templates",
        "",
        "| File | Purpose |",
        "|------|---------|",
        "| TBD | TBD |",
        "",
        "## Scripts",
        "",
        "| File | Purpose | When to call |",
        "|------|---------|--------------|",
        "| TBD | TBD | TBD |",
        "",
        "## Related",
        "",
        f"- parent skill: `{parent_skill_link}`",
        "",
    ]

    return "\n".join(fm_lines) + "\n".join(sections)


def emit_core_rules_xml(rules: list[ET.Element], slug: str) -> str:
    """Wrap migrated <rule testable="true"> elements as <text id="01-core-rules">."""
    out: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<text id="01-core-rules" title="{escape(slug)} Core Rules" '
        f'version="1.0.0" est_tokens="800" depth="essential">',
        f"  <summary>Migrated testable rules for {escape(slug)}. "
        "Verify and refine before relying on for production.</summary>",
        "",
        '  <section title="Rule set">',
    ]
    if not rules:
        out.append('    <rule id="r1" testable="true" depth="essential">')
        out.append("      <statement>TBD — v1 source contained no testable rules. "
                   "Author at least one rule for this methodology.</statement>")
        out.append('      <rationale source="migration-stub">Stub created by '
                   "migrate-methodology-to-v2; replace with a real rule.</rationale>")
        out.append("    </rule>")
    else:
        for idx, rule in enumerate(rules, start=1):
            statement_el = rule.find("statement")
            rationale_el = rule.find("rationale")
            statement = (statement_el.text or "").strip() if statement_el is not None else ""
            rationale = (rationale_el.text or "").strip() if rationale_el is not None else ""
            rationale_src = (
                rationale_el.get("source") if rationale_el is not None else ""
            ) or "v1-source"
            rid = rule.get("id") or f"r{idx}"
            out.append(f'    <rule id="{escape(rid)}" testable="true" depth="essential">')
            out.append(f"      <statement>{escape(statement) or 'TBD'}</statement>")
            out.append(
                f'      <rationale source="{escape(rationale_src)}">'
                f"{escape(rationale) or 'TBD'}</rationale>"
            )
            out.append("    </rule>")
    out.append("  </section>")
    out.append("</text>")
    return "\n".join(out) + "\n"


def emit_output_contract_xml(slug: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<text id="02-output-contract" title="{escape(slug)} Output Contract" '
        'version="1.0.0" est_tokens="600" depth="essential">\n'
        "  <summary>Output schema for the subagent applying this methodology. "
        "Stub created by migration; fill before relying on it.</summary>\n"
        "\n"
        "  <output-contract>\n"
        "    <required>\n"
        '      <field name="TBD" format="TBD"/>\n'
        "    </required>\n"
        "    <forbidden>\n"
        '      <pattern id="f1">TBD — encode patterns v1 marks as anti-examples</pattern>\n'
        "    </forbidden>\n"
        "    <allowed-transformations>\n"
        "      <transformation>TBD — bounded normalizations allowed before return</transformation>\n"
        "    </allowed-transformations>\n"
        "  </output-contract>\n"
        "\n"
        '  <section title="Self-check checklist">\n'
        "    <list>\n"
        "      <item>TBD — first checkable invariant</item>\n"
        "    </list>\n"
        "  </section>\n"
        "</text>\n"
    )


def emit_failure_modes_xml(antipatterns: list[ET.Element], slug: str) -> str:
    out: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<text id="03-failure-modes" title="{escape(slug)} Failure Modes" '
        'version="1.0.0" est_tokens="700" depth="essential">',
        f"  <summary>Migrated antipatterns for {escape(slug)} as failure modes. "
        "Add detector + repair clauses where missing.</summary>",
        "",
        '  <section title="Failure modes">',
    ]
    if not antipatterns:
        out.append('    <failure-mode id="fm-01" severity="medium">')
        out.append("      <description>TBD — v1 source contained no antipatterns. "
                   "Document at least one LLM failure mode for this methodology.</description>")
        out.append("      <detector>TBD — observable check for the failure</detector>")
        out.append("      <repair>TBD — corrective action when detector fires</repair>")
        out.append("    </failure-mode>")
    else:
        for idx, ap in enumerate(antipatterns, start=1):
            desc_el = ap.find("description")
            reason_el = ap.find("reason")
            desc = (desc_el.text or "").strip() if desc_el is not None else ""
            reason = (reason_el.text or "").strip() if reason_el is not None else ""
            out.append(f'    <failure-mode id="fm-{idx:02d}" severity="medium">')
            out.append(f"      <description>{escape(desc) or 'TBD'}</description>")
            out.append("      <detector>TBD — observable signal that this antipattern is happening</detector>")
            out.append(
                f"      <repair>{escape(reason) or 'TBD — corrective action'}</repair>"
            )
            out.append("    </failure-mode>")
    out.append("  </section>")
    out.append("</text>")
    return "\n".join(out) + "\n"


def migrate(v1_path: Path, *, force: bool = False) -> int:
    if not v1_path.is_file():
        print(f"ERROR: not a file: {v1_path}", file=sys.stderr)
        return 2
    try:
        tree = ET.parse(v1_path)
    except ET.ParseError as exc:
        print(f"ERROR: unparseable v1 XML {v1_path}: {exc}", file=sys.stderr)
        return 2

    root = tree.getroot()
    if root.tag != "methodology":
        print(f"ERROR: v1 root tag is <{root.tag}>, expected <methodology>",
              file=sys.stderr)
        return 2

    methodology_dir = v1_path.parent
    slug = root.get("slug") or methodology_dir.name
    metadata = root.find("metadata")
    content = root.find("content")

    tier = text_or_empty(metadata, "tier") or "solo"
    group = text_or_empty(metadata, "group") or "research"
    domain = text_or_empty(metadata, "domain") or methodology_dir.parent.name
    summary = text_or_empty(metadata, "summary")
    tags = collect_tags(metadata)

    title_el = content.find("title") if content is not None else None
    title = (title_el.text or "").strip() if title_el is not None and title_el.text else slug

    content_summary_el = content.find("summary") if content is not None else None
    summary_para = (
        (content_summary_el.text or "").strip()
        if content_summary_el is not None and content_summary_el.text else summary
    )

    applies_items = collect_list_items(content, "when-to-use") if content is not None else []
    skip_items = collect_list_items(content, "when-not-to-use") if content is not None else []

    rules = [r for r in (content.iter("rule") if content is not None else [])
             if (r.get("testable") or "").lower() == "true"]
    antipatterns = list(content.iter("antipattern")) if content is not None else []

    content_id = compute_content_id(slug, DEFAULT_VERSION)
    today = date.today().isoformat()

    content_dir = methodology_dir / "content"
    agents_path = methodology_dir / "AGENTS.md"
    bak_path = methodology_dir / "methodology-v1.xml.bak"

    if agents_path.exists() and not force:
        print(f"ERROR: AGENTS.md already exists at {agents_path}. "
              "Pass --force to overwrite.", file=sys.stderr)
        return 2

    content_dir.mkdir(exist_ok=True)
    core_rules_path = content_dir / "01-core-rules.xml"
    output_contract_path = content_dir / "02-output-contract.xml"
    failure_modes_path = content_dir / "03-failure-modes.xml"

    core_rules_path.write_text(emit_core_rules_xml(rules, slug), encoding="utf-8")
    output_contract_path.write_text(emit_output_contract_xml(slug), encoding="utf-8")
    failure_modes_path.write_text(emit_failure_modes_xml(antipatterns, slug), encoding="utf-8")

    parent_skill_link = f"{tier}/{group}/{domain}/"

    agents_md = render_agents_md(
        slug=slug,
        tier=tier,
        group=group,
        domain=domain,
        version=DEFAULT_VERSION,
        status=DEFAULT_STATUS,
        last_reviewed=today,
        content_id=content_id,
        summary_para=summary_para or summary,
        title=title,
        tags=tags,
        applies_items=applies_items,
        skip_items=skip_items,
        content_files=[core_rules_path, output_contract_path, failure_modes_path],
        parent_skill_link=parent_skill_link,
    )
    agents_path.write_text(agents_md, encoding="utf-8")

    # Rename v1 source LAST so the migration is recoverable mid-flight.
    if not bak_path.exists():
        v1_path.rename(bak_path)

    files_made = sorted(content_dir.glob("*.xml"))
    print(f"v2 directory: {methodology_dir}")
    print(f"AGENTS.md:    {agents_path}")
    print(f"content/:     {len(files_made)} files")
    for f in files_made:
        print(f"  - {f.name}")
    print(f"v1 backup:    {bak_path}")
    print(f"content_id:   {content_id}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate a v1 methodology.xml to v2 directory layout",
    )
    parser.add_argument("v1_path", help="path to v1 methodology.xml")
    parser.add_argument("--force", action="store_true",
                        help="overwrite existing AGENTS.md")
    ns = parser.parse_args()
    return migrate(Path(ns.v1_path).resolve(), force=ns.force)


if __name__ == "__main__":
    sys.exit(main())
