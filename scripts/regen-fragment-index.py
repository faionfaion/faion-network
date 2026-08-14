#!/usr/bin/env python3
"""P1.1: regenerate the L2 indexes for the fragment / recipe / tool layer.

The knowledge layer routes L1 `knowledge/domains.xml` -> L2
`knowledge/<domain>/INDEX.xml`; playbooks route `playbooks/taxonomy.xml`
-> `playbooks/by-goal/<goal>/INDEX.xml`. The composable layer had no
index of any kind, so an agent could only reach `research-first-build`
by already knowing the directory existed. This script writes the
missing L2 indexes:

    skills/faion/fragments/INDEX.xml    one <pack> per fragment pack
    skills/faion/recipes/INDEX.xml      one <recipe> per recipe dir
    skills/faion/tools/INDEX.xml        one <pack> per tool pack

Every entry is derived from the pack's own `meta.json` (slug, tier,
summary) plus what is actually on disk (fragment names, card and script
paths, stage counts), so the index cannot drift from the tree the way a
hand-kept list does. Modelled on `regen-tier-manifest.py`, which reads
`meta.json` — deliberately NOT on the deleted `build-domain-index-v2.py`,
which read YAML frontmatter no envelope carries and emptied the file it
targeted.

`generated=` is only bumped when the body actually changes, so a rerun
on an unchanged tree is a no-op instead of a one-line diff.

Usage:
    python3 scripts/regen-fragment-index.py             # write all three
    python3 scripts/regen-fragment-index.py --dry-run   # report, write nothing
    python3 scripts/regen-fragment-index.py --check     # exit 1 if stale
    python3 scripts/regen-fragment-index.py --only fragments

Exit: 0 written / clean · 1 stale under --check · 2 the script could not
run (missing directory, unreadable meta.json).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent.parent
FRAGMENTS = ROOT / "skills" / "faion" / "fragments"
RECIPES = ROOT / "skills" / "faion" / "recipes"
TOOLS = ROOT / "skills" / "faion" / "tools"

INDEX_VERSION = "1.0"

DESCRIPTIONS = {
    "fragments": (
        "L2 index of fragment packs. A fragment is one role prompt a recipe "
        "composes; recipes address it as corpus:<name>, and the name is the "
        "file basename, flat across the whole tree. The retriever reads this "
        "after routing to the composable layer, picks the packs it needs, and "
        "only then opens a fragment body. One meta.json per pack gates every "
        "fragment beneath it. Authoring rules: fragments/AGENTS.md."
    ),
    "recipes": (
        "L2 index of workflow recipes. A recipe is a platform-neutral F027 "
        "pipeline `faion workflow build` compiles into a Claude Dynamic "
        "Workflow and a Codex chain. The retriever reads this to pick a "
        "pipeline shape, then reads that recipe's card — the card is the "
        "contract and is enough to invoke from; recipe.json is the compiler's "
        "input, not the agent's. Authoring rules: recipes/AGENTS.md."
    ),
    "tools": (
        "L2 index of tool packs. A tool is a real, dependency-free script an "
        "agent runs instead of writing a throwaway one. The retriever reads "
        "this to find an existing tool before writing code, then reads that "
        "tool's card — the card is the full contract, never the script. One "
        "meta.json per pack gates its scripts and cards. Authoring rules: "
        "tools/AGENTS.md."
    ),
}


class Abort(Exception):
    """The script cannot run — a missing tree or an unreadable meta.json."""


def load_meta(meta_path: Path) -> dict:
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Abort(f"{meta_path.relative_to(ROOT)}: {exc}") from exc


def pack_dirs(base: Path) -> list[Path]:
    """Every child directory of `base` carrying a meta.json."""
    if not base.is_dir():
        raise Abort(f"no directory at {base}")
    return sorted(d for d in base.iterdir()
                  if d.is_dir() and (d / "meta.json").is_file())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fragment_names(pack: Path) -> list[tuple[str, bool]]:
    """(fragment name, has paired schema) for every fragment in a pack."""
    out = []
    for md in sorted(pack.glob("*.md")):
        if md.name.endswith(".schema.md") or md.name in ("AGENTS.md", "CLAUDE.md"):
            continue
        name = md.stem
        out.append((name, (pack / f"{name}.schema.md").is_file()))
    return out


def tool_names(pack: Path) -> list[tuple[str, str, str]]:
    """(tool name, card path, script path) for every carded tool in a pack."""
    out = []
    for card in sorted((pack / "tools").glob("*.card.md")):
        name = card.name[: -len(".card.md")]
        scripts = sorted((pack / "scripts").glob(f"{name}.*"))
        script = rel(scripts[0]) if scripts else ""
        out.append((name, rel(card), script))
    return out


def stage_count(recipe_json: Path) -> int:
    try:
        return len(json.loads(recipe_json.read_text(encoding="utf-8")).get("stages") or [])
    except (OSError, json.JSONDecodeError) as exc:
        raise Abort(f"{rel(recipe_json)}: {exc}") from exc


def entry_open(tag: str, attrs: list[tuple[str, str]]) -> str:
    pairs = " ".join(f"{k}={quoteattr(v)}" for k, v in attrs if v != "")
    return f"  <{tag} {pairs}>"


def build_fragments() -> tuple[str, int]:
    lines: list[str] = []
    packs = pack_dirs(FRAGMENTS)
    rows = []
    for pack in packs:
        meta = load_meta(pack / "meta.json")
        rows.append((meta.get("slug") or pack.name, meta, pack))
    rows.sort(key=lambda r: r[0])
    for slug, meta, pack in rows:
        names = fragment_names(pack)
        lines.append(entry_open("pack", [
            ("slug", slug),
            ("group", meta.get("group") or pack.name),
            ("tier", meta.get("tier") or ""),
            ("fragments", str(len(names))),
            ("path", rel(pack)),
        ]))
        lines.append(f"    <summary>{escape(meta.get('summary') or '')}</summary>")
        for name, has_schema in names:
            attrs = [("name", name), ("ref", f"corpus:{name}")]
            if has_schema:
                attrs.append(("schema", f"corpus:{name}.schema"))
            pairs = " ".join(f"{k}={quoteattr(v)}" for k, v in attrs)
            lines.append(f"    <fragment {pairs}/>")
        lines.append("  </pack>")
    return "\n".join(lines), len(rows)


def build_recipes() -> tuple[str, int]:
    lines: list[str] = []
    rows = []
    for directory in pack_dirs(RECIPES):
        meta = load_meta(directory / "meta.json")
        rows.append((meta.get("slug") or directory.name, meta, directory))
    rows.sort(key=lambda r: r[0])
    for slug, meta, directory in rows:
        card = directory / f"{directory.name}.card.md"
        recipe_json = directory / "recipe.json"
        attrs = [
            ("slug", slug),
            ("name", directory.name),
            ("tier", meta.get("tier") or ""),
        ]
        if recipe_json.is_file():
            attrs.append(("stages", str(stage_count(recipe_json))))
        attrs.append(("path", rel(directory)))
        if card.is_file():
            attrs.append(("card", rel(card)))
        lines.append(entry_open("recipe", attrs))
        lines.append(f"    <summary>{escape(meta.get('summary') or '')}</summary>")
        lines.append("  </recipe>")
    return "\n".join(lines), len(rows)


def build_tools() -> tuple[str, int]:
    lines: list[str] = []
    rows = []
    for pack in pack_dirs(TOOLS):
        meta = load_meta(pack / "meta.json")
        rows.append((meta.get("slug") or pack.name, meta, pack))
    rows.sort(key=lambda r: r[0])
    for slug, meta, pack in rows:
        tools = tool_names(pack)
        lines.append(entry_open("pack", [
            ("slug", slug),
            ("group", meta.get("group") or pack.name),
            ("tier", meta.get("tier") or ""),
            ("tools", str(len(tools))),
            ("path", rel(pack)),
        ]))
        lines.append(f"    <summary>{escape(meta.get('summary') or '')}</summary>")
        for name, card, script in tools:
            attrs = [("name", name), ("card", card)]
            if script:
                attrs.append(("script", script))
            pairs = " ".join(f"{k}={quoteattr(v)}" for k, v in attrs)
            lines.append(f"    <tool {pairs}/>")
        lines.append("  </pack>")
    return "\n".join(lines), len(rows)


BUILDERS = {
    "fragments": (FRAGMENTS, build_fragments),
    "recipes": (RECIPES, build_recipes),
    "tools": (TOOLS, build_tools),
}

GENERATED_ATTR = re.compile(r'generated="[^"]*"')


def render(domain: str, today: str, previous: str | None) -> str:
    base, builder = BUILDERS[domain]
    body, count = builder()
    header = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<index domain="{domain}" count="{count}" version="{INDEX_VERSION}" '
        f'generated="{today}">\n'
        f'  <description>{escape(DESCRIPTIONS[domain])}</description>\n'
    )
    out = header + body + "\n</index>\n"
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
    ap.add_argument("--only", choices=sorted(BUILDERS),
                    help="regenerate one index instead of all three")
    ap.add_argument("--date", default=datetime.date.today().isoformat(),
                    help="value for generated= when the body changes")
    args = ap.parse_args()

    domains = [args.only] if args.only else sorted(BUILDERS)
    stale: list[str] = []
    try:
        for domain in domains:
            base, _ = BUILDERS[domain]
            target = base / "INDEX.xml"
            previous = target.read_text(encoding="utf-8") if target.is_file() else None
            out = render(domain, args.date, previous)
            # `render` returns `previous` verbatim when the body is
            # unchanged, so a hand-mangled INDEX.xml can reach here with
            # no count= at all. Report it; never crash on the match.
            found = re.search(r'count="(\d+)"', out)
            if found is None:
                raise Abort(f"{rel(target)}: no count= attribute — the file "
                            "is not a generated index; delete it and rerun")
            count = found.group(1)
            if out == previous:
                print(f"{domain}: up to date ({count} entries)")
                continue
            stale.append(domain)
            verb = "would write" if (args.dry_run or args.check) else "wrote"
            if not (args.dry_run or args.check):
                target.write_text(out, encoding="utf-8")
            print(f"{domain}: {verb} {rel(target)} ({count} entries)")
    except Abort as exc:
        print(f"regen-fragment-index: {exc}", file=sys.stderr)
        return 2

    if args.check and stale:
        print(f"STALE: {', '.join(stale)} — run "
              "python3 scripts/regen-fragment-index.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
