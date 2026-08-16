#!/usr/bin/env python3
"""tpl-jinja.py — convert one Markdown template into the three-file Jinja form.

`templates/<name>.md` becomes `<name>.md.j2`, `<name>.html.j2` and
`<name>.vars.schema.json` (.aidocs/conventions/template-jinja-migration.md).
The HTML is generated from the MARKDOWN SOURCE STRUCTURE, not by converting a
rendered document at runtime, so the two are siblings a generator wrote
together rather than one file with a format branch in it.

It proposes. It does not decide, and it writes nothing without --write.

The judgements it refuses to make are the point:

  * a prose placeholder (`<Optional: 'ready for owner review'>`) is guidance to
    a reader, not a variable. Declaring it produces a build that refuses BY
    NAME for a parameter that should never have existed, so it is flagged and
    left exactly where it is.
  * a placeholder that repeats down a table's body rows cannot be one variable
    — §2.3 has no loops, and this tool does not invent one. Reported, left.
  * a template whose placeholders are already HTML-escaped (`&lt;name&gt;`,
    1,183 of them in the corpus) is refused whole: un-escaping is a
    prerequisite and is out of scope (§6).
  * a `sections:` header, a raw `{%`/`{#` delimiter in the body, or a `{{x}}`
    with no declaration behind it are each refused by name rather than
    translated on a guess.

The placeholder scanner, the header parser and the Markdown→HTML renderer are
tpl-migrate.py and lib/tplcore.py, loaded and reused. A second copy of the
naming rules would be a second thing that can disagree with tpl-build.

Input:  --template {file.md} [--out-dir {dir}] [--dictionary {file}] [--write]
Output: the three files, or all three to stdout when dry-running.

Exit: 0 every placeholder resolved · 1 placeholders were left for a human (the
      normal outcome) · 2 the tool could not run · 3 refused, the placeholders
      are already HTML-escaped · 4 refused, the source carries a construct this
      converter will not translate.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

NAME = "tpl-jinja"


def _load(stem: str, *relatives: str):
    """Load a pack file by absolute path — see tpl-build.py for why."""
    here = Path(__file__).resolve().parent
    for relative in relatives:
        candidate = here / relative
        if not candidate.is_file():
            candidate = here.parent / "scripts" / relative
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
MIGRATE = _load("faion_tplmigrate", "tpl-migrate.py")

# `{{ name }}` is what this converter emits; anything else already in the body
# was refused upstream by CORE.scan_placeholders.
SPACED = re.compile(r"\{\{\s*([a-z][a-z0-9_]{0,63})\s*\}\}")
# The two Jinja delimiters a Markdown source must not already carry. `{{` is
# handled by scan_placeholders, which accepts only a bare variable name.
RAW_DELIMITER = re.compile(r"\{%|\{#")
# A `variables:` or `sections:` run inside a header, which §2 moves out of the
# template and into the schema.
MOVED_KEY = re.compile(r"^(variables|sections)\s*:", re.MULTILINE)
TOP_KEY = re.compile(r"^[a-z][a-z0-9_-]*\s*:")
# A Markdown link whose href holds a variable. Autoescape makes the value
# text-safe but says nothing about its SCHEME, so `{{ url }}` = `javascript:…`
# would be a live vector. Reported, and the emitted HTML renders it as text.
# The URL group admits spaces because `{{ name }}` carries two.
LINK = re.compile(r"\[([^\]]*)\]\(([^)\n]*)\)")


class Refused(Exception):
    """The converter will not translate this template. `.code` is the exit."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


# --------------------------------------------------------------- structure

def table_rows(body: str) -> list[tuple[int, int, int, int]]:
    """(start, end, table index, row index) for every table BODY row.

    A placeholder in a header cell names a column; one in a body cell names a
    cell, and a cell that repeats down the rows is a loop wearing a variable's
    clothes. Telling them apart needs the table structure, which is why this
    reads the same shape CORE.md_to_html does rather than pattern-matching `|`.
    """
    lines = body.split("\n")
    starts: list[int] = []
    offset = 0
    for line in lines:
        starts.append(offset)
        offset += len(line) + 1
    rows: list[tuple[int, int, int, int]] = []
    index, table = 0, 0
    while index + 1 < len(lines):
        if "|" in lines[index] and "|" in lines[index + 1] \
                and CORE._TABLE_SEP.match(lines[index + 1]):
            index += 2
            row = 0
            while index < len(lines) and "|" in lines[index] \
                    and lines[index].strip():
                rows.append((starts[index],
                             starts[index] + len(lines[index]), table, row))
                index += 1
                row += 1
            table += 1
            continue
        index += 1
    return rows


def per_row_names(items: list[dict], rows: list[tuple[int, int, int, int]]
                  ) -> set[str]:
    """Names that appear in more than one body row of the same table."""
    seen: dict[str, set[tuple[int, int]]] = {}
    for item in items:
        if item["verdict"] != "parameter":
            continue
        for start, end, table, row in rows:
            if start <= item["start"] < end:
                seen.setdefault(item["name"], set()).add((table, row))
                break
    return {name for name, cells in seen.items() if len(cells) > 1}


def strip_moved_keys(head: str) -> str:
    """The header text with its `variables:` and `sections:` runs removed.

    §2 moves both into the schema. Leaving them behind would give a template
    two declarations of the same thing, and the corpus already has 187 cases
    of two copies of one document drifting apart.
    """
    kept: list[str] = []
    skipping = False
    for line in head.split("\n"):
        if MOVED_KEY.match(line):
            skipping = True
            continue
        if skipping and (not line.strip() or not TOP_KEY.match(line)):
            continue
        skipping = False
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    return "\n".join(kept)


def title_of(markdown: str, fallback: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


# --------------------------------------------------------------- the plan

def convert(text: str, stem: str, *, dictionary: dict,
            dictionary_ref: str | None, schema_id: str,
            where: str | None = None) -> dict:
    """The whole conversion for one template. Raises Refused, or TplError.

    Pure: no I/O beyond what the caller already read, no exits. This is what
    --self-test exercises.
    """
    where = where or stem
    source = CORE.parse_source(text, where)
    body, declared = source["body"], source["variables"]
    offset = len(text) - len(body)

    if source["sections"]:
        raise Refused(4, f"{where}: declares `sections:`. Translating a "
                         "when-clause into a Jinja conditional is a decision "
                         "about document shape, not a mechanical rewrite — "
                         "convert it by hand or drop the sections first")
    delimiter = RAW_DELIMITER.search(body)
    if delimiter:
        line = body[:delimiter.start()].count("\n") + 1 + text[:offset].count("\n")
        raise Refused(4, f"{where} line {line}: the body already carries a "
                         f"{delimiter.group(0)!r} delimiter. In a .md.j2 that "
                         "is Jinja syntax, so the source must be wrapped in "
                         "`{% raw %}` by a human who knows what it is showing")

    existing = CORE.scan_placeholders(body, where)
    orphans = sorted(existing - set(declared))
    if orphans:
        raise Refused(4, f"{where}: `{{{{{orphans[0]}}}}}` has no declaration "
                         "behind it. A schema property needs a description — "
                         "the question put to the author — and inventing one "
                         "is the failure this converter exists to avoid")

    found = MIGRATE.candidates(body)
    escaped = [c for c in found if c["kind"] == "escaped"]
    if escaped:
        raise Refused(3, f"{where}: {len(escaped)} placeholder(s) are already "
                         f"HTML-escaped (first: {escaped[0]['raw']!r}). They "
                         "must be un-escaped before they can be variables at "
                         "all, and that is a prerequisite, not part of this "
                         "conversion (§6)")

    items = MIGRATE.classify(body, found, declared)
    for item in items:
        item["line"] += text[:offset].count("\n")
    colliding = {c.split(":", 1)[0] for c in MIGRATE.find_collisions(items)}
    repeated = per_row_names(items, table_rows(body))
    for item in items:
        if item["verdict"] != "parameter":
            continue
        if item["name"] in colliding:
            item["verdict"], item["reason"] = "unclear", "collision"
        elif item["name"] in repeated:
            item["verdict"] = "unclear"
            item["reason"] = "per-row-table"
            item["name"] = None

    new_body = body
    for item in sorted(items, key=lambda i: i["start"], reverse=True):
        if item["verdict"] == "parameter":
            new_body = (new_body[: item["start"]] + "{{ " + item["name"]
                        + " }}" + new_body[item["end"]:])
    new_body = SPACED.sub(r"{{ \1 }}", new_body)

    # The declarations, in body order: what the header already declared and is
    # still used, then what this run proposes.
    decls: list[dict] = []
    seen: set[str] = set()
    for name in sorted(existing):
        decls.append(dict(declared[name]))
        seen.add(name)
    for item in items:
        if item["verdict"] != "parameter" or item["name"] in seen:
            continue
        seen.add(item["name"])
        if item["name"] in declared:
            decls.append(dict(declared[item["name"]]))
            continue
        decls.append({"name": item["name"], "type": item["type"],
                      "required": item["required"], "default": None,
                      "sensitive": False, "placeholder": None,
                      "options": item["options"],
                      "description": item["description"]})
    decls.sort(key=lambda d: d["name"])

    head, _ = CORE.split_header(text)
    if head and MOVED_KEY.search(head):
        kept = strip_moved_keys(head)
        header = f"<!--\n{kept}\n-->\n\n" if kept.strip() else ""
    else:
        header = text[:offset]
    md_j2 = header + new_body

    # The HTML is built from THIS Markdown structure, with each variable held
    # as an opaque sentinel through the render and put back as `{{ name }}`
    # afterwards. So the two templates cannot drift, and no value is anywhere
    # near this code path — at render time autoescape is what makes a value
    # text (§0), and here there are no values at all.
    marks: list[str] = []

    def mark(match: re.Match) -> str:
        marks.append("{{ " + match.group(1) + " }}")
        return f"\x01{len(marks) - 1}\x01"

    marked = SPACED.sub(mark, new_body)
    title = title_of(new_body, stem)
    html_j2 = CORE.md_to_html(marked.strip("\n") + "\n", title, marks or None)

    hrefs = sorted({m.group(2) for m in LINK.finditer(new_body)
                    if "{{" in m.group(2)})
    notes: list[str] = []
    for href in hrefs:
        notes.append(f"href-variable {href} — a variable that is a whole URL. "
                     "Autoescape makes it text-safe and says nothing about its "
                     "scheme, so the HTML renders it as text rather than an "
                     "href. Decide by hand whether it should be a link")

    used = JINJA.template_variables(md_j2)
    for name in sorted(used - {d["name"] for d in decls}):
        notes.append(f"{name} is referenced and not declared")
    for decl in decls:
        if decl["name"] not in used:
            notes.append(f"{decl['name']} is declared and never referenced")

    schema = JINJA.build_schema(
        decls, schema_id=schema_id,
        title=f"{stem} template variables",
        description=(f"Values for templates/{stem}.md.j2 and "
                     f"templates/{stem}.html.j2. Generated by {NAME} from "
                     f"{stem}.md; `description` on each property is the "
                     "question put to the author."),
        dictionary=dictionary, dictionary_ref=dictionary_ref)

    unclear = [i for i in items if i["verdict"] == "unclear"]
    return {"where": where, "stem": stem, "items": items, "declarations": decls,
            "md_j2": md_j2, "html_j2": html_j2, "schema": schema,
            "notes": notes, "unclear": len(unclear),
            "parameters": sum(1 for i in items if i["verdict"] == "parameter"),
            "variables": sorted(used),
            "dictionary_refs": schema.get("x-faion-dictionary-refs", 0)}


def verify(plan: dict, mods) -> list[str]:
    """Parse and render what was generated, before anything is written.

    Emitting a Jinja file nobody parsed is exactly the half-working state the
    dependency rule (§4) exists to forbid, so this runs on every conversion
    and a failure blocks the write.
    """
    problems: list[str] = []
    values = {name: f"«{name}»" for name in plan["variables"]}
    md_env = JINJA.environment(mods, autoescape=False)
    html_env = JINJA.environment(mods, autoescape=True)
    jinja2, _ = mods
    for label, env, text in (("md.j2", md_env, plan["md_j2"]),
                             ("html.j2", html_env, plan["html_j2"])):
        try:
            rendered = JINJA.render_source(env, text, values)
        except jinja2.TemplateError as exc:
            problems.append(f"{label}: does not render: {exc}")
            continue
        if label == "md.j2":
            # The pre-Jinja builder substituted `{{name}}` with tplcore. The
            # converted template must produce the same document from the same
            # values, or the migration changed what the corpus emits.
            if rendered != CORE.substitute(text, values):
                problems.append("md.j2: renders differently from the "
                                "pre-Jinja tplcore substitution of the same "
                                "source with the same values")
        else:
            for finding in JINJA.external_references(rendered):
                problems.append(f"html.j2: {finding}")
    return problems


def targets(stem: str, out_dir: Path) -> dict[str, Path]:
    return {"md_j2": out_dir / f"{stem}.md.j2",
            "html_j2": out_dir / f"{stem}.html.j2",
            "schema": out_dir / f"{stem}.vars.schema.json"}


def write_plan(plan: dict, out_dir: Path, write: bool) -> list[Path]:
    """Write the three files, or nothing. Default everywhere is nothing."""
    if not write:
        return []
    paths = targets(plan["stem"], out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths["md_j2"].write_text(plan["md_j2"], encoding="utf-8")
    paths["html_j2"].write_text(plan["html_j2"], encoding="utf-8")
    paths["schema"].write_text(JINJA.dumps(plan["schema"]), encoding="utf-8")
    return [paths["md_j2"], paths["html_j2"], paths["schema"]]


def report(plan: dict) -> str:
    lines = [f"{plan['where']}: variables={len(plan['declarations'])} "
             f"dictionary-refs={plan['dictionary_refs']} "
             f"unclear={plan['unclear']}"]
    for item in plan["items"]:
        if item["verdict"] == "parameter":
            lines.append(f"  line {item['line']:>4}  {item['raw']} -> "
                         f"{{{{ {item['name']} }}}}  {item['type']}")
    for item in plan["items"]:
        if item["verdict"] == "unclear":
            lines.append(f"  line {item['line']:>4}  {item['raw']}  "
                         f"UNCLEAR: {item['reason']} — left alone")
    for note in plan["notes"]:
        lines.append(f"  NOTE {note}")
    return "\n".join(lines)


def schema_id_for(path: Path | None, stem: str) -> str:
    """A stable, unique `$id`. The methodology directory disambiguates a stem
    like `checklist.md`, which the corpus carries dozens of."""
    owner = ""
    if path is not None:
        parts = path.resolve().parts
        if "templates" in parts:
            index = len(parts) - 1 - parts[::-1].index("templates")
            owner = "/".join(parts[max(0, index - 2):index])
    prefix = f"{owner}/" if owner else ""
    return f"https://faion.net/schemas/vars/{prefix}{stem}.vars.schema.json"


def dictionary_ref_for(out_dir: Path, dictionary: Path | None) -> str | None:
    """The relative path a schema in `out_dir` uses to reach the dictionary."""
    if dictionary is None or not Path(dictionary).is_file():
        return None
    import os
    return os.path.relpath(Path(dictionary).resolve(),
                           Path(out_dir).resolve()).replace("\\", "/")


def find_dictionary(explicit: str | None, template: Path | None) -> Path | None:
    """The corpus dictionary, named or discovered by walking up from the
    template. Absent is a normal state during the migration."""
    if explicit:
        return Path(explicit)
    if template is None:
        return None
    for parent in Path(template).resolve().parents:
        candidate = parent / JINJA.DICTIONARY_REL
        if candidate.is_file():
            return candidate
    return None


# ------------------------------------------------------------- self-test

CLEAN_FIXTURE = """<!--
purpose: service runbook
produces: markdown runbook
-->
# Runbook for <service_name>

## Identity

Owner: <Optional: 'ready for owner review'>

Docs: [runbook](<doc_url>)

```sh
systemctl restart <service_name>
```
"""

DECLARED_FIXTURE = """<!--
purpose: release note
produces: markdown release note
variables:
  - name: release_tag
    type: string
    required: true
    description: The git tag this release ships.
  - name: channel
    type: enum
    required: true
    options: [stable, beta]
    description: Which channel the release goes to.
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
-->
# Release {{release_tag}}

Channel {{channel}} on port {{port}}. Secret: {{db_password}}.
"""

TABLE_FIXTURE = """# Risks

| Risk | Owner | Status |
|---|---|---|
| <risk_title> | <owner_name> | open |
| <risk_title> | <owner_name> | open |
"""

ESCAPED_FIXTURE = "# Doc\n\nIdentity: &lt;artefact_id&gt;\n"

SECTIONS_FIXTURE = """<!--
purpose: p
produces: markdown
variables:
  - name: stack
    type: enum
    required: true
    options: [django, fastapi]
    description: Which runtime section to assemble.
sections:
  - name: django
    description: gunicorn unit.
    when: stack in [django]
-->
# S

<!-- faion:section django -->
gunicorn
<!-- faion:endsection -->
"""

RAW_FIXTURE = "# Doc\n\nSee `{% for x in y %}` in the engine.\n"

ORPHAN_FIXTURE = "# Doc\n\nOwner is {{owner}}.\n"


def _convert(text: str, stem: str = "fixture", dictionary=None) -> dict:
    return convert(text, stem, dictionary=dictionary or {},
                   dictionary_ref="../vars-dictionary.schema.json"
                   if dictionary else None,
                   schema_id=f"https://faion.net/schemas/vars/{stem}"
                             ".vars.schema.json")


def self_test() -> list[str]:
    """Every judgement and every guarantee this converter is not allowed to
    get wrong. Twenty-six checks."""
    failures: list[str] = []
    try:
        mods = JINJA.load_jinja()
    except JINJA.JinjaMissing as exc:
        return [f"Jinja is required to self-test: {exc}"]

    plan = _convert(CLEAN_FIXTURE)
    if "{{ service_name }}" not in plan["md_j2"]:
        failures.append("a clean placeholder did not become {{ service_name }}")
    if plan["md_j2"].count("{{ service_name }}") != 1:
        failures.append("a placeholder inside a code fence was rewritten")
    if "<Optional:" not in plan["md_j2"]:
        failures.append("a prose placeholder was not left alone")
    if any(i["verdict"] == "parameter" and "Optional" in i["raw"]
           for i in plan["items"]):
        failures.append("a prose placeholder was declared as a variable")
    if "service_name" not in plan["schema"]["properties"]:
        failures.append("the schema does not declare service_name")
    if plan["schema"]["$schema"] != JINJA.DRAFT07:
        failures.append("the schema is not draft-07")
    if plan["schema"].get("additionalProperties") is not False:
        failures.append("the schema accepts undeclared keys")
    if "x-faion-todo" not in plan["schema"]:
        failures.append("a schema generated with no dictionary carries no TODO")
    if not any("href-variable" in n for n in plan["notes"]):
        failures.append("a variable used as a whole href was not reported")
    for problem in verify(plan, mods):
        failures.append(f"clean fixture: {problem}")
    if set(plan["schema"]["properties"]) != set(
            JINJA.template_variables(plan["html_j2"])) | {"doc_url"}:
        # doc_url is the href case: the HTML renders it as text, so it is a
        # variable of the md template and of the html template's text.
        if set(JINJA.template_variables(plan["md_j2"])) != set(
                JINJA.template_variables(plan["html_j2"])):
            failures.append("the two templates declare different variables")

    declared = _convert(DECLARED_FIXTURE)
    props = declared["schema"]["properties"]
    if props.get("channel", {}).get("enum") != ["stable", "beta"]:
        failures.append("an enum declaration lost its options")
    if props.get("port", {}).get("default") != 8000:
        failures.append("an integer default was not carried as an integer")
    if not props.get("db_password", {}).get("x-faion-sensitive"):
        failures.append("a sensitive declaration lost x-faion-sensitive")
    if "db_password" in declared["schema"].get("required", []):
        failures.append("a sensitive variable was demanded of the caller")
    if "port" in declared["schema"].get("required", []):
        failures.append("a variable with a default was demanded of the caller")
    if "variables:" in declared["md_j2"]:
        failures.append("the header kept a variables: block the schema now owns")
    if "purpose: release note" not in declared["md_j2"]:
        failures.append("stripping variables: also ate the documentation keys")
    for problem in verify(declared, mods):
        failures.append(f"declared fixture: {problem}")

    table = _convert(TABLE_FIXTURE)
    if "risk_title" in table["schema"]["properties"]:
        failures.append("a per-row table placeholder became a variable")
    if not any(i["reason"] == "per-row-table" for i in table["items"]):
        failures.append("a per-row table placeholder was not reported")
    if "<risk_title>" not in table["md_j2"]:
        failures.append("a per-row table placeholder was rewritten anyway")

    for label, fixture, code in (("html-escaped", ESCAPED_FIXTURE, 3),
                                 ("sections:", SECTIONS_FIXTURE, 4),
                                 ("a raw {% delimiter", RAW_FIXTURE, 4),
                                 ("an undeclared {{x}}", ORPHAN_FIXTURE, 4)):
        try:
            _convert(fixture)
            failures.append(f"{label}: converted instead of refused")
        except Refused as exc:
            if exc.code != code:
                failures.append(f"{label}: refused with exit {exc.code}, "
                                f"expected {code}")
        except CORE.TplError as exc:
            failures.append(f"{label}: wrong refusal: {exc}")

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out"
        if write_plan(plan, out, False):
            failures.append("files were written without --write")
        if out.exists():
            failures.append("the output directory was created without --write")
        written = write_plan(plan, out, True)
        if len(written) != 3 or not all(p.is_file() for p in written):
            failures.append("--write did not produce the three files")
        else:
            loaded = json.loads(written[2].read_text(encoding="utf-8"))
            if loaded != plan["schema"]:
                failures.append("the written schema is not the planned one")
            env = JINJA.environment(mods, autoescape=False)
            values = {n: "x" for n in plan["variables"]}
            if "x" not in JINJA.render_file(env, written[0], values):
                failures.append("the written md.j2 did not render from disk")
    return failures


# ------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", help="the Markdown template to convert")
    ap.add_argument("--out-dir",
                    help="where the three files go (default: beside the "
                         "template)")
    ap.add_argument("--dictionary",
                    help="vars-dictionary.schema.json (default: discovered by "
                         "walking up from the template)")
    ap.add_argument("--write", action="store_true",
                    help="write the three files; without it nothing is touched")
    ap.add_argument("--json", action="store_true",
                    help="emit the plan as JSON on stdout")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if CORE is None or JINJA is None or MIGRATE is None:
        print(f"{NAME}: cannot load the pack helpers beside this script "
              "(lib/tplcore.py, lib/tpljinja.py, tpl-migrate.py)",
              file=sys.stderr)
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

    if not args.template:
        print(f"{NAME}: --template is required (or --self-test)",
              file=sys.stderr)
        return 2
    path = Path(args.template)
    out_dir = Path(args.out_dir) if args.out_dir else path.parent
    stem = path.name[:-3] if path.name.endswith(".md") else path.stem

    dictionary_path = find_dictionary(args.dictionary, path)
    try:
        text = path.read_text(encoding="utf-8")
        dictionary = JINJA.load_dictionary(dictionary_path)
    except (OSError, JINJA.SchemaBroken) as exc:
        print(f"{NAME}: cannot read: {exc}", file=sys.stderr)
        return 2

    try:
        plan = convert(text, stem, dictionary=dictionary,
                       dictionary_ref=dictionary_ref_for(out_dir,
                                                         dictionary_path),
                       schema_id=schema_id_for(path, stem), where=path.name)
    except Refused as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code
    except CORE.TplError as exc:
        print(f"{NAME}: {path}: {exc}", file=sys.stderr)
        return 2

    problems = verify(plan, mods)
    if problems:
        for problem in problems:
            print(f"{NAME}: {problem}", file=sys.stderr)
        print(f"{NAME}: {path}: the generated templates did not verify; "
              "nothing written", file=sys.stderr)
        return 2

    written = write_plan(plan, out_dir, args.write)
    summary = (f"{NAME}: {path} variables={len(plan['declarations'])} "
               f"dictionary-refs={plan['dictionary_refs']} "
               f"unclear={plan['unclear']} notes={len(plan['notes'])} -> "
               + (", ".join(str(p) for p in written) or "stdout (dry run)"))
    if args.json:
        print(json.dumps({k: v for k, v in plan.items()
                          if k != "items"} | {"items": plan["items"]},
                         indent=2, sort_keys=True, default=str))
        print(report(plan), file=sys.stderr)
        print(summary, file=sys.stderr)
    elif written:
        print(report(plan))
        print(summary)
    else:
        for label, body in (("md.j2", plan["md_j2"]),
                            ("html.j2", plan["html_j2"]),
                            ("vars.schema.json", JINJA.dumps(plan["schema"]))):
            print(f"===== {plan['stem']}.{label} =====")
            print(body, end="" if body.endswith("\n") else "\n")
        print(report(plan), file=sys.stderr)
        print(summary, file=sys.stderr)

    return 1 if plan["unclear"] or plan["notes"] else 0


if __name__ == "__main__":
    sys.exit(main())
