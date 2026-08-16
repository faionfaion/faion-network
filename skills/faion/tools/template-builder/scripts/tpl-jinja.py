#!/usr/bin/env python3
"""tpl-jinja.py — convert one Markdown template into the Jinja form.

`templates/<name>.md` becomes `<name>.md.j2`, `<name>.html.j2` and
`<name>.vars.schema.json` (.aidocs/conventions/template-jinja-migration.md).
The HTML is generated from the MARKDOWN SOURCE STRUCTURE, not by converting a
rendered document at runtime, so the two are siblings a generator wrote
together rather than one file with a format branch in it.

It proposes. It does not decide, and it writes nothing without --write.

ONE SOURCE, SEVERAL GENERATED FORMS (--migrate). The source of truth is
`<name>.md.j2` plus `<name>.vars.schema.json`. `<name>.html.j2` and
`<name>.md` are OUTPUTS of it. The `.md` stays on disk because it is the form
the one supported instantiator eats — faion-solo-framework/scripts/
init_project.py substitutes `<token>` by literal string replacement and its
`--check` scans for the same shape — but it stops being authored: --migrate
regenerates it from the `.md.j2` so it cannot hold bytes the source does not
imply. --check re-derives every generated form and diffs it, which is the same
gate init_project.py --check already is.

--migrate is ATOMIC per template. It writes the three Jinja files, regenerates
the `.md`, rewrites that methodology's `## Templates` table rows and the inline
`## Template Contents` body — or it does none of them. A half-migrated template
makes validate-methodology-templates.py fail with "declared template missing",
so partial application is the one outcome that must be impossible.

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
        [--resolver {file} | --no-resolver] [--migrate | --check] [--write]
Output: the three files, or all three to stdout when dry-running.

Exit: 0 every placeholder resolved · 1 placeholders were left for a human (the
      normal outcome), or --check found drift · 2 the tool could not run · 3
      refused, the placeholders are already HTML-escaped · 4 refused, the
      source carries a construct this converter will not translate · 5 refused,
      --migrate found no `## Templates` row naming this template.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
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


# ----------------------------------------------------- the generated forms
#
# Everything here derives ONE output from `<name>.md.j2` and nothing else. That
# is what makes --check a real drift test rather than a diff of two unrelated
# artefacts, and it is why convert() calls the same functions instead of
# carrying a second copy of the rendering.

# What the regenerated `.md` writes where the `.md.j2` holds a variable.
#
# `<name>`, the corpus's incumbent angle convention — because it is the shape
# the one supported instantiator understands. faion-solo-framework/scripts/
# init_project.py substitutes by literal `text.replace("<token>", value)` and
# its `--check` scans for that same spelling. A `{{ name }}` left in the `.md`
# would be invisible to BOTH: never substituted, and never reported as
# unsubstituted, which is a document that ships with a hole and nothing to say
# so.
#
# template-builder.md §1 rejected `<Angle>` as the BUILDER's INPUT, where a
# hand-written `<one paragraph>` cannot be told apart from a variable. That
# argument does not reach this file, because here the angle tokens are OUTPUT:
# every one of them is generated from a declared schema property, so it is
# always a snake_case name the schema carries. The ambiguity §1 measured is a
# property of hand authoring, and nothing here is hand-authored.
ANGLE_FOR_VAR = r"<\1>"


def md_from_j2(md_j2: str) -> str:
    """The standalone Markdown form. Pure.

    Whole-file, header included: the header cannot hold a `{{ }}` (the
    `variables:` run the schema now owns is stripped before this runs), so
    there is no region to protect and no split to get wrong.
    """
    return SPACED.sub(ANGLE_FOR_VAR, md_j2)


def html_from_j2(md_j2: str, stem: str) -> str:
    """The self-contained HTML form. Pure.

    Each variable is held as an opaque sentinel through the Markdown render and
    put back as `{{ name }}` afterwards, so the two templates cannot drift and
    no value is anywhere near this code path — at render time autoescape is
    what makes a value text (§0), and here there are no values at all.
    """
    _, body = CORE.split_header(md_j2)
    marks: list[str] = []

    def mark(match: re.Match) -> str:
        marks.append("{{ " + match.group(1) + " }}")
        return f"\x01{len(marks) - 1}\x01"

    marked = SPACED.sub(mark, body)
    return CORE.md_to_html(marked.strip("\n") + "\n", title_of(body, stem),
                           marks or None)


# The five keys validate-methodology-templates.py demands of every file the
# `## Templates` table names, and the exact shape it demands them in. Copied
# rather than imported because a tool pack ships alone — but copied from the
# GATE, so a regenerated `.md` that would fail it is refused before it is
# written rather than discovered by the pre-commit hook.
GATE_HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on",
                    "token-budget-impact")


def gate_header_keys(text: str) -> set[str]:
    """Which of the five keys the gate would find in this file."""
    head = "\n".join(text.splitlines()[:20]).lower()
    return {key for key in GATE_HEADER_KEYS
            if re.search(rf"^\s*\W*\s*{re.escape(key)}\s*:\s*\S", head, re.M)}


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
    html_j2 = html_from_j2(md_j2, stem)

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
            "md": md_from_j2(md_j2), "source": text,
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

    # Both files the `## Templates` table will name are header-checked by
    # validate-methodology-templates.py. A key the source carried and a
    # generated form lost is a validator failure this tool would have caused,
    # so it is caught here — before anything is written — rather than by the
    # pre-commit hook after 2,500 templates have moved.
    had = gate_header_keys(plan.get("source", ""))
    for label, text in (("md", plan.get("md", "")),
                        ("md.j2", plan["md_j2"])):
        lost = sorted(had - gate_header_keys(text))
        if lost:
            problems.append(
                f"{label}: the source carried {', '.join(lost)} in its first 20 "
                "lines and this form does not — validate-methodology-templates "
                "would report the header incomplete")
    if "{{" in plan.get("md", ""):
        problems.append("md: a `{{` survived into the standalone Markdown, "
                        "where the framework's substituter neither fills it "
                        "nor reports it")
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


# --------------------------------------------------------------- migration
#
# WHAT THE `## Templates` TABLE NAMES AFTER A MIGRATION, and why.
#
# Two rows: `templates/<name>.md.j2` (the source) and `templates/<name>.md`
# (the generated deliverable). Not `.html.j2`, not `.vars.schema.json`.
#
# validate-methodology-templates.py header-checks whatever the table names, and
# the five-key header exists for a HUMAN opening the file. Both named rows have
# one for free: the header rides through the conversion into the `.md.j2` and
# back out into the `.md`. The other two forms have no reader to serve — the
# `.html.j2` is a rendered document with no comment header at all, and the
# schema is JSON, which would need a `__faion_header__` key restating what its
# own `title` and `description` already say. Naming them would mean inventing a
# header for two machine artefacts to satisfy a gate written for readable
# templates.
#
# Delivery does not depend on the table either way: `packablePath` ships
# EVERYTHING under a `templates/` path segment un-extension-gated (F036/AD-024),
# so all four files reach a user's disk whether or not a row names them. The
# table is a reading guide, and the rule is "name what a human opens".

SUBSECTION = re.compile(r"^### `([^`]+)`[ \t]*$")
FENCE_RUN = re.compile(r"(`{3,})")
FENCE_LINE = re.compile(r"^\s*(`{3,}|~{3,})")
GENERATED_NOTE = ("Generated from `templates/{stem}.md.j2` by "
                  "`tpl-jinja --migrate`; do not hand-edit.")


def outside_fence(text: str):
    """(offset, line) for every line NOT inside a fenced code block.

    Both sections this module edits are found by heading, and an inlined
    template body is full of headings — `## Identity`, `### Steps` — inside its
    fence. A plain `^## ` regex ends the `## Template Contents` section at the
    first of them, which made a second --migrate on the same methodology parse
    a section that stops in the middle of a code block. Nothing about that is
    hypothetical: it is the first thing --check caught.
    """
    offset = 0
    fence: str | None = None
    for line in text.split("\n"):
        found = FENCE_LINE.match(line)
        run = found.group(1) if found else None
        if fence is None:
            if run:
                fence = run
            else:
                yield offset, line
        elif run and run[0] == fence[0] and len(run) >= len(fence):
            fence = None
        offset += len(line) + 1


def section_span(text: str, heading: str) -> tuple[int, int] | None:
    """(body start, body end) for `## <heading>`, or None. Fence-aware."""
    start = None
    for offset, line in outside_fence(text):
        if start is None:
            if line.strip() == f"## {heading}":
                start = offset + len(line) + 1
            continue
        if line.startswith("## "):
            return start, offset
    return (start, len(text)) if start is not None else None


class MigrationRefused(Exception):
    """--migrate will not touch this template. `.code` is the exit."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def retable(text: str, stem: str) -> str:
    """The AGENTS.md with this template's `## Templates` row split in two.

    Pure. Raises MigrationRefused(5) when no row names `templates/<stem>.md`:
    a template no row names is not documented today (the shape CR-010 describes),
    and ADDING a row is a delivery decision a converter must not make on its own.
    Refusing leaves the template exactly as it was, in the report, for a human.
    """
    span = section_span(text, "Templates")
    if span is None:
        raise MigrationRefused(
            5, f"{stem}.md: the methodology's AGENTS.md has no `## Templates` "
               "section, so there is no row to point at the new source. Adding "
               "the section is a documentation decision, not a conversion")
    body = text[span[0]:span[1]]
    source_name = f"templates/{stem}.md.j2"
    target_name = f"templates/{stem}.md"
    lines = body.split("\n")
    index = None
    for position, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        cells = _cells(line)
        if cells and cells[0].strip("`") == target_name:
            index = position
            break
        if cells and cells[0].strip("`") == source_name:
            return text            # already migrated; idempotent
    if index is None:
        raise MigrationRefused(
            5, f"{stem}.md: no `## Templates` row names it, so it is not a "
               "declared template of this methodology. Converting it would "
               "leave the source undeclared and the row absent — decide "
               "whether it should be declared first")
    cells = _cells(lines[index])
    note = GENERATED_NOTE.format(stem=stem)
    source_cells = list(cells)
    source_cells[0] = f"`{source_name}`"
    generated_cells = list(cells)
    generated_cells[0] = f"`{target_name}`"
    if note not in generated_cells[-1]:
        generated_cells[-1] = (generated_cells[-1] + " " + note).strip()
    lines[index:index + 1] = [_row(source_cells), _row(generated_cells)]
    return text[:span[0]] + "\n".join(lines) + text[span[1]:]


def fence_for(body: str) -> str:
    """A fence longer than any the body already opens.

    A `.md.j2` full of shell and JSON examples routinely carries ``` runs of
    its own, and inlining it inside a three-backtick fence would end the block
    at the first of them — the inline would silently show a third of the file.
    """
    longest = max((len(m.group(1)) for m in FENCE_RUN.finditer(body)),
                  default=0)
    return "`" * max(3, longest + 1)


def inline_block(stem: str, md_j2: str) -> str:
    """The `### templates/<stem>.md.j2` subsection, source verbatim."""
    fence = fence_for(md_j2)
    body = md_j2 if md_j2.endswith("\n") else md_j2 + "\n"
    return (f"### `templates/{stem}.md.j2`\n\n"
            f"{fence}jinja\n{body}{fence}\n")


def reinline(text: str, stem: str, md_j2: str) -> str:
    """The AGENTS.md with this template's inline body regenerated. Pure.

    NO-OP when the methodology has no `## Template Contents` section, or has
    one that never inlined this template. The section exists for files the
    packer does not ship standalone; `.md.j2` and `.md` both ship by path, so
    CREATING an inline would duplicate bytes already delivered — 2,505 times,
    into the file every retrieval loads first. Where an inline already exists
    it is regenerated, from the `.md.j2` and by the same call that writes the
    `.md.j2`, so the pair cannot drift.
    """
    span = section_span(text, "Template Contents")
    if span is None:
        return text
    body = text[span[0]:span[1]]
    marks = [(offset, SUBSECTION.match(line).group(1))
             for offset, line in outside_fence(body)
             if SUBSECTION.match(line)]
    wanted = (f"templates/{stem}.md", f"templates/{stem}.md.j2")
    for position, (offset, name) in enumerate(marks):
        if name not in wanted:
            continue
        end = marks[position + 1][0] if position + 1 < len(marks) else len(body)
        tail = body[end:]
        new_body = body[:offset] + inline_block(stem, md_j2)
        if tail and not new_body.endswith("\n\n"):
            new_body += "\n"
        new_body += tail
        return text[:span[0]] + new_body + text[span[1]:]
    return text


def migration_texts(plan: dict, agents_md: str) -> dict[str, str]:
    """Every file body this migration writes, keyed by role. Pure.

    Computing ALL of it before any I/O is what makes the operation atomic in
    the case that actually happens: a template with no table row, or an inline
    that cannot be parsed, fails here — with nothing on disk touched, because
    nothing on disk has been opened for writing yet.
    """
    stem = plan["stem"]
    staged = retable(agents_md, stem)
    return {"md_j2": plan["md_j2"],
            "html_j2": plan["html_j2"],
            "schema": JINJA.dumps(plan["schema"]),
            "md": plan["md"],
            "agents": reinline(staged, stem, plan["md_j2"])}


def migration_paths(stem: str, template: Path, out_dir: Path,
                    agents_md: Path) -> dict[str, Path]:
    return {"md_j2": out_dir / f"{stem}.md.j2",
            "html_j2": out_dir / f"{stem}.html.j2",
            "schema": out_dir / f"{stem}.vars.schema.json",
            "md": template,
            "agents": agents_md}


def apply_atomic(files: dict[Path, str], fault=None) -> list[Path]:
    """Write every file, or leave every one of them exactly as it was.

    Two phases. Phase one stages each new body beside its target, so a full
    disk or a read-only tree is discovered before anything is replaced. Phase
    two swaps them in with os.replace, which is atomic per file; the batch is
    made atomic by holding every original's bytes and putting them back if any
    swap raises. A file this call created is removed rather than restored.

    `fault` is the self-test's way in: it is called as fault(phase, path) at
    every point a real failure could occur, and raising from it must leave the
    tree untouched. A rollback nobody has ever executed is a rollback that does
    not work.
    """
    targets = sorted(files)
    originals: dict[Path, bytes | None] = {}
    staged: dict[Path, Path] = {}
    done: list[Path] = []
    try:
        for path in targets:
            path.parent.mkdir(parents=True, exist_ok=True)
            originals[path] = path.read_bytes() if path.exists() else None
            tmp = path.with_name(path.name + ".faion-migrate-tmp")
            tmp.write_text(files[path], encoding="utf-8")
            staged[path] = tmp
            if fault is not None:
                fault("stage", path)
        for path in targets:
            if fault is not None:
                fault("replace", path)
            os.replace(staged.pop(path), path)
            done.append(path)
    except BaseException:
        for path in done:
            original = originals[path]
            if original is None:
                path.unlink()
            else:
                path.write_bytes(original)
        for tmp in staged.values():
            tmp.unlink(missing_ok=True)
        raise
    return targets


def check_findings(md_j2: str, stem: str, on_disk: dict[str, str],
                   schema: dict | None) -> list[str]:
    """Every generated form re-derived from the `.md.j2` and diffed. Pure.

    This is the drift gate, and it is the same shape as
    init_project.py --check: regenerate, compare, exit 1 on a difference. It
    checks only what the `.md.j2` DETERMINES — the `.md`, the `.html.j2` and
    the inline. The schema is not derivable from the source (a property's
    `description` is the question put to the author, and the placeholder text
    it was drafted from is gone), so the schema is a SECOND source of truth and
    is checked for agreement, never regenerated.
    """
    findings: list[str] = []
    expected = {"md": md_from_j2(md_j2), "html_j2": html_from_j2(md_j2, stem)}
    for role, want in expected.items():
        have = on_disk.get(role)
        if have is None:
            findings.append(f"{role}: not on disk beside the source")
        elif have != want:
            findings.append(f"{role}: on disk does not match what "
                            f"{stem}.md.j2 generates — it was hand-edited, or "
                            "the generator changed")
    agents = on_disk.get("agents")
    if agents is not None and reinline(agents, stem, md_j2) != agents:
        findings.append("agents: the inline `## Template Contents` body does "
                        f"not match {stem}.md.j2")
    if schema is not None:
        used = JINJA.template_variables(md_j2)
        declared = set(schema.get("properties") or {})
        for name in sorted(used - declared):
            findings.append(f"schema: {name} is used by the template and the "
                            "schema does not declare it — the render refuses "
                            "by name")
        for name in sorted(declared - used):
            findings.append(f"schema: {name} is declared and the template "
                            "never references it")
    return findings


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


RENAMING_FIXTURE = """<!--
purpose: p
produces: markdown
-->
# Doc

- Owner: [Owner Name]
"""

AGENTS_FIXTURE = """# fixture-methodology

## Summary

A fixture.

## Templates

| File | Purpose |
|------|---------|
| `templates/other.sh` | A shell scaffold. |
| `templates/fixture.md` | The runbook skeleton. |

Files the packer does not ship standalone have their bodies inlined under \
`## Template Contents` at the end of this file - read them there.

## Related

- [[something]]

## Template Contents

Bodies of the templates above.

### `templates/other.sh`

```sh
echo hi
```

### `templates/fixture.md`

```markdown
the stale inlined copy
```
"""

AGENTS_NO_ROW = AGENTS_FIXTURE.replace(
    "| `templates/fixture.md` | The runbook skeleton. |\n", "")
AGENTS_NO_SECTION = AGENTS_FIXTURE.replace("## Templates", "## Artefacts", 1)
AGENTS_NO_INLINE = AGENTS_FIXTURE.split("## Template Contents")[0]
AGENTS_OTHER_INLINE = AGENTS_FIXTURE.replace(
    "### `templates/fixture.md`\n\n```markdown\nthe stale inlined copy\n```\n",
    "")


def _tree(root: Path, agents: str, template: str) -> tuple[Path, Path]:
    """A scratch methodology dir: AGENTS.md plus templates/fixture.md."""
    (root / "templates").mkdir(parents=True, exist_ok=True)
    agents_md = root / "AGENTS.md"
    agents_md.write_text(agents, encoding="utf-8")
    md = root / "templates" / "fixture.md"
    md.write_text(template, encoding="utf-8")
    return agents_md, md


def _untouched(agents_md: Path, md: Path, agents: str, template: str,
               label: str) -> list[str]:
    """Nothing moved. The single most important assertion in --migrate."""
    out: list[str] = []
    if not md.is_file():
        out.append(f"{label}: the source .md is gone")
    elif md.read_text(encoding="utf-8") != template:
        out.append(f"{label}: the source .md was rewritten anyway")
    if agents_md.read_text(encoding="utf-8") != agents:
        out.append(f"{label}: AGENTS.md was rewritten anyway")
    strays = sorted(p.name for p in md.parent.iterdir()
                    if p.name != "fixture.md")
    if strays:
        out.append(f"{label}: left {', '.join(strays)} behind")
    return out


def migrate_checks() -> list[str]:
    """--migrate: the table rule, the inline rule, and atomicity.

    Atomicity is the one that matters. A half-migrated template makes
    validate-methodology-templates.py fail with "declared template missing",
    so every failure path below asserts that the tree is exactly as it was.
    """
    failures: list[str] = []
    plan = _convert(CLEAN_FIXTURE)

    # ---- the `## Templates` table rule
    retabled = retable(AGENTS_FIXTURE, "fixture")
    if "| `templates/fixture.md.j2` | The runbook skeleton. |" not in retabled:
        failures.append("retable: the .md row did not gain a .md.j2 source row")
    if "`templates/fixture.md` | The runbook skeleton. Generated from" \
            not in retabled:
        failures.append("retable: the .md row does not say it is generated")
    if retabled.index("fixture.md.j2`") > retabled.index("| `templates/fixture.md` |"):
        failures.append("retable: the generated row precedes its source")
    if "| `templates/other.sh` | A shell scaffold. |" not in retabled:
        failures.append("retable: another template's row was disturbed")
    if retable(retabled, "fixture") != retabled:
        failures.append("retable: a second run changed the table again — a "
                        "re-migration would duplicate every row")
    for label, text in (("no row names it", AGENTS_NO_ROW),
                        ("no ## Templates section", AGENTS_NO_SECTION)):
        try:
            retable(text, "fixture")
            failures.append(f"retable: {label} and it converted anyway — "
                            "adding a row is a delivery decision")
        except MigrationRefused as exc:
            if exc.code != 5:
                failures.append(f"retable: {label} refused with exit "
                                f"{exc.code}, expected 5")

    # ---- the inline rule
    inlined = reinline(AGENTS_FIXTURE, "fixture", plan["md_j2"])
    if "### `templates/fixture.md.j2`" not in inlined:
        failures.append("reinline: the inline heading still names the .md")
    if "the stale inlined copy" in inlined:
        failures.append("reinline: the stale inlined body survived")
    if plan["md_j2"] not in inlined:
        failures.append("reinline: the inline is not the .md.j2 verbatim")
    if "### `templates/other.sh`" not in inlined or "echo hi" not in inlined:
        failures.append("reinline: another template's inline was eaten")
    if reinline(AGENTS_NO_INLINE, "fixture", plan["md_j2"]) != AGENTS_NO_INLINE:
        failures.append("reinline: a methodology with no ## Template Contents "
                        "section had one written into it")
    if reinline(AGENTS_OTHER_INLINE, "fixture", plan["md_j2"]) \
            != AGENTS_OTHER_INLINE:
        failures.append("reinline: a section that never inlined this template "
                        "gained an entry for it")
    if fence_for("a ``` fence\n") <= "```":
        failures.append("fence_for: an inlined body carrying ``` would end the "
                        "block early and show a third of the file")

    # ---- the generated forms
    regenerated = md_from_j2(plan["md_j2"])
    if "{{" in regenerated:
        failures.append("md_from_j2: a Jinja delimiter survived into the .md")
    if "<service_name>" not in regenerated:
        failures.append("md_from_j2: a variable did not come back as <angle>, "
                        "so the framework substituter cannot fill it")
    if regenerated != plan["md"]:
        failures.append("the plan's .md is not what md_from_j2 produces")
    # convert() CALLS html_from_j2, so --check re-deriving the same bytes is
    # true by construction rather than by test — which is the stronger form.
    # What is worth asserting is that the derivation keeps the variable: an
    # .html.j2 that lost it renders from a different value map than its
    # Markdown sibling, which is the drift §1 forbids.
    if "<h1>Runbook for {{ service_name }}</h1>" not in plan["html_j2"]:
        failures.append("html_from_j2: the HTML body lost a variable the "
                        "Markdown keeps, so the pair no longer renders from "
                        "one value map")
    # The `.md` is an OUTPUT, not the original bytes: a placeholder spelt
    # `[Owner Name]` comes back as the declared name `<owner_name>`. Proving
    # that on a fixture whose spelling actually changes is the only way to see
    # it — CLEAN_FIXTURE's `<service_name>` is already its own declared name,
    # so it regenerates byte-identical and would pass a broken generator too.
    renaming = _convert(RENAMING_FIXTURE)
    if renaming["md"] == RENAMING_FIXTURE:
        failures.append("the regenerated .md is the authored bytes — it is an "
                        "output now, so a placeholder must come back spelt as "
                        "the name the schema declares")
    if "<owner_name>" not in renaming["md"] or "[Owner Name]" in renaming["md"]:
        failures.append("the regenerated .md did not normalise a placeholder "
                        "onto its declared name")

    # ---- the header the gate reads, on both files the table will name
    mods = JINJA.load_jinja()
    five = "<!--\n" + "\n".join(f"{k}: x" for k in GATE_HEADER_KEYS) + "\n-->\n"
    if gate_header_keys(five) != set(GATE_HEADER_KEYS):
        failures.append("gate_header_keys: a five-key header was not read the "
                        "way validate-methodology-templates reads it")
    if gate_header_keys("# Doc\n\npurpose of this\n"):
        failures.append("gate_header_keys: prose was counted as a header key")
    doctored = dict(plan)
    doctored["source"] = five + plan["source"]
    if not any("header incomplete" in p for p in verify(doctored, mods)):
        failures.append("verify: a generated form that dropped a header key "
                        "the source carried was not caught — validator 5 would "
                        "have found it after 2,500 templates had moved")
    holed = dict(plan)
    holed["md"] = plan["md_j2"]
    if not any("`{{` survived" in p for p in verify(holed, mods)):
        failures.append("verify: a `{{` left in the .md was not caught, and "
                        "the framework substituter neither fills nor reports it")

    # ---- --check
    on_disk = {"md": plan["md"], "html_j2": plan["html_j2"],
               "agents": reinline(retable(AGENTS_FIXTURE, "fixture"),
                                  "fixture", plan["md_j2"])}
    if check_findings(plan["md_j2"], "fixture", on_disk, plan["schema"]):
        failures.append("check: a freshly migrated set reported drift: "
                        + "; ".join(check_findings(plan["md_j2"], "fixture",
                                                   on_disk, plan["schema"])))
    for role in ("md", "html_j2", "agents"):
        edited = dict(on_disk)
        edited[role] = edited[role].replace("Identity", "Identity ")
        if not check_findings(plan["md_j2"], "fixture", edited, None):
            failures.append(f"check: a hand-edited {role} was not reported")
    widened = json.loads(json.dumps(plan["schema"]))
    widened["properties"]["not_used_anywhere"] = {"type": "string",
                                                  "description": "?"}
    if not check_findings(plan["md_j2"], "fixture", on_disk, widened):
        failures.append("check: a schema property the template never "
                        "references was not reported")

    # ---- atomicity
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "m"
        agents_md, md = _tree(root, AGENTS_FIXTURE, CLEAN_FIXTURE)
        texts = migration_texts(plan, agents_md.read_text(encoding="utf-8"))
        if set(texts) != {"md_j2", "html_j2", "schema", "md", "agents"}:
            failures.append(f"migration_texts: wrote {sorted(texts)}, expected "
                            "the five forms")
        paths = migration_paths("fixture", md, md.parent, agents_md)
        files = {paths[role]: body for role, body in texts.items()}

        def die(phase: str, want: str, budget: list[int]):
            def fault(seen: str, _path: Path) -> None:
                if seen != want:
                    return
                budget[0] -= 1
                if budget[0] < 0:
                    raise OSError(f"forced failure during {phase}")
            return fault

        for label, phase, budget in (("staging", "stage", [1]),
                                     ("the swap", "replace", [1])):
            try:
                apply_atomic(files, die(label, phase, budget))
                failures.append(f"apply_atomic: a failure during {label} did "
                                "not propagate")
            except OSError:
                pass
            failures.extend(_untouched(agents_md, md, AGENTS_FIXTURE,
                                       CLEAN_FIXTURE,
                                       f"rollback after {label}"))

        written = apply_atomic(files)
        if len(written) != 5 or not all(p.is_file() for p in written):
            failures.append("apply_atomic: a clean run did not write the five "
                            "files")
        if md.read_text(encoding="utf-8") != plan["md"]:
            failures.append("apply_atomic: the .md on disk is not the form "
                            "regenerated from the .md.j2")
        noise = io.StringIO()
        with contextlib.redirect_stdout(noise), \
                contextlib.redirect_stderr(noise):
            drifted = run_check(md.parent / "fixture.md.j2")
        if drifted != 0:
            failures.append("--check: a set --migrate just wrote reports "
                            f"drift: {noise.getvalue().strip()}")

    # ---- steps 3 and 4 fail before anything is written
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "m"
        agents_md, md = _tree(root, AGENTS_NO_ROW, CLEAN_FIXTURE)
        try:
            migration_texts(plan, agents_md.read_text(encoding="utf-8"))
            failures.append("step 3: a template no row names was migrated")
        except MigrationRefused:
            pass
        failures.extend(_untouched(agents_md, md, AGENTS_NO_ROW, CLEAN_FIXTURE,
                                   "step 3 refusal"))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "m"
        agents_md, md = _tree(root, AGENTS_FIXTURE, CLEAN_FIXTURE)
        original = globals()["reinline"]

        def explode(*_args, **_kwargs):
            raise OSError("forced failure in step 4")

        globals()["reinline"] = explode
        try:
            migration_texts(plan, agents_md.read_text(encoding="utf-8"))
            failures.append("step 4: the inline rewrite failed and the "
                            "migration continued")
        except OSError:
            pass
        finally:
            globals()["reinline"] = original
        failures.extend(_untouched(agents_md, md, AGENTS_FIXTURE,
                                   CLEAN_FIXTURE, "step 4 failure"))
    return failures


def self_test() -> list[str]:
    """Every judgement and every guarantee this converter is not allowed to
    get wrong. Eighty-one checks."""
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
    return failures + resolver_checks() + migrate_checks()


# ------------------------------------------------------------------ main

def agents_md_for(template: Path) -> Path:
    """The methodology AGENTS.md that declares this template."""
    return template.resolve().parent.parent / "AGENTS.md"


def run_check(path: Path) -> int:
    """--check: regenerate from the `.md.j2` and diff. Writes nothing."""
    if not path.name.endswith(".md.j2"):
        print(f"{NAME}: --check reads the SOURCE, so --template must name a "
              f"`.md.j2`; got {path.name}", file=sys.stderr)
        return 2
    stem = path.name[:-len(".md.j2")]
    agents = agents_md_for(path)
    try:
        md_j2 = path.read_text(encoding="utf-8")
        on_disk: dict[str, str] = {}
        for role, sibling in (("md", path.with_name(f"{stem}.md")),
                              ("html_j2", path.with_name(f"{stem}.html.j2"))):
            if sibling.is_file():
                on_disk[role] = sibling.read_text(encoding="utf-8")
        if agents.is_file():
            on_disk["agents"] = agents.read_text(encoding="utf-8")
        schema_path = path.with_name(f"{stem}.vars.schema.json")
        schema = JINJA.load_schema(schema_path) if schema_path.is_file() \
            else None
    except (OSError, JINJA.SchemaBroken) as exc:
        print(f"{NAME}: cannot read: {exc}", file=sys.stderr)
        return 2
    findings = check_findings(md_j2, stem, on_disk, schema)
    for finding in findings:
        print(f"{NAME}: {path}: {finding}", file=sys.stderr)
    print(f"{NAME}: --check {path} forms={len(on_disk)} "
          f"drift={len(findings)}")
    return 1 if findings else 0


def run_migrate(plan: dict, template: Path, out_dir: Path,
                write: bool) -> int:
    """--migrate: the whole operation, or none of it."""
    agents = agents_md_for(template)
    if not agents.is_file():
        print(f"{NAME}: {agents}: the methodology has no AGENTS.md, so the "
              "table row and the inline cannot be updated", file=sys.stderr)
        return 2
    try:
        texts = migration_texts(plan, agents.read_text(encoding="utf-8"))
    except MigrationRefused as exc:
        print(f"{NAME}: {exc}", file=sys.stderr)
        return exc.code
    except OSError as exc:
        print(f"{NAME}: cannot read: {exc}", file=sys.stderr)
        return 2
    paths = migration_paths(plan["stem"], template, out_dir, agents)
    files = {paths[role]: body for role, body in texts.items()}
    if not write:
        print(report(plan))
        print(f"{NAME}: --migrate DRY RUN {template} -> "
              + ", ".join(str(paths[r]) for r in sorted(paths))
              + "; nothing written without --write")
        return 1 if plan["unclear"] or plan["notes"] else 0
    try:
        apply_atomic(files)
    except OSError as exc:
        print(f"{NAME}: {template}: the migration failed and was rolled back: "
              f"{exc}", file=sys.stderr)
        return 2
    print(report(plan))
    print(f"{NAME}: --migrate {template} variables="
          f"{len(plan['declarations'])} unclear={plan['unclear']} -> "
          + ", ".join(str(paths[r]) for r in sorted(paths)))
    return 1 if plan["unclear"] or plan["notes"] else 0


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
    ap.add_argument("--migrate", action="store_true",
                    help="the whole per-template operation, all or nothing: "
                         "the three files, the .md regenerated from the new "
                         ".md.j2, the AGENTS.md `## Templates` rows and the "
                         "inline `## Template Contents` body")
    ap.add_argument("--check", action="store_true",
                    help="regenerate every form from an already-migrated "
                         ".md.j2 and report anything on disk that differs; "
                         "writes nothing")
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
        print(f"{NAME}: self-test checks=81 failures={len(failures)}")
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

    if args.check:
        return run_check(path)
    if args.migrate and args.out_dir \
            and out_dir.resolve() != path.parent.resolve():
        print(f"{NAME}: --migrate rewrites the AGENTS.md rows, which name "
              "`templates/<name>.md.j2` beside the template. An --out-dir "
              "elsewhere would make those rows point at nothing", file=sys.stderr)
        return 2

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

    if args.migrate:
        return run_migrate(plan, path, out_dir, args.write)

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
