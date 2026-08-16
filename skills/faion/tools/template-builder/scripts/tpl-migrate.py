#!/usr/bin/env python3
"""tpl-migrate.py — propose declared {{name}} parameters for a legacy template.

1,670 corpus templates carry `<Angle>` placeholders and 556 carry `[bracket]`
ones. Hand-migrating them to the 2.2 `variables:` contract does not scale, so
this tool does the mechanical half: it extracts every candidate placeholder
with its position and its surrounding heading and label, proposes a snake_case
name, a type and a description DRAFTED FROM THAT CONTEXT, and emits the
declaration plus the rewritten body.

It proposes. It does not decide, and it does not touch the template without
--write.

The judgement it refuses to make is the one that matters: a placeholder is not
automatically a parameter. `<Optional: 'ready for owner review'>` is guidance
to the reader and `<service_name>` is a parameter, and when the text cannot be
told apart from prose the placeholder is reported as unclear and LEFT ALONE.
A wrong declaration is worse than none — tpl-build then refuses a build by
name for a parameter that never should have existed. So a high unclear share
is a finding about the corpus, not a failure of this tool.

Also refused, each named rather than guessed at: a placeholder inside a code
fence or a code span, an already-HTML-escaped `&lt;name&gt;` (a 58-file family
stores them that way and rewriting one mangles it), a bare FILL_ME that
carries no name at all, and two placeholders that normalise onto one name —
reported as a collision, never silently merged.

Input:  --template {file.md} | --report [--root {dir}]
Output: the rewritten template on stdout or --out; the analysis on stderr.

Exit: 0 every candidate resolved · 1 unresolved placeholders remain, or the
      header would pass the 40-line window validator 5 reads · 2 the tool
      could not run · 3 two placeholders collide on one name.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

NAME = "tpl-migrate"


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

# ------------------------------------------------------------- extraction

# `<Angle>` is the incumbent convention (22% of templates). The exclusions
# below are what keeps a real HTML tag, an autolink and an attribute out of
# the candidate set.
ANGLE = re.compile(r"<([^<>\n]{1,80})>")
# The 58-file family that stores its placeholders already entity-escaped.
# Detected so it is reported; never rewritten, because a rewrite there is
# indistinguishable from mangling the entity.
ESCAPED = re.compile(r"&lt;([^&<>\n]{1,80})&gt;")
# `[bracket]`: a Markdown inline link, reference link, task box and footnote
# are all bracket-shaped, so each is excluded by lookaround rather than by a
# post-filter that would have to re-find the context.
# `[[wikilink]]` is the corpus's cross-reference convention — 8,283 of them,
# with their own maintenance script. The inner `[slug]` matched here, so
# `- [[slug]]` became `- [{{ slug }}]`: the link destroyed AND `slug`
# declared REQUIRED, so the template refused to build until a human answered
# "what slug?" about something that was never a parameter. Nothing caught it —
# drift stayed 0 and every validator stayed green. Hence `[` in the lookbehind
# and `]` in the lookahead: a doubled bracket is a link, not a placeholder.
BRACKET = re.compile(r"(?<![\]\^\[])\[([^\[\]\n]{1,80})\](?![\(\[\]])")
# `{brace}`: as wide as ANGLE and BRACKET, and mixed case on purpose — CR-013
# §1. The ALL-CAPS-only rule this replaces was justified as *"ambiguous with
# f-strings, Go templates"*, which is true INSIDE code and nowhere else: of the
# mixed-case tokens measured across the migrated corpus, 1,643 sit in prose and
# tables against 42 in a fenced block and 53 in a code span. A `{owner}` matched
# none of the four forms, so it was not flagged unclear — it was NOT SEEN, and a
# template carrying it reported `variables=0`, exited 0 and passed every gate
# while a render would ship `{Product}` literally to a user.
#
# The ambiguity is answered where it is real rather than everywhere: inside a
# fence or a code span, only what BRACE_LEGACY_CAPS matches is still a
# candidate, which is byte-for-byte the set the old pattern saw there.
BRACE = re.compile(r"(?<!\{)\{([^{}\n]{1,80})\}(?!\})")
BRACE_LEGACY_CAPS = re.compile(r"^[A-Z][A-Z0-9_]{0,60}$")
TOKEN = re.compile(r"\b(FILL[_-]?ME|FILL|TBD|XXX|PLACEHOLDER|FIXME)\b")
FENCE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN = re.compile(r"`[^`\n]*`")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
AUTOLINK = re.compile(r"^(?:[^\s@]+@[^\s@]+\.[A-Za-z]{2,}|[a-z][a-z0-9+.-]*://\S*)$")
ATTRIBUTE = re.compile(r"=\s*[\"']")
HTML_TAGS = {
    "a", "abbr", "b", "blockquote", "br", "code", "dd", "div", "dl", "dt",
    "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "kbd", "li",
    "ol", "p", "pre", "s", "small", "span", "strong", "sub", "summary",
    "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul", "details",
    "figure", "figcaption", "main", "nav", "section", "header", "footer",
}
# HTML_TAGS is a closed list, and the tags that actually matter here are not
# HTML at all: a prompt template that tells a model to answer between
# `<reasoning>` and `</reasoning>` carries them as LITERAL markup the model must
# emit. The general rule needs no list — **a placeholder has no closing form.**
# So an angle token whose `</name>` also appears in the body is markup, not a
# slot, and naming it would both invent a parameter and delete the tag the
# prompt depends on. Measured before it was added: 0 of the 2,463 templates
# already migrated carry a variable whose closing tag is also in the file, so
# this changes nothing that has shipped.
CLOSING_TAG = re.compile(r"</([A-Za-z][A-Za-z0-9_-]*)\s*>")

# --------------------------------------------------------- the name rules

_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_WORDS = re.compile(r"[^A-Za-z0-9]+")
# Sentence punctuation. Its presence means the text is a phrase addressed to a
# reader, not an identifier — which is exactly the line this tool must not
# cross on its own.
PROSE_PUNCT = re.compile(r"[.,;:!?\"'`()<>]")
NAME_WORD_CAP = 3
TEXT_LEN_CAP = 48
# A token that carries no name at all. `<FILL>` says fill something; it does
# not say what, and inventing the what is the failure mode this tool exists to
# avoid.
NO_NAME = {"fill", "filled", "todo", "tbd", "xxx", "placeholder", "fixme",
           "fill_me", "fillme", "tk", "na", "n/a", "none", "text", "value?",
           "...", "…", "?", "-", "x", "…?"}
# A leading imperative or qualifier makes the rest an instruction to a human.
DIRECTIVE_LEAD = {"fill", "todo", "tbd", "insert", "replace", "describe",
                  "write", "choose", "pick", "enter", "specify", "add", "see",
                  "list", "note", "optional", "example", "e", "eg", "state",
                  "explain", "summarise", "summarize", "give", "provide",
                  "one", "your", "if", "either", "use", "put", "repeat"}
# An article or preposition is the cheapest reliable signal that a phrase is
# prose. A parameter name does not carry one.
STOPWORDS = {"the", "a", "an", "of", "for", "with", "per", "to", "in", "at",
             "and", "or", "this", "that", "from", "by", "on", "as", "is",
             "are", "be", "do", "not", "your", "here", "least", "one", "each",
             "its", "it", "any", "all", "must", "should", "may", "you"}
FORMAT_TOKEN = re.compile(
    r"^(?:y{2,4}[-/ ]?m{1,2}[-/ ]?d{1,2}|d{1,2}[-/ ]m{1,2}[-/ ]y{2,4}"
    r"|iso[- ]?8601.*|hh:mm(?::ss)?|n+|x+|#+|\d+|\$\d*|https?://.*|www\..*"
    r"|[a-z]{3} \d{1,2}, \d{4})$", re.IGNORECASE)
ALTERNATIVES = re.compile(r"\s*(?:\||/| or )\s*")
# The window scripts/validate-methodology-templates.py reads a header from.
HEADER_WINDOW = 40


def normalise(text: str) -> str | None:
    """A snake_case name for this text, or None when there is no legal one."""
    words = [w for w in _WORDS.split(_CAMEL.sub("_", text.strip())) if w]
    if not words:
        return None
    name = re.sub(r"_+", "_", "_".join(w.lower() for w in words)).strip("_")
    if not name or name[0].isdigit():
        return None
    return name[:64]


def name_from_text(text: str) -> tuple[str | None, str]:
    """Propose a name for a placeholder's own text, or say why there is none.

    Pure, and the whole judgement of the tool lives here: every path that
    returns None is a placeholder this tool refuses to declare.
    """
    raw = text.strip()
    low = raw.lower()
    if not raw or low in NO_NAME:
        return None, "no-name"
    if len(raw) > TEXT_LEN_CAP:
        return None, "prose"
    if PROSE_PUNCT.search(raw):
        return None, "prose"
    words = [w for w in _WORDS.split(_CAMEL.sub("_", raw)) if w]
    if len(words) > 1 and words[0].lower() in DIRECTIVE_LEAD:
        return None, "instruction"
    if len(words) > NAME_WORD_CAP:
        return None, "prose"
    if any(w.lower() in STOPWORDS for w in words):
        return None, "prose"
    if FORMAT_TOKEN.match(raw):
        return None, "format-token"
    name = normalise(raw)
    if name is None:
        return None, "unnameable"
    if not CORE.VAR_NAME.match(name):
        return None, "unnameable"
    return name, "parameter"


def guess_type(name: str, text: str, options: list[str] | None) -> str:
    """The declared type, from the name and the placeholder's own shape."""
    low = text.strip().lower()
    if options:
        return "enum"
    if name.startswith(("is_", "has_", "should_", "can_")) \
            or low in ("yes / no", "yes/no", "true/false", "true|false",
                       "yes|no", "y/n"):
        return "boolean"
    if re.fullmatch(r"n+|\d+", low) or name in ("count", "port", "n") \
            or name.endswith(("_count", "_port", "_size", "_limit",
                              "_number")):
        return "integer"
    if name in ("path", "dir", "filepath", "filename") \
            or name.endswith(("_path", "_dir", "_file", "_filename")):
        return "path"
    return "string"


def alternatives(text: str) -> list[str] | None:
    """`go|hold|no-op` as enum options, or None when it is not a choice list."""
    if not re.search(r"\||\s/\s| or ", text):
        return None
    parts = [p.strip() for p in ALTERNATIVES.split(text.strip()) if p.strip()]
    if len(parts) < 2 or len(parts) > 8:
        return None
    for part in parts:
        if len(part) > 24 or PROSE_PUNCT.search(part) or "," in part:
            return None
    return parts


# ----------------------------------------------------------- the context

def code_ranges(text: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """(fenced block ranges, inline code span ranges).

    Reported apart because they mean different things to whoever reads the
    survey: a placeholder in a fenced block is usually inside example code,
    where a rewrite changes what the example demonstrates, while one in a
    code span is usually just a value the author chose to set in monospace.
    Both are left alone; only one of them is likely to stay that way.
    """
    fences: list[tuple[int, int]] = []
    pos, fence, start = 0, None, 0
    for line in text.split("\n"):
        opener = FENCE.match(line)
        if opener and fence is None:
            fence, start = opener.group(1), pos
        elif opener and line.strip().startswith(fence):
            fences.append((start, pos + len(line)))
            fence = None
        pos += len(line) + 1
    if fence is not None:
        fences.append((start, len(text)))
    spans = [m.span() for m in CODE_SPAN.finditer(text)
             if not in_range(m.start(), fences)]
    return fences, spans


def in_range(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(lo <= pos < hi for lo, hi in ranges)


def clean_label(text: str) -> str | None:
    """A label stripped of Markdown decoration, or None when there is none."""
    label = text.strip()
    # A heading or a cell often carries a placeholder of its own. Leaving it in
    # would quote `[ID]` back at the human being asked the question.
    label = re.sub(r"<[^<>]*>|\[[^\[\]]*\]|\{[^{}]*\}|&lt;[^&]*&gt;", "", label)
    label = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", label)
    label = re.sub(r"^#{1,6}\s*", "", label)
    label = label.replace("**", "").replace("`", "").replace("|", " ")
    label = label.replace("*", "").replace("_", " ")
    label = label.strip().strip(":=-–—").strip()
    if ":" in label:
        label = label.rsplit(":", 1)[0].strip() or label
    words = label.split()
    if len(words) > 8:
        words = words[-8:]
    label = " ".join(words)
    return label if len(label) >= 2 else None


def context_of(text: str, start: int) -> dict:
    """The heading above a placeholder and the label beside it."""
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", start)
    line_end = len(text) if line_end < 0 else line_end
    line = text[line_start:line_end]
    lineno = text.count("\n", 0, start) + 1
    heading = heading_raw = None
    for prev in reversed(text[:line_start].split("\n")):
        found = HEADING.match(prev)
        if found:
            # Two forms on purpose. `heading` is cleaned for the DESCRIPTION,
            # where "From section 'Feedback Response'" reads better than the
            # full title. `heading_raw` is for IDENTITY, because clean_label
            # truncates at a colon — so `## Feedback Response: Shipped`,
            # `: Not Planned` and `: More Info Needed` all cleaned to one
            # string, three distinct sections compared equal, and the
            # multi-site carve-out let their shared variable through.
            heading_raw = found.group(1).strip()
            heading = clean_label(found.group(1))
            break
    before = line[: start - line_start]
    label = None
    if line.lstrip().startswith("|"):
        cells = [c for c in line.strip().strip("|").split("|")]
        offset, index = line.index("|") + 1, 0
        for position, cell in enumerate(cells):
            if offset <= start - line_start < offset + len(cell):
                index = position
                break
            offset += len(cell) + 1
        if index > 0:
            label = clean_label(cells[0])
    if label is None:
        label = clean_label(before)
    return {"line": lineno, "text": line.strip()[:200], "heading": heading,
            "heading_raw": heading_raw, "label": label}


def draft_description(name: str, ctx: dict) -> str | None:
    """A description drafted from the label and heading, or None.

    Never invented from nothing: with neither a label nor a heading there is
    no evidence for what the parameter means, and 2.2's description is the
    question a human is asked — a made-up one is worse than an unmigrated
    placeholder.
    """
    words = name.replace("_", " ")
    heading, label = ctx.get("heading"), ctx.get("label")
    if label and label.lower() not in ("", words):
        base = label[0].upper() + label[1:]
        desc = base.rstrip(". ") + "."
        if heading and heading.lower() not in desc.lower():
            desc = f"{desc} From section '{heading}'."
    elif heading:
        desc = f"The {words} used under '{heading}'."
    else:
        return None
    return " ".join(desc.split())[:CORE.DESC_MAX]


# --------------------------------------------------------- the proposal

def candidates(body: str) -> list[dict]:
    """Every placeholder-shaped span in the body, in position order."""
    fences, spans = code_ranges(body)
    closed = {m.group(1).lower() for m in CLOSING_TAG.finditer(body)}
    claimed: list[tuple[int, int]] = []
    found: list[dict] = []

    def overlaps(span: tuple[int, int]) -> bool:
        return any(a < span[1] and span[0] < b for a, b in claimed)

    for kind, pattern in (("escaped", ESCAPED), ("angle", ANGLE),
                          ("bracket", BRACKET), ("brace", BRACE),
                          ("token", TOKEN)):
        for match in pattern.finditer(body):
            span = match.span()
            if overlaps(span):
                continue
            inner = match.group(1).strip()
            in_code = ("in-fence" if in_range(span[0], fences)
                       else "in-code-span" if in_range(span[0], spans) else "")
            if kind == "brace":
                # Same alnum guard the bracket form uses, then the code
                # exemption: `{fmt}` in a Python f-string is syntax, `{owner}`
                # in a table cell is a slot nobody can fill.
                if not any(c.isalnum() for c in inner):
                    continue
                if in_code and not BRACE_LEGACY_CAPS.match(match.group(1)):
                    continue
            if kind == "angle":
                first = inner.split()[0].lower() if inner.split() else ""
                if inner[:1] in "/!?" or ATTRIBUTE.search(inner) \
                        or first.rstrip("/") in HTML_TAGS \
                        or first.rstrip("/") in closed \
                        or AUTOLINK.match(inner):
                    continue
            if kind == "bracket" and (not any(c.isalnum() for c in inner)
                                      or inner.lower() in ("x", " ")):
                continue
            claimed.append(span)
            found.append({"kind": kind, "raw": match.group(0), "text": inner,
                          "start": span[0], "end": span[1],
                          "in_code": in_code})
    found.sort(key=lambda c: c["start"])
    return found


def classify(body: str, found: list[dict], declared: dict) -> list[dict]:
    """Each candidate as parameter or unclear, with the reason for the verdict.

    Pure: no I/O, no exits. This plus name_from_text is the whole of the
    judgement, so --self-test exercises exactly these two.
    """
    out: list[dict] = []
    for cand in found:
        item = dict(cand)
        item.update(context_of(body, cand["start"]))
        item["name"] = None
        item["options"] = None
        if cand["kind"] == "escaped":
            item["verdict"], item["reason"] = "unclear", "html-escaped"
            out.append(item)
            continue
        if cand["in_code"]:
            item["verdict"], item["reason"] = "unclear", cand["in_code"]
            out.append(item)
            continue
        if cand["kind"] == "token":
            item["verdict"], item["reason"] = "unclear", "no-name"
            out.append(item)
            continue
        name, reason = name_from_text(cand["text"])
        # An enum reading is a FALLBACK, never an overlay. `Role / Person` is a
        # column header that also names a parameter; reading it as two options
        # would declare `Role` and `Person` as the only legal values, which is
        # a wrong declaration dressed as a precise one.
        options = alternatives(cand["text"]) if name is None else None
        if name is None and (options or reason == "format-token"):
            # The text is a value shape, not a name. A label beside it is
            # evidence; nothing else is, so without one this stays unclear.
            from_label = name_from_text(item["label"] or "")[0]
            if from_label is None:
                item["verdict"] = "unclear"
                item["reason"] = ("options-without-name" if options
                                  else "format-token")
                out.append(item)
                continue
            name, reason = from_label, "parameter"
        if name is None:
            item["verdict"], item["reason"] = "unclear", reason
            out.append(item)
            continue
        item["name"] = name
        item["options"] = options
        item["type"] = declared[name]["type"] if name in declared \
            else guess_type(name, cand["text"], options)
        item["required"] = "optional" not in item["text"].lower() \
            and "optional" not in (item["label"] or "").lower()
        item["description"] = declared[name]["description"] if name in declared \
            else draft_description(name, item)
        if item["description"] is None:
            item["verdict"], item["reason"] = "unclear", "no-context"
            item["name"] = None
            out.append(item)
            continue
        item["verdict"] = "parameter"
        item["reason"] = "declared" if name in declared else "parameter"
        out.append(item)
    return out


def find_collisions(items: list[dict]) -> list[str]:
    """Names two different placeholder texts normalise onto. Never merged."""
    texts: dict[str, set[str]] = {}
    for item in items:
        if item["verdict"] == "parameter":
            texts.setdefault(item["name"], set()).add(item["raw"])
    collisions = []
    for name, raws in sorted(texts.items()):
        if len(raws) > 1:
            collisions.append(f"{name}: " + " and ".join(sorted(raws)))
    return collisions


def refuse_multi_site(items: list[dict]) -> list[str]:
    """CR-013 §2. Refuse a name bound to several sites under DIFFERENT headings.

    Filling it once fills them all with the same value.

    `find_collisions` cannot catch this: it fires when one name is proposed from
    DIFFERENT text, and here the text is identical. That is exactly what made it
    silent — `hr/employee-value-proposition` rendered
    `## Competitor A: {{ name }}` / `B: {{ name }}` / `C: {{ name }}`, three
    companies sharing one variable, with nothing flagged.

    Refusing costs one line in a review queue a human is already reading.
    Declaring wrongly ships a document with the same value in three places and
    nothing downstream can detect it. That asymmetry is the whole rule, and it
    deliberately refuses legitimate repeats too — an owner named under ten
    headings of one deck lands in the queue rather than being guessed at.

    Lives here and is called by BOTH proposal paths — `build_plan` and
    `tpl-jinja`'s converter. It sat inline in `build_plan` for one commit, which
    made the corpus writer the one caller that never ran it, so the rule was
    true of every report and of no file on disk.

    Returns the names it refused, in body order.
    """
    sites: dict[str, list[dict]] = {}
    for item in items:
        if item["verdict"] == "parameter" and item["name"]:
            sites.setdefault(item["name"], []).append(item)
    refused: list[str] = []
    for name, group in sites.items():
        if len(group) < 2:
            continue
        # Two sites on ONE line are always distinct values, so the heading
        # carve-out below must not reach them. A table row binds its cells to
        # one variable — `**Last updated:** {{ date }} | **Next review:**
        # {{ date }}` is two dates, `Design: {{ xd }}, Dev: {{ xd }}, QA:
        # {{ xd }}` is three estimates — and every one of those sits under a
        # single heading, so the carve-out shipped them.
        #
        # No exception for a legitimate same-line repeat (`{{ slug }}/{{ slug
        # }}.md`) because the corpus has none: all 63 same-line repeats measured
        # across the migrated templates are distinct-value columns or list
        # items. The rule is as wide as the evidence and no wider.
        same_line = len({g.get("line") for g in group}) < len(group)
        headings = {(g.get("heading_raw") or g.get("heading") or "") for g in group}
        if not same_line and len(headings) < 2:
            continue  # every site under one heading, on its own line: one slot
        refused.append(name)
        for g in group:
            g["verdict"], g["reason"] = "unclear", "multi-site"
            g["name"] = None
    return refused


def build_plan(text: str, where: str) -> dict:
    """The whole proposal for one template. Raises TplError on a bad source."""
    source = CORE.parse_source(text, where)
    body, declared = source["body"], source["variables"]
    offset = len(text) - len(body)
    items = classify(body, candidates(body), declared)
    for item in items:
        # context_of counts lines in the body; a reader counts them in the
        # file, and the header is not nothing.
        item["line"] += text[:offset].count("\n")
    collisions = find_collisions(items)
    colliding = {c.split(":", 1)[0] for c in collisions}
    for item in items:
        if item["verdict"] == "parameter" and item["name"] in colliding:
            item["verdict"], item["reason"] = "unclear", "collision"

    refuse_multi_site(items)

    decls: list[dict] = []
    seen: set[str] = set()
    for item in items:
        if item["verdict"] != "parameter" or item["name"] in seen \
                or item["name"] in declared:
            continue
        seen.add(item["name"])
        decls.append({"name": item["name"], "type": item["type"],
                      "required": item["required"], "default": None,
                      "sensitive": False, "placeholder": None,
                      "options": item["options"],
                      "description": item["description"]})

    new_body = body
    for item in sorted(items, key=lambda i: i["start"], reverse=True):
        if item["verdict"] == "parameter":
            new_body = (new_body[: item["start"]] + "{{" + item["name"] + "}}"
                        + new_body[item["end"]:])
    new_text = text[:offset] + new_body if new_body != body else text
    block, blocked = "", None
    if decls:
        block = CORE.format_variables(decls)
        try:
            new_text = CORE.splice_variables(new_text, block)
        except CORE.TplError as exc:
            # The declaration cannot go in — most often the template already
            # carries a hand-authored `variables:` block. The rewrite is
            # dropped whole rather than partially applied: a `{{name}}` with
            # no declaration is a template tpl-build refuses to build, which
            # is a worse state than the legacy placeholder it replaced.
            blocked, new_text = str(exc), text

    roundtrip = None
    if not blocked and (decls or new_body != body):
        try:
            check = CORE.parse_source(new_text, where)
            used = CORE.scan_placeholders(check["body"], where)
            missing = sorted(used - set(check["variables"]))
            if missing:
                roundtrip = f"rewritten body uses undeclared {missing}"
        except CORE.TplError as exc:
            roundtrip = str(exc)

    # scripts/validate-methodology-templates.py reads the header from the first
    # 40 lines of the file and nothing past them. Four lines per declaration
    # plus the five existing keys means roughly seven parameters fit; the
    # eighth silently falls outside the window and validator 5 then reports it
    # as a variable with no type. The write still happens — but nobody should
    # find that out from a failing gate.
    head_lines = (len(new_text.split("\n"))
                  - len(CORE.split_header(new_text)[1].split("\n"))) \
        if new_text != text else 0
    unclear = [i for i in items if i["verdict"] == "unclear"]
    return {"header_lines": head_lines, "over_cap": head_lines > HEADER_WINDOW,
            "where": where, "items": items, "declarations": decls,
            "collisions": collisions, "roundtrip": roundtrip, "text": new_text,
            "changed": new_text != text, "unclear": len(unclear),
            "block": block, "blocked": blocked,
            "parameters": sum(1 for i in items if i["verdict"] == "parameter")}


def apply_to_file(path: Path, plan: dict, write: bool) -> bool:
    """Write the rewritten template back. Returns whether bytes were touched.

    The default is False everywhere it is called from. That is the contract:
    a proposal tool that edits by default is a tool nobody can safely point at
    a corpus.
    """
    if not write or not plan["changed"] or plan["roundtrip"]:
        return False
    path.write_text(plan["text"], encoding="utf-8")
    return True


# ------------------------------------------------------------- reporting

def plan_report(plan: dict) -> str:
    """The per-template analysis a human reads before accepting anything."""
    lines = [f"{plan['where']}: candidates={len(plan['items'])} "
             f"parameter={plan['parameters']} unclear={plan['unclear']}"]
    for item in plan["items"]:
        if item["verdict"] == "parameter":
            lines.append(f"  line {item['line']:>4}  {item['raw']} -> "
                         f"{{{{{item['name']}}}}}  {item['type']}")
    for item in plan["items"]:
        if item["verdict"] == "unclear":
            lines.append(f"  line {item['line']:>4}  {item['raw']}  "
                         f"UNCLEAR: {item['reason']} — left alone")
    for collision in plan["collisions"]:
        lines.append(f"  COLLISION {collision} — reported, not merged")
    if plan["over_cap"]:
        lines.append(f"  CAP header is {plan['header_lines']} lines; "
                     f"validate-methodology-templates.py reads only the first "
                     f"{HEADER_WINDOW} and reports the rest as malformed")
    if plan["blocked"]:
        lines.append(f"  BLOCKED {plan['blocked']} — nothing rewritten; the "
                     "declaration below is for a human to merge")
        lines += ["  " + line for line in plan["block"].split("\n")]
    if plan["roundtrip"]:
        lines.append(f"  ROUNDTRIP {plan['roundtrip']} — nothing written")
    return "\n".join(lines)


def survey(paths: list[Path], limit: int) -> dict:
    """The corpus-wide migration surface. One pass per template."""
    shape = Counter()
    reasons: Counter = Counter()
    names: Counter = Counter()
    texts: Counter = Counter()
    unreadable: Counter = Counter()
    for path in paths:
        shape["templates"] += 1
        try:
            plan = build_plan(path.read_text(encoding="utf-8"), path.name)
        except (OSError, CORE.TplError) as exc:
            shape["unparsable"] += 1
            unreadable[str(exc).split(":")[-1].strip()[:60]] += 1
            continue
        total = len(plan["items"])
        if plan["blocked"]:
            shape["blocked"] += 1
        if plan["over_cap"]:
            shape["header_over_window"] += 1
        if plan["roundtrip"]:
            shape["roundtrip_refused"] += 1
        if not total:
            shape["no_placeholders"] += 1
        elif plan["unclear"] == 0:
            shape["fully_mechanical"] += 1
        elif plan["parameters"] == 0:
            shape["human_only"] += 1
        else:
            shape["partly_mechanical"] += 1
        shape["candidates"] += total
        shape["parameters"] += plan["parameters"]
        shape["unclear"] += plan["unclear"]
        if plan["collisions"]:
            shape["templates_with_collisions"] += 1
        for item in plan["items"]:
            if item["verdict"] == "parameter":
                names[item["name"]] += 1
            else:
                reasons[item["reason"]] += 1
                texts[item["raw"][:60]] += 1
    return {"shape": dict(shape), "reasons": reasons.most_common(),
            "top_names": names.most_common(limit),
            "top_unclear": texts.most_common(limit),
            "distinct_names": len(names),
            "unreadable": unreadable.most_common(limit)}


def survey_report(data: dict) -> str:
    """The table that tells an owner whether migration is a week or a quarter."""
    shape = data["shape"]
    order = ("templates", "no_placeholders", "fully_mechanical",
             "partly_mechanical", "human_only", "unparsable", "blocked",
             "roundtrip_refused", "header_over_window",
             "templates_with_collisions", "candidates",
             "parameters", "unclear")
    lines = ["migration surface"]
    for key in order:
        lines.append(f"  {key.replace('_', ' '):<26}{shape.get(key, 0):>8}")
    lines += ["", "unresolved by reason"]
    for reason, count in data["reasons"]:
        lines.append(f"  {reason:<26}{count:>8}")
    lines += ["", f"most common proposed names ({data['distinct_names']} "
                  "distinct — the ones worth standardising)"]
    for name, count in data["top_names"]:
        lines.append(f"  {name:<26}{count:>8}")
    lines += ["", "most common unresolved placeholders"]
    for text, count in data["top_unclear"]:
        lines.append(f"  {text[:60]:<62}{count:>6}")
    if data["unreadable"]:
        lines += ["", "templates whose header this parser refuses"]
        for reason, count in data["unreadable"]:
            lines.append(f"  {reason[:60]:<62}{count:>6}")
    return "\n".join(lines)


def collect(root: Path, pattern: str) -> list[Path]:
    """Every template the report walks. Sorted, so two runs agree."""
    skip = {".git", "node_modules", ".venv", "__pycache__", ".archive"}
    return sorted(p for p in root.glob(pattern)
                  if p.is_file() and not skip & set(p.parts))


# ------------------------------------------------------------- self-test

CLEAN_FIXTURE = """<!--
purpose: service runbook
produces: markdown runbook
-->
# Runbook

## Identity

Service name: <service_name>

Owner: <Optional: 'ready for owner review'>

Escalation: &lt;pager_rota&gt;

```sh
systemctl restart <service_name>
```
"""

# The corpus's most common header form: one whole comment per line, 1,607 of
# the 2,918 Markdown templates. A declaration written into it has to come back
# out, which is what the round-trip assertion below is for.
INLINE_FIXTURE = """<!-- purpose: release note -->
<!-- produces: markdown release note -->
<!-- stub fixture; replace with a realistic example -->
## Release

Release tag: <release_tag>
"""

# CR-013 §1. Five judgements about `{brace}`, and the last two are the reason
# the form is not simply widened everywhere: `{width}` in a code span and
# `{owner}` in a fence are syntax, while `{RELEASE_TAG}` in that same fence is
# still read exactly as it was before the widening.
BRACE_FIXTURE = """<!--
purpose: brace fixture
produces: markdown release note
-->
# Release

## Identity

Product name: {product_name}

Ships on {YYYY-MM-DD}, recording {one-line decision the artefact records}.

Call `format(fmt={width})` when the column is narrow.

```py
print(f"{owner} shipped {RELEASE_TAG}")
```
"""

# CR-013 §2: three competitors, identical placeholder text, three headings.
# `find_collisions` sees no collision because the text is identical — which is
# exactly how this shipped silently in hr/employee-value-proposition.
MULTI_SITE_FIXTURE = """<!--
purpose: p
consumes: c
produces: markdown
depends-on: d
token-budget-impact: low
-->
# EVP benchmark

## Competitor A
- name: <name>

## Competitor B
- name: <name>

## Competitor C
- name: <name>
"""

# The converse: one heading, so one slot repeated. Must still declare.
# Two distinct values on one line, under a single heading — the carve-out below
# must not reach this. Real specimen shape from product/roadmap-design.
# Real specimen shape from pm/feedback-management: three sections whose titles
# differ only after the colon. clean_label truncates there, so identity must not
# use it.
COLON_HEADING_FIXTURE = """<!--
purpose: p
consumes: c
produces: markdown
depends-on: d
token-budget-impact: low
-->
# Responses

## Feedback Response: Shipped
- owner: <owner>

## Feedback Response: Not Planned
- owner: <owner>

## Feedback Response: More Info Needed
- owner: <owner>
"""

SAME_LINE_FIXTURE = """<!--
purpose: p
consumes: c
produces: markdown
depends-on: d
token-budget-impact: low
-->
# Roadmap

## Header
**Last updated:** [date] | **Next review:** [date]
"""

SAME_HEADING_FIXTURE = """<!--
purpose: p
consumes: c
produces: markdown
depends-on: d
token-budget-impact: low
-->
# Service

## Deploy
- service: <service name>
- restart: systemctl restart <service name>
"""

COLLIDE_FIXTURE = """# Inputs

## Wiring

Input: <input name>

Second: <input-name>
"""


def self_test() -> list[str]:
    """The six judgements this tool is not allowed to get wrong."""
    failures: list[str] = []
    plan = build_plan(CLEAN_FIXTURE, "fixture")
    names = [d["name"] for d in plan["declarations"]]
    if names != ["service_name"]:
        failures.append(f"clean <service_name> did not become the one declared "
                        f"parameter: {names}")
    if "{{service_name}}" not in plan["text"]:
        failures.append("clean placeholder was not substituted in the body")
    if plan["text"].count("{{service_name}}") != 1:
        failures.append("a placeholder inside a code fence was rewritten")
    if not [i for i in plan["items"] if i["reason"] == "in-fence"]:
        failures.append("a placeholder inside a code fence was not flagged")
    prose = [i for i in plan["items"] if "Optional:" in i["raw"]]
    if not prose or prose[0]["verdict"] != "unclear":
        failures.append("a prose placeholder was not flagged unclear")
    elif prose[0]["raw"] not in plan["text"]:
        failures.append("a prose placeholder was not left alone in the body")
    escaped = [i for i in plan["items"] if i["reason"] == "html-escaped"]
    if not escaped:
        failures.append("an already-escaped &lt;name&gt; was not detected")
    elif "&lt;pager_rota&gt;" not in plan["text"]:
        failures.append("an already-escaped placeholder was mangled")
    if plan["roundtrip"]:
        failures.append(f"the rewritten template does not parse: "
                        f"{plan['roundtrip']}")

    inline = build_plan(INLINE_FIXTURE, "fixture")
    if [d["name"] for d in inline["declarations"]] != ["release_tag"]:
        failures.append("the one-line comment header form produced no "
                        "declaration")
    if inline["roundtrip"] or inline["blocked"]:
        failures.append(f"a declaration written into a one-line comment header "
                        f"did not parse back: {inline['roundtrip'] or inline['blocked']}")
    if "<!-- stub fixture" not in inline["text"]:
        failures.append("a human note under the header was eaten")
    if re.search(r"^\s*type: \w+ -->", inline["text"], re.MULTILINE):
        failures.append("a declaration field kept a trailing --> that "
                        "validate-methodology-templates.py reads as the value")

    already = build_plan(inline["text"] + "\nOwner: <owner_handle>\n",
                         "fixture")
    if not already["blocked"]:
        failures.append("a template that already declares variables was not "
                        "refused a second block")
    if already["changed"]:
        failures.append("a blocked template was rewritten anyway")

    wide = build_plan("# Fields\n\n" + "\n".join(
        f"- Field {n}: <field_{n}>" for n in range(1, 11)), "fixture")
    if not wide["over_cap"]:
        failures.append("a header past the 40-line window validator 5 reads "
                        "was not flagged")

    braces = build_plan(BRACE_FIXTURE, "fixture")
    raws = {i["raw"]: i for i in braces["items"]}
    if [d["name"] for d in braces["declarations"]] != ["product_name"]:
        failures.append(f"a mixed-case {{product_name}} did not become the one "
                        f"declared parameter: "
                        f"{[d['name'] for d in braces['declarations']]}")
    if "{{product_name}}" not in braces["text"]:
        failures.append("a mixed-case brace parameter was not substituted")
    for raw, why in (("{YYYY-MM-DD}", "format-token"),
                     ("{one-line decision the artefact records}", "prose")):
        if raw not in raws:
            failures.append(f"a mixed-case brace {raw} was not seen at all")
        elif raws[raw]["verdict"] != "unclear":
            failures.append(f"{raw} was declared instead of flagged {why}")
        elif raw not in braces["text"]:
            failures.append(f"{raw} was not left alone in the body")
    for raw, where in (("{width}", "a code span"), ("{owner}", "a fence")):
        if raw in raws:
            failures.append(f"a mixed-case brace inside {where} was read as a "
                            f"placeholder: {raw}")
        if raw not in braces["text"]:
            failures.append(f"a mixed-case brace inside {where} was rewritten: "
                            f"{raw}")
    caps = raws.get("{RELEASE_TAG}")
    if caps is None or caps["reason"] != "in-fence":
        failures.append("an ALL-CAPS brace inside a fence stopped being "
                        "flagged in-fence when the form was widened")

    collided = build_plan(COLLIDE_FIXTURE, "fixture")
    if not collided["collisions"]:
        failures.append("two placeholders normalising onto input_name were "
                        "merged instead of reported")
    if collided["declarations"]:
        failures.append("a collision still produced a declaration")

    # CR-013 §2 — the same placeholder text under different headings is three
    # slots, not one variable. Identical text means `find_collisions` sees no
    # collision, which is precisely why this shipped silently.
    multi = build_plan(MULTI_SITE_FIXTURE, "fixture")
    if any(d["name"] == "name" for d in multi["declarations"]):
        failures.append("multi-site: three competitors under three headings "
                        "collapsed into one `name` variable")
    if not [i for i in multi["items"] if i.get("reason") == "multi-site"]:
        failures.append("multi-site: the repeat was not reported as unclear")
    if "{{name}}" in multi["text"]:
        failures.append("multi-site: a refused placeholder was substituted anyway")
    # Headings that differ only after a colon are DIFFERENT sections.
    colon = build_plan(COLON_HEADING_FIXTURE, "fixture")
    if any(d["name"] == "owner" for d in colon["declarations"]):
        failures.append("multi-site: three `Response: X` sections shared one "
                        "variable because clean_label truncated at the colon")
    # Two sites on ONE line are distinct values even under one heading.
    online = build_plan(SAME_LINE_FIXTURE, "fixture")
    if any(d["name"] == "date" for d in online["declarations"]):
        failures.append("multi-site: two dates in one row shared a variable")
    # ...and a repeat under ONE heading is one slot, so it still declares.
    same = build_plan(SAME_HEADING_FIXTURE, "fixture")
    if not any(d["name"] == "service_name" for d in same["declarations"]):
        failures.append("multi-site: a genuine repeat under one heading was "
                        "refused — the rule is about differing headings")

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "t.md"
        target.write_text(CLEAN_FIXTURE, encoding="utf-8")
        if apply_to_file(target, plan, False):
            failures.append("a file was touched without --write")
        if target.read_text(encoding="utf-8") != CLEAN_FIXTURE:
            failures.append("the template changed on disk without --write")
        if not apply_to_file(target, plan, True):
            failures.append("--write did not apply the plan")
        if "{{service_name}}" not in target.read_text(encoding="utf-8"):
            failures.append("--write wrote no substitution")
    return failures


# ------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", help="the legacy template to migrate")
    ap.add_argument("--out", help="write the rewritten template here")
    ap.add_argument("--write", action="store_true",
                    help="apply the proposal to the template in place")
    ap.add_argument("--report", action="store_true",
                    help="survey every template under --root instead")
    ap.add_argument("--root", default=".", help="report root (default .)")
    ap.add_argument("--glob", default="**/templates/*.md",
                    help="report pattern (default **/templates/*.md)")
    ap.add_argument("--limit", type=int, default=25,
                    help="rows in each report table (default 25)")
    ap.add_argument("--json", action="store_true", help="emit JSON on stdout")
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
        print(f"{NAME}: self-test checks=27 failures={len(failures)}")
        return 1 if failures else 0

    if args.report:
        root = Path(args.root)
        if not root.is_dir():
            print(f"{NAME}: --root {args.root}: not a directory",
                  file=sys.stderr)
            return 2
        paths = collect(root, args.glob)
        if not paths:
            print(f"{NAME}: no template matched {args.glob!r} under {root}",
                  file=sys.stderr)
            return 2
        data = survey(paths, args.limit)
        summary = (f"{NAME}: templates={data['shape']['templates']} "
                   f"mechanical={data['shape'].get('fully_mechanical', 0)} "
                   f"partial={data['shape'].get('partly_mechanical', 0)} "
                   f"unclear={data['shape'].get('unclear', 0)}")
        if args.json:
            print(json.dumps(data, indent=2, sort_keys=True))
            print(summary, file=sys.stderr)
        else:
            print(survey_report(data))
            print(summary)
        return 0

    if not args.template:
        print(f"{NAME}: --template is required (or --report, or --self-test)",
              file=sys.stderr)
        return 2
    path = Path(args.template)
    try:
        original = path.read_text(encoding="utf-8")
        plan = build_plan(original, path.name)
    except OSError as exc:
        print(f"{NAME}: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    except CORE.TplError as exc:
        print(f"{NAME}: {path}: {exc}", file=sys.stderr)
        return 2

    written = apply_to_file(path, plan, args.write)
    targets = ([str(path)] if written else []) + ([args.out] if args.out else [])
    destination = ", ".join(targets) or "stdout"
    if args.out:
        try:
            Path(args.out).write_text(plan["text"], encoding="utf-8")
        except OSError as exc:
            print(f"{NAME}: cannot write {args.out}: {exc}", file=sys.stderr)
            return 2
    summary = (f"{NAME}: {path} candidates={len(plan['items'])} "
               f"parameter={plan['parameters']} unclear={plan['unclear']} "
               f"collisions={len(plan['collisions'])} -> {destination}")
    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
        print(plan_report(plan), file=sys.stderr)
        print(summary, file=sys.stderr)
    elif written or args.out or args.write:
        print(plan_report(plan))
        print(summary)
    else:
        print(plan["text"], end="")
        print(plan_report(plan), file=sys.stderr)
        print(summary, file=sys.stderr)

    if plan["collisions"]:
        return 3
    if plan["roundtrip"] or plan["blocked"]:
        return 2
    return 1 if plan["unclear"] or plan["over_cap"] else 0


if __name__ == "__main__":
    sys.exit(main())
