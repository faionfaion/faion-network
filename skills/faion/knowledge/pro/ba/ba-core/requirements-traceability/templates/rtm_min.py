#!/usr/bin/env python3
"""rtm_min.py — first-principles RTM generator from frontmatter links.
Usage: python rtm_min.py [docs-root]
Exit 0 = coverage gates pass. Exit 1 = gate failure. Exit 2 = schema error.
Allowed link roles: satisfies, derives, implements, verifies, conflicts.
Expected frontmatter: id, traces: [{to, role}] or traces: ["REQ-XXX"]
"""
from __future__ import annotations
import sys, pathlib, collections
try:
    import yaml
except ImportError:
    print("pip install pyyaml"); sys.exit(2)

ROLES = {"satisfies", "derives", "implements", "verifies", "conflicts"}
PARENTS = {"SR": "BR", "FR": "SR", "D": "FR", "M": "D", "TC": "FR"}


def fm(p: pathlib.Path) -> dict:
    t = p.read_text()
    if not t.startswith("---"):
        return {}
    return yaml.safe_load(t.split("---", 2)[1]) or {}


def main(root: str = "docs") -> int:
    nodes, edges = {}, []
    for p in pathlib.Path(root).rglob("*.md"):
        d = fm(p)
        nid = d.get("id")
        if not nid:
            continue
        nodes[nid] = nid.split("-")[0]
        for ln in d.get("traces", []) or []:
            tgt = ln if isinstance(ln, str) else ln.get("to", "")
            role = "satisfies" if isinstance(ln, str) else ln.get("role", "satisfies")
            if role not in ROLES:
                print(f"ERR bad role '{role}' in {nid}"); return 2
            edges.append((nid, tgt, role))

    up: dict = collections.defaultdict(set)
    down: dict = collections.defaultdict(set)
    for s, t, _ in edges:
        up[t].add(s); down[s].add(t)

    by_type = collections.Counter(nodes.values())
    print(f"{'Type':<6}{'Total':>6}{'Linked':>8}{'Coverage':>10}")
    rc = 0
    for ty in sorted(by_type):
        total = by_type[ty]
        linked = sum(1 for n, t in nodes.items() if t == ty and (up[n] or down[n]))
        cov = 100 * linked // total if total else 0
        print(f"{ty:<6}{total:>6}{linked:>8}{cov:>9}%")
        if ty in PARENTS and cov < 95:
            rc = 1

    orphans_up = [n for n, t in nodes.items() if t in PARENTS and not up[n]]
    if orphans_up:
        print("\nOrphans (no parent):", ", ".join(orphans_up)); rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))

# Pre-commit hook (add to .pre-commit-config.yaml):
# - id: rtm-min
#   name: RTM coverage and orphan check
#   entry: python scripts/rtm_min.py docs/
#   language: system
#   pass_filenames: false
#   files: ^(docs|requirements)/
