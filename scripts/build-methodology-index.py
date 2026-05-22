#!/usr/bin/env python3
"""Build per-domain L2 INDEX.xml files for methodology discovery.

Walks `skills/faion/knowledge/` and groups methodology AGENTS.md entries by the
`domain:` frontmatter value. For each requested domain, writes a sorted
INDEX.xml at `skills/faion/knowledge/<domain>/INDEX.xml`.

If `--domain <name>` is passed (repeatable), only those domains are emitted.
Otherwise every distinct domain found is emitted.

Schema (per entry):
    <methodology>
      <slug>...</slug>
      <tier>...</tier>
      <summary>...</summary>
      <path>...</path>
    </methodology>

Paths are repo-relative (POSIX). Output is sorted by slug. XML special chars in
text are escaped via xml.sax.saxutils.escape.

Usage:
    python3 scripts/build-methodology-index.py
    python3 scripts/build-methodology-index.py --domain research --domain ai-core
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_ROOT = REPO_ROOT / "skills" / "faion" / "knowledge"

FRONTMATTER_KEYS = ("slug", "tier", "domain", "summary")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return a flat dict of frontmatter keys, stripping quotes on values."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    out: dict[str, str] = {}
    for raw in block.splitlines():
        if ":" not in raw or raw.startswith(" ") or raw.startswith("\t"):
            continue
        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()
        if key not in FRONTMATTER_KEYS:
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        out[key] = val
    return out


def collect_entries() -> dict[str, list[dict[str, str]]]:
    by_domain: dict[str, list[dict[str, str]]] = defaultdict(list)
    for agents in KNOWLEDGE_ROOT.rglob("AGENTS.md"):
        try:
            text = agents.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fm = parse_frontmatter(text)
        slug = fm.get("slug")
        domain = fm.get("domain")
        if not slug or not domain:
            continue
        rel_path = agents.parent.relative_to(REPO_ROOT).as_posix()
        by_domain[domain].append(
            {
                "slug": slug,
                "tier": fm.get("tier", ""),
                "summary": fm.get("summary", ""),
                "path": rel_path,
            }
        )
    return by_domain


def _attr(value: str) -> str:
    return escape(value, {'"': "&quot;"})


def render_index(domain: str, entries: list[dict[str, str]]) -> str:
    entries_sorted = sorted(entries, key=lambda e: e["slug"])
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append(
        f'<index domain="{_attr(domain)}" count="{len(entries_sorted)}">'
    )
    for e in entries_sorted:
        lines.append(
            "  <methodology "
            f'slug="{_attr(e["slug"])}" '
            f'tier="{_attr(e["tier"])}" '
            f'path="{_attr(e["path"])}">'
        )
        lines.append(f"    <summary>{escape(e['summary'])}</summary>")
        lines.append("  </methodology>")
    lines.append("</index>")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build per-domain L2 INDEX.xml")
    parser.add_argument(
        "--domain",
        action="append",
        default=None,
        help="Restrict to one domain (repeatable). Default: all domains.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print counts only, do not write files.",
    )
    args = parser.parse_args()

    by_domain = collect_entries()
    selected = args.domain or sorted(by_domain.keys())

    written: list[tuple[str, int, Path]] = []
    for domain in selected:
        entries = by_domain.get(domain, [])
        target_dir = KNOWLEDGE_ROOT / domain
        target = target_dir / "INDEX.xml"
        if args.check:
            written.append((domain, len(entries), target))
            continue
        target_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(render_index(domain, entries), encoding="utf-8")
        written.append((domain, len(entries), target))

    for domain, count, target in written:
        rel = target.relative_to(REPO_ROOT).as_posix()
        sys.stdout.write(f"{domain}\t{count}\t{rel}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
