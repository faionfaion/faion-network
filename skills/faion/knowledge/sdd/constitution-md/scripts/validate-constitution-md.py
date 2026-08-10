#!/usr/bin/env python3
"""Validate the STRUCTURE of a constitution.md.

This checks shape only: rule count, word cap, why present, sequential ids,
sections present, footer parses, no unresolved placeholders. It cannot check
whether the rules are good, whether two of them contradict each other, or
whether the code obeys them — see content/03-failure-modes.xml, f1.

Usage:
  validate-constitution-md.py <constitution.md>
  validate-constitution-md.py --draft <constitution.md>   allow TODO(...) placeholders
  validate-constitution-md.py --self-test
  validate-constitution-md.py --help

Exit codes: 0 ok, 1 violations, 2 usage/IO failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_RULES = 20
MAX_RULE_WORDS = 60
REQUIRED_SECTIONS = ("Scope", "Rules", "Compliance", "Amendment")

RE_H1 = re.compile(r"^#\s+\S", re.MULTILINE)
RE_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
RE_RULE_HEAD = re.compile(r"^###\s+(R-\d{2})\s+(.+?)\s*$", re.MULTILINE)
RE_WHY = re.compile(r"^\*\*Why:\*\*\s*(.+?)\s*$", re.MULTILINE)
RE_SYNC = re.compile(r"<!--\s*Sync Impact Report(.*?)-->", re.DOTALL)
RE_FOOTER = re.compile(
    r"\*\*Version:\*\*\s*(\d+\.\d+\.\d+).*?"
    r"\*\*Ratified:\*\*\s*(\d{4}-\d{2}-\d{2}).*?"
    r"\*\*Last amended:\*\*\s*(\d{4}-\d{2}-\d{2})",
    re.DOTALL,
)
RE_TODO = re.compile(r"TODO\([A-Z_]+\)|\[PLACEHOLDER\]")
RE_PROJECT_SPEC = re.compile(r"project-spec/")
# A why is one sentence: at most one terminal '.', '?' or '!' and it ends the line.
RE_SENTENCE_END = re.compile(r"[.?!]")


RE_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
RE_TODO_TOKEN = re.compile(r"TODO\(([A-Z_]+)\)")


def _draft_fill(text: str) -> str:
    """Substitute placeholders so a draft's footer can still be shape-checked."""
    def sub(m: re.Match[str]) -> str:
        name = m.group(1)
        if "VERSION" in name:
            return "0.0.0"
        if "DATE" in name:
            return "0001-01-01"
        return "-"
    return RE_TODO_TOKEN.sub(sub, text)


def _rule_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return (id, title, body) for each ### R-NN block.

    A block ends at the next rule heading OR the next H2, whichever comes first —
    otherwise the last rule absorbs every section below it.
    """
    heads = list(RE_RULE_HEAD.finditer(text))
    h2s = [m.start() for m in RE_H2.finditer(text)]
    blocks: list[tuple[str, str, str]] = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        for pos in h2s:
            if m.end() <= pos < end:
                end = pos
                break
        body = RE_COMMENT.sub("", text[m.end():end])
        blocks.append((m.group(1), m.group(2), body))
    return blocks


def violations(text: str, draft: bool = False) -> list[str]:
    errs: list[str] = []

    if not RE_H1.search(text):
        errs.append("no H1 title (f6)")
    if not RE_SYNC.search(text):
        errs.append("missing Sync Impact Report comment at the top of the file (r6)")

    headings = [h.strip() for h in RE_H2.findall(text)]
    for want in REQUIRED_SECTIONS:
        if not any(h == want or h.startswith(want + " ") for h in headings):
            errs.append(f"missing '## {want}' section (f6)")

    scope = ""
    m = re.search(r"(?ms)^##\s+Scope\s*\n(.*?)(?=^##\s|\Z)", text)
    if m:
        scope = m.group(1)
    if not RE_PROJECT_SPEC.search(scope):
        errs.append(
            "Scope does not name a `project-spec/` location; delegation is mandatory "
            "(f7, r7-delegate-domain-to-project-spec)"
        )

    blocks = _rule_blocks(text)
    if not blocks:
        errs.append("no `### R-NN` rule blocks found (f1)")
    if len(blocks) > MAX_RULES:
        errs.append(
            f"{len(blocks)} rules exceeds the cap of {MAX_RULES}: merge, demote or "
            "retire one — do not raise the cap (f1, r2-twenty-rule-cap)"
        )

    seen: set[str] = set()
    for idx, (rid, title, body) in enumerate(blocks, start=1):
        expected = f"R-{idx:02d}"
        if rid in seen:
            errs.append(f"duplicate rule id {rid} (f3)")
        seen.add(rid)
        if rid != expected:
            errs.append(f"rule id {rid} is out of sequence; expected {expected} (f3)")
        if not title.strip():
            errs.append(f"{rid}: no title")

        whys = RE_WHY.findall(body)
        if not whys:
            errs.append(f"{rid}: missing `**Why:**` line (f2, r3-why-before-rule)")
        elif len(RE_SENTENCE_END.findall(whys[0].strip().rstrip("."))) > 0:
            errs.append(f"{rid}: `**Why:**` must be exactly one sentence (f2)")

        rule_text = RE_WHY.sub("", body).strip()
        words = len(rule_text.split())
        if words == 0:
            errs.append(f"{rid}: rule body is empty (f2)")
        elif words > MAX_RULE_WORDS:
            errs.append(
                f"{rid}: rule body is {words} words, cap is {MAX_RULE_WORDS} "
                "(f1, r2-twenty-rule-cap)"
            )

    fm = RE_FOOTER.search(_draft_fill(text) if draft else text)
    if not fm:
        errs.append(
            "missing or unparseable footer: expected "
            "`**Version:** X.Y.Z · **Ratified:** YYYY-MM-DD · **Last amended:** YYYY-MM-DD` (f5)"
        )
    elif fm.group(2) > fm.group(3):
        errs.append(
            f"ratified date {fm.group(2)} is later than last amended {fm.group(3)} (f5)"
        )

    if not draft:
        stray = sorted(set(RE_TODO.findall(text)))
        if stray:
            errs.append(
                "unresolved placeholders in a ratified constitution: "
                + ", ".join(stray)
                + " — pass --draft while the file is still being filled in (f4)"
            )

    return errs


GOOD = """# Example Constitution

<!--
Sync Impact Report
version: 0.0.0 -> 1.0.0
added: R-01, R-02
modified: -
removed: -
out of sync: -
-->

## Scope

Domain facts, business rules, the data model and deploy topology live in
`.product/project-spec/`, not here.

## Rules

### R-01 One migration per pull request

**Why:** two migrations in one pull request cannot be rolled back independently

Each pull request contains at most one schema migration. A change needing two
migrations is split into two pull requests, merged in order.

### R-02 No new runtime dependency without a named alternative

**Why:** every dependency we regret was added without anyone naming what it replaced

Adding a runtime dependency requires naming the alternative considered and the
reason it loses, recorded in the pull request description.

## Compliance

The reviewer checks R-01 by counting migration files in the diff and R-02 by
reading the pull request description. R-01 is additionally checked by CI.

## Amendment

Propose a change as a pull request against this file. MAJOR on removal or
reversal, MINOR on addition, PATCH on wording.

---

**Version:** 1.0.0 · **Ratified:** 2026-08-04 · **Last amended:** 2026-08-04
"""


def self_test() -> int:
    over_cap = GOOD.replace(
        "## Compliance",
        "".join(
            f"### R-{i:02d} filler\n\n**Why:** a reason\n\nA rule body.\n\n"
            for i in range(3, 23)
        )
        + "## Compliance",
    )
    no_why = GOOD.replace(
        "**Why:** two migrations in one pull request cannot be rolled back independently\n\n",
        "",
    )
    out_of_seq = GOOD.replace("### R-02", "### R-05")
    no_delegation = GOOD.replace("`.product/project-spec/`", "somewhere else")
    bad_footer = GOOD.replace("**Ratified:** 2026-08-04", "**Ratified:** 2026-09-01")
    long_body = GOOD.replace(
        "Each pull request contains at most one schema migration. A change needing two\n"
        "migrations is split into two pull requests, merged in order.",
        "word " * 70,
    )
    with_todo = GOOD.replace("out of sync: -", "out of sync: TODO(DOWNSTREAM_FILES)")

    cases = [
        ("valid constitution", GOOD, False, 0),
        ("over the 20-rule cap", over_cap, False, 1),
        ("rule with no why", no_why, False, 1),
        ("rule ids out of sequence", out_of_seq, False, 1),
        ("Scope without a project-spec/ pointer", no_delegation, False, 1),
        ("ratified later than last amended", bad_footer, False, 1),
        ("rule body over the word cap", long_body, False, 1),
        ("unresolved TODO in a ratified file", with_todo, False, 1),
        ("same file accepted as a draft", with_todo, True, 0),
    ]
    failed = 0
    for name, doc, draft, expect in cases:
        errs = violations(doc, draft=draft)
        got = 1 if errs else 0
        if got != expect:
            failed += 1
            print(f"[FAIL] {name} -> {errs}")
        else:
            print(f"[ok  ] {name}" + (f" -> {errs[0]}" if errs else ""))
    print(f"\n{len(cases) - failed}/{len(cases)} self-tests passed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        return 2
    if "--self-test" in args:
        return self_test()
    draft = "--draft" in args
    positional = [a for a in args if not a.startswith("-")]
    if len(positional) != 1:
        print(__doc__)
        return 2
    path = Path(positional[0])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    errs = violations(path.read_text(encoding="utf-8"), draft=draft)
    if not errs:
        print(f"OK  {path}" + (" (draft)" if draft else ""))
        return 0
    print(f"FAIL  {path}", file=sys.stderr)
    for e in errs:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
