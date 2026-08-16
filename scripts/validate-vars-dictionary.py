#!/usr/bin/env python3
"""Validator 11: the variable dictionary and its resolver.

`skills/faion/templates/` shipped with NO gate. Nothing in `scripts/` opened
either file, so a resolver rule naming an entry that had been renamed or
deleted went dead in silence: `tpl-jinja` would stop emitting that `$ref` and
quietly fall back to a local declaration, which looks exactly like "this
template just needs review" — the failure is indistinguishable from the normal
outcome. That is the same shape as the vacuous gates found across this corpus
(`content_id` declared a hash and matching 0 of 2,520; a rule check satisfied
by all 16,147 rules declaring `testable="true"`), and the fix is the same: a
check that can actually fail.

What is enforced:
  D1  the dictionary parses, is draft-07, and carries a non-empty `$defs`
  D2  every entry has `type`, `title` and a `description`
  D3  a description is <= 240 chars — the cap a human reads under an
      AskUserQuestion prompt, matching validate-methodology-templates.py
  D4  `x-faion-sensitive` implies `x-faion-placeholder`: a sensitive value
      never travels, so the assembler needs something to emit in its place
  D5  an `enum` is a non-empty list of unique scalars
  D6  entry names match the same `^[a-z][a-z0-9_]{0,63}$` the template
      `variables:` contract uses, so a dictionary name is always a legal
      template variable name
  R1  every resolver rule carries `id`, `name`, `entry`, `when`, `why`
  R2  rule ids are unique
  R3  **every rule's `entry` exists in the dictionary** — the dead-pointer
      check this file exists for
  R4  every regex in a rule's `when` compiles
  R5  the resolver's declared `dictionary` path resolves to the file actually
      being validated, so the two cannot drift apart unnoticed

Usage:
    python3 scripts/validate-vars-dictionary.py
    python3 scripts/validate-vars-dictionary.py <templates-dir>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "skills" / "faion" / "templates"

VAR_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
DESC_CAP = 240

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.name}: not valid JSON: {exc}")
    except OSError as exc:
        fail(f"{path.name}: unreadable: {exc}")
    return None


def validate_dictionary(path: Path) -> set[str]:
    doc = _load(path)
    if doc is None:
        return set()
    schema = str(doc.get("$schema", ""))
    if "draft-07" not in schema:
        fail(f"{path.name}: $schema is {schema!r}, not draft-07 — the corpus's "
             "2,081 output contracts are draft-07 and $ref only composes "
             "across one dialect")
    defs = doc.get("$defs")
    if not isinstance(defs, dict) or not defs:
        fail(f"{path.name}: no non-empty `$defs` map")
        return set()

    for name, entry in sorted(defs.items()):
        at = f"{path.name}: {name!r}"
        if not VAR_NAME.match(name):
            fail(f"{at}: does not match ^[a-z][a-z0-9_]{{0,63}}$, so it cannot "
                 "be used as a template variable name")
        if not isinstance(entry, dict):
            fail(f"{at}: not an object")
            continue
        for key in ("type", "title", "description"):
            if not str(entry.get(key, "")).strip():
                fail(f"{at}: has no {key!r}")
        desc = str(entry.get("description", ""))
        if len(desc) > DESC_CAP:
            fail(f"{at}: description is {len(desc)} chars, over the "
                 f"{DESC_CAP}-char cap a human reads under a prompt")
        if entry.get("x-faion-sensitive") and \
                not str(entry.get("x-faion-placeholder", "")).strip():
            fail(f"{at}: sensitive with no `x-faion-placeholder` — a sensitive "
                 "value never travels, so the assembler needs something to emit")
        if "enum" in entry:
            options = entry["enum"]
            if not isinstance(options, list) or not options:
                fail(f"{at}: `enum` is not a non-empty list")
            elif len(set(map(str, options))) != len(options):
                fail(f"{at}: `enum` repeats a value: {options!r}")
    print(f"{path.name}: {len(defs)} entries")
    return set(defs)


def validate_resolver(path: Path, entries: set[str], dict_path: Path) -> None:
    if not path.exists():
        print(f"{path.name}: absent (optional)")
        return
    doc = _load(path)
    if doc is None:
        return

    declared = str(doc.get("dictionary", "")).strip()
    if declared:
        target = (path.parent / declared).resolve()
        if target != dict_path.resolve():
            fail(f"{path.name}: `dictionary` points at {declared!r}, which is "
                 f"not the dictionary being validated ({dict_path.name})")

    rules = doc.get("rules")
    if not isinstance(rules, list) or not rules:
        fail(f"{path.name}: no non-empty `rules` list")
        return

    seen: set[str] = set()
    for i, rule in enumerate(rules):
        at = f"{path.name}: rule {rule.get('id', i) if isinstance(rule, dict) else i!r}"
        if not isinstance(rule, dict):
            fail(f"{at}: not an object")
            continue
        for key in ("id", "name", "entry", "when", "why"):
            if key not in rule or not rule[key]:
                fail(f"{at}: has no {key!r}")
        rid = str(rule.get("id", ""))
        if rid:
            if rid in seen:
                fail(f"{at}: duplicate rule id {rid!r}")
            seen.add(rid)
        entry = str(rule.get("entry", ""))
        # R3 — the whole reason this validator exists.
        if entry and entry not in entries:
            fail(f"{at}: resolves to {entry!r}, which is not in the "
                 "dictionary. A rule pointing at a renamed or deleted entry "
                 "does not raise at runtime — it silently stops resolving, "
                 "which is indistinguishable from the template simply needing "
                 "review")
        when = rule.get("when")
        if isinstance(when, dict):
            for field, pattern in when.items():
                if not isinstance(pattern, str):
                    fail(f"{at}: `when.{field}` is not a string")
                    continue
                try:
                    re.compile(pattern)
                except re.error as exc:
                    fail(f"{at}: `when.{field}` is not a valid regex: {exc}")
        elif when is not None:
            fail(f"{at}: `when` is not an object")
    print(f"{path.name}: {len(rules)} rules -> {len(entries)} entries")


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else TEMPLATES_DIR
    dictionary = target / "vars-dictionary.schema.json"
    resolver = target / "vars-resolver.json"

    if not dictionary.exists():
        print(f"FAIL: {dictionary} not found", file=sys.stderr)
        return 1

    entries = validate_dictionary(dictionary)
    validate_resolver(resolver, entries, dictionary)

    if errors:
        print(f"FAIL: {len(errors)} problem(s)", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("OK: variable dictionary and resolver valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
