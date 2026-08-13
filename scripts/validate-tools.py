#!/usr/bin/env python3
"""Validate the tool packs under skills/faion/tools/.

A tool pack is a `meta.json` gating a `scripts/` directory of real,
dependency-free executables and a `tools/` directory of instruction
cards. The **card is the contract**: an agent must be able to run the
tool having read `tools/<name>.card.md` and nothing else, never the
script. That rule had no enforcement at all — tools were the one part
of the composable layer with zero validation — so a card could drift
from its script and the only symptom would be an agent passing an
argument the script does not have.

Checked here:

  * `meta.json` valid against docs/schemas/tool-pack-meta.schema.json,
    with `group` matching the directory
  * layout: every card has a script and every script has a card
  * card shape via docs/schemas/card.schema.json — the six ordered
    sections and the 40-line cap
  * `## Invoke` writes the script's own position as `{script}` and
    carries no literal `scripts/` path: the CLI substitutes the
    materialised absolute path into the placeholder, and a literal path
    resolves only through a shim that guesses from the filename
  * **the card's documented arguments match the script's actual
    interface**, both directions — an undocumented flag is a capability
    no agent can reach, a documented flag the script does not define is
    an invocation that fails
  * every exit status the script can return is documented on the card
  * the script contract: a shebang, and stdlib imports only
  * `tools/INDEX.xml` agrees with the tree (`scripts/regen-fragment-index.py`)

Usage:
    python3 scripts/validate-tools.py            # every pack
    python3 scripts/validate-tools.py <pack>...  # named pack dirs

Exit: 0 clean · 1 at least one finding · 2 the validator could not run.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# `schema_check.py` sits beside this file. Load it from that absolute
# path rather than by name: a bare `from schema_check import ...` leans
# on sys.path[0] being this directory, which is true only when this file
# is the invoked script, and is unresolvable to a static checker that
# does not replay a sys.path mutation.
_spec = importlib.util.spec_from_file_location(
    "faion_schema_check", Path(__file__).resolve().parent / "schema_check.py")
if _spec is None or _spec.loader is None:  # pragma: no cover - packaging error
    raise ImportError("cannot load schema_check.py beside this script")
schema_check = importlib.util.module_from_spec(_spec)
sys.modules.setdefault(_spec.name, schema_check)
_spec.loader.exec_module(schema_check)
SchemaError, check, load = (schema_check.SchemaError, schema_check.check,
                            schema_check.load)

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "skills" / "faion" / "tools"
META_SCHEMA = ROOT / "docs" / "schemas" / "tool-pack-meta.schema.json"
CARD_SCHEMA = ROOT / "docs" / "schemas" / "card.schema.json"

CARD_SUFFIX = ".card.md"

FLAG = re.compile(r"--[a-z][a-z0-9-]*")
ADD_ARGUMENT = re.compile(r"""add_argument\(\s*['"](--[a-z0-9-]+)['"]""")
SH_CASE_ARM = re.compile(r"^\s*(--[a-z0-9-]+(?:\|--[a-z0-9-]+)*)\)", re.MULTILINE)
SH_EXIT = re.compile(r"^\s*exit\s+(\d+)", re.MULTILINE)
CARD_EXIT_CODES = re.compile(r"`(\d+)`")


def parse_card(path: Path) -> dict:
    """The card as the object docs/schemas/card.schema.json describes."""
    lines = path.read_text(encoding="utf-8").splitlines()
    count = len(lines)
    while count and not lines[count - 1].strip():
        count -= 1
    sections: list[str] = []
    bodies: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections.append(current)
            bodies.setdefault(current, [])
            continue
        if current is not None:
            bodies[current].append(line)
    return {
        "name": path.name[: -len(CARD_SUFFIX)],
        "title": lines[0].strip() if lines else "",
        "sections": sections,
        "lines": count,
        "invoke": "\n".join(bodies.get("Invoke", [])).strip(),
        "inputs": "\n".join(bodies.get("Inputs", [])).strip(),
        "outputs": "\n".join(bodies.get("Outputs", [])).strip(),
    }


def script_flags(script: Path, body: str) -> set[str]:
    """Every long option the script's own parser defines."""
    if script.suffix == ".py":
        return set(ADD_ARGUMENT.findall(body))
    flags: set[str] = set()
    for arm in SH_CASE_ARM.findall(body):
        flags.update(arm.split("|"))
    return flags


def script_exits(script: Path, body: str) -> set[int]:
    """Every exit status the script can hand back.

    For Python this reads `return <int>` inside `def main` plus any
    literal `sys.exit(<int>)`; scoping to main matters, because a
    heredoc of nginx config in the module body contains `return 301`
    and it is not an exit status.
    """
    if script.suffix != ".py":
        return {int(code) for code in SH_EXIT.findall(body)}
    try:
        tree = ast.parse(body)
    except SyntaxError:
        return set()
    codes: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "exit" and node.args \
                and isinstance(node.args[0], ast.Constant) \
                and isinstance(node.args[0].value, int):
            codes.add(node.args[0].value)
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                or node.name != "main":
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Return) and isinstance(inner.value, ast.Constant) \
                    and isinstance(inner.value.value, int):
                codes.add(inner.value.value)
            if isinstance(inner, ast.IfExp):
                for branch in (inner.body, inner.orelse):
                    if isinstance(branch, ast.Constant) and isinstance(branch.value, int):
                        codes.add(branch.value)
    return codes


def non_stdlib_imports(body: str) -> set[str]:
    try:
        tree = ast.parse(body)
    except SyntaxError:
        return set()
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.add(node.module.split(".")[0])
    return {m for m in modules if m not in sys.stdlib_module_names}


def check_index(packs: dict[str, Path], tools: set[str]) -> list[str]:
    index = TOOLS / "INDEX.xml"
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
    indexed = {e.get("slug") or "" for e in entries}
    for slug in sorted(set(packs) - indexed):
        findings.append(f"INDEX.xml: pack {slug!r} is on disk and not in the index")
    for slug in sorted(indexed - set(packs)):
        findings.append(f"INDEX.xml: pack {slug!r} is indexed and not on disk")
    listed = {t.get("name") or "" for t in root.iter("tool")}
    for name in sorted(tools - listed):
        findings.append(f"INDEX.xml: tool {name!r} is on disk and not in the index")
    for name in sorted(listed - tools):
        findings.append(f"INDEX.xml: tool {name!r} is indexed and not on disk")
    if findings:
        findings.append("INDEX.xml is generated — run "
                        "python3 scripts/regen-fragment-index.py")
    return findings


def check_tool(name: str, card: Path, script: Path, card_schema: dict,
               fail) -> None:
    parsed = parse_card(card)
    if parsed["title"] != f"# {name}":
        fail(f"{card.name}: first line must be '# {name}', got {parsed['title']!r}")
    for problem in check(parsed, card_schema):
        fail(f"{card.name}: {problem}")

    invoke = parsed["invoke"]
    if "{script}" not in invoke:
        fail(f"{card.name}: ## Invoke does not write the script's position as "
             "'{script}' — the CLI substitutes the materialised path there")
    if re.search(r"\bscripts/", invoke):
        fail(f"{card.name}: ## Invoke carries a literal scripts/ path, correct "
             "only inside this repo")

    body = script.read_text(encoding="utf-8")
    if not body.startswith("#!"):
        fail(f"{script.name}: no shebang")
    for module in sorted(non_stdlib_imports(body)):
        fail(f"{script.name}: imports {module!r}, which is not in the standard "
             "library — a tool pack ships no dependencies")

    documented = set(FLAG.findall(parsed["inputs"]))
    mentioned = documented | set(FLAG.findall(invoke))
    actual = script_flags(script, body)
    for flag in sorted(actual - documented):
        fail(f"{card.name}: {flag} is defined by {script.name} and is not in "
             "## Inputs — the card is the contract, and an agent may never read "
             "the script to find an argument")
    for flag in sorted(mentioned - actual):
        fail(f"{card.name}: documents {flag}, which {script.name} does not "
             "define — an invocation that fails")

    coded = {int(code) for code in CARD_EXIT_CODES.findall(parsed["outputs"])}
    for code in sorted(script_exits(script, body) - coded):
        fail(f"{card.name}: ## Outputs does not say what exit {code} means")


def check_pack(pack: Path, meta_schema: dict, card_schema: dict) -> tuple[list[str], str | None, set[str]]:
    findings: list[str] = []
    names: set[str] = set()

    def fail(msg: str) -> None:
        findings.append(f"{pack.name}: {msg}")

    meta_path = pack / "meta.json"
    if not meta_path.is_file():
        fail("no meta.json — the pack would inherit the skill-level tier silently")
        return findings, None, names
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"meta.json is not valid JSON: {exc}")
        return findings, None, names
    for problem in check(meta, meta_schema):
        fail(f"meta.json: {problem}")
    if meta.get("group") != pack.name:
        fail(f"meta.json group {meta.get('group')!r} != directory {pack.name!r}")

    cards = sorted((pack / "tools").glob(f"*{CARD_SUFFIX}"))
    scripts = sorted(p for p in (pack / "scripts").glob("*")
                     if p.is_file() and p.suffix in (".py", ".sh"))
    if not cards:
        fail("holds no card — a pack an agent cannot read is not a pack")

    by_name = {p.stem: p for p in scripts}
    for card in cards:
        name = card.name[: -len(CARD_SUFFIX)]
        names.add(name)
        script = by_name.pop(name, None)
        if script is None:
            fail(f"{card.name}: no scripts/{name}.py|sh to run")
            continue
        check_tool(name, card, script, card_schema, fail)
    for orphan in sorted(by_name):
        fail(f"scripts/{by_name[orphan].name}: no tools/{orphan}{CARD_SUFFIX} — "
             "an agent may never open a script to work out its arguments, so a "
             "carded tool is the only kind that exists")

    return findings, meta.get("slug"), names


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="*", help="tool pack directories (default: all)")
    args = ap.parse_args()

    if not TOOLS.is_dir():
        print(f"validate-tools: no tools directory at {TOOLS}", file=sys.stderr)
        return 2
    try:
        meta_schema = load(META_SCHEMA)
        card_schema = load(CARD_SCHEMA)
    except OSError as exc:
        print(f"validate-tools: {exc}", file=sys.stderr)
        return 2

    every = sorted(d for d in TOOLS.iterdir() if d.is_dir())
    targets = [Path(d).resolve() for d in args.dirs] if args.dirs else every
    for target in targets:
        if not target.is_dir():
            print(f"validate-tools: not a directory: {target}", file=sys.stderr)
            return 2

    findings: list[str] = []
    slugs: dict[str, Path] = {}
    all_tools: set[str] = set()
    try:
        for pack in every:
            pack_findings, slug, names = check_pack(pack, meta_schema, card_schema)
            all_tools |= names
            if slug:
                if slug in slugs:
                    findings.append(f"{pack.name}: slug {slug!r} already used by "
                                    f"{slugs[slug].name}")
                slugs[slug] = pack
            if pack in targets:
                findings += pack_findings
    except SchemaError as exc:
        print(f"validate-tools: {exc}", file=sys.stderr)
        return 2

    if not args.dirs:
        findings += check_index(slugs, all_tools)

    for finding in findings:
        print(f"FAIL {finding}")
    print(f"summary: {len(targets)} pack(s), {len(all_tools)} tool(s), "
          f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
