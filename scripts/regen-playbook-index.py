#!/usr/bin/env python3
"""P2.3: regenerate the 11 L2 goal indexes for the playbook layer.

Playbook retrieval routes L1 `playbooks/taxonomy.xml` -> L2
`playbooks/by-goal/<goal>/INDEX.xml` -> a leaf. The leaves live at
`playbooks/<goal>/<slug>/`, directly under the playbook root; `by-goal/`
holds indexes only and carries no leaf of its own. The indexes were
written before F-067 and still pointed `path=` at the retired
`<tier>/<group>/<slug>` layout, so every one of the 455 entries named a
directory that does not exist. Counts were right, destinations were not.

Every entry here is derived from the leaf's own `meta.json` (slug, tier,
complexity, summary) and from where the leaf actually sits on disk, so
the index cannot drift from the tree the way a hand-kept list does. The
goal set and each index's `<description>` come from `taxonomy.xml`, so
L1 and L2 cannot disagree about which categories exist: a category with
no leaf directory, or a leaf directory with no category, aborts the run
instead of writing a half-correct index.

Modelled on `regen-fragment-index.py` and `regen-tier-manifest.py`,
which read `meta.json` — deliberately NOT on the deleted
`build-domain-index-v2.py`, which read YAML frontmatter no envelope
carries and emptied the file it targeted.

`generated=` is only bumped when the body actually changes, so a rerun
on an unchanged tree is a no-op instead of an eleven-line diff.

Usage:
    python3 scripts/regen-playbook-index.py             # write all 11
    python3 scripts/regen-playbook-index.py --dry-run   # report, write nothing
    python3 scripts/regen-playbook-index.py --check     # exit 1 if stale
    python3 scripts/regen-playbook-index.py --only build-ship

Exit: 0 written / clean · 1 stale under --check · 2 the script could not
run (missing tree, unreadable meta.json, taxonomy out of sync with disk).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent.parent
PLAYBOOKS = ROOT / "skills" / "faion" / "playbooks"
TAXONOMY = PLAYBOOKS / "taxonomy.xml"
BY_GOAL = PLAYBOOKS / "by-goal"

# Longest summary carried into an L2 index. The indexes are a retrieval
# surface an agent reads whole before it opens any leaf, so a runaway
# summary costs every lookup, not just its own.
SUMMARY_MAX = 200


class Abort(Exception):
    """The script cannot run — a missing tree, bad meta.json, or L1/L2 drift."""


def load_meta(meta_path: Path) -> dict:
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Abort(f"{meta_path.relative_to(ROOT)}: {exc}") from exc


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def taxonomy_goals() -> dict[str, str]:
    """Goal id -> index description, in taxonomy document order.

    The description is the category's `<intent>` followed by its
    `<scope>`, which is what the pre-F-067 indexes carried and what a
    router needs to choose between two categories without opening either.
    """
    if not TAXONOMY.is_file():
        raise Abort(f"no taxonomy at {rel(TAXONOMY)}")
    try:
        root = ET.parse(TAXONOMY).getroot()
    except ET.ParseError as exc:
        raise Abort(f"{rel(TAXONOMY)}: {exc}") from exc
    goals: dict[str, str] = {}
    for cat in root.findall("category"):
        goal = cat.get("id")
        if not goal:
            raise Abort(f"{rel(TAXONOMY)}: <category> without id=")
        parts = [(cat.findtext(tag) or "").strip() for tag in ("intent", "scope")]
        goals[goal] = " ".join(p for p in parts if p)
    if not goals:
        raise Abort(f"{rel(TAXONOMY)}: no <category> elements")
    return goals


def leaf_dirs(goal: str) -> list[Path]:
    """Every playbook leaf under `playbooks/<goal>/`, sorted by slug."""
    base = PLAYBOOKS / goal
    if not base.is_dir():
        raise Abort(f"taxonomy category {goal!r} has no directory at {rel(base)}")
    leaves = sorted(d for d in base.iterdir()
                    if d.is_dir() and (d / "meta.json").is_file())
    if not leaves:
        raise Abort(f"taxonomy category {goal!r} has no leaves under {rel(base)} — "
                    "remove the category from taxonomy.xml or add a playbook")
    return leaves


def check_no_orphan_goal_dirs(goals: set[str]) -> None:
    """Every goal directory on disk must be a taxonomy category.

    `by-goal/` is the index directory, not a goal; anything else with a
    leaf beneath it and no category above it is unroutable content.
    """
    for d in sorted(PLAYBOOKS.iterdir()):
        if not d.is_dir() or d.name == "by-goal" or d.name in goals:
            continue
        if any(d.rglob("meta.json")) or any(d.rglob("playbook.md")):
            raise Abort(f"{rel(d)} holds playbook leaves but is not a "
                        "taxonomy category — add the category or move the leaves")


def clip(summary: str) -> str:
    """Trim a summary to SUMMARY_MAX characters on a word boundary."""
    summary = " ".join(summary.split())
    if len(summary) <= SUMMARY_MAX:
        return summary
    head = summary[:SUMMARY_MAX]
    cut = head.rsplit(" ", 1)[0] if " " in head else head
    return cut.rstrip(" ,;:-") + "..."


def build_goal(goal: str) -> tuple[str, int]:
    lines: list[str] = []
    leaves = leaf_dirs(goal)
    for leaf in leaves:
        meta = load_meta(leaf / "meta.json")
        attrs = [
            ("slug", meta.get("slug") or leaf.name),
            ("tier", meta.get("tier") or ""),
            ("complexity", meta.get("complexity") or ""),
            ("path", rel(leaf)),
        ]
        pairs = " ".join(f"{k}={quoteattr(v)}" for k, v in attrs if v != "")
        lines.append(f"  <playbook {pairs}>")
        lines.append(f"    <summary>{escape(clip(meta.get('summary') or ''))}</summary>")
        lines.append("  </playbook>")
    return "\n".join(lines), len(leaves)


GENERATED_ATTR = re.compile(r'generated="[^"]*"')


def render(goal: str, description: str, today: str, previous: str | None) -> str:
    body, count = build_goal(goal)
    out = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<index goal="{goal}" generated="{today}" count="{count}">\n'
        f'  <description>{escape(description)}</description>\n'
        + body + "\n</index>\n"
    )
    if previous is not None and GENERATED_ATTR.sub("", out) == GENERATED_ATTR.sub("", previous):
        return previous
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change; write nothing")
    ap.add_argument("--check", action="store_true",
                    help="write nothing; exit 1 when an index is stale")
    ap.add_argument("--only", help="regenerate one goal instead of all 11")
    ap.add_argument("--date", default=datetime.date.today().isoformat(),
                    help="value for generated= when the body changes")
    args = ap.parse_args()

    stale: list[str] = []
    try:
        goals = taxonomy_goals()
        check_no_orphan_goal_dirs(set(goals))
        if args.only:
            if args.only not in goals:
                raise Abort(f"{args.only!r} is not a taxonomy category "
                            f"({', '.join(sorted(goals))})")
            goals = {args.only: goals[args.only]}
        for goal, description in goals.items():
            target = BY_GOAL / goal / "INDEX.xml"
            target.parent.mkdir(parents=True, exist_ok=True)
            previous = target.read_text(encoding="utf-8") if target.is_file() else None
            out = render(goal, description, args.date, previous)
            # `render` returns `previous` verbatim when the body is
            # unchanged, so a hand-mangled INDEX.xml can reach here with
            # no count= at all. Report it; never crash on the match.
            found = re.search(r'count="(\d+)"', out)
            if found is None:
                raise Abort(f"{rel(target)}: no count= attribute — the file "
                            "is not a generated index; delete it and rerun")
            count = found.group(1)
            if out == previous:
                print(f"{goal}: up to date ({count} entries)")
                continue
            stale.append(goal)
            verb = "would write" if (args.dry_run or args.check) else "wrote"
            if not (args.dry_run or args.check):
                target.write_text(out, encoding="utf-8")
            print(f"{goal}: {verb} {rel(target)} ({count} entries)")
    except Abort as exc:
        print(f"regen-playbook-index: {exc}", file=sys.stderr)
        return 2

    if args.check and stale:
        print(f"STALE: {', '.join(stale)} — run "
              "python3 scripts/regen-playbook-index.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
