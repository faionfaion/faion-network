#!/usr/bin/env python3
"""F-066 B3 validator: methodology templates discipline.

Rules per checklist B3.1..B3.5:
  B3.1 every file listed in AGENTS.md `## Templates` table exists in <dir>/templates/
  B3.2 templates are non-empty (heuristic: >50 bytes, not literal TBD placeholder)
  B3.3 each starts with a 5-line header (purpose / consumes / produces / depends-on / token-budget-impact)
  B3.6 a declared `variables:` block is shape-checked (AD-025 / retrieval-content-contracts.md §2.2):
       name pattern, type enum, required, enum implies options, sensitive implies
       placeholder, description under 240 chars. Absence means a static template
       on the unchanged delivery path, so nothing fires unless an author opted in.
       The block is read from the HEADER region only — the whole file would match
       every GitLab CI, Compose and Ansible template, whose `variables:` is theirs.

Note: this validator only reads the `## Templates` H2 section in the
AGENTS.md body — it never parses meta.json. The body-section check is
independent of the meta.json layout.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO_ROOT / "skills" / "faion" / "knowledge"

HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on", "token-budget-impact")

# Files whose syntax has no comment form for headers; we allow a __faion_header__ key inside.
# Formats with no comment syntax, so the header has to live in the data itself
# as a `__faion_header__` key. `.jsonl` and `.webmanifest` are here because they
# ARE JSON and were being checked as if they were not: four `.jsonl` templates
# carried a perfectly good five-key header written as `#` or `<!-- -->` comment
# lines, which made the file unparseable as JSONL — a header that costs the
# artefact its format is worse than a missing one. All 12 `.jsonl` in the corpus
# parse as of 2026-08-15 and this set is what keeps them that way.
JSON_LIKE = {".json", ".jsonl", ".webmanifest"}

# Every comment opener the corpus's template formats actually use, measured
# rather than guessed: 141 `.py`/`.tmpl` files carry the header in a module
# docstring, 6 `.php` open with `<?php`, and there is one each of XML, INI, VB
# and Mermaid. A docstring header is as valid as a `<!-- -->` one — neither
# renders into the artefact, which is the property being checked.
COMMENT_OPENERS = ("<!--", "/*", "#", "//", "--", '"""', "'''", "<?", ";",
                   "'", "%%")


def _templates_listed(agents_md: Path) -> list[str]:
    if not agents_md.exists():
        return []
    text = agents_md.read_text(encoding="utf-8", errors="replace")
    # find ## Templates section, parse the table
    m = re.search(r"(?ms)^## Templates\s*\n(.*?)(?:^## |\Z)", text)
    if not m:
        return []
    body = m.group(1)
    files: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols or cols[0].lower() in ("file", "---", ""):
            continue
        cell = cols[0].strip("`")
        # The section regex above already scopes this to `## Templates`. The
        # prefix test is the second half: a row there may still name something
        # outside `templates/`, and only a template owes a header. This drops
        # zero rows in the corpus as of 2026-08-15 — it is a guard against a
        # future row, not a fix for a present one.
        if cell.startswith("templates/"):
            files.append(cell)
    return files


def _missing_header_keys(p: Path) -> list[str]:
    """Which of the five header keys are absent, as `key: value` in the first 20 lines.

    The old check was a lowercase SUBSTRING scan wanting 3 of 5 keys anywhere,
    which a `content/*.xml` file passes by accident — the words "purpose" and
    "produces" occur in ordinary methodology prose. Requiring `key:` followed by
    a value is what makes the header a parseable block rather than a vocabulary
    coincidence, and that is the precondition for the sixth key `variables:`
    being enforceable instead of advisory (retrieval-content-contracts.md §2.1).

    Tightening it found 19 templates, and 17 of them already carried all five
    keys — they failed on shape, not on content: eight wrote the whole header on
    one pipe-separated line, five used `_purpose` instead of `__faion_header__`,
    four wrote comment syntax into a JSON format. Only two had no header at all.
    """
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return list(HEADER_KEYS)
    if p.suffix in JSON_LIKE:
        return [] if "__faion_header__" in text else ["__faion_header__"]
    lines = text.splitlines()[:20]
    head = "\n".join(lines).lower()
    missing = [k for k in HEADER_KEYS
               if not re.search(rf"^\s*\W*\s*{re.escape(k)}\s*:\s*\S", head, re.M)]
    if missing:
        return missing
    # B3.4 the header must be COMMENTED. Matching the key regardless of comment
    # markers accepted a bare `purpose: ...` at the top of a Markdown file — and
    # that is not a header at all: `split_header` captures nothing, so the five
    # lines fall into the BODY and render into the delivered document as visible
    # text. A repair pass spliced one back unwrapped and every check stayed green,
    # `--check` included, which is how this was found.
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith(COMMENT_OPENERS):
            return []
        # the first non-blank line is not a comment opener, so whatever follows
        # is body text no matter which keys it happens to contain.
        return ["a commented header (the keys are bare text, so they render)"]
    return []


VAR_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
# The five of retrieval-content-contracts.md §2.2, plus `text` — the sixth type
# added by .aidocs/conventions/template-builder.md §3 and already implemented in
# skills/faion/tools/template-builder/scripts/lib/tplcore.py (VAR_TYPES there).
# `text` is prose an LLM composes from the author's answer to `description`; it
# is never a value the builder generates. Without it here the assembler accepts
# a type this gate rejects, and no author can declare a prose parameter at all.
VAR_TYPES = {"string", "integer", "boolean", "enum", "path", "text"}


def _header_block(text: str, suffix: str) -> str:
    """The header region only — never the whole file.

    `variables:` extends the header (retrieval-content-contracts.md §2.2), so
    it has to be read from inside it. Scanning the whole file instead would
    flag every GitLab CI, Compose and Ansible template in the corpus, each of
    which has a `variables:` key of its own that means something else entirely.
    """
    if suffix in JSON_LIKE:
        return text if "__faion_header__" in text else ""
    lines = text.splitlines()
    # The header is the leading comment region: everything up to the first line
    # that is neither blank nor comment-like nor inside an open block comment.
    # The slice is a BACKSTOP, not the boundary — the `break` below is what ends
    # the header, at the first line that is neither blank nor comment-like. So a
    # low ceiling does not protect anything; it silently truncates.
    #
    # It was 40, and at ~4 lines per `variables:` entry that capped a template at
    # roughly SEVEN parameters. The eighth fell outside the window and this
    # validator reported it as "variable has no type" — a declaration that is
    # correct on disk, failing because the reader stopped early. Measured on a
    # full scratch migration: 181 of 1,079 rewritten templates exceeded 40 lines
    # and 161 failed the gate, and **every** validator-5 finding in that run was
    # explained by this and nothing else.
    #
    # 400 is chosen to be past any plausible declaration (20 parameters is 80
    # lines) while still bounding a pathological file that is comments to its end.
    out, in_block = [], False
    for line in lines[:400]:
        s = line.strip()
        if s.startswith("<!--") or s.startswith("/*"):
            in_block = True
        if in_block or s.startswith("#") or s.startswith("//") or not s:
            out.append(line)
            if s.endswith("-->") or s.endswith("*/"):
                in_block = False
            continue
        break
    return "\n".join(out)


def _variables_region(header: str) -> str:
    """The `variables:` list only — never the sibling keys after it.

    `sections:` (retrieval-content-contracts.md §2.3) is a list of `- name:`
    mappings too, and scanning the whole header made every section entry look
    like a variable missing its `type` and `required`. Nothing in the corpus
    declared `sections:` while adoption of `variables:` was zero, so the first
    author to use §2.3 would have been the one to find this.
    """
    lines = header.split("\n")
    start, prefix = None, ""
    for i, line in enumerate(lines):
        m = re.match(r"(?i)^(\s*\W*\s*)variables\s*:", line)
        if m:
            start, prefix = i + 1, m.group(1)
            break
    if start is None:
        return ""
    # A sibling key sits at exactly the same prefix; list items and their
    # continuations are indented past it, so they never match.
    sibling = re.compile(rf"^{re.escape(prefix)}[a-z][a-z0-9_-]*\s*:")
    out: list[str] = []
    for line in lines[start:]:
        if sibling.match(line):
            break
        out.append(line)
    return "\n".join(out)


def _variable_findings(p: Path, header: str) -> list[str]:
    """Shape-check a declared `variables:` block. Absence means a static
    template on the unchanged delivery path, which is the documented default —
    so nothing here fires unless an author opted in."""
    if not re.search(r"(?im)^\s*\W*\s*variables\s*:", header):
        return []
    errs: list[str] = []
    entries = re.findall(r"(?ms)^\s*\W*\s*-\s+name\s*:\s*(\S+)(.*?)(?=^\s*\W*\s*-\s+name\s*:|\Z)",
                         _variables_region(header))
    if not entries:
        return [f"{p.name}: declares 'variables:' with no '- name:' entry"]
    for name, body in entries:
        name = name.strip().strip("\"'")
        if not VAR_NAME.match(name):
            errs.append(f"{p.name}: variable {name!r} does not match ^[a-z][a-z0-9_]{{0,63}}$")
        def field(key: str) -> str | None:
            m = re.search(rf"(?im)^\s*\W*\s*{key}\s*:\s*(.+)$", body)
            return m.group(1).strip().strip("\"'") if m else None
        vtype, required = field("type"), field("required")
        if vtype is None:
            errs.append(f"{p.name}: variable {name!r} has no 'type'")
        elif vtype not in VAR_TYPES:
            errs.append(f"{p.name}: variable {name!r} type {vtype!r} is not one of "
                        f"{', '.join(sorted(VAR_TYPES))}")
        if required is None:
            errs.append(f"{p.name}: variable {name!r} has no 'required'")
        if vtype == "enum" and field("options") is None:
            errs.append(f"{p.name}: variable {name!r} is an enum with no 'options'")
        if (field("sensitive") or "").lower() == "true" and field("placeholder") is None:
            errs.append(f"{p.name}: variable {name!r} is sensitive with no 'placeholder' — "
                        "a sensitive value never travels, so the server needs something to emit")
        desc = field("description")
        if desc is None:
            errs.append(f"{p.name}: variable {name!r} has no 'description'")
        elif len(desc) > 240:
            errs.append(f"{p.name}: variable {name!r} description is {len(desc)} chars, "
                        "over the 240 cap a human reads under an AskUserQuestion prompt")
    return errs


def validate_dir(dir_path: Path) -> list[str]:
    errs: list[str] = []
    listed = _templates_listed(dir_path / "AGENTS.md")
    if not listed:
        return errs  # nothing declared → nothing to check
    for f in listed:
        # paths in AGENTS.md are written as `templates/foo.ext`
        path = dir_path / f
        if not path.exists():
            errs.append(f"declared template missing: {f}")
            continue
        if path.stat().st_size < 50:
            errs.append(f"template too small (<50 bytes): {f}")
            continue
        missing = _missing_header_keys(path)
        if missing:
            errs.append(
                f"template header incomplete, missing {', '.join(missing)} "
                f"as 'key: value' on its own line in the first 20 lines: {f}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        errs.extend(_variable_findings(path, _header_block(text, path.suffix)))
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()

    targets: list[Path]
    if args.all:
        targets = [p.parent for p in KNOWLEDGE.rglob("AGENTS.md")]
    else:
        if not args.target:
            ap.error("provide target dir or --all")
        targets = [Path(args.target).resolve()]

    def _display(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT))
        except ValueError:
            return str(p)

    fail = 0
    for d in targets:
        errs = validate_dir(d)
        if errs:
            fail += 1
            print(f"FAIL {_display(d)}")
            for e in errs:
                print(f"  - {e}")
        elif not args.all:
            print(f"PASS {_display(d)}")
    if args.all:
        print(f"\nsummary: {len(targets)-fail} pass / {fail} fail / {len(targets)} total")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
