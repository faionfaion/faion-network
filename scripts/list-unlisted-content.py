#!/usr/bin/env python3
"""CR-010 — every `content/*.xml` file gets a row in its envelope's `## Content` table.

The table is the document's table of contents: an agent reads `AGENTS.md` first
and decides from that table what to load. A file missing from it is still
*delivered* — delivery resolves by directory, and CR-010's correction records the
evidence — but it is never *chosen*, and it carries no depth or token estimate a
caller could budget against.

    --report   what is unlisted, with the row that would be written
    --write    add the rows
    --check    exit 1 if any content file is unlisted

Nothing here writes prose. The description in each row is the file's own
`<summary>`, first sentence, falling back to its `<text title=…>` when that
sentence runs past the column's width. Both are authored text already in the
file; a mechanical pass that invented a description would be putting words in a
methodology's mouth.

Depth is written as `recommended` for every added row, deliberately. Depth is an
editorial judgement — `essential` means an agent should load it before deciding —
and a script cannot make it. Raising a row is the editorial pass CR-010 calls
option 1; this is the stopgap that makes the table true first.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE = os.path.join(REPO_ROOT, "skills", "faion", "knowledge")

SUMMARY = re.compile(r"<summary[^>]*>(.*?)</summary>", re.S)
TITLE = re.compile(r'<text[^>]*\btitle="([^"]*)"')
# The header plus separator of the four-column table every affected envelope has.
TABLE = re.compile(
    r"(?ms)^(## Content[^\n]*\n\n\|[^\n]*\|\n\|[-\s|:]+\|\n)((?:\|[^\n]*\|\n)*)")

DESC_MAX = 150


def first_sentence(text: str) -> str:
    flat = " ".join(text.split())
    # Unescape the four entities the corpus's XML actually uses.
    for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&apos;", "'"), ("&quot;", '"')):
        flat = flat.replace(ent, ch)
    # A sentence ends at a full stop the NEXT word capitalises. Splitting on any
    # `.` cut "RPA vs. BPA" after "vs." and shipped a row ending in "RPA vs."
    for m in re.finditer(r"[.!?](?=\s+[A-Z(\u201c\"]|$)", flat):
        head = flat[:m.end()]
        if re.search(r"\b(vs|e\.g|i\.e|etc|approx|cf|Dr|Mr|Ms|No|Fig|Sec|Ch)\.$", head):
            continue
        return head.strip()
    return flat.strip()


def describe(raw: str) -> str:
    summary = SUMMARY.search(raw)
    title = TITLE.search(raw)
    if summary:
        sentence = first_sentence(summary.group(1))
        if sentence and len(sentence) <= DESC_MAX:
            return sentence
    if title:
        return title.group(1).strip()
    if summary:
        return first_sentence(summary.group(1))[:DESC_MAX].rstrip() + "…"
    return ""


def est_tokens(nbytes: int) -> int:
    """Rounded to the nearest 50, the granularity every existing row uses."""
    return max(50, int(round(nbytes / 4 / 50.0)) * 50)


def unlisted(envelope: str) -> list[str]:
    slug_dir = os.path.dirname(envelope)
    content_dir = os.path.join(slug_dir, "content")
    if not os.path.isdir(content_dir):
        return []
    text = open(envelope, encoding="utf-8", errors="replace").read()
    return [f for f in sorted(os.listdir(content_dir))
            if f.endswith(".xml") and f not in text and f"content/{f}" not in text]


def row_for(content_path: str, tilde: bool) -> str:
    raw = open(content_path, encoding="utf-8", errors="replace").read()
    name = os.path.basename(content_path)
    desc = describe(raw).replace("|", "\\|")
    # The corpus is split almost evenly on `~1100` versus `1100`, so there is no
    # house style to follow — only the table being edited, which must not end up
    # inconsistent with itself.
    est = est_tokens(os.path.getsize(content_path))
    return (f"| `content/{name}` | recommended | {desc} | "
            f"{'~' if tilde else ''}{est} |")


def envelopes():
    return sorted(glob.glob(os.path.join(KNOWLEDGE, "*", "*", "AGENTS.md")))


def rel(path: str) -> str:
    return os.path.relpath(path, REPO_ROOT)


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--report", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    ap.add_argument("--domain")
    args = ap.parse_args()

    paths = envelopes()
    if args.domain:
        paths = [p for p in paths if f"/{args.domain}/" in p]

    dirs = files = written = 0
    no_table = []
    for envelope in paths:
        missing = unlisted(envelope)
        if not missing:
            continue
        dirs += 1
        files += len(missing)
        slug_dir = os.path.dirname(envelope)
        if args.check:
            print(f"FAIL {rel(slug_dir)}")
            for name in missing:
                print(f"  - content/{name} is not in the ## Content table")
            continue
        envelope_text = open(envelope, encoding="utf-8", errors="replace").read()
        tilde = bool(re.search(r"(?m)^\|\s*`content/[^`]+`\s*\|[^|]*\|[^|]*\|\s*~", envelope_text))
        rows = [row_for(os.path.join(slug_dir, "content", name), tilde) for name in missing]
        if args.report:
            print(f"{rel(slug_dir)}  (+{len(rows)})")
            for row in rows:
                print(f"    {row}")
            continue
        text = envelope_text
        m = TABLE.search(text)
        if not m:
            no_table.append(rel(envelope))
            continue
        body = m.group(2).rstrip("\n")
        merged = body + "\n" + "\n".join(rows) + "\n"
        text = text[:m.start(2)] + merged + text[m.end(2):]
        open(envelope, "w", encoding="utf-8").write(text)
        written += 1

    if args.check:
        if files:
            print(f"\n{files} content file(s) over {dirs} slug(s) are absent from "
                  f"their ## Content table", file=sys.stderr)
            return 1
        print(f"every content file is listed, across {len(paths)} envelope(s)")
        return 0

    print(f"{files} unlisted file(s) over {dirs} slug(s)"
          + (f"; rows added to {written} envelope(s)" if args.write else ""))
    for path in no_table:
        print(f"  SKIPPED, no parseable ## Content table: {path}", file=sys.stderr)
    return 1 if no_table else 0


if __name__ == "__main__":
    sys.exit(main())
