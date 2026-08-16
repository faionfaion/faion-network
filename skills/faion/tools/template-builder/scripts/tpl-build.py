#!/usr/bin/env python3
"""tpl-build.py — assemble a template or block set into Markdown plus HTML.

A methodology template is filled by hand today, which means every filled copy
is a fresh chance to leave a placeholder in. This assembles one instead: from a
source template or an ordered block set, with parameters resolved explicit ->
project store -> declared default -> ask, and a required parameter that reaches
the end with nothing to fill it refused BY NAME rather than substituted empty.

The template language is `{{name}}` substitution plus
`when: <var> in [<literal>, ...]` sections, and deliberately nothing else — the
same assembler runs on behalf of other accounts, so expressions, loops, filters
and nested partials are refused by name rather than interpreted. The Markdown
renderer is partial by the same logic: it covers headings, paragraphs, lists,
tables, fenced code, blockquotes, links and emphasis, escapes everything else,
and is not CommonMark.

An assembly is normally blocks PLUS literal passthrough: measured over the
corpus, blocks cover the envelope and the median template shares no bytes with
any other, so --use takes `kind/name` block references and `.md` file paths in
one ordered list. A section matching no block is assembled from literals; that
is the normal case, not an error.

A successful build remembers what it was given: every value from --set or
--values is written to the project store, so the next build asks for less. A
value that came FROM the store is already there, and a value that came from a
declared default is deliberately not written — persisting a default freezes it,
and a later change to the block would silently stop taking effect. A sensitive
parameter is never persisted at all. --no-remember opts out.

Input:  --template {file} | [--blocks {dir}] --use {kind/name or path.md,...}
Output: {out}.md (canonical) and {out}.html (self-contained).

Exit: 0 built · 1 the template is invalid · 2 the tool could not run ·
      3 required parameters unresolved · 4 a supplied value refused.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

NAME = "tpl-build"


def _load_core():
    """Load the pack helper by absolute path.

    In the repo it is `scripts/lib/tplcore.py` beside this file; once
    `faion tools sync` materialises the pack the script sits at the pack root
    and the helper keeps its `scripts/lib/` path. Both are tried.
    """
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

# --self-test fixtures. OK assembles clean; each BAD names one construct this
# tool refuses rather than interprets.
OK_FIXTURE = """<!--
purpose: service runbook
consumes: nothing
produces: markdown runbook
depends-on: none
token-budget-impact: ~200 tokens
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
  - name: db_password
    type: string
    required: true
    sensitive: true
    placeholder: "__FAION_DB_PASSWORD__"
    description: Database password. Never transmitted.
  - name: stack
    type: enum
    required: true
    options: [django, fastapi]
    description: Which runtime section to assemble.
sections:
  - name: django
    description: gunicorn unit and WSGI entrypoint.
    when: stack in [django]
  - name: fastapi
    description: uvicorn unit and ASGI entrypoint.
    when: stack in [fastapi]
-->
# {{service_name}}

Binds port {{port}}. Password placeholder: {{db_password}}.

<!-- faion:section django -->
Run `gunicorn {{service_name}}.wsgi` on {{port}}.
<!-- faion:endsection -->
<!-- faion:section fastapi -->
Run `uvicorn {{service_name}}:app` on {{port}}.
<!-- faion:endsection -->
"""

BAD_WHEN_FIXTURE = OK_FIXTURE.replace("when: stack in [django]",
                                      "when: stack != django")
BAD_FILTER_FIXTURE = OK_FIXTURE.replace("{{service_name}}",
                                        "{{service_name | upper}}")
BAD_STATEMENT_FIXTURE = OK_FIXTURE.replace(
    "Binds port", "{% for x in y %}Binds port")
BAD_UNDECLARED_FIXTURE = OK_FIXTURE.replace("{{port}}", "{{undeclared_thing}}")

MISSING_REQUIRED_FIXTURE = """<!--
purpose: p
produces: markdown
variables:
  - name: owner
    type: string
    required: true
    description: Who is on call for this service.
-->
# Owned by {{owner}}
"""

INJECTION_FIXTURE = """<!--
purpose: p
produces: markdown
variables:
  - name: note
    type: text
    required: true
    description: A free-text note the agent composes.
-->
# Note

{{note}}
"""


def collect_explicit(pairs: list[str] | None, values_file: str | None
                     ) -> dict[str, str]:
    """`--set name=value` plus `--values file.json`, explicit winning."""
    out: dict[str, str] = {}
    if values_file:
        try:
            data = json.loads(Path(values_file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CORE.TplError(f"--values {values_file}: {exc}") from exc
        if not isinstance(data, dict):
            raise CORE.TplError(f"--values {values_file}: not a JSON object")
        for key, value in data.items():
            out[str(key)] = "" if value is None else str(value)
    for pair in pairs or []:
        if "=" not in pair:
            raise CORE.TplError(f"--set {pair!r} is not name=value")
        key, _, value = pair.partition("=")
        out[key.strip()] = value
    return out


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


def assemble(source: dict, explicit: dict[str, str], store: dict) -> dict:
    """Validate, resolve, prune, substitute. Raises on every refusal."""
    variables, sections = source["variables"], source["sections"]
    for name in explicit:
        if name not in variables:
            raise CORE.ValueRefused(
                f"{name}: not declared by {source['where']}; declared are "
                + (", ".join(variables) or "(none)"))
        CORE.accept_value(variables[name], explicit[name])

    declared = CORE.scan_placeholders(source["body"], source["where"])
    for name in sorted(declared - set(variables)):
        raise CORE.TplError(
            f"{source['where']}: `{{{{{name}}}}}` is not declared under "
            "`variables:` — an undeclared placeholder would substitute empty, "
            "which is the hole this builder exists to refuse")

    when_vars = {s["var"] for s in sections if s["var"]}
    values, questions, _ = CORE.resolve(variables, explicit, store, when_vars)
    if any(q["required"] for q in questions):
        # A `when` variable with no value means no section can be evaluated, so
        # the surviving body is unknown. Report every required parameter the
        # body references rather than one round trip per unknown: an agent that
        # has to ask three times asks the user three times.
        _, every, _ = CORE.resolve(variables, explicit, store,
                                   declared | when_vars)
        unresolved = {q["name"] for q in every if q["required"]}
        raise CORE.Unresolved([n for n in variables if n in unresolved])

    body = CORE.prune_sections(source["body"], sections, values,
                               source["where"])
    used = CORE.scan_placeholders(body, source["where"])
    values, questions, origins = CORE.resolve(variables, explicit, store,
                                              used | when_vars)
    blocking = [q["name"] for q in questions if q["required"]]
    if blocking:
        raise CORE.Unresolved(blocking)

    markdown = CORE.substitute(body, values).strip("\n") + "\n"
    # The HTML is rendered from the SAME body with values held as sentinels,
    # so source text and value text never share an escaping pass.
    marked, marks = CORE.substitute_marked(body, values)
    return {"markdown": markdown, "marked": marked.strip("\n") + "\n",
            "marks": marks, "values": values, "origins": origins,
            "kept": [s["name"] for s in sections
                     if s["var"] is None
                     or values.get(s["var"], "") in s["literals"]]}


def title_of(markdown: str, fallback: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


def out_paths(out: str) -> tuple[Path, Path]:
    path = Path(out)
    if path.suffix != ".md":
        path = path.with_name(path.name + ".md")
    return path, path.with_suffix(".html")


def self_test() -> list[str]:
    """Every refusal this tool exists to make, asserted against the fixtures."""
    failures: list[str] = []
    empty = {"version": 1, "params": {}}

    def build(text, explicit=None, store=None):
        return assemble(CORE.parse_source(text, "fixture"), explicit or {},
                        store or dict(empty))

    result = build(OK_FIXTURE, {"service_name": "billing", "stack": "django"})
    if "gunicorn billing.wsgi" not in result["markdown"]:
        failures.append("OK fixture: the selected section was not kept")
    if "uvicorn" in result["markdown"]:
        failures.append("OK fixture: the unselected section was not pruned")
    if "8000" not in result["markdown"]:
        failures.append("OK fixture: the declared default was not applied")
    if "__FAION_DB_PASSWORD__" not in result["markdown"]:
        failures.append("OK fixture: a sensitive parameter did not emit its "
                        "placeholder")

    # Both spellings of the version stamp parse. Each one shipped broken: the
    # header was read correctly and then thrown away on its own first line,
    # silently turning 251 corpus templates into "no parseable header" — a
    # failure that looks like bad content and is not. Assert the marker is
    # gone from the header, that the five keys survive it, and that it is not
    # pushed back into the body.
    for label, fixture in (
        ("one-line run",
         "<!-- __faion_header_v1__ -->\n<!-- purpose: p -->\n"
         "<!-- consumes: c -->\n<!-- produces: r -->\n"
         "<!-- depends-on: d -->\n<!-- token-budget-impact: t -->\n\n# Body\n"),
        ("block opener",
         "<!-- __faion_header__\npurpose: p\nconsumes: c\nproduces: r\n"
         "depends-on: d\ntoken-budget-impact: t\n-->\n\n# Body\n"),
    ):
        try:
            head, body = CORE.split_header(fixture)
            parsed = CORE.parse_header(head)
            if parsed.get("purpose") != "p":
                failures.append(f"{label} marker: purpose lost, got {parsed!r}")
            if "__faion_header" in head:
                failures.append(f"{label} marker: left in the header text")
            if "__faion_header" in body:
                failures.append(f"{label} marker: pushed into the body")
        except CORE.TplError as exc:
            failures.append(f"{label} marker: raised instead of parsing: {exc}")

    # A required parameter with no default and no value is refused BY NAME.
    try:
        build(MISSING_REQUIRED_FIXTURE)
        failures.append("missing required parameter: built anyway")
    except CORE.Unresolved as exc:
        if exc.names != ["owner"]:
            failures.append(f"missing required parameter: named {exc.names}")
    except CORE.TplError as exc:
        failures.append(f"missing required parameter: wrong error: {exc}")

    # `when` with anything but `<var> in [...]`.
    for label, fixture in (("!= operator", BAD_WHEN_FIXTURE),
                           ("a filter", BAD_FILTER_FIXTURE),
                           ("a {% %} statement", BAD_STATEMENT_FIXTURE),
                           ("an undeclared variable", BAD_UNDECLARED_FIXTURE)):
        try:
            build(fixture, {"service_name": "b", "stack": "django"})
            failures.append(f"{label}: accepted instead of refused")
        except CORE.TplError:
            pass

    # A value that is or looks like a secret never gets in.
    try:
        build(OK_FIXTURE, {"db_password": "hunter2", "stack": "django",
                           "service_name": "b"})
        failures.append("sensitive parameter: a value was accepted")
    except CORE.ValueRefused:
        pass
    try:
        build(OK_FIXTURE, {"service_name": "ghp_" + "A1b2C3d4E5f6G7h8I9j0",
                           "stack": "django"})
        failures.append("secret shape: a GitHub token was accepted for a "
                        "non-sensitive parameter")
    except CORE.ValueRefused:
        pass

    # A tag in a parameter value cannot escape into the HTML.
    for payload in ("<script>alert(1)</script>",
                    "</p><script>alert(1)</script><p>",
                    "\n# forged heading\n", "`</code></pre><script>x</script>"):
        rendered = build(INJECTION_FIXTURE, {"note": payload})
        html = CORE.md_to_html(rendered["marked"], "t", rendered["marks"])
        if "<script" in html:
            failures.append(f"injection: {payload[:20]!r} reached the HTML as "
                            "a tag")
        if "forged heading" in html and "<h1>forged" in html:
            failures.append("injection: a value forged a heading")
    escaped = build(INJECTION_FIXTURE, {"note": "<script>alert(1)</script>"})
    if "&lt;script&gt;" not in CORE.md_to_html(escaped["marked"], "t",
                                               escaped["marks"]):
        failures.append("injection: the payload was dropped rather than "
                        "escaped")
    if 'href="javascript:' in CORE.md_to_html("[x](javascript:alert(1))", "t"):
        failures.append("injection: a javascript: URL was opened as an href")

    # Source text that is ALREADY entity-escaped must not be escaped twice,
    # and that leniency must not reach a value.
    source_html = CORE.md_to_html("Fill `&lt;artefact_id&gt;` before use.", "t")
    if "&amp;lt;" in source_html:
        failures.append("escaping: source text already holding &lt; was "
                        "double-escaped")
    if "&lt;artefact_id&gt;" not in source_html:
        failures.append("escaping: an existing character reference was lost")
    entity_value = build(INJECTION_FIXTURE, {"note": "&lt;b&gt;"})
    if "&amp;lt;b&amp;gt;" not in CORE.md_to_html(
            entity_value["marked"], "t", entity_value["marks"]):
        failures.append("escaping: a parameter value got the source path's "
                        "entity pass-through")

    # A block-level HTML comment is dropped from the render, kept in the .md.
    if "purpose: x" in CORE.md_to_html("<!-- purpose: x -->\n\nBody.", "t"):
        failures.append("comments: a block comment reached the rendered HTML")
    if "&lt;!-- kept --&gt;" not in CORE.md_to_html("```\n<!-- kept -->\n```",
                                                    "t"):
        failures.append("comments: a comment inside a code fence was dropped")

    # What a successful build remembers, and what it must not.
    memo = {"version": 1, "params": {}}
    source = CORE.parse_source(OK_FIXTURE, "fixture")
    first = assemble(source, {"service_name": "billing", "stack": "django"},
                     memo)
    written = CORE.remember(memo, source["variables"], first["values"],
                            first["origins"])
    if written != ["service_name", "stack"]:
        failures.append(f"remember: wrote {written}, expected the two --set "
                        "values")
    if CORE.store_value(memo, "port") is not None:
        failures.append("remember: a value that came from a declared default "
                        "was frozen into the store")
    if "value" in (memo["params"].get("db_password") or {}):
        failures.append("remember: a sensitive parameter reached the store")
    try:
        # A second build, given nothing, must resolve from what was remembered.
        second = assemble(source, {}, memo)
    except CORE.Unresolved as exc:
        failures.append(f"remember: a second build re-asked for {exc.names}")
    else:
        if second["markdown"] != first["markdown"]:
            failures.append("remember: a second build from the store differed "
                            "from the first")
        if second["origins"].get("service_name") != "store":
            failures.append("remember: the second build did not resolve from "
                            "the store")
    # Nothing that was refused can be remembered, because it never resolved.
    if json.dumps(memo).find("hunter2") >= 0:
        failures.append("remember: a refused value is in the store")

    # Resolution order: explicit beats store beats default.
    stored = {"version": 1, "params": {"port": {"value": "9001"}}}
    if "9001" not in build(OK_FIXTURE, {"service_name": "b",
                                        "stack": "django"},
                           stored)["markdown"]:
        failures.append("resolution: the store did not beat the default")
    if "9100" not in build(OK_FIXTURE, {"service_name": "b", "stack": "django",
                                        "port": "9100"}, stored)["markdown"]:
        failures.append("resolution: an explicit value did not beat the store")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", help="source template file")
    ap.add_argument("--blocks", help="block library root directory")
    ap.add_argument("--use", help="comma-separated kind/name block references")
    ap.add_argument("--set", dest="sets", action="append", metavar="NAME=VALUE",
                    help="an explicit parameter value; repeatable")
    ap.add_argument("--values", help="JSON object of parameter values")
    ap.add_argument("--project", default=".",
                    help="project root holding .faion/template-params.json")
    ap.add_argument("--out", help="output path; the .html sibling is derived")
    ap.add_argument("--no-html", action="store_true",
                    help="emit only the canonical Markdown")
    ap.add_argument("--no-remember", action="store_true",
                    help="do not write the answers back to the project store")
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
        print(f"{NAME}: self-test checks=30 failures={len(failures)}")
        return 1 if failures else 0

    if not (args.template or args.blocks or args.use):
        print(f"{NAME}: --template, or --blocks with --use, is required",
              file=sys.stderr)
        return 2
    if not args.out:
        print(f"{NAME}: --out is required — the build writes files, never "
              "stdout", file=sys.stderr)
        return 2

    try:
        source = load_source(args.template, args.blocks, args.use)
        explicit = collect_explicit(args.sets, args.values)
        store = CORE.load_store(Path(args.project))
    except CORE.TplError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 2

    try:
        result = assemble(source, explicit, store)
    except CORE.Unresolved as exc:
        for name in exc.names:
            decl = source["variables"][name]
            print(f"{NAME}: required parameter {name!r} has no value and no "
                  f"default — ask: {decl['description']}", file=sys.stderr)
        print(f"{NAME}: {len(exc.names)} required parameter(s) unresolved; "
              "run tpl-params --ask for the questions", file=sys.stderr)
        return 3
    except CORE.ValueRefused as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 4
    except CORE.TplError as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return 1

    md_path, html_path = out_paths(args.out)
    written = [md_path]
    try:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(result["markdown"], encoding="utf-8")
        if not args.no_html:
            html_path.write_text(
                CORE.md_to_html(result["marked"],
                                title_of(result["markdown"], md_path.stem),
                                result["marks"]),
                encoding="utf-8")
            written.append(html_path)
    except OSError as exc:
        print(f"{NAME}: cannot write output: {exc}", file=sys.stderr)
        return 2

    # Persist only after the build succeeded, and only what this run was
    # actually given: a value read from the store is already there, and a value
    # that came from a declared default must never be frozen into the project.
    remembered: list[str] = []
    if not args.no_remember:
        try:
            remembered = CORE.remember(store, source["variables"],
                                       result["values"], result["origins"])
            CORE.save_store(Path(args.project), store)
        except (CORE.TplError, OSError) as exc:
            # The document is written and correct; only the memory failed. Say
            # so loudly and still report the build as the success it was.
            print(f"{NAME}: built, but the store was not updated: {exc}",
                  file=sys.stderr)
            remembered = []

    print(f"{NAME}: source={source['where']} vars={len(result['values'])} "
          f"sections={len(result['kept'])} remembered={len(remembered)} -> "
          + ", ".join(str(p) for p in written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
