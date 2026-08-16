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

THE RESOLVER (skills/faion/templates/vars-resolver.json). The name drafted from
a placeholder's own text is raw — `name`, `handle`, `slug` — and the dictionary
deliberately carries disambiguated ones — `owner_handle`, `artefact_slug`. The
two lists barely intersect BY DESIGN. The resolver bridges them: a raw name plus
a context predicate over the label, heading and line, mapping to one entry. It
is consulted only after an exact dictionary match fails, and a candidate it does
not place falls through to a local declaration in the review queue. That is the
designed outcome, because a WRONG resolution has no visible failure — it builds
a correct-looking document with someone else's value silently inside it, since
the project store carries values between artefacts. Refuse rather than guess.

Input:  --template {file.md} [--out-dir {dir}] [--dictionary {file}]
        [--resolver {file} | --no-resolver] [--write]
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


# --------------------------------------------------------------- resolver

RESOLVER_REL = "skills/faion/templates/vars-resolver.json"
# Every predicate a rule may carry. An unknown one is a typo in the data file
# and is refused loudly: a silently ignored predicate makes a rule fire wider
# than its author measured, which is the one failure this layer must not have.
PREDICATES = ("label", "heading", "line", "raw", "not_line",
              "any_of_label_heading")
FIELD_OF = {"label": "label", "heading": "heading", "line": "text",
            "raw": "raw"}


class ResolverBroken(Exception):
    """The resolver file is not usable. Never silently ignored."""


def load_resolver(path: Path | None) -> list[dict]:
    """The compiled rules, or [] when there is no resolver.

    Absent is a normal state: the resolver is a heuristic layer and every
    caller must work without it. Present-but-malformed is not — a rule whose
    predicate this code does not understand would match more than it was
    measured on.
    """
    if path is None or not Path(path).is_file():
        return []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResolverBroken(f"{path}: not readable as JSON: {exc}") from exc
    return compile_rules(data)


def compile_rules(data: dict) -> list[dict]:
    """Rules with their predicates compiled. Pure; raises ResolverBroken."""
    rules = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(rules, list):
        raise ResolverBroken("no `rules` array")
    out: list[dict] = []
    for raw in rules:
        if not isinstance(raw, dict):
            raise ResolverBroken("a rule is not an object")
        for key in ("id", "name", "entry", "when"):
            if key not in raw:
                raise ResolverBroken(f"a rule has no `{key}`")
        when: dict = {}
        for key, pattern in raw["when"].items():
            if key not in PREDICATES:
                raise ResolverBroken(f"{raw['id']}: unknown predicate {key!r}; "
                                     f"known are {', '.join(PREDICATES)}")
            try:
                when[key] = re.compile(pattern, re.IGNORECASE)
            except re.error as exc:
                raise ResolverBroken(f"{raw['id']}: {key}: {exc}") from exc
        if not when:
            raise ResolverBroken(f"{raw['id']}: no predicate — a rule keyed "
                                 "only on the raw name is what the dictionary "
                                 "already does")
        out.append({"id": raw["id"], "name": raw["name"],
                    "entry": raw["entry"], "when": when})
    return out


def rule_matches(rule: dict, item: dict) -> bool:
    """Every predicate present must match. Absent is not a constraint."""
    for key, pattern in rule["when"].items():
        if key == "any_of_label_heading":
            if not (pattern.search(item.get("label") or "")
                    or pattern.search(item.get("heading") or "")):
                return False
        elif key == "not_line":
            if pattern.search(item.get("text") or ""):
                return False
        elif not pattern.search(item.get(FIELD_OF[key]) or ""):
            return False
    return True


def refuse_reason(entry: str, item: dict, dictionary: dict) -> str | None:
    """Why this candidate must NOT take this entry, or None.

    These are the guards a rule author cannot forget, because they are not
    written per rule. Each one is a real specimen from the corpus, not a
    hypothetical.
    """
    spec = dictionary.get(entry)
    if not isinstance(spec, dict):
        return f"{entry} is not in the dictionary"
    want = spec.get("type")
    local = JINJA.JSON_TYPE.get(item.get("type") or "string", "string")
    if want in ("array", "boolean") and want != local:
        # `- approved: <yes / no>` against the boolean `approved`: Jinja
        # renders a Python bool as `True`, so the artefact would ship
        # `approved: True` where its own contract says `yes`.
        return f"{entry} is {want} and the placeholder is {local}"
    options = item.get("options")
    if options:
        allowed = spec.get("enum")
        if not allowed or not set(options) <= set(allowed):
            # `- decision: <go|hold|no-op>` against decision_statement, which
            # is any string: widening an enum turns a refusal into silence.
            return (f"{entry} does not carry the enum "
                    f"{'/'.join(str(o) for o in options)}")
    return None


def apply_resolver(items: list[dict], rules: list[dict], dictionary: dict,
                   declared: dict) -> list[dict]:
    """Rename every parameter the resolver can place in the dictionary.

    Returns one record per resolution. Anything it does not place is left
    exactly as it was — the review queue, which is the designed outcome.
    """
    if not rules or not dictionary:
        return []
    taken = set(declared)
    proposals: list[tuple[int, str, str]] = []
    for index, item in enumerate(items):
        if item["verdict"] != "parameter" or not item.get("name"):
            continue
        if item["name"] in dictionary or item["name"] in declared:
            continue                      # exact match, or the author decided
        entries = {rule["entry"] for rule in rules
                   if rule["name"] == item["name"] and rule_matches(rule, item)}
        if len(entries) != 1:
            continue                      # no rule, or two rules disagree
        entry = entries.pop()
        if entry in taken or refuse_reason(entry, item, dictionary):
            continue
        rule_id = next(rule["id"] for rule in rules
                       if rule["name"] == item["name"]
                       and rule["entry"] == entry and rule_matches(rule, item))
        proposals.append((index, entry, rule_id))
    # Two slots on ONE line taking one entry would render one value twice.
    # `**Last updated:** [Date] | **Next review:** [Date]` is the specimen: the
    # label parser hands both slots the label `Last updated`.
    seen_on_line: dict[tuple[int, str], int] = {}
    for index, entry, _ in proposals:
        key = (items[index]["line"], entry)
        seen_on_line[key] = seen_on_line.get(key, 0) + 1
    records: list[dict] = []
    for index, entry, rule_id in proposals:
        if seen_on_line[(items[index]["line"], entry)] > 1:
            continue
        item = items[index]
        records.append({"line": item["line"], "raw": item["raw"],
                        "from": item["name"], "entry": entry, "rule": rule_id})
        item["resolved_from"] = item["name"]
        item["resolved_by"] = rule_id
        item["name"] = entry
    return records


def find_resolver(explicit: str | None, template: Path | None) -> Path | None:
    """The corpus resolver, named or discovered by walking up."""
    if explicit:
        return Path(explicit)
    if template is None:
        return None
    for parent in Path(template).resolve().parents:
        candidate = parent / RESOLVER_REL
        if candidate.is_file():
            return candidate
    return None


# --------------------------------------------------------------- the plan

def convert(text: str, stem: str, *, dictionary: dict,
            dictionary_ref: str | None, schema_id: str,
            where: str | None = None, resolver: list[dict] | None = None) -> dict:
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

    # Exact dictionary match first (apply_resolver skips those), then the
    # resolver, then a local declaration. Per-row and collision downgrades run
    # BEFORE this on purpose: a name the converter already refuses to declare
    # is not a name the resolver gets a second go at.
    resolutions = apply_resolver(items, resolver or [], dictionary, declared)

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
            "resolutions": resolutions, "resolved": len(resolutions),
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
             f"resolved={plan.get('resolved', 0)} "
             f"unclear={plan['unclear']}"]
    for item in plan["items"]:
        if item["verdict"] == "parameter":
            via = (f"  RESOLVED {item['resolved_from']} -> {item['name']} "
                   f"by {item['resolved_by']}" if item.get("resolved_by")
                   else "")
            lines.append(f"  line {item['line']:>4}  {item['raw']} -> "
                         f"{{{{ {item['name']} }}}}  {item['type']}{via}")
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

# The resolver fixtures. Four lines, and each is a real corpus shape: the one
# that must resolve, the two the guards must refuse, and the pair on one line
# that renders one value twice if nothing stops it.
RESOLVE_FIXTURE = """# Runbook

- owner: <@handle>
- decision: <go|hold|no-op>

**Last updated:** [Date] | **Next review:** [Date]

## Out of Scope

- [exclusion]
"""

TAKEN_FIXTURE = """<!--
purpose: p
produces: markdown
variables:
  - name: owner_handle
    type: string
    required: true
    description: The handle of whoever signs this off, decided by hand.
-->
# Doc

Signed by {{owner_handle}}.

- owner: <@handle>
"""

MINI_DICTIONARY = {
    "owner_handle": {"type": "string", "title": "Owner handle",
                     "description": "Which handle identifies the owner?"},
    "reviewer_name": {"type": "string", "title": "Reviewer",
                      "description": "Who reviews this?"},
    "decision_statement": {"type": "string", "title": "Decision",
                           "description": "What was decided?"},
    "out_of_scope": {"type": "array", "title": "Out of scope",
                     "description": "What is explicitly NOT covered here?"},
    "last_reviewed_date": {"type": "string", "title": "Last reviewed",
                           "description": "When was this last reviewed?"},
}

MINI_RESOLVER = {"rules": [
    {"id": "owner-handle", "name": "handle", "entry": "owner_handle",
     "when": {"label": "^owner$"}, "why": "fixture"},
    {"id": "decision-widens", "name": "decision", "entry": "decision_statement",
     "when": {"label": "^decision$"}, "why": "fixture: must be refused"},
    {"id": "scope-retypes", "name": "exclusion", "entry": "out_of_scope",
     "when": {"heading": "^out of scope$"}, "why": "fixture: must be refused"},
    {"id": "last-updated", "name": "date", "entry": "last_reviewed_date",
     "when": {"label": "^last.updated$"}, "why": "fixture: must be refused"},
    {"id": "missing-entry", "name": "handle", "entry": "not_in_dictionary",
     "when": {"label": "^nowhere$"}, "why": "fixture"},
]}

AMBIGUOUS_RESOLVER = {"rules": [
    {"id": "one", "name": "handle", "entry": "owner_handle",
     "when": {"label": "^owner$"}, "why": "fixture"},
    {"id": "two", "name": "handle", "entry": "reviewer_name",
     "when": {"line": "^- owner:"}, "why": "fixture: disagrees with `one`"},
]}


def _convert(text: str, stem: str = "fixture", dictionary=None,
             resolver=None) -> dict:
    return convert(text, stem, dictionary=dictionary or {},
                   dictionary_ref="../vars-dictionary.schema.json"
                   if dictionary else None,
                   schema_id=f"https://faion.net/schemas/vars/{stem}"
                             ".vars.schema.json",
                   resolver=resolver)


def resolver_checks() -> list[str]:
    """The resolver's judgements, and every guard that must refuse.

    A wrong resolution has no visible failure — it builds a correct-looking
    document with someone else's value in it — so more than half of these
    assert a REFUSAL rather than a result.
    """
    failures: list[str] = []
    rules = compile_rules(MINI_RESOLVER)

    plan = _convert(RESOLVE_FIXTURE, dictionary=MINI_DICTIONARY,
                    resolver=rules)
    props = plan["schema"]["properties"]
    if "owner_handle" not in props:
        failures.append("resolver: `<@handle>` under an owner label did not "
                        "become owner_handle")
    if "handle" in props:
        failures.append("resolver: the raw name survived the resolution")
    if props.get("owner_handle") != {
            "$ref": "../vars-dictionary.schema.json#/$defs/owner_handle"}:
        failures.append("resolver: a resolved name did not $ref the dictionary")
    if plan["resolved"] != 1:
        failures.append(f"resolver: resolved={plan['resolved']}, expected 1 — "
                        "a guard let something through")
    if [r["rule"] for r in plan["resolutions"]] != ["owner-handle"]:
        failures.append("resolver: the resolution does not name its rule")
    if "decision" not in props:
        failures.append("guard: an enum-widening resolution was allowed — "
                        "decision_statement takes any string, so go|hold|no-op "
                        "would stop being refused")
    if "exclusion" not in props:
        failures.append("guard: an array entry took a one-bullet placeholder — "
                        "the rendered line would be a Python list")
    if "last_reviewed_date" in props or props.get("date") is None:
        failures.append("guard: two slots on one line took one entry, so the "
                        "same value would render twice")

    bare = _convert(RESOLVE_FIXTURE, dictionary=MINI_DICTIONARY, resolver=None)
    if "handle" not in bare["schema"]["properties"] \
            or bare["resolved"] != 0:
        failures.append("--no-resolver: a name was resolved with no resolver")

    ambiguous = _convert(RESOLVE_FIXTURE, dictionary=MINI_DICTIONARY,
                         resolver=compile_rules(AMBIGUOUS_RESOLVER))
    if "handle" not in ambiguous["schema"]["properties"]:
        failures.append("guard: two rules disagreed about one candidate and it "
                        "was resolved anyway — refusing is the whole contract")

    taken = _convert(TAKEN_FIXTURE, dictionary=MINI_DICTIONARY, resolver=rules)
    if taken["resolved"]:
        failures.append("guard: a rule took a name the template's own header "
                        "already declares")

    # A rule may name an entry the dictionary does not carry — a rename or a
    # deletion on the dictionary side, which nothing else in this repo checks.
    if not refuse_reason("not_in_dictionary", {"type": "string"},
                         MINI_DICTIONARY):
        failures.append("guard: a rule pointing at an entry the dictionary "
                        "does not carry was allowed to resolve")

    for label, data, fragment in (
            ("an unknown predicate",
             {"rules": [{"id": "x", "name": "handle", "entry": "owner_handle",
                         "when": {"colour": "^blue$"}}]}, "unknown predicate"),
            ("a rule with no predicate",
             {"rules": [{"id": "x", "name": "handle", "entry": "owner_handle",
                         "when": {}}]}, "no predicate"),
            ("a rule with no entry",
             {"rules": [{"id": "x", "name": "handle",
                         "when": {"label": "^owner$"}}]}, "`entry`"),
            ("a file with no rules array", {"note": "hi"}, "no `rules`")):
        try:
            compile_rules(data)
            failures.append(f"{label}: compiled instead of refusing")
        except ResolverBroken as exc:
            if fragment not in str(exc):
                failures.append(f"{label}: refused with the wrong message: "
                                f"{exc}")
    return failures


def self_test() -> list[str]:
    """Every judgement and every guarantee this converter is not allowed to
    get wrong. Forty-one checks."""
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
    return failures + resolver_checks()


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
    ap.add_argument("--resolver",
                    help="vars-resolver.json, the raw-name-plus-context to "
                         "dictionary-entry rules (default: discovered beside "
                         "the dictionary)")
    ap.add_argument("--no-resolver", action="store_true",
                    help="do not consult the resolver; every name that is not "
                         "already a dictionary entry stays local")
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
        print(f"{NAME}: self-test checks=41 failures={len(failures)}")
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
    resolver_path = None if args.no_resolver \
        else find_resolver(args.resolver, path)
    try:
        text = path.read_text(encoding="utf-8")
        dictionary = JINJA.load_dictionary(dictionary_path)
        resolver = load_resolver(resolver_path)
    except (OSError, JINJA.SchemaBroken, ResolverBroken) as exc:
        print(f"{NAME}: cannot read: {exc}", file=sys.stderr)
        return 2

    try:
        plan = convert(text, stem, dictionary=dictionary,
                       dictionary_ref=dictionary_ref_for(out_dir,
                                                         dictionary_path),
                       schema_id=schema_id_for(path, stem), where=path.name,
                       resolver=resolver)
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
               f"resolved={plan['resolved']} "
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
