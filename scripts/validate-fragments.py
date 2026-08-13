#!/usr/bin/env python3
"""Validate the fragment library under skills/faion/fragments/.

A fragment is one role prompt a recipe composes. Recipes address it as
`corpus:<name>`, and the name is the file basename **flat across the
whole tree**, so the library's rules are library-wide, not per pack.
They lived as prose in `fragments/AGENTS.md`; this script is the half
of that prose a machine can hold you to.

Checked here:

  * every pack directory carries a `meta.json` valid against
    docs/schemas/fragment-pack-meta.schema.json (a pack without one
    inherits the skill-level tier silently, which is a tier bug that
    reads as an omission)
  * `group` matches the directory, and the pack slug is unique
  * fragment names are unique flat across the tree — `build/` and
    `research/` may not both ship a `market-analyst`
  * every `{{include:<ref>}}` resolves to a fragment file, is a
    `corpus:` reference, and does not cycle
  * a `<name>.schema.md` has a `<name>.md` beside it and parses as JSON
  * ROLE fragments (opening line `You are a|an|the <role>.`) state a
    hard boundary, gather their slots under a trailing `Inputs:`
    heading, and declare no slot above it. Shared include blocks and
    emitted blocks are deliberately exempt: `research-source-discipline`
    declares no slots on purpose, and `search-refine` is text the CLI
    prints to a user, not a role handed to a subagent
  * the 80-line body cap
  * a fragment that names a tool is gated at or above that tool's pack
    — a free fragment naming a solo tool is an instruction its reader
    cannot follow
  * `fragments/INDEX.xml` agrees with the tree (`scripts/regen-fragment-index.py`)

Recipe-side rules — fragment tier <= recipe tier, slot coverage,
reference resolution from a recipe — live in `validate-recipes.py`,
which is the script that already reads both sides.

Usage:
    python3 scripts/validate-fragments.py            # whole library
    python3 scripts/validate-fragments.py <pack>...  # named pack dirs

Exit: 0 clean · 1 at least one finding · 2 the validator could not run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_check import SchemaError, check, load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FRAGMENTS = ROOT / "skills" / "faion" / "fragments"
TOOLS = ROOT / "skills" / "faion" / "tools"
SCHEMA = ROOT / "docs" / "schemas" / "fragment-pack-meta.schema.json"

TIER_ORDER = {"free": 0, "solo": 1, "pro": 2, "geek": 3}
MAX_BODY_LINES = 80

SLOT = re.compile(r"\{\{slot(\??):([A-Za-z0-9_][A-Za-z0-9_.-]*)\}\}")
INCLUDE = re.compile(r"\{\{include:([^}]+)\}\}")
ROLE_LINE = re.compile(r"^You are (?:an?|the) ([^.]*)\.", re.MULTILINE)
INPUTS_HEADING = re.compile(r"^Inputs:\s*$", re.MULTILINE)
HARD_BOUNDARY = re.compile(r"hard boundary", re.IGNORECASE)

NON_FRAGMENT = {"AGENTS.md", "CLAUDE.md", "INDEX.xml"}


def packs(base: Path) -> list[Path]:
    return sorted(d for d in base.iterdir() if d.is_dir())


def fragment_files(pack: Path) -> list[Path]:
    return sorted(p for p in pack.glob("*.md")
                  if p.name not in NON_FRAGMENT and not p.name.endswith(".schema.md"))


def tool_tiers() -> dict[str, str]:
    """Tool name -> the tier of the pack that ships it."""
    out: dict[str, str] = {}
    if not TOOLS.is_dir():
        return out
    for meta_path in sorted(TOOLS.glob("*/meta.json")):
        try:
            tier = json.loads(meta_path.read_text(encoding="utf-8")).get("tier")
        except (OSError, json.JSONDecodeError):
            continue
        for card in sorted((meta_path.parent / "tools").glob("*.card.md")):
            out[card.name[: -len(".card.md")]] = tier
    return out


def check_index(names: dict[str, Path], pack_slugs: dict[str, Path]) -> list[str]:
    """fragments/INDEX.xml must describe the tree that is actually there."""
    index = FRAGMENTS / "INDEX.xml"
    if not index.is_file():
        return ["INDEX.xml is missing — run python3 scripts/regen-fragment-index.py"]
    try:
        root = ET.parse(index).getroot()
    except ET.ParseError as exc:
        return [f"INDEX.xml: xml parse error: {exc}"]
    findings = []
    entries = root.findall("pack")
    if root.get("count") != str(len(entries)):
        findings.append(f"INDEX.xml: count={root.get('count')!r} but it holds "
                        f"{len(entries)} <pack> entries")
    slugs = [e.get("slug") or "" for e in entries]
    if slugs != sorted(slugs):
        findings.append("INDEX.xml: <pack> entries are not alphabetical by slug")
    indexed = {e.get("slug") for e in entries}
    for slug in sorted(set(pack_slugs) - indexed):
        findings.append(f"INDEX.xml: pack {slug!r} is on disk and not in the index")
    for slug in sorted(indexed - set(pack_slugs)):
        findings.append(f"INDEX.xml: pack {slug!r} is indexed and not on disk")
    listed = {f.get("name") for f in root.iter("fragment")}
    for name in sorted(set(names) - listed):
        findings.append(f"INDEX.xml: fragment {name!r} is on disk and not in the index")
    for name in sorted(listed - set(names)):
        findings.append(f"INDEX.xml: fragment {name!r} is indexed and not on disk")
    if findings:
        findings.append("INDEX.xml is generated — run "
                        "python3 scripts/regen-fragment-index.py")
    return findings


def check_pack(pack: Path, schema: dict, all_names: dict[str, Path],
               tools: dict[str, str]) -> tuple[list[str], str | None, str | None]:
    """Findings for one pack, plus its slug and tier for the caller."""
    findings: list[str] = []
    rel = pack.relative_to(FRAGMENTS)

    def fail(msg: str) -> None:
        findings.append(f"{rel}: {msg}")

    meta_path = pack / "meta.json"
    if not meta_path.is_file():
        fail("no meta.json — the pack would inherit the skill-level tier silently")
        return findings, None, None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"meta.json is not valid JSON: {exc}")
        return findings, None, None
    for problem in check(meta, schema):
        fail(f"meta.json: {problem}")
    if meta.get("group") != pack.name:
        fail(f"meta.json group {meta.get('group')!r} != directory {pack.name!r}")
    tier = meta.get("tier")

    files = fragment_files(pack)
    if not files:
        fail("holds no fragment — an empty pack is a tier entry gating nothing")

    for path in sorted(pack.glob("*.schema.md")):
        base = pack / f"{path.name[: -len('.schema.md')]}.md"
        if not base.is_file():
            fail(f"{path.name}: no {base.name} beside it — a schema is paired "
                 "with the fragment whose output it constrains")
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path.name}: not valid JSON: {exc}")

    for path in files:
        name = path.stem
        body = path.read_text(encoding="utf-8")
        lines = body.splitlines()
        if len(lines) > MAX_BODY_LINES:
            fail(f"{path.name}: {len(lines)} lines, cap is {MAX_BODY_LINES}")

        for match in INCLUDE.finditer(body):
            ref = match.group(1).strip()
            if not ref.startswith("corpus:"):
                fail(f"{path.name}: include {ref!r} is not a corpus: reference — "
                     "a bare reference resolves against user space first")
                continue
            target = ref.split(":", 1)[1]
            if target == name:
                fail(f"{path.name}: includes itself")
            elif target not in all_names:
                fail(f"{path.name}: include {ref!r} resolves to no fragment")

        role = ROLE_LINE.search(body)
        slots = list(SLOT.finditer(body))
        if role:
            if not HARD_BOUNDARY.search(body):
                fail(f"{path.name}: a role fragment states its hard boundary — "
                     "what it writes and what it must never touch")
            heading = INPUTS_HEADING.search(body)
            if slots and heading is None:
                fail(f"{path.name}: declares slots and has no trailing "
                     "'Inputs:' heading to gather them under")
            elif heading is not None:
                early = [m.group(2) for m in slots if m.start() < heading.start()]
                if early:
                    fail(f"{path.name}: slot(s) {', '.join(sorted(set(early)))} "
                         "appear above the 'Inputs:' heading — static text first, "
                         "slots last")

        for tool, tool_tier in tools.items():
            if not re.search(rf"\b{re.escape(tool)}\b", body):
                continue
            if tier and TIER_ORDER.get(tool_tier, 0) > TIER_ORDER.get(tier, 0):
                fail(f"{path.name}: names the tool {tool!r} (tier {tool_tier}) "
                     f"from a tier-{tier} pack — the reader who can load this "
                     "fragment cannot run the tool it tells them to run")

    return findings, meta.get("slug"), tier


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="*", help="pack directories (default: all)")
    args = ap.parse_args()

    if not FRAGMENTS.is_dir():
        print(f"validate-fragments: no fragments directory at {FRAGMENTS}",
              file=sys.stderr)
        return 2
    try:
        schema = load(SCHEMA)
    except OSError as exc:
        print(f"validate-fragments: {exc}", file=sys.stderr)
        return 2

    every_pack = packs(FRAGMENTS)
    all_names: dict[str, Path] = {}
    findings: list[str] = []
    for pack in every_pack:
        for path in fragment_files(pack):
            if path.stem in all_names:
                findings.append(
                    f"{pack.name}/{path.name}: name {path.stem!r} already ships at "
                    f"{all_names[path.stem].relative_to(FRAGMENTS)} — corpus names "
                    "are flat, so the reference is ambiguous")
            else:
                all_names[path.stem] = path

    targets = ([Path(d).resolve() for d in args.dirs] if args.dirs else every_pack)
    for target in targets:
        if not target.is_dir():
            print(f"validate-fragments: not a directory: {target}", file=sys.stderr)
            return 2

    tools = tool_tiers()
    slugs: dict[str, Path] = {}
    try:
        for pack in every_pack:
            pack_findings, slug, _ = check_pack(pack, schema, all_names, tools)
            if slug:
                if slug in slugs:
                    findings.append(f"{pack.name}: slug {slug!r} already used by "
                                    f"{slugs[slug].name}")
                slugs[slug] = pack
            if pack in targets:
                findings += pack_findings
    except SchemaError as exc:
        print(f"validate-fragments: {SCHEMA.name}: {exc}", file=sys.stderr)
        return 2

    if not args.dirs:
        findings += check_index(all_names, slugs)

    for finding in findings:
        print(f"FAIL {finding}")
    print(f"summary: {len(targets)} pack(s), {len(all_names)} fragment(s), "
          f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
