#!/usr/bin/env python3
"""tpl-params.py — inspect, resolve and store a template's declared parameters.

tpl-build refuses a required parameter it cannot fill. This is the tool that
says which ones those are and what to ask for each: every declared parameter
with its type, whether it is required, its default, and whether the project
store already answers it — plus an --ask mode whose JSON is exactly the
question list an agent turns into prompts.

A `text` parameter is prose an LLM composes from the user's answer. This tool
never generates it. It reports the question and accepts the answer as a value.

A `sensitive: true` parameter is never written to the store: 2.2 says the value
never travels, so the store records the parameter's existence and its
placeholder and nothing else. A value that merely looks like a secret is
refused too, whatever the declaration says — two checks, neither trusting the
other.

Input:  --template {file} | [--blocks {dir}] --use {kind/name or path.md,...}
Output: a table, or JSON under --ask / --json. The store is
        {project}/.faion/template-params.json.

Exit: 0 every parameter resolved · 1 the template is invalid · 2 the tool could
      not run · 3 parameters remain unresolved · 4 a supplied value refused.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

NAME = "tpl-params"


def _load_core():
    """Load the pack helper by absolute path — see tpl-build.py for why."""
    here = Path(__file__).resolve().parent
    for candidate in (here / "lib" / "tplcore.py",
                      here / "scripts" / "lib" / "tplcore.py",
                      here.parent / "scripts" / "lib" / "tplcore.py"):
        if candidate.is_file():
            spec = importlib.util.spec_from_file_location(
                "faion_tplcore", candidate)
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            sys.modules.setdefault("faion_tplcore", module)
            spec.loader.exec_module(module)
            return module
    return None


CORE = _load_core()

FIXTURE = """<!--
purpose: service runbook
produces: markdown runbook
variables:
  - name: service_name
    type: string
    required: true
    description: The systemd unit and process identity.
  - name: port
    type: integer
    required: true
    default: "8000"
    description: The port the service binds.
  - name: rationale
    type: text
    required: true
    description: Why this service exists, in the operator's own words.
  - name: db_password
    type: string
    required: true
    sensitive: true
    placeholder: "__FAION_DB_PASSWORD__"
    description: Database password. Never transmitted.
-->
# {{service_name}} on {{port}}

{{rationale}}

Password: {{db_password}}
"""

BAD_FIXTURE = FIXTURE.replace("    type: integer", "    type: decimal")


def load_source(template: str | None, blocks: str | None, use: str | None):
    """One template file, or an ordered block set, as a single source."""
    if template and use:
        raise CORE.TplError("--template and --use are alternatives; to mix a "
                            "literal file into a block set, name it in --use "
                            "as a path ending .md")
    if template:
        return CORE.load_template(Path(template))
    if not use:
        raise CORE.TplError("--use is required with --blocks")
    root = None
    if blocks:
        root = Path(blocks)
        if not root.is_dir():
            raise CORE.TplError(f"--blocks {blocks}: not a directory")
    paths = CORE.resolve_blocks(root, use.split(","))
    return CORE.merge([CORE.load_template(p) for p in paths])


def apply_sets(store: dict, variables: dict[str, dict],
               pairs: list[str] | None, unsets: list[str] | None) -> list[str]:
    """Mutate the store. Returns one line per change, for the caller to print."""
    changes: list[str] = []
    for name in unsets or []:
        if store.get("params", {}).pop(name.strip(), None) is not None:
            changes.append(f"unset {name.strip()}")
    for pair in pairs or []:
        if "=" not in pair:
            raise CORE.ValueRefused(f"--set {pair!r} is not name=value")
        key, _, value = pair.partition("=")
        key = key.strip()
        if key not in variables:
            raise CORE.ValueRefused(
                f"{key}: not declared by this template; declared are "
                + (", ".join(variables) or "(none)"))
        decl = variables[key]
        if decl["sensitive"]:
            raise CORE.ValueRefused(
                f"{key}: declared sensitive, so its value is never written to "
                f"the store. The build emits {decl['placeholder']!r} and you "
                "substitute the real value locally afterwards (2.2)")
        CORE.accept_value(decl, value)
        changes.append(f"set {key} ({CORE.store_put(store, decl, value)})")
    return changes


def describe(variables: dict[str, dict], store: dict) -> list[dict]:
    """Every declared parameter plus where its value would come from."""
    rows: list[dict] = []
    for name, decl in variables.items():
        if decl["sensitive"]:
            source = "placeholder"
        elif CORE.store_value(store, name) is not None:
            source = "store"
        elif decl["default"] is not None:
            source = "default"
        else:
            source = "ask"
        rows.append({
            "name": name, "type": decl["type"], "required": decl["required"],
            "default": decl["default"], "sensitive": decl["sensitive"],
            "in_store": CORE.store_value(store, name) is not None,
            "resolved_from": source, "description": decl["description"],
        })
    return rows


def table(rows: list[dict]) -> str:
    """The human listing. One line per parameter, widest column padded."""
    head = ("name", "type", "req", "sensitive", "from", "default")
    body = [(r["name"], r["type"], "yes" if r["required"] else "no",
             "yes" if r["sensitive"] else "no", r["resolved_from"],
             "-" if r["default"] is None else r["default"]) for r in rows]
    widths = [max(len(str(c)) for c in col) for col in zip(head, *body)] \
        if body else [len(h) for h in head]
    lines = ["  ".join(h.ljust(w) for h, w in zip(head, widths)).rstrip()]
    for row in body:
        lines.append("  ".join(str(c).ljust(w)
                               for c, w in zip(row, widths)).rstrip())
    return "\n".join(lines)


def self_test() -> list[str]:
    """The store rules and the declaration rules, asserted."""
    failures: list[str] = []
    source = CORE.parse_source(FIXTURE, "fixture")
    variables = source["variables"]
    store = {"version": 1, "params": {}}

    rows = {r["name"]: r for r in describe(variables, store)}
    if rows["port"]["resolved_from"] != "default":
        failures.append("listing: a declared default was not reported")
    if rows["rationale"]["resolved_from"] != "ask":
        failures.append("listing: a text parameter with no default was not "
                        "reported as ask")
    if rows["db_password"]["resolved_from"] != "placeholder":
        failures.append("listing: a sensitive parameter was not reported as "
                        "resolving to its placeholder")

    _, questions, _ = CORE.resolve(variables, {}, store)
    asked = {q["name"]: q for q in questions}
    if "service_name" not in asked or "rationale" not in asked:
        failures.append("ask: an unresolved required parameter was not asked")
    if "db_password" in asked:
        failures.append("ask: a sensitive parameter was asked for")
    if not asked.get("rationale", {}).get("compose"):
        failures.append("ask: a text parameter was not flagged for the LLM to "
                        "compose")

    # A sensitive value never reaches the store, by either check.
    try:
        apply_sets(store, variables, ["db_password=hunter2"], None)
        failures.append("store: a sensitive parameter accepted a value")
    except CORE.ValueRefused:
        pass
    try:
        apply_sets(store, variables, ["service_name=ghp_"
                                      + "A1b2C3d4E5f6G7h8I9j0"], None)
        failures.append("store: a GitHub-token-shaped value was accepted for a "
                        "parameter nobody declared sensitive")
    except CORE.ValueRefused:
        pass
    CORE.sync_declarations(store, variables)
    entry = store["params"].get("db_password") or {}
    if "value" in entry:
        failures.append("store: a sensitive entry carries a value")
    if entry.get("placeholder") != "__FAION_DB_PASSWORD__":
        failures.append("store: a sensitive entry lost its placeholder")
    if json.dumps(store).find("hunter2") >= 0:
        failures.append("store: the refused secret is still in the store")

    apply_sets(store, variables, ["service_name=billing"], None)
    if CORE.store_value(store, "service_name") != "billing":
        failures.append("store: an ordinary value did not round-trip")
    apply_sets(store, variables, None, ["service_name"])
    if CORE.store_value(store, "service_name") is not None:
        failures.append("store: --unset did not remove the value")

    try:
        apply_sets(store, variables, ["port=eight"], None)
        failures.append("type: an integer parameter accepted a word")
    except CORE.ValueRefused:
        pass
    try:
        CORE.parse_source(BAD_FIXTURE, "fixture")
        failures.append("declaration: an unknown type was accepted")
    except CORE.TplError:
        pass
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", help="source template file")
    ap.add_argument("--blocks", help="block library root directory")
    ap.add_argument("--use", help="comma-separated kind/name block references")
    ap.add_argument("--project", default=".",
                    help="project root holding .faion/template-params.json")
    ap.add_argument("--set", dest="sets", action="append", metavar="NAME=VALUE",
                    help="write a value to the project store; repeatable")
    ap.add_argument("--unset", action="append", metavar="NAME",
                    help="drop a value from the project store; repeatable")
    ap.add_argument("--ask", action="store_true",
                    help="emit the unresolved parameters and their questions "
                         "as JSON")
    ap.add_argument("--json", action="store_true",
                    help="emit the full listing as JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if CORE is None:
        print(f"{NAME}: cannot load lib/tplcore.py beside this script",
              file=sys.stderr)
        return 2

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=15 failures={len(failures)}")
        return 1 if failures else 0

    if not (args.template or args.blocks or args.use):
        print(f"{NAME}: --template, or --blocks with --use, is required",
              file=sys.stderr)
        return 2

    try:
        source = load_source(args.template, args.blocks, args.use)
    except CORE.TplError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 1 if source_is_invalid(exc) else 2
    try:
        store = CORE.load_store(Path(args.project))
    except CORE.TplError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 2

    variables = source["variables"]
    changes: list[str] = []
    if args.sets or args.unset:
        try:
            changes = apply_sets(store, variables, args.sets, args.unset)
            CORE.sync_declarations(store, variables)
            CORE.save_store(Path(args.project), store)
        except CORE.ValueRefused as exc:
            print(f"{NAME}: {exc}", file=sys.stderr)
            return 4
        except CORE.TplError as exc:
            print(f"{NAME}: {exc}", file=sys.stderr)
            return 2

    rows = describe(variables, store)
    _, questions, _ = CORE.resolve(variables, {}, store)
    blocking = [q for q in questions if q["required"]]

    if args.ask:
        print(json.dumps({"tool": NAME, "source": source["where"],
                          "unresolved": questions,
                          "store": str(CORE.store_path(Path(args.project)))},
                         indent=2, sort_keys=True))
    elif args.json:
        print(json.dumps({"tool": NAME, "source": source["where"],
                          "parameters": rows, "unresolved": questions,
                          "store": str(CORE.store_path(Path(args.project)))},
                         indent=2, sort_keys=True))
    elif rows:
        print(table(rows))

    for change in changes:
        print(f"{NAME}: {change}", file=sys.stderr)
    for question in blocking:
        print(f"{NAME}: ask {question['name']!r}: {question['question']}",
              file=sys.stderr)
    # Under --ask / --json stdout is the machine-readable answer and nothing
    # else: a summary line appended to it makes json.load fail on the caller's
    # side, which is the one thing the ask channel exists to avoid.
    print(f"{NAME}: source={source['where']} params={len(rows)} "
          f"unresolved={len(blocking)} store="
          f"{CORE.store_path(Path(args.project))}",
          file=sys.stderr if (args.ask or args.json) else sys.stdout)
    return 3 if blocking else 0


def source_is_invalid(exc: Exception) -> bool:
    """A refusal about the template's own shape is exit 1; a missing file or an
    unusable flag combination is exit 2."""
    text = str(exc)
    return not (text.startswith("cannot read") or "not a directory" in text
                or "no such block" in text or "--template and --blocks" in text
                or "required together" in text or "names no blocks" in text
                or "not `<kind>/<name>`" in text
                or "lowercase identifiers" in text)


if __name__ == "__main__":
    sys.exit(main())
