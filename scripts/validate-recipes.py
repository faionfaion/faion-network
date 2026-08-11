#!/usr/bin/env python3
"""Validate the workflow-recipe library under skills/faion/recipes/.

A recipe directory is three files that must agree with each other:

    <name>/meta.json         tier gate for the directory
    <name>/recipe.json       the F027 platform-neutral recipe
    <name>/<name>.card.md    the F029-shaped card the AGENT reads

The card is what an agent picks from, so a card that omits an input
the recipe demands is not a documentation nit — it is a recipe the
agent cannot invoke. This validator fails on:

  * a card missing one of the six ordered sections, or over the line cap
  * a `{{var:NAME}}` (or a declared var) absent from the card's Inputs
  * a fragment reference that resolves to no file in the corpus
  * a recipe `faion workflow validate` refuses

It also gates the fragment library on one rule that is not about
recipes at all, and belongs here because this is the script that reads
every fragment: **a research-role fragment must include the source
discipline block.** faion never goes to the internet — the calling
agent does — so the corpus's job is to demand and shape the fetch. A
research prompt that does not carry the sourcing bar asks for less
than an agent with no prompt at all, which is measured, not
hypothetical (2026-08-11: 14 competitors and 0 URLs against 31 and
108). A fragment is a research role when its opening role line names
one, or when it lives under `fragments/research/`; it satisfies the
rule by containing `{{include:corpus:research-source-discipline}}`.
The block itself must keep its four anchors, so the include can never
degrade into a pointer at an empty file.

The `faion` binary is located via $FAION_BIN, then ../faion-cli/bin/faion,
then PATH. When it is absent the compile check is reported as skipped
(the corpus is validated far more often than the CLI is built);
--strict makes an absent binary fatal instead.

Usage:
    python3 scripts/validate-recipes.py            # all recipes
    python3 scripts/validate-recipes.py <dir>...   # named recipe dirs
    python3 scripts/validate-recipes.py --strict   # absent faion binary is fatal

Exit: 0 all recipes valid and the fragment library holds · 1 at least
one finding · 2 the validator could not run (no recipes directory,
unreadable input).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "skills" / "faion" / "recipes"
FRAGMENTS = ROOT / "skills" / "faion" / "fragments"

TIERS = ("free", "solo", "pro", "geek")

CARD_SECTIONS = ("Purpose", "Invoke", "Inputs", "Outputs", "When NOT to use", "Cost")
MAX_CARD_LINES = 40

VAR_REF = re.compile(r"\{\{var:([a-zA-Z0-9_]+)\}\}")

# The shared sourcing block, and the include that pulls it in.
DISCIPLINE = "research-source-discipline"
DISCIPLINE_INCLUDE = "{{include:corpus:" + DISCIPLINE + "}}"

# A fragment's opening role line: "You are a|an|the <role>." The role
# noun is what decides, not the paragraph — "You are the concept
# synthesizer. You read the research catalogs" is not a research role,
# and an SDD intake *analyzer* is not an *analyst*.
ROLE_LINE = re.compile(r"^You are (?:an?|the) ([^.]*)\.", re.MULTILINE)
RESEARCH_ROLE = re.compile(
    r"\b(research|researcher|analyst|market|competitor|competitive|"
    r"evidence|source)\b", re.IGNORECASE)

# What the discipline block must actually say, so that including it
# means something. One probe per requirement, deliberately loose about
# wording and strict about the requirement existing at all. Probed
# against the block with its whitespace collapsed, because a fragment
# is hard-wrapped at ~68 columns and a requirement does not stop being
# stated because it fell across a line break.
DISCIPLINE_ANCHORS = (
    ("a URL and an access date on every load-bearing claim",
     re.compile(r"URL and the date you accessed", re.IGNORECASE)),
    ("the H/M/L confidence definitions",
     re.compile(r"- H —.*?- M —.*?- L —")),
    ("the no-reliable-figure path",
     re.compile(r"no reliable public figure found", re.IGNORECASE)),
    ("the recalled-not-verified label",
     re.compile(r"recalled from training, not re-verified", re.IGNORECASE)),
    ("faion fact add provenance",
     re.compile(r"faion fact add .*?--source", re.IGNORECASE)),
)


def find_faion() -> str | None:
    """Locate the faion binary: env override, sibling checkout, PATH."""
    env = os.environ.get("FAION_BIN")
    if env and Path(env).is_file() and os.access(env, os.X_OK):
        return env
    sibling = ROOT.parent / "faion-cli" / "bin" / "faion"
    if sibling.is_file() and os.access(sibling, os.X_OK):
        return str(sibling)
    return shutil.which("faion")


def fragment_refs(recipe: dict) -> list[tuple[str, str]]:
    """Every fragment reference in a recipe, as (json-path, ref) pairs."""
    refs: list[tuple[str, str]] = []
    for i, stage in enumerate(recipe.get("stages") or []):
        where = f"stages[{i}]"
        if stage.get("prompt"):
            refs.append((f"{where}.prompt", stage["prompt"]))
        schema = (stage.get("output") or {}).get("schema")
        if schema:
            refs.append((f"{where}.output.schema", schema))
        gate = stage.get("gate") or {}
        for key in ("verifier", "verifier_schema", "fixer"):
            if gate.get(key):
                refs.append((f"{where}.gate.{key}", gate[key]))
    return refs


def resolve_fragment(ref: str) -> Path | None:
    """Resolve `corpus:<name>` against the corpus fragment tree."""
    name = ref.split(":", 1)[1]
    for path in FRAGMENTS.rglob(f"{name}.md"):
        return path
    return None


def card_sections(lines: list[str]) -> list[str]:
    """The card's H2 headings, in file order."""
    return [ln[3:].strip() for ln in lines if ln.startswith("## ")]


def section_body(lines: list[str], heading: str) -> str:
    """The body of one H2 section, empty when the section is absent."""
    out: list[str] = []
    inside = False
    for ln in lines:
        if ln.startswith("## "):
            inside = ln[3:].strip() == heading
            continue
        if inside:
            out.append(ln)
    return "\n".join(out)


def check_card(name: str, card: Path, declared: set[str], referenced: set[str],
               fail) -> None:
    """Card shape, line cap, and Inputs coverage of every var."""
    lines = card.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != f"# {name}":
        fail(f"{card.name}: first line must be '# {name}'")
    count = len(lines)
    while count and not lines[count - 1].strip():
        count -= 1
    if count > MAX_CARD_LINES:
        fail(f"{card.name}: {count} lines, cap is {MAX_CARD_LINES}")

    found = card_sections(lines)
    if found != list(CARD_SECTIONS):
        missing = [s for s in CARD_SECTIONS if s not in found]
        if missing:
            fail(f"{card.name}: missing section(s): {', '.join(missing)}")
        else:
            fail(f"{card.name}: sections out of order or extra: "
                 f"{' | '.join(found)}")

    inputs = section_body(lines, "Inputs")
    for var in sorted(declared | referenced):
        if f"`{var}`" not in inputs:
            fail(f"{card.name}: var '{var}' is not documented in ## Inputs")


def is_research_role(path: Path, body: str) -> bool:
    """Whether this fragment claims a role that goes and sources things."""
    if path.parent.name == "research":
        return True
    match = ROLE_LINE.search(body)
    return bool(match and RESEARCH_ROLE.search(match.group(1)))


def check_fragments() -> list[str]:
    """Every research-role fragment carries the source discipline block."""
    findings: list[str] = []
    if not FRAGMENTS.is_dir():
        return findings

    block = FRAGMENTS / "research" / f"{DISCIPLINE}.md"
    if not block.is_file():
        return [f"fragments: {DISCIPLINE}.md is missing — every research "
                "role includes it, so its absence breaks them all"]

    flat = " ".join(block.read_text(encoding="utf-8").split())
    for what, probe in DISCIPLINE_ANCHORS:
        if not probe.search(flat):
            findings.append(f"fragments: {DISCIPLINE}.md does not state "
                            f"{what} — the block every research role "
                            "includes must carry the bar, not point at it")

    for path in sorted(FRAGMENTS.rglob("*.md")):
        if path.name.endswith(".schema.md") or path == block:
            continue
        body = path.read_text(encoding="utf-8")
        if not is_research_role(path, body):
            continue
        if DISCIPLINE_INCLUDE not in body:
            rel = path.relative_to(FRAGMENTS)
            findings.append(
                f"fragments: {rel} is a research role and does not include "
                f"'{DISCIPLINE_INCLUDE}' — the corpus instructs the fetch, "
                "it never substitutes for it")
    return findings


def check_recipe(directory: Path, faion: str | None, strict: bool) -> list[str]:
    """Validate one recipe directory; returns its findings."""
    findings: list[str] = []
    name = directory.name

    def fail(msg: str) -> None:
        findings.append(f"{name}: {msg}")

    meta_path = directory / "meta.json"
    recipe_path = directory / "recipe.json"
    card_path = directory / f"{name}.card.md"

    for required in (meta_path, recipe_path, card_path):
        if not required.is_file():
            fail(f"missing {required.name}")
    if findings:
        return findings

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"meta.json is not valid JSON: {exc}")
        return findings
    if meta.get("tier") not in TIERS:
        fail(f"meta.json tier {meta.get('tier')!r} is not one of {TIERS}")

    try:
        recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"recipe.json is not valid JSON: {exc}")
        return findings

    if recipe.get("name") != name:
        fail(f"recipe.json name {recipe.get('name')!r} != directory {name!r}")

    declared = set((recipe.get("vars") or {}).keys())
    referenced = set(VAR_REF.findall(json.dumps(recipe)))
    for var in sorted(referenced - declared):
        fail(f"recipe.json references undeclared var '{var}'")

    check_card(name, card_path, declared, referenced, fail)

    for where, ref in fragment_refs(recipe):
        if not ref.startswith("corpus:"):
            fail(f"{where}: {ref!r} is not a corpus: reference — a shipped "
                 "recipe may only compose corpus fragments")
            continue
        if resolve_fragment(ref) is None:
            fail(f"{where}: fragment {ref!r} resolves to no file under "
                 "skills/faion/fragments/")

    if faion is None:
        if strict:
            fail("faion binary not found and --strict was given")
        return findings

    args = [faion, "workflow", "validate", str(recipe_path)]
    for var, spec in (recipe.get("vars") or {}).items():
        if spec.get("required"):
            args += ["--var", f"{var}=validate-recipes-placeholder"]
    proc = subprocess.run(args, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()
        fail("faion workflow validate refused the recipe: "
             + " / ".join(tail[-3:]))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dirs", nargs="*", help="recipe directories (default: all)")
    parser.add_argument("--strict", action="store_true",
                        help="an absent faion binary is a failure, not a skip")
    args = parser.parse_args()

    if args.dirs:
        targets = [Path(d).resolve() for d in args.dirs]
    else:
        if not RECIPES.is_dir():
            print(f"validate-recipes: no recipes directory at {RECIPES}",
                  file=sys.stderr)
            return 2
        targets = sorted(d for d in RECIPES.iterdir() if d.is_dir())

    if not targets:
        print("validate-recipes: no recipe directories found", file=sys.stderr)
        return 2

    faion = find_faion()
    if faion is None:
        print("validate-recipes: faion binary not found — compile check "
              "skipped (set FAION_BIN or build ../faion-cli)", file=sys.stderr)

    findings: list[str] = []
    for directory in targets:
        if not directory.is_dir():
            print(f"validate-recipes: not a directory: {directory}",
                  file=sys.stderr)
            return 2
        findings += check_recipe(directory, faion, args.strict)

    ok = len(targets) - len({f.split(':', 1)[0] for f in findings})

    # Library-wide, so it runs even when named recipe dirs were given:
    # a research fragment that drops the sourcing block breaks every
    # recipe composing it, including the ones not named on this line.
    fragment_findings = check_fragments()
    findings += fragment_findings

    for finding in findings:
        print(f"FAIL {finding}")
    print(f"summary: {ok}/{len(targets)} recipes pass, "
          f"{len(fragment_findings)} fragment finding(s), "
          f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
