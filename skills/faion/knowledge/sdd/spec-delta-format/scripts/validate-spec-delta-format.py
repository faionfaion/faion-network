#!/usr/bin/env python3
"""Validate the STRUCTURE of a spec delta file.

Checks the shape only: baseline ref, closed section vocabulary, merge order,
identifiers in operation blocks, rename arrows, scenario lines, and cross-section
identifier collisions. It does NOT check the delta against the actual baseline —
that needs the baseline and is the reviewer's job.

Usage:
  validate-spec-delta-format.py <spec.md>
  validate-spec-delta-format.py --self-test
  validate-spec-delta-format.py --help

Exit codes: 0 ok, 1 violations, 2 usage/IO failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MERGE_ORDER = ("RENAMED", "REMOVED", "CHANGED", "ADDED")
ALLOWED_H2 = ("Out of Scope",) + MERGE_ORDER
NEEDS_SCENARIOS = ("REMOVED", "CHANGED")

RE_H1 = re.compile(r"^#\s+\S", re.MULTILINE)
RE_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
RE_H3 = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
RE_BASELINE = re.compile(
    r"^\*\*Baseline:\*\*\s*`?([^`\s]+)`?\s*@\s*`?([0-9a-f]{7,40})`?\s*$",
    re.MULTILINE,
)
RE_BASELINE_LOOSE = re.compile(r"^\*\*Baseline:\*\*", re.MULTILINE)
RE_SCENARIOS = re.compile(r"^\*\*Scenarios:\*\*\s*(\S.*)$", re.MULTILINE)
RE_ARROW = re.compile(r"->|→")
# An identifier is the leading token of a block heading: DM-04, BR-07, R-12, 3.2
RE_IDENT = re.compile(r"^([A-Z]{1,4}-\d{1,4}|\d+(?:\.\d+)*)\b")


def _sections(text: str) -> list[tuple[str, str]]:
    """Return (heading, body) for each H2, in file order."""
    heads = list(RE_H2.finditer(text))
    out: list[tuple[str, str]] = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((m.group(1).strip(), text[m.end():end]))
    return out


def _blocks(body: str) -> list[tuple[str, str]]:
    """Return (heading, body) for each H3 inside one section."""
    heads = list(RE_H3.finditer(body))
    out: list[tuple[str, str]] = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        out.append((m.group(1).strip(), body[m.end():end]))
    return out


def violations(text: str) -> list[str]:
    errs: list[str] = []

    if not RE_H1.search(text):
        errs.append("no H1 title")
    if not RE_BASELINE.search(text):
        if RE_BASELINE_LOOSE.search(text):
            errs.append(
                "baseline has no git ref: expected "
                "`**Baseline:** `<path>/project-spec/` @ `<git-ref>`` (f1)"
            )
        else:
            errs.append("missing `**Baseline:**` line (f1, r1-baseline-by-reference)")

    sections = _sections(text)
    for heading, _ in sections:
        if heading not in ALLOWED_H2:
            errs.append(
                f"section '## {heading}' is not in the closed vocabulary "
                f"{list(ALLOWED_H2)} (f2)"
            )

    op_sections = [(h, b) for h, b in sections if h in MERGE_ORDER]
    if not op_sections:
        errs.append("no operation section: a delta with no operations is not a delta (f9)")

    seen_order = [h for h, _ in op_sections]
    ranks = [MERGE_ORDER.index(h) for h in seen_order]
    if ranks != sorted(ranks):
        errs.append(
            f"operation sections are out of merge order: got {seen_order}, "
            f"required order is {list(MERGE_ORDER)} (f3, r3-merge-order)"
        )
    for verb in MERGE_ORDER:
        if seen_order.count(verb) > 1:
            errs.append(f"section '## {verb}' appears more than once")

    scope = [b for h, b in sections if h == "Out of Scope"]
    if not scope:
        errs.append("missing `## Out of Scope` section (f8, r5-bounded-out-of-scope)")
    elif not [ln for ln in scope[0].splitlines() if ln.strip().startswith(("-", "*"))]:
        errs.append("`## Out of Scope` is empty (f8)")

    # identifier -> sections it appears in
    where: dict[str, list[str]] = {}
    rename_pairs: list[tuple[str, str]] = []

    for verb, body in op_sections:
        blocks = _blocks(body)
        if not blocks:
            errs.append(f"'## {verb}' has no `###` operation block")
        for heading, block in blocks:
            if verb == "RENAMED":
                if not RE_ARROW.search(heading):
                    errs.append(
                        f"RENAMED block {heading!r} has no `->` pair; a rename expressed "
                        "as REMOVED plus ADDED loses every reference (f4, r2-four-verbs-closed)"
                    )
                    continue
                left, right = RE_ARROW.split(heading, maxsplit=1)
                lm, rm = RE_IDENT.match(left.strip()), RE_IDENT.match(right.strip())
                if not lm or not rm:
                    errs.append(f"RENAMED block {heading!r}: both sides need an identifier (f7)")
                    continue
                rename_pairs.append((lm.group(1), rm.group(1)))
                where.setdefault(rm.group(1), []).append(verb)
            else:
                m = RE_IDENT.match(heading)
                if not m:
                    errs.append(
                        f"'## {verb}' block {heading!r} has no identifier in its heading "
                        "(f7, r6-ids-inside-operation-blocks)"
                    )
                    continue
                where.setdefault(m.group(1), []).append(verb)

            if verb in NEEDS_SCENARIOS:
                if not RE_SCENARIOS.search(block):
                    errs.append(
                        f"'## {verb}' block {heading!r} has no `**Scenarios:**` line: "
                        "coverage disappears exactly here (f5, r4-scenario-loss-check)"
                    )

    renamed_to = {new for _, new in rename_pairs}
    for ident, verbs in where.items():
        if len(verbs) < 2:
            continue
        # The one legal pairing: RENAMED then CHANGED on the same (post-rename) id.
        if ident in renamed_to and sorted(verbs) == ["CHANGED", "RENAMED"]:
            continue
        errs.append(
            f"identifier {ident} appears in {sorted(set(verbs))}; only RENAMED+CHANGED "
            "on one id is legal (f6, r6-ids-inside-operation-blocks)"
        )

    return errs


GOOD = """# Spec Delta — F-081 Refund window

**Baseline:** `.product/project-spec/` @ `a1b2c3d`

## Out of Scope

- Chargebacks. Separate flow with its own provider contract; unchanged here.

## RENAMED

### BR-07 Cancellation rules -> BR-07 Refund rules

**Scenarios:** AC-14, AC-15 and `tests/billing/test_refund.py` reference BR-07 by id and carry across.

The id is retained deliberately.

## CHANGED

### BR-07 Refund rules

**Scenarios:** AC-14 updated to 30 days, AC-15 unaffected, `user-flows.md#refund` updated.

**Was:** a refund is available within 14 days of purchase.
**Now:** a refund is available within 30 days of purchase.

## ADDED

### BR-11 Annual plan refund window

Annual plans have a 90-day refund window.
"""


def self_test() -> int:
    no_ref = GOOD.replace(" @ `a1b2c3d`", "")
    bad_order = (
        "# Spec Delta — F-082 Pricing\n\n"
        "**Baseline:** `.product/project-spec/` @ `a1b2c3d`\n\n"
        "## Out of Scope\n\n- Taxes; handled by the provider.\n\n"
        "## ADDED\n\n### PR-03 Annual discount\n\nAnnual plans get 20% off.\n\n"
        "## REMOVED\n\n### PR-01 Monthly-only pricing\n\n"
        "**Scenarios:** none; verified with a search across .product/.\n\nNo longer accurate.\n"
    )
    invented_verb = GOOD.replace("## CHANGED", "## UPDATED")
    no_scenarios = GOOD.replace(
        "**Scenarios:** AC-14 updated to 30 days, AC-15 unaffected, `user-flows.md#refund` updated.\n\n",
        "",
    )
    unchanged_section = GOOD + "\n## Unchanged\n\nEverything else.\n"
    rename_no_arrow = GOOD.replace(
        "### BR-07 Cancellation rules -> BR-07 Refund rules",
        "### BR-07 Cancellation rules",
    )
    collision = GOOD.replace("### BR-11 Annual plan refund window", "### BR-07 Refund rules")
    no_scope = GOOD.replace(
        "## Out of Scope\n\n- Chargebacks. Separate flow with its own provider contract; unchanged here.\n\n",
        "",
    )
    no_ops = (
        "# Spec Delta — F-090\n\n"
        "**Baseline:** `.product/project-spec/` @ `a1b2c3d`\n\n"
        "## Out of Scope\n\n- Everything.\n"
    )

    cases = [
        ("valid delta", GOOD, 0),
        ("baseline without a git ref", no_ref, 1),
        ("operation sections out of merge order", bad_order, 1),
        ("invented verb `## UPDATED`", invented_verb, 1),
        ("CHANGED block without a Scenarios line", no_scenarios, 1),
        ("`## Unchanged` section", unchanged_section, 1),
        ("RENAMED without an arrow", rename_no_arrow, 1),
        ("same id in RENAMED, CHANGED and ADDED", collision, 1),
        ("missing Out of Scope", no_scope, 1),
        ("no operation sections", no_ops, 1),
    ]
    failed = 0
    for name, doc, expect in cases:
        errs = violations(doc)
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
    positional = [a for a in args if not a.startswith("-")]
    if len(positional) != 1:
        print(__doc__)
        return 2
    path = Path(positional[0])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    errs = violations(path.read_text(encoding="utf-8"))
    if not errs:
        print(f"OK  {path}")
        return 0
    print(f"FAIL  {path}", file=sys.stderr)
    for e in errs:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
