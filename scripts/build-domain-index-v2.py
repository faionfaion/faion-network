#!/usr/bin/env python3
"""F-066 A2 backfill: regenerate per-domain INDEX.xml v2.

Differences vs v1:
  - <groups> partition (parent group derived from path: <tier>/<domain>/<group>/<slug>)
  - <methodology> carries complexity= + produces= + est_tokens= attrs when present in frontmatter
  - <description> kept verbatim if already present, else minimal stub

Idempotent — safe to re-run after each refactor wave.

Usage:
  build-domain-index-v2.py --domain dev
  build-domain-index-v2.py --all
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

KEYS = (
    "slug", "tier", "group", "domain", "summary",
    "complexity", "produces", "est_tokens",
)


def parse_frontmatter(p: Path) -> dict[str, str] | None:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith(" "):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def collect_by_domain() -> dict[str, list[dict]]:
    """Walk knowledge/, group methodologies by domain."""
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for agents_md in KNOWLEDGE.rglob("AGENTS.md"):
        # Skip per-domain INDEX dir agents (none expected) + scripts/templates
        rel = agents_md.relative_to(REPO_ROOT)
        parts = rel.parts
        if "templates" in parts or "scripts" in parts:
            continue
        fm = parse_frontmatter(agents_md)
        if not fm:
            continue
        domain = fm.get("domain", "").strip()
        if not domain:
            continue
        slug = fm.get("slug", "").strip()
        if not slug:
            continue
        entry = {k: fm.get(k, "") for k in KEYS}
        entry["path"] = str(rel.parent)
        # Sub-group inferred from path: <tier>/<domain-or-area>/<group>/<slug>
        # We use the directory immediately under <tier>/ as the sub-cluster.
        path_parts = entry["path"].split("/")
        # paths look like: skills/faion/knowledge/<tier>/<area>/<sub>/<slug>
        # Strip the prefix
        if path_parts[:3] == ["skills", "faion", "knowledge"]:
            tail = path_parts[3:]
        else:
            tail = path_parts
        sub = "uncategorised"
        if len(tail) >= 3:
            sub = tail[-3]  # the directory right above leaf slug, e.g. "code-quality"
        entry["sub"] = sub
        by_domain[domain].append(entry)
    return by_domain


def render_index(domain: str, entries: list[dict]) -> str:
    # Partition by sub-group
    groups: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        groups[e["sub"]].append(e)
    # Sort entries within group by slug + tier
    for g in groups.values():
        g.sort(key=lambda x: (x.get("slug", ""), x.get("tier", "")))

    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(f'<index domain="{escape(domain)}" count="{len(entries)}" version="2.0" generated="2026-05-22">')
    parts.append(f"  <description>L2 index of methodologies in the {escape(domain)} domain. The retriever reads this after picking {escape(domain)} from L1 domains.xml. Entries are partitioned into sub-clusters; each methodology carries complexity + produces attrs to let the agent pre-filter before opening any AGENTS.md.</description>")
    parts.append("  <groups>")
    for sub in sorted(groups.keys()):
        parts.append(f'    <group id="{escape(sub)}" count="{len(groups[sub])}">')
        for e in groups[sub]:
            slug = escape(e["slug"])
            tier = escape(e.get("tier", ""))
            path = escape(e["path"])
            cx = e.get("complexity", "")
            pr = e.get("produces", "")
            et = e.get("est_tokens", "")
            attrs = [f'slug="{slug}"', f'tier="{tier}"', f'path="{path}"']
            if cx:
                attrs.append(f'complexity="{escape(cx)}"')
            if pr:
                attrs.append(f'produces="{escape(pr)}"')
            if et and et.strip("\""+"'").isdigit():
                attrs.append(f'est_tokens="{escape(et)}"')
            summary = escape(e.get("summary", "")).replace("\n", " ").strip()
            parts.append(f'      <methodology {" ".join(attrs)}>')
            parts.append(f'        <summary>{summary}</summary>')
            parts.append("      </methodology>")
        parts.append("    </group>")
    parts.append("  </groups>")
    parts.append("</index>")
    return "\n".join(parts) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", help="single domain")
    ap.add_argument("--all", action="store_true", help="all domains")
    ap.add_argument("--write", action="store_true", help="write to disk (default: print to stdout)")
    args = ap.parse_args()

    by = collect_by_domain()

    if args.all:
        targets = sorted(by.keys())
    elif args.domain:
        targets = [args.domain]
    else:
        ap.error("provide --domain X or --all")

    for d in targets:
        xml = render_index(d, by.get(d, []))
        out_path = KNOWLEDGE / d / "INDEX.xml"
        if args.write:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(xml, encoding="utf-8")
            print(f"wrote {out_path.relative_to(REPO_ROOT)}  ({len(by.get(d, []))} entries)")
        else:
            print(f"--- {d} ({len(by.get(d, []))} entries) ---")
            print(xml[:1000])
            print(f"... ({len(xml)} bytes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
