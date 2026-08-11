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

The `faion` binary is located via $FAION_BIN, then ../faion-cli/bin/faion,
then PATH. When it is absent the compile check is reported as skipped
(the corpus is validated far more often than the CLI is built);
--strict makes an absent binary fatal instead.

Usage:
    python3 scripts/validate-recipes.py            # all recipes
    python3 scripts/validate-recipes.py <dir>...   # named recipe dirs
    python3 scripts/validate-recipes.py --strict   # absent faion binary is fatal

Exit: 0 all recipes valid · 1 at least one finding · 2 the validator
could not run (no recipes directory, unreadable input).
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

    for finding in findings:
        print(f"FAIL {finding}")
    ok = len(targets) - len({f.split(':', 1)[0] for f in findings})
    print(f"summary: {ok}/{len(targets)} recipes pass, {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
