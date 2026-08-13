#!/usr/bin/env python3
"""P2.6: remap or drop the stale methodology references in playbook leaves.

A playbook leaf cites the methodologies each of its stages leans on, in
three places, and all three were written against the pre-F-067
role-based taxonomy:

  AGENTS.md   `**Methodologies in chain:**`  - `<slug>` -> `<tier>/<domain>/<role>/<slug>`
  AGENTS.md   `**Backed by methodology**`    - `<tier>/<domain>/<role>/<slug>` (tier: X)
  content/01-playbook.xml                    <ref slug="<slug>"/>

The two Markdown carriers name a **path**, and F-067 moved every
methodology to `<domain>/<slug>`, so not one of those paths resolves.
The XML carrier names a **bare slug**, which is path-independent and
survived the move — its residue is a different defect (slugs with no
methodology anywhere) and is much smaller.

Two actions, decided per reference, the same rule set
`remap-dangling-wikilinks.py` applied to the methodology side:

  remap  a successor exists under the current taxonomy and is verified
         on disk before anything is written.
  drop   no successor exists, or more than one target is plausible. A
         reference resolving to the wrong methodology is worse than no
         reference, so ambiguity always drops.

Never invent a target. Four ordered sources of evidence, first hit wins:

  A  `scripts/slug-rename-map.json` — the F-067 migration's own per-path
     decision table, keyed by the exact old path. Authoritative, and the
     only source that can disambiguate a slug living in two domains,
     because it knows which old path became which new one. `delete`
     entries follow their `kept_path`.
  B  the slug is unique in the corpus -> `<domain>/<slug>`.
  C  the slug is duplicated, but a segment of the old path is a current
     domain that holds it -> that domain.
  D  the ratified rename table inside `remap-dangling-wikilinks.py`
     (title-slug drift and dropped qualifiers, each justified there),
     re-checked through B and C so a ratified rename onto a duplicated
     slug still has to disambiguate.

Dropping a bullet removes the whole line. A `**Backed by methodology**`
heading left with no bullets is removed too; an emptied
`**Methodologies in chain:**` block gets the placeholder the corpus
already uses in 34 leaves. An emptied `<methodologies>` element is left
in place — 97 stages already ship one, so an empty element is the shape
in use, and deleting it would be a schema change rather than a fix.

Usage:
    python3 scripts/repair-playbook-bridge.py --dry-run
    python3 scripts/repair-playbook-bridge.py --report   # per-decision table
    python3 scripts/repair-playbook-bridge.py            # apply
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "skills" / "faion" / "knowledge"
PLAYBOOKS = ROOT / "skills" / "faion" / "playbooks"
RENAME_MAP = ROOT / "scripts" / "slug-rename-map.json"
WIKILINK_SCRIPT = ROOT / "scripts" / "remap-dangling-wikilinks.py"

CHAIN_HEAD = "**Methodologies in chain:**"
BACKED_HEAD = "**Backed by methodology**"
CHAIN_EMPTY = "- (no resolved methodologies -- see gaps below)"

CHAIN_BULLET = re.compile(r"^(\s*)-\s+`([^`]+)`\s*(?:→|->)\s*`([^`]+)`\s*$")
BACKED_BULLET = re.compile(r"^(\s*)-\s+`([^`]+)`\s*(?:\(tier:\s*\w+\))?\s*$")
XML_REF = re.compile(r'^(\s*)<ref\s+slug="([^"]+)"\s*/>\s*$')


class Abort(Exception):
    """The script cannot run — a missing tree or an unreadable input."""


def corpus_index() -> dict[str, list[str]]:
    """slug -> every domain holding a methodology with that slug."""
    if not KNOWLEDGE.is_dir():
        raise Abort(f"no knowledge tree at {KNOWLEDGE}")
    index: dict[str, list[str]] = defaultdict(list)
    for domain in sorted(d for d in KNOWLEDGE.iterdir() if d.is_dir()):
        for leaf in domain.iterdir():
            if leaf.is_dir() and (leaf / "meta.json").is_file():
                index[leaf.name].append(domain.name)
    return index


def rename_map() -> dict[str, dict]:
    try:
        data = json.loads(RENAME_MAP.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Abort(f"{RENAME_MAP.name}: {exc}") from exc
    return {r["old_path"]: r for r in data.get("renames", [])}


def ratified_renames() -> dict[str, str]:
    """The REMAP table of `remap-dangling-wikilinks.py`, read as data.

    Importing the module would be cleaner, but it walks the corpus at
    import time; the table is a literal and parses on its own.
    """
    try:
        src = WIKILINK_SCRIPT.read_text(encoding="utf-8")
        literal = src.split("REMAP = ", 1)[1].split("\n}", 1)[0] + "\n}"
        return ast.literal_eval(literal)
    except (OSError, IndexError, SyntaxError, ValueError) as exc:
        raise Abort(f"{WIKILINK_SCRIPT.name}: cannot read REMAP: {exc}") from exc


class Resolver:
    def __init__(self) -> None:
        self.slugs = corpus_index()
        self.renames = rename_map()
        self.ratified = ratified_renames()
        self.classes: Counter[str] = Counter()
        self.dropped: Counter[str] = Counter()

    def _via_rename_map(self, old_path: str, depth: int = 0) -> str | None:
        row = self.renames.get(old_path)
        if row is None or depth > 3:
            return None
        if row.get("action") == "delete":
            return self._via_rename_map(row.get("kept_path", ""), depth + 1)
        dest = f"{row.get('new_domain')}/{row.get('new_slug')}"
        return dest if (KNOWLEDGE / dest).is_dir() else None

    def _by_slug(self, slug: str, hints: list[str]) -> str | None:
        domains = self.slugs.get(slug) or []
        if len(domains) == 1:
            return f"{domains[0]}/{slug}"
        for hint in hints:
            if hint in domains:
                return f"{hint}/{slug}"
        return None

    def resolve_path(self, path: str) -> tuple[str | None, str]:
        """A `<tier>/<domain>/<role>/<slug>` reference -> `<domain>/<slug>`."""
        if (KNOWLEDGE / path).is_dir():
            return path, "already-valid"
        dest = self._via_rename_map(f"skills/faion/knowledge/{path}")
        if dest:
            return dest, "A-rename-map"
        parts = path.split("/")
        hints, slug = parts[:-1], parts[-1]
        dest = self._by_slug(slug, hints)
        if dest:
            return dest, "B-unique-slug" if len(self.slugs[slug]) == 1 else "C-domain-hint"
        successor = self.ratified.get(slug)
        if successor:
            dest = self._by_slug(successor, hints)
            if dest:
                return dest, "D-ratified-rename"
        return None, "drop"

    def resolve_slug(self, slug: str) -> tuple[str | None, str]:
        """A bare-slug reference -> a slug that exists in the corpus."""
        if slug in self.slugs:
            return slug, "already-valid"
        successor = self.ratified.get(slug)
        if successor and successor in self.slugs:
            return successor, "D-ratified-rename"
        return None, "drop"

    def record(self, kind: str, target: str, outcome: str) -> None:
        self.classes[f"{kind}:{outcome}"] += 1
        if outcome == "drop":
            self.dropped[target] += 1


def tier_of(dest: str) -> str:
    meta = KNOWLEDGE / dest / "meta.json"
    try:
        return json.loads(meta.read_text(encoding="utf-8")).get("tier") or ""
    except (OSError, json.JSONDecodeError):
        return ""


def repair_agents(text: str, r: Resolver) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        head = lines[i].strip()
        kind = ("chain" if head.startswith(CHAIN_HEAD)
                else "backed" if head.startswith(BACKED_HEAD) else None)
        if kind is None:
            out.append(lines[i])
            i += 1
            continue
        j = i + 1
        kept: list[str] = []
        saw_bullet = False
        while j < len(lines) and lines[j].lstrip().startswith("- "):
            body = lines[j].rstrip("\n")
            match = (CHAIN_BULLET if kind == "chain" else BACKED_BULLET).match(body)
            if match is None:
                kept.append(lines[j])          # placeholder or hand-written note
                j += 1
                continue
            saw_bullet = True
            indent = match.group(1)
            target = match.group(3) if kind == "chain" else match.group(2)
            dest, outcome = r.resolve_path(target)
            r.record(kind, target, outcome)
            if dest is None:
                j += 1
                continue
            slug = dest.split("/")[-1]
            if kind == "chain":
                kept.append(f"{indent}- `{slug}` → `{dest}`\n")
            else:
                tier = tier_of(dest)
                suffix = f" (tier: {tier})" if tier else ""
                kept.append(f"{indent}- `{dest}`{suffix}\n")
            j += 1
        if saw_bullet and not kept:
            if kind == "chain":
                out.append(lines[i])
                out.append(CHAIN_EMPTY + "\n")
            # a `Backed by methodology` heading with nothing under it is
            # dropped with its bullets: there is no placeholder convention
            # for it, and a bare bold line reads as a formatting bug. The
            # blank line above it goes too, or the removal leaves a
            # double blank where a heading used to be.
            elif out and not out[-1].strip() and j < len(lines) and not lines[j].strip():
                out.pop()
        else:
            out.append(lines[i])
            out.extend(kept)
        i = j
    return "".join(out)


def repair_playbook_xml(text: str, r: Resolver) -> str:
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        match = XML_REF.match(line.rstrip("\n"))
        if match is None:
            out.append(line)
            continue
        indent, slug = match.group(1), match.group(2)
        dest, outcome = r.resolve_slug(slug)
        r.record("xml", slug, outcome)
        if dest is None:
            continue
        out.append(f'{indent}<ref slug="{dest}" />\n')
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="report counts; write nothing")
    ap.add_argument("--report", action="store_true",
                    help="dry-run plus the per-target decision table")
    args = ap.parse_args()

    try:
        r = Resolver()
    except Abort as exc:
        print(f"repair-playbook-bridge: {exc}", file=sys.stderr)
        return 2

    write = not (args.dry_run or args.report)
    touched = 0
    for path in sorted(PLAYBOOKS.rglob("AGENTS.md")):
        text = path.read_text(encoding="utf-8")
        new = repair_agents(text, r)
        if new != text:
            touched += 1
            if write:
                path.write_text(new, encoding="utf-8")
    for path in sorted(PLAYBOOKS.rglob("content/01-playbook.xml")):
        text = path.read_text(encoding="utf-8")
        new = repair_playbook_xml(text, r)
        if new != text:
            touched += 1
            if write:
                path.write_text(new, encoding="utf-8")

    for key in sorted(r.classes):
        print(f"{key}: {r.classes[key]}")
    print(f"files {'written' if write else 'that would change'}: {touched}")
    if args.report and r.dropped:
        print("\ndropped, by target:")
        for target, n in sorted(r.dropped.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {n:4}  {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
