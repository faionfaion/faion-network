#!/usr/bin/env python3
"""lever-check.py — count a concept's answers against the commercial-lever
ledger the evidence stage wrote, and fail when a lever went unanswered.

Two inputs, both produced earlier in the same run:
  --ledger   the JSONL `source-table.py --levers` emits, one object per
             tagged claim, `{"id","lever","claim","url","date","confidence"}`
  --concept  the concept verdict JSON, carrying `commercial_findings`:
             `{"id","lever","disposition","lands_in","reason","decline_class"}`

What is checked is arithmetic, never judgement:
  - every ledger id has exactly one entry
  - `disposition` is `applied` or `declined`
  - an applied lever names where it lands (not empty, not "none")
  - a declined lever gives a reason and classifies it as one of
    dark-pattern / envelope / evidence / economics / dependency
  - no entry answers an id the ledger does not carry

What is NOT checked, deliberately: whether a reason is a good reason.
That is a judgement, and a gate that blocks on a judgement gets talked
past — the cheapest way through is to reword. So the reason is printed
instead, with its class and its lever, where a reviewer and a human
both read it. The blocking condition is the one thing that cannot be
argued with: a finding the research marked commercially significant
that the concept never answered at all.

A `dark-pattern` decline passes exactly like any other. The tool has no
opinion on which class is used, only that one is.

Exit: 0 every lever answered and well-formed · 1 at least one is not ·
      2 an input is missing, unreadable or malformed.
Zero model calls.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DISPOSITIONS = ("applied", "declined")
DECLINE_CLASSES = ("dark-pattern", "envelope", "evidence", "economics",
                   "dependency")


def esc(text: str) -> str:
    """Make a value safe inside a markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def read_ledger(path: str) -> list[dict] | int:
    """The ledger as a list of entries, or an exit code on failure."""
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"lever-check: cannot read ledger: {exc}", file=sys.stderr)
        return 2
    entries = []
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"lever-check: ledger line {lineno}: bad JSON: {exc}",
                  file=sys.stderr)
            return 2
        if not isinstance(obj, dict) or not str(obj.get("id") or "").strip():
            print(f"lever-check: ledger line {lineno}: no 'id'", file=sys.stderr)
            return 2
        entries.append(obj)
    return entries


def read_findings(path: str) -> list[dict] | int:
    """`commercial_findings` from the concept verdict, or an exit code."""
    try:
        verdict = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"lever-check: cannot read concept: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"lever-check: concept is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(verdict, dict):
        print("lever-check: concept is not a JSON object", file=sys.stderr)
        return 2
    found = verdict.get("commercial_findings", [])
    if not isinstance(found, list):
        print("lever-check: 'commercial_findings' is not an array", file=sys.stderr)
        return 2
    for entry in found:
        if not isinstance(entry, dict):
            print("lever-check: a commercial_findings entry is not an object",
                  file=sys.stderr)
            return 2
    return found


def audit(ledger: list[dict], found: list[dict]) -> tuple[dict, list[str]]:
    """Match answers to levers; return the per-id verdict and the findings."""
    answers: dict[str, dict] = {}
    problems: list[str] = []
    ids = [str(entry["id"]).strip() for entry in ledger]

    for entry in found:
        key = str(entry.get("id") or "").strip()
        if not key:
            problems.append("a commercial_findings entry carries no id")
            continue
        if key not in ids:
            problems.append(f"{key}: answers a lever the ledger does not carry")
            continue
        if key in answers:
            problems.append(f"{key}: answered more than once")
            continue
        answers[key] = entry

    for entry in ledger:
        key = str(entry["id"]).strip()
        lever = str(entry.get("lever") or "").strip()
        answer = answers.get(key)
        if answer is None:
            problems.append(f"{key}: UNANSWERED — the research marked this "
                            f"commercially significant and the concept neither "
                            f"applied nor declined it: {lever}")
            continue
        disposition = str(answer.get("disposition") or "").strip()
        lands_in = str(answer.get("lands_in") or "").strip()
        reason = str(answer.get("reason") or "").strip()
        klass = str(answer.get("decline_class") or "").strip()
        if disposition not in DISPOSITIONS:
            problems.append(f"{key}: disposition {disposition!r} is not "
                            f"'applied' or 'declined'")
            continue
        if not reason:
            problems.append(f"{key}: no reason given")
        if disposition == "applied" and lands_in.lower() in ("", "none", "n/a"):
            problems.append(f"{key}: applied and names nowhere it lands")
        if disposition == "declined" and klass not in DECLINE_CLASSES:
            problems.append(f"{key}: declined with decline_class {klass!r} — "
                            f"one of {'/'.join(DECLINE_CLASSES)} is required, and "
                            f"deferring to a later slice is a decline like any other")
    return answers, problems


def report(ledger: list[dict], answers: dict[str, dict],
           problems: list[str]) -> str:
    """The decisions report: the counts, then every decline in full."""
    applied = [e for e in answers.values()
               if str(e.get("disposition") or "").strip() == "applied"]
    declined = [e for e in answers.values()
                if str(e.get("disposition") or "").strip() == "declined"]
    out = ["## Commercial lever decisions", "",
           f"levers {len(ledger)} · applied {len(applied)} · "
           f"declined {len(declined)} · unanswered "
           f"{len(ledger) - len(answers)}", "",
           "| id | lever | disposition | lands in / class | reason |",
           "|----|-------|-------------|------------------|--------|"]
    for entry in ledger:
        key = str(entry["id"]).strip()
        answer = answers.get(key) or {}
        disposition = str(answer.get("disposition") or "").strip() or "**unanswered**"
        detail = (str(answer.get("lands_in") or "").strip()
                  if disposition == "applied"
                  else str(answer.get("decline_class") or "").strip())
        out.append(f"| {esc(key)} | {esc(entry.get('lever') or '')} | "
                   f"{disposition} | {esc(detail) or '—'} | "
                   f"{esc(answer.get('reason') or '')or '—'} |")
    out += ["", "### Declines", ""]
    if declined:
        for entry in declined:
            out.append(f"- **{esc(entry.get('id') or '')}** "
                       f"({esc(entry.get('decline_class') or '')}) — "
                       f"{esc(entry.get('lever') or '')} — "
                       f"{esc(entry.get('reason') or '')}")
    else:
        out.append("- none")
    out += ["", "### Findings", ""]
    out += [f"- {p}" for p in problems] if problems else ["- none"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", required=True, help="commercial-lever ledger JSONL")
    ap.add_argument("--concept", required=True, help="concept verdict JSON")
    ap.add_argument("--report", help="decisions report path (default stdout)")
    args = ap.parse_args()

    ledger = read_ledger(args.ledger)
    if isinstance(ledger, int):
        return ledger
    found = read_findings(args.concept)
    if isinstance(found, int):
        return found

    answers, problems = audit(ledger, found)
    text = report(ledger, answers, problems)
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    else:
        print(text)

    applied = sum(1 for e in answers.values()
                  if str(e.get("disposition") or "").strip() == "applied")
    declined = sum(1 for e in answers.values()
                   if str(e.get("disposition") or "").strip() == "declined")
    for problem in problems:
        print(f"lever-check: {problem}", file=sys.stderr)
    print(f"lever-check: levers={len(ledger)} applied={applied} "
          f"declined={declined} unanswered={len(ledger) - len(answers)} "
          f"findings={len(problems)} -> {args.report or 'stdout'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
