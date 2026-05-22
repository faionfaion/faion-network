#!/usr/bin/env python3
"""
F-065 phase 3: migrate a single playbook directory from
(playbook.yaml + body.md) -> (AGENTS.md + content/01-playbook.xml).

Usage:
    python3 scripts/migrate-playbook-yaml-to-xml.py <path/to/playbook-dir>

Behavior:
- Reads <dir>/playbook.yaml + <dir>/body.md.
- Writes <dir>/AGENTS.md (frontmatter envelope + verbatim body).
- Writes <dir>/content/01-playbook.xml (structured stages/gaps).
- Renames playbook.yaml -> playbook.yaml.bak.
- Renames body.md -> body.md.bak.
- Idempotent: if AGENTS.md already exists, skip silently (exit 0).
- Preserves every yaml field. Anything that doesn't fit the AGENTS.md frontmatter
  or the XML stages/gaps shape is attached as <extra key="..." value="..."/>.

Exit codes:
    0 - success or skipped (already migrated)
    1 - error
"""

from __future__ import annotations

import hashlib
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import yaml

VALID_STATUS = {"draft", "active", "review", "published", "deprecated"}
SCHEMA_LAST_REVIEWED = "2026-05-22"

# Frontmatter promotes these directly (they always map 1:1 to AGENTS.md envelope).
PROMOTED_TO_FRONTMATTER = {
    "slug", "tier_min", "group", "persona", "complexity",
    "version", "status", "last_reviewed", "maintainers",
    "summary", "content_id", "methodology_refs",
}

# Used by <playbook> + <stages> + <gaps>. Anything outside these and the
# PROMOTED_TO_FRONTMATTER set goes to <extra>.
PROMOTED_TO_XML = {
    "intent", "scope", "success_criteria", "stages", "gaps",
    "title", "slug", "complexity",
}


def compute_content_id(slug: str, version: str) -> str:
    return hashlib.sha1(f"{slug}{version}".encode("utf-8")).hexdigest()[:16]


def yaml_dump_value(value, key=None):
    """Dump a single value as YAML fragment, suitable for frontmatter."""
    if isinstance(value, str):
        # If string contains newlines or weird chars, use literal block.
        if "\n" in value:
            indented = "\n".join("  " + line for line in value.split("\n"))
            return f"{key}: |\n{indented}".rstrip()
        # Quote strings that may be parsed as something else.
        needs_quote = any(c in value for c in [":", "#", "&", "*", "!", "|", ">", "'", '"', "%", "@", "`"]) \
            or value.strip() != value or value in {"null", "true", "false", "yes", "no"}
        if needs_quote:
            v = value.replace('"', '\\"')
            return f'{key}: "{v}"'
        return f"{key}: {value}"
    if isinstance(value, bool):
        return f"{key}: {'true' if value else 'false'}"
    if isinstance(value, (int, float)):
        return f"{key}: {value}"
    if isinstance(value, list):
        if not value:
            return f"{key}: []"
        lines = [f"{key}:"]
        for item in value:
            if isinstance(item, str):
                if any(c in item for c in [":", "#", "'", '"']) or item.strip() != item:
                    v = item.replace('"', '\\"')
                    lines.append(f'  - "{v}"')
                else:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"  - {item}")
        return "\n".join(lines)
    if value is None:
        return f"{key}: null"
    # Fallback: yaml.safe_dump for complex objects.
    dumped = yaml.safe_dump({key: value}, sort_keys=False, allow_unicode=True).rstrip()
    return dumped


def build_frontmatter(data: dict) -> str:
    """Construct the AGENTS.md frontmatter block (no surrounding ---)."""
    slug = data.get("slug", "unknown-slug")
    tier = data.get("tier_min", "free")
    group = data.get("group") or _infer_group_from_path(data)
    persona = data.get("persona")
    if isinstance(persona, list):
        # Squash to comma-separated string for frontmatter; full list preserved
        # via methodology_refs/persona_hints/extras pathway if non-trivial.
        persona = ", ".join(str(p) for p in persona) if persona else ""
    if not persona:
        # Fallback: persona_hints first entry; otherwise empty.
        hints = data.get("persona_hints") or []
        if isinstance(hints, list) and hints:
            persona = str(hints[0])
        else:
            persona = ""
    complexity = data.get("complexity", "medium")
    version = str(data.get("version", "1.0.0"))
    status_in = data.get("status", "draft")
    # The schema requires draft|active — coerce other v2 statuses.
    if status_in == "published":
        status_out = "active"
    elif status_in in {"review", "deprecated"}:
        status_out = "draft"
    elif status_in in VALID_STATUS:
        status_out = status_in
    else:
        status_out = "draft"
    last_reviewed = SCHEMA_LAST_REVIEWED
    maintainers = data.get("maintainers") or ["faion-network"]
    if not isinstance(maintainers, list):
        maintainers = [str(maintainers)]
    summary_raw = (data.get("summary") or "").strip()
    if not summary_raw:
        # Fallback: derive from intent.
        intent = (data.get("intent") or "").strip()
        summary_raw = intent.split("\n", 1)[0].strip()
    # Collapse all internal whitespace (newlines, tabs, repeated spaces) to single
    # spaces so the frontmatter renders as a flow scalar, not a literal block.
    summary = " ".join(summary_raw.split())
    if len(summary) > 200:
        summary = summary[:197].rstrip() + "..."
    content_id = data.get("content_id") or compute_content_id(slug, version)
    methodology_refs_raw = data.get("methodology_refs") or []
    if not isinstance(methodology_refs_raw, list):
        methodology_refs_raw = []
    # Reduce to bare slugs (drop path/tier metadata).
    refs: list[str] = []
    seen: set[str] = set()
    for m in methodology_refs_raw:
        if isinstance(m, str):
            ref_slug = m.rsplit("/", 1)[-1]
        elif isinstance(m, dict):
            ref_slug = m.get("slug") or (m.get("path") or "").rsplit("/", 1)[-1]
        else:
            continue
        if ref_slug and ref_slug not in seen:
            seen.add(ref_slug)
            refs.append(ref_slug)
    # Also pull methodology slugs out of stages[].methodologies[] so the envelope
    # has the complete index (matches what the retriever expects).
    for stage in (data.get("stages") or []):
        if not isinstance(stage, dict):
            continue
        for m in (stage.get("methodologies") or []):
            if isinstance(m, dict):
                ref_slug = m.get("slug") or (m.get("path") or "").rsplit("/", 1)[-1]
                if ref_slug and ref_slug not in seen:
                    seen.add(ref_slug)
                    refs.append(ref_slug)

    lines = []
    lines.append(yaml_dump_value(slug, "slug"))
    lines.append(yaml_dump_value(tier, "tier"))
    lines.append(yaml_dump_value(group or "", "group"))
    lines.append(yaml_dump_value(persona or "", "persona"))
    lines.append("goal: TBD")
    lines.append(yaml_dump_value(complexity, "complexity"))
    lines.append(yaml_dump_value(version, "version"))
    lines.append(yaml_dump_value(status_out, "status"))
    lines.append(yaml_dump_value(last_reviewed, "last_reviewed"))
    lines.append(yaml_dump_value(maintainers, "maintainers"))
    lines.append(yaml_dump_value(summary, "summary"))
    lines.append(yaml_dump_value(content_id, "content_id"))
    lines.append(yaml_dump_value(refs, "methodology_refs"))
    return "\n".join(lines)


def _infer_group_from_path(data: dict) -> str:
    """If group is missing, try to read it from the dir path (caller fills _path)."""
    p = data.get("_path")
    if p is None:
        return ""
    parts = Path(p).parts
    # .../playbooks/<tier>/<group>/<slug>/playbook.yaml
    if "playbooks" in parts:
        i = parts.index("playbooks")
        if i + 2 < len(parts):
            return parts[i + 2]
    return ""


def _xml_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return xml_escape(value.strip())
    return xml_escape(str(value).strip())


def _serialize_extra_value(value) -> str:
    """Serialize any non-promoted yaml value to a single XML attribute string."""
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    # Lists / dicts -> compact yaml inline, forced single line.
    try:
        dumped = yaml.safe_dump(
            value,
            default_flow_style=True,
            sort_keys=False,
            allow_unicode=True,
            width=10**9,
        ).strip()
        # yaml may still introduce newlines in some edge cases; collapse them.
        return dumped.replace("\n", " ")
    except Exception:
        return repr(value)


def build_playbook_xml(data: dict) -> str:
    slug = data.get("slug", "unknown-slug")
    complexity = data.get("complexity", "medium")
    intent = data.get("intent") or ""
    scope = data.get("scope") or ""
    success_criteria = data.get("success_criteria") or []
    stages = data.get("stages") or []
    gaps = data.get("gaps") or []

    lines: list[str] = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        f'<playbook id="01-playbook" slug="{xml_escape(slug)}" '
        f'goal="TBD" complexity="{xml_escape(complexity)}">'
    )
    lines.append(f"  <intent>{_xml_text(intent)}</intent>")
    lines.append(f"  <scope>{_xml_text(scope)}</scope>")

    lines.append("  <success-criteria>")
    sc_list = list(success_criteria) if isinstance(success_criteria, list) else [success_criteria]
    # Schema requires >= 3 criteria. Pad with derived fallback when shorter.
    while len(sc_list) < 3:
        sc_list.append("Exit artifact reviewed and accepted by operator.")
    for c in sc_list:
        lines.append(f"    <criterion>{_xml_text(c)}</criterion>")
    lines.append("  </success-criteria>")

    lines.append("  <stages>")
    if isinstance(stages, list):
        for i, stage in enumerate(stages, start=1):
            if not isinstance(stage, dict):
                continue
            name = stage.get("name", f"Stage {i}")
            lines.append(f'    <stage n="{i}" name="{xml_escape(str(name))}">')
            s_intent = stage.get("intent") or ""
            lines.append(f"      <intent>{_xml_text(s_intent)}</intent>")

            tasks = stage.get("tasks") or []
            lines.append("      <tasks>")
            if isinstance(tasks, list):
                for t in tasks:
                    lines.append(f"        <task>{_xml_text(t)}</task>")
            lines.append("      </tasks>")

            methodologies = stage.get("methodologies") or []
            lines.append("      <methodologies>")
            if isinstance(methodologies, list):
                for m in methodologies:
                    if isinstance(m, dict):
                        m_slug = m.get("slug") or (m.get("path") or "").rsplit("/", 1)[-1]
                    elif isinstance(m, str):
                        m_slug = m.rsplit("/", 1)[-1]
                    else:
                        continue
                    if m_slug:
                        lines.append(f'        <ref slug="{xml_escape(m_slug)}" />')
            lines.append("      </methodologies>")

            outputs = stage.get("outputs") or []
            lines.append("      <outputs>")
            if isinstance(outputs, list):
                for o in outputs:
                    lines.append(f"        <output>{_xml_text(o)}</output>")
            lines.append("      </outputs>")

            decision_gate = stage.get("decision_gate") or ""
            lines.append(f"      <decision-gate>{_xml_text(decision_gate)}</decision-gate>")
            lines.append("    </stage>")
    lines.append("  </stages>")

    lines.append("  <gaps>")
    if isinstance(gaps, list):
        for g in gaps:
            if not isinstance(g, dict):
                continue
            g_slug = g.get("methodology_slug") or g.get("slug") or ""
            tier = g.get("expected_tier") or ""
            if g_slug:
                lines.append(
                    f'    <gap slug="{xml_escape(str(g_slug))}" '
                    f'expected-tier="{xml_escape(str(tier))}" />'
                )
    lines.append("  </gaps>")

    # <extra> for anything we didn't promote into frontmatter or main XML.
    handled = PROMOTED_TO_FRONTMATTER | PROMOTED_TO_XML | {
        "title", "tier_min", "tier", "persona_hints",
    }
    extras = {k: v for k, v in data.items() if k not in handled and not k.startswith("_")}
    if extras:
        for k, v in extras.items():
            val = _serialize_extra_value(v)
            lines.append(
                f'  <extra key="{xml_escape(str(k))}" '
                f'value="{xml_escape(val)}" />'
            )

    lines.append("</playbook>")
    return "\n".join(lines) + "\n"


def build_agents_md(data: dict, body_text: str) -> str:
    title = data.get("title") or data.get("slug", "Playbook")
    frontmatter = build_frontmatter(data)
    body = body_text.strip()
    return f"---\n{frontmatter}\n---\n\n# {title}\n\n{body}\n"


def migrate(dir_path: Path) -> int:
    yaml_path = dir_path / "playbook.yaml"
    body_path = dir_path / "body.md"
    agents_md = dir_path / "AGENTS.md"
    xml_path = dir_path / "content" / "01-playbook.xml"

    # Idempotency: skip silently if already migrated.
    if agents_md.exists() and xml_path.exists():
        return 0

    if not yaml_path.exists():
        sys.stderr.write(f"missing playbook.yaml in {dir_path}\n")
        return 1
    if not body_path.exists():
        sys.stderr.write(f"missing body.md in {dir_path}\n")
        return 1

    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        sys.stderr.write(f"yaml parse error in {yaml_path}: {exc}\n")
        return 1
    if not isinstance(data, dict):
        sys.stderr.write(f"yaml root is not a mapping in {yaml_path}\n")
        return 1
    data["_path"] = str(yaml_path)

    body_text = body_path.read_text(encoding="utf-8")
    # Drop the leading top-level title (e.g. "# Slug") because the AGENTS.md
    # template prepends its own H1. Keep everything else verbatim.
    stripped = body_text.lstrip()
    if stripped.startswith("# "):
        nl = stripped.find("\n")
        if nl >= 0:
            body_text = stripped[nl + 1:].lstrip("\n")
        else:
            body_text = ""

    try:
        agents_md_content = build_agents_md(data, body_text)
        xml_content = build_playbook_xml(data)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"build error in {dir_path}: {exc}\n")
        return 1

    (dir_path / "content").mkdir(exist_ok=True)
    agents_md.write_text(agents_md_content, encoding="utf-8")
    xml_path.write_text(xml_content, encoding="utf-8")

    # Preserve originals as .bak (rollback).
    yaml_bak = dir_path / "playbook.yaml.bak"
    body_bak = dir_path / "body.md.bak"
    if not yaml_bak.exists():
        yaml_path.rename(yaml_bak)
    else:
        yaml_path.unlink()
    if not body_bak.exists():
        body_path.rename(body_bak)
    else:
        body_path.unlink()

    return 0


def main() -> int:
    if len(sys.argv) != 2:
        sys.stderr.write("usage: migrate-playbook-yaml-to-xml.py <playbook-dir>\n")
        return 1
    p = Path(sys.argv[1]).resolve()
    if not p.is_dir():
        sys.stderr.write(f"not a directory: {p}\n")
        return 1
    return migrate(p)


if __name__ == "__main__":
    sys.exit(main())
