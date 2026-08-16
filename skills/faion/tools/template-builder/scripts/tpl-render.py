#!/usr/bin/env python3
"""tpl-render.py — render a Jinja template pair against a value map.

The consumer of what tpl-jinja.py produces: `<name>.md.j2`, `<name>.html.j2`
and `<name>.vars.schema.json` go in, a Markdown document and a self-contained
HTML copy come out (.aidocs/conventions/template-jinja-migration.md §1, §2).

Three properties this renderer holds, and each is the reason the migration was
allowed at all (§0):

  * **it never double-renders.** Template source is read from a FILE and
    values are bound as CONTEXT. A rendered result, a value, or anything a
    caller supplied is never handed back in as source, so a value cannot
    become syntax. That single rule is what keeps the injection surface at
    zero, and it is worth more than the whole template-language ban it
    replaced.
  * **SandboxedEnvironment, and autoescape on the HTML.** A value carrying
    `</h1><script>alert(1)</script>` lands in the document as text.
  * **StrictUndefined.** A missing variable raises BY NAME. Jinja's default
    would render it as the empty string, which is a document shipped with a
    hole in it and no signal — the exact failure declaring variables exists to
    prevent.

Values are checked against the schema before anything renders, so an unknown
key, a wrong type, a value outside an `enum` and a credential-shaped string
are each refused by name rather than quietly rendered.

Jinja is a declared dependency of this pack (meta.json `dependencies`, §4). It
is imported inside a guard, so its absence is an install line and exit 2, never
a traceback and never a half-rendered document.

Input:  --template {file.md.j2} [--values {file.json}] [--set NAME=VALUE]
Output: {out}.md and {out}.html, or the Markdown on stdout.

Exit: 0 rendered · 1 the template or schema is invalid · 2 the tool could not
      run (including: Jinja is not installed) · 3 a required variable has no
      value · 4 a supplied value was refused.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

NAME = "tpl-render"


def _load(stem: str, relative: str):
    """Load a pack helper by absolute path — see tpl-build.py for why."""
    here = Path(__file__).resolve().parent
    for candidate in (here / relative, here / "scripts" / relative,
                      here.parent / "scripts" / relative):
        if candidate.is_file():
            spec = importlib.util.spec_from_file_location(stem, candidate)
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            sys.modules.setdefault(stem, module)
            spec.loader.exec_module(module)
            return module
    return None


CORE = _load("faion_tplcore", "lib/tplcore.py")
JINJA = _load("faion_tpljinja", "lib/tpljinja.py")


def siblings(template: Path) -> tuple[Path, Path]:
    """The `.html.j2` and `.vars.schema.json` beside a `.md.j2`.

    Derived rather than asked for: the three files are one artefact, and a
    caller who can point at two of them separately can point at a schema that
    does not describe the template.
    """
    name = template.name
    stem = name[:-6] if name.endswith(".md.j2") else template.stem
    return (template.with_name(f"{stem}.html.j2"),
            template.with_name(f"{stem}.vars.schema.json"))


def collect_values(values_file: str | None, pairs: list[str] | None) -> dict:
    """`--values file.json` plus `--set name=value`, explicit winning.

    A `--set` value is always a string; the schema check coerces it to the
    declared type, so `--set port=8000` satisfies an integer property without
    the caller writing JSON.
    """
    out: dict = {}
    if values_file:
        try:
            data = json.loads(Path(values_file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"--values {values_file}: {exc}") from exc
        if not isinstance(data, dict):
            raise ValueError(f"--values {values_file}: not a JSON object")
        out.update(data)
    for pair in pairs or []:
        if "=" not in pair:
            raise ValueError(f"--set {pair!r} is not name=value")
        key, _, value = pair.partition("=")
        out[key.strip()] = value
    return out


def render_pair(mods, md_path: Path, html_path: Path | None,
                values: dict) -> dict:
    """Render one or both templates. Source comes from disk, always.

    Two environments, not one with a flag: Markdown must not be escaped (it is
    plain text, and `&lt;` in a .md file is a bug) and HTML must be, so the
    escaping decision belongs to the file being rendered.
    """
    jinja2, _ = mods
    out: dict = {}
    out["markdown"] = JINJA.render_file(
        JINJA.environment(mods, autoescape=False), md_path, values)
    if html_path is not None:
        out["html"] = JINJA.render_file(
            JINJA.environment(mods, autoescape=True), html_path, values)
    return out


def undefined_name(exc) -> str | None:
    """The variable StrictUndefined refused, out of its message."""
    text = str(exc)
    if "'" in text:
        parts = text.split("'")
        if len(parts) >= 2 and parts[1]:
            return parts[1]
    return None


# ------------------------------------------------------------- self-test

MD_FIXTURE = """# Release {{ release_tag }}

Channel {{ channel }} on port {{ port }}. Note: {{ note }}
Secret: {{ db_password }}
"""

HTML_FIXTURE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Release {{ release_tag }}</title>
<style>body{color:#111}</style></head>
<body>
<h1>Release {{ release_tag }}</h1>
<p>Channel {{ channel }} on port {{ port }}. Note: {{ note }}</p>
<p>Secret: {{ db_password }}</p>
</body></html>
"""

SCHEMA_FIXTURE = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://faion.net/schemas/vars/fixture.vars.schema.json",
    "title": "fixture template variables",
    "type": "object",
    "additionalProperties": False,
    "required": ["release_tag", "channel", "note"],
    "properties": {
        "release_tag": {"type": "string", "title": "Release tag",
                        "description": "The git tag this release ships."},
        "channel": {"type": "string", "title": "Channel",
                    "description": "Which channel the release goes to.",
                    "enum": ["stable", "beta"]},
        "port": {"type": "integer", "title": "Port", "default": 8000,
                 "description": "The port the service binds."},
        "note": {"type": "string", "title": "Note", "x-faion-compose": True,
                 "description": "A free-text note an LLM composes."},
        "db_password": {"type": "string", "title": "Db password",
                        "description": "Database password. Never transmitted.",
                        "x-faion-sensitive": True,
                        "x-faion-placeholder": "__FAION_DB_PASSWORD__"},
    },
}

OK_VALUES = {"release_tag": "v1.2.0", "channel": "stable", "note": "fine"}


def self_test() -> list[str]:
    """Every guarantee this renderer makes. Twenty-six checks."""
    failures: list[str] = []
    try:
        mods = JINJA.load_jinja()
    except JINJA.JinjaMissing as exc:
        return [f"Jinja is required to self-test: {exc}"]
    jinja2, sandbox = mods

    if not JINJA.INSTALL_HINT.strip() or "pip install" not in JINJA.INSTALL_HINT:
        failures.append("the missing-Jinja message does not name an install "
                        "command, so a caller without Jinja is stuck")

    md_env = JINJA.environment(mods, autoescape=False)
    html_env = JINJA.environment(mods, autoescape=True)
    if not isinstance(md_env, sandbox.SandboxedEnvironment):
        failures.append("the Markdown environment is not sandboxed")
    if not isinstance(html_env, sandbox.SandboxedEnvironment):
        failures.append("the HTML environment is not sandboxed")
    if html_env.autoescape is not True:
        failures.append("the HTML environment does not autoescape")
    if md_env.autoescape is not False:
        failures.append("the Markdown environment escapes, which would put "
                        "entities in a plain-text file")
    if md_env.undefined is not jinja2.StrictUndefined:
        failures.append("the Markdown environment does not use StrictUndefined")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        md = root / "fixture.md.j2"
        html = root / "fixture.html.j2"
        schema_path = root / "fixture.vars.schema.json"
        md.write_text(MD_FIXTURE, encoding="utf-8")
        html.write_text(HTML_FIXTURE, encoding="utf-8")
        schema_path.write_text(json.dumps(SCHEMA_FIXTURE), encoding="utf-8")
        schema = JINJA.load_schema(schema_path)

        ready, refusals, _ = JINJA.prepare_values(schema, dict(OK_VALUES), root,
                                                  CORE.secret_shape)
        if refusals:
            failures.append(f"a valid value map was refused: {refusals}")
        if ready.get("port") != 8000:
            failures.append("a declared default was not applied")
        if ready.get("db_password") != "__FAION_DB_PASSWORD__":
            failures.append("a sensitive variable did not emit its placeholder")
        rendered = render_pair(mods, md, html, ready)
        if "v1.2.0" not in rendered["markdown"]:
            failures.append("the Markdown did not render its value")
        if "__FAION_DB_PASSWORD__" not in rendered["html"]:
            failures.append("the HTML did not render the placeholder")
        for finding in JINJA.external_references(rendered["html"]):
            failures.append(f"the rendered HTML is not self-contained: {finding}")

        # A missing REQUIRED variable raises by name rather than rendering
        # empty. Both halves matter: the schema check names it first, and
        # StrictUndefined is the backstop when a caller skips the schema.
        partial = dict(OK_VALUES)
        partial.pop("release_tag")
        _, missing, _ = JINJA.prepare_values(schema, partial, root)
        if not any("release_tag" in r for r in missing):
            failures.append("a missing required variable was not refused by name")
        try:
            render_pair(mods, md, None, {"channel": "stable", "port": 1,
                                         "note": "n", "db_password": "p"})
            failures.append("StrictUndefined did not raise on a missing "
                            "variable — the document would ship with a hole")
        except jinja2.UndefinedError as exc:
            if undefined_name(exc) != "release_tag":
                failures.append(f"StrictUndefined raised without naming the "
                                f"variable: {exc}")

        # A value is text. It cannot open a tag, and it cannot be syntax.
        payload = "</h1><script>alert(1)</script>"
        hostile = dict(OK_VALUES) | {"note": payload}
        ready, refusals, _ = JINJA.prepare_values(schema, hostile, root)
        if refusals:
            failures.append(f"a hostile-but-legal value was refused: {refusals}")
        out = render_pair(mods, md, html, ready)
        if "<script>" in out["html"]:
            failures.append("a value reached the HTML as a live tag")
        if "&lt;script&gt;" not in out["html"]:
            failures.append("the payload was dropped rather than escaped")
        if payload not in out["markdown"]:
            failures.append("the Markdown escaped a value it should have left "
                            "as text")

        # NEVER DOUBLE-RENDER. A value that looks like template source stays
        # text in both outputs.
        for source in ("{{ 7 * 7 }}", "{% for x in y %}", "{{ self }}",
                       "{{ ''.__class__ }}"):
            ready, _, _ = JINJA.prepare_values(
                schema, dict(OK_VALUES) | {"note": source}, root)
            out = render_pair(mods, md, html, ready)
            if source not in out["markdown"]:
                failures.append(f"a value {source!r} was interpreted as "
                                "template source in the Markdown")
            if "49" in out["markdown"] and source == "{{ 7 * 7 }}":
                failures.append("a value was evaluated — the renderer "
                                "double-rendered")

        # The sandbox holds even against template source, which is the case
        # this renderer is not supposed to have to survive.
        try:
            JINJA.render_source(md_env, "{{ ''.__class__.__mro__ }}", {})
            failures.append("the sandbox let a template reach __class__")
        except jinja2.TemplateError:
            pass

        # A $ref into the corpus dictionary resolves, and the entry it lands
        # on is what the refusal quotes. An unresolvable ref reads exactly
        # like "the dictionary has not landed yet", so a ref that silently
        # fails to resolve is invisible — which is why it is asserted here.
        (root / "vars-dictionary.schema.json").write_text(json.dumps(
            {"$defs": {"owner_handle": {
                "type": "string", "title": "Owner handle",
                "description": "Whose handle owns this artefact?"}}}),
            encoding="utf-8")
        ref_schema = {
            "$schema": JINJA.DRAFT07, "$id": "urn:fixture", "title": "t",
            "type": "object", "additionalProperties": False,
            "required": ["owner_handle"],
            "properties": {"owner_handle": {
                "$ref": "vars-dictionary.schema.json#/$defs/owner_handle"}}}
        _, refusals, unresolved = JINJA.prepare_values(ref_schema, {}, root)
        if unresolved:
            failures.append("a $ref into the dictionary beside the schema did "
                            "not resolve")
        if not any("Whose handle owns this artefact?" in r for r in refusals):
            failures.append("a refusal did not quote the dictionary's own "
                            "question, so the $ref bought nothing")
        _, refusals, _ = JINJA.prepare_values(
            ref_schema, {"owner_handle": 7}, root)
        if not any("owner_handle" in r and "string" in r for r in refusals):
            failures.append("a type declared only in the dictionary was not "
                            "enforced")

        # Type, enum and secret shape are each refused by name.
        for label, bad, needle in (
                ("an unknown key", {"nope": "x"}, "nope"),
                ("a bad enum", {"channel": "nightly"}, "channel"),
                ("a bad type", {"port": "eighty"}, "port"),
                ("a secret shape",
                 {"note": "ghp_" + "A1b2C3d4E5f6G7h8I9j0"}, "note"),
                ("a value for a sensitive variable",
                 {"db_password": "hunter2"}, "db_password")):
            _, refusals, _ = JINJA.prepare_values(
                schema, dict(OK_VALUES) | bad, root, CORE.secret_shape)
            if not any(needle in r for r in refusals):
                failures.append(f"{label} was not refused by name")
    return failures


# ------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", help="the .md.j2 to render")
    ap.add_argument("--schema",
                    help="the .vars.schema.json (default: the sibling)")
    ap.add_argument("--values", help="JSON object of variable values")
    ap.add_argument("--set", dest="sets", action="append", metavar="NAME=VALUE",
                    help="one explicit value; repeatable, beats --values")
    ap.add_argument("--out",
                    help="output path; the .html sibling is derived. Without "
                         "it the Markdown goes to stdout and no file is written")
    ap.add_argument("--no-html", action="store_true",
                    help="render only the Markdown")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if CORE is None or JINJA is None:
        print(f"{NAME}: cannot load the pack helpers beside this script "
              "(lib/tplcore.py, lib/tpljinja.py)", file=sys.stderr)
        return 2

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=26 failures={len(failures)}")
        return 1 if failures else 0

    try:
        mods = JINJA.load_jinja()
    except JINJA.JinjaMissing as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 2
    jinja2, _ = mods

    if not args.template:
        print(f"{NAME}: --template is required (or --self-test)",
              file=sys.stderr)
        return 2
    md_path = Path(args.template)
    if not md_path.is_file():
        print(f"{NAME}: no such template: {md_path}", file=sys.stderr)
        return 2
    html_sibling, schema_sibling = siblings(md_path)
    schema_path = Path(args.schema) if args.schema else schema_sibling
    html_path = None if args.no_html else html_sibling
    if html_path is not None and not html_path.is_file():
        print(f"{NAME}: {md_path} has no {html_path.name} beside it; the two "
              "templates are one artefact — regenerate with tpl-jinja, or pass "
              "--no-html", file=sys.stderr)
        return 2

    try:
        values = collect_values(args.values, args.sets)
    except ValueError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 2

    unresolved = 0
    if schema_path.is_file():
        try:
            schema = JINJA.load_schema(schema_path)
            values, refusals, unresolved = JINJA.prepare_values(
                schema, values, schema_path.parent, CORE.secret_shape)
        except JINJA.SchemaBroken as exc:
            print(f"{NAME}: {exc}", file=sys.stderr)
            return 1
        if unresolved:
            print(f"{NAME}: {unresolved} property(ies) $ref a dictionary this "
                  "schema cannot reach; they render unchecked. Point --schema "
                  "at a copy sitting beside vars-dictionary.schema.json",
                  file=sys.stderr)
        required = [r for r in refusals if "required and not supplied" in r]
        for refusal in refusals:
            print(f"{NAME}: {refusal}", file=sys.stderr)
        if required:
            print(f"{NAME}: {len(required)} required variable(s) unresolved",
                  file=sys.stderr)
            return 3
        if refusals:
            return 4
    else:
        print(f"{NAME}: no {schema_path.name} beside the template — rendering "
              "with no value checking; StrictUndefined is the only guard left",
              file=sys.stderr)

    try:
        rendered = render_pair(mods, md_path, html_path, values)
    except jinja2.UndefinedError as exc:
        name = undefined_name(exc)
        print(f"{NAME}: {md_path}: required variable "
              f"{name or 'unknown'!r} has no value — StrictUndefined refused "
              "rather than render it empty", file=sys.stderr)
        return 3
    except jinja2.TemplateError as exc:
        print(f"{NAME}: {md_path}: {exc}", file=sys.stderr)
        return 1

    if not args.out:
        print(rendered["markdown"], end="")
        print(f"{NAME}: {md_path} vars={len(values)} unresolved-refs="
              f"{unresolved} -> stdout (no file written)", file=sys.stderr)
        return 0

    out_md = Path(args.out)
    if out_md.suffix != ".md":
        out_md = out_md.with_name(out_md.name + ".md")
    written = [out_md]
    try:
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(rendered["markdown"], encoding="utf-8")
        if "html" in rendered:
            out_html = out_md.with_suffix(".html")
            out_html.write_text(rendered["html"], encoding="utf-8")
            written.append(out_html)
    except OSError as exc:
        print(f"{NAME}: cannot write output: {exc}", file=sys.stderr)
        return 2

    print(f"{NAME}: {md_path} vars={len(values)} unresolved-refs={unresolved} "
          "-> " + ", ".join(str(p) for p in written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
