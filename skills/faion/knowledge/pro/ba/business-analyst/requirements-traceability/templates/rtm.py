#!/usr/bin/env python3
"""rtm.py — generate Requirements Traceability Matrix from frontmatter traces.

Walks a docs tree, reads `traces:` YAML frontmatter, builds a link graph,
prints coverage summary and orphan lists matching the RTM template.

Usage: python rtm.py [docs-root]
       python rtm.py requirements/

Wire into pre-commit: any change under docs/ triggers rtm.py and fails on new orphans.

Frontmatter link format:
  traces:
    - REQ-101                          # short form: role defaults to "satisfies"
    - {to: REQ-102, role: verifies}    # full form with explicit role

Exit 0: clean. Exit 1: orphans or coverage gaps found.
"""
from __future__ import annotations
import sys, pathlib, collections, yaml

ROLES = {"satisfies", "verifies", "derives", "implements", "conflicts"}
ARTIFACT_TYPES = {"BR", "SR", "FR", "D", "TC", "M"}

def load(p: pathlib.Path) -> dict:
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}

def main(root: str = "docs") -> int:
    nodes: dict[str, dict] = {}
    edges: list[tuple[str, str, str]] = []

    for p in pathlib.Path(root).rglob("*.md"):
        fm = load(p)
        nid = fm.get("id")
        if not nid:
            continue
        nodes[nid] = {
            "path": str(p),
            "type": nid.split("-")[0],
            "title": fm.get("title", ""),
        }
        for link in fm.get("traces", []) or []:
            if isinstance(link, str):
                tgt, role = link, "satisfies"
            elif isinstance(link, dict):
                tgt, role = link.get("to", ""), link.get("role", "satisfies")
            else:
                continue
            if role not in ROLES:
                print(f"WARN: unknown link role '{role}' in {nid} -> {tgt}")
                continue
            edges.append((nid, tgt, role))

    fwd: dict[str, set] = collections.defaultdict(set)
    bwd: dict[str, set] = collections.defaultdict(set)
    for s, t, _ in edges:
        fwd[s].add(t)
        bwd[t].add(s)

    orphans_up = [n for n, m in nodes.items()
                  if m["type"] in {"SR", "FR", "TC"} and not bwd[n]]
    orphans_down = [n for n, m in nodes.items()
                    if m["type"] in {"BR", "SR", "FR"} and not fwd[n]]

    by_type: dict[str, int] = collections.Counter(m["type"] for m in nodes.values())

    print(f"{'Type':<10} {'Total':>6} {'Linked':>7}  {'Coverage':>8}")
    print("-" * 38)
    for t in sorted(by_type):
        total = by_type[t]
        linked = sum(1 for n, m in nodes.items()
                     if m["type"] == t and (fwd[n] or bwd[n]))
        pct = 100 * linked / total if total else 0
        print(f"{t:<10} {total:>6} {linked:>7}  {pct:>7.0f}%")

    if orphans_up:
        print(f"\nOrphans (no upstream): {', '.join(sorted(orphans_up))}")
    if orphans_down:
        print(f"Orphans (no downstream): {', '.join(sorted(orphans_down))}")

    has_issues = bool(orphans_up or orphans_down)
    if not has_issues:
        print("\nNo orphans detected.")
    return 1 if has_issues else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "docs"))
