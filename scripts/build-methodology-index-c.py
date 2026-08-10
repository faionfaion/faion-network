#!/usr/bin/env python3
"""Fallback L2 index builder for F-065 Phase 2 (executor C).

Walks `skills/faion/knowledge/` AGENTS.md files, filters by frontmatter `domain`,
emits `skills/faion/knowledge/<domain>/INDEX.xml` per domain.

Schema:
  <index domain="X" count="N" generated="ISO">
    <methodology slug="..." tier="..." path="...">
      <summary>...</summary>
    </methodology>
    ...
  </index>

Sorted by slug. XML-escaped. Used only if indexer A's
`build-methodology-index.py` is not yet on origin/main at run time.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_ROOT = REPO_ROOT / "skills" / "faion" / "knowledge"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        # strip surrounding quotes
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        out[key] = val
    return out


def collect(domain: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for agents_path in KNOWLEDGE_ROOT.rglob("AGENTS.md"):
        try:
            text = agents_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        fm = parse_frontmatter(text)
        if fm.get("domain") != domain:
            continue
        slug = fm.get("slug") or agents_path.parent.name
        tier = fm.get("tier", "")
        summary = fm.get("summary", "")
        rel = agents_path.parent.relative_to(REPO_ROOT).as_posix()
        rows.append(
            {
                "slug": slug,
                "tier": tier,
                "summary": summary,
                "path": rel,
            }
        )
    rows.sort(key=lambda r: r["slug"])
    return rows


def render(domain: str, rows: list[dict[str, str]]) -> str:
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<index domain="{xml_escape(domain, {chr(34): "&quot;"})}" '
        f'count="{len(rows)}" generated="{now}">',
    ]
    for r in rows:
        lines.append(
            '  <methodology '
            f'slug="{xml_escape(r["slug"], {chr(34): "&quot;"})}" '
            f'tier="{xml_escape(r["tier"], {chr(34): "&quot;"})}" '
            f'path="{xml_escape(r["path"], {chr(34): "&quot;"})}">'
        )
        lines.append(f"    <summary>{xml_escape(r['summary'])}</summary>")
        lines.append("  </methodology>")
    lines.append("</index>")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--domain", required=True, action="append",
                   help="Domain to index (repeat for multiple).")
    p.add_argument("--out-root", default=str(KNOWLEDGE_ROOT),
                   help="Root for per-domain INDEX.xml output.")
    args = p.parse_args(argv)

    out_root = Path(args.out_root)
    for domain in args.domain:
        rows = collect(domain)
        out_dir = out_root / domain
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "INDEX.xml"
        out_path.write_text(render(domain, rows), encoding="utf-8")
        print(f"{domain}: {len(rows)} -> {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
