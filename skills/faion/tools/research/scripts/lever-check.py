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
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

NAME = "lever-check"
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

    # A ledger id carried twice — two research passes concatenated, most
    # often — used to sail through: one answer covered both rows, `unanswered`
    # was computed as len(ledger) - len(answers) and reported 1, and the exit
    # code came from `problems`, which stayed empty. The summary said a lever
    # went unanswered and the gate said pass.
    seen: set[str] = set()
    for key in ids:
        if key in seen:
            problems.append(f"{key}: appears more than once in the ledger — one "
                            f"answer cannot dispose of two levers, so give each "
                            f"its own id")
        seen.add(key)

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


def run_cli(argv: list[str]) -> int:
    """main() over a fixed argv, output swallowed. --self-test uses it to prove
    the exit contract end to end: an unanswered lever must reach the caller as
    exit 1, and a malformed input as exit 2, because a pipeline branches on the
    difference between 'the concept skipped a lever' and 'I could not read'."""
    saved = sys.argv
    sys.argv = [NAME] + argv
    try:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return main()
    finally:
        sys.argv = saved


LEDGER = [
    {"id": "C1", "lever": "charge for seats over five"},
    {"id": "C2", "lever": "sell the export as an add-on"},
    {"id": "C3", "lever": "raise the annual plan"},
]
ANSWERS = [
    {"id": "C1", "lever": "charge for seats over five", "disposition": "applied",
     "lands_in": "pricing page + billing", "reason": "already metered"},
    {"id": "C2", "lever": "sell the export as an add-on", "disposition": "declined",
     "reason": "the export is the reason people trust the tool",
     "decline_class": "dark-pattern"},
]


def self_test() -> list[str]:
    """Prove the audit against inline fixtures: what counts as answered, the
    arithmetic, and the exit code on the one condition that blocks."""
    failures: list[str] = []

    def problems_for(ledger: list[dict], found: list[dict]) -> list[str]:
        return audit(ledger, found)[1]

    # 1: a lever the concept never answered is a finding and is printed with
    # its lever text — the whole reason this tool exists.
    answers, problems = audit(LEDGER, ANSWERS)
    unanswered = [p for p in problems if p.startswith("C3:")]
    if len(problems) != 1 or not unanswered:
        failures.append(f"an unanswered lever gave {problems}")
    elif "UNANSWERED" not in unanswered[0] or "raise the annual plan" not in unanswered[0]:
        failures.append(f"the unanswered finding does not name the lever: "
                        f"{unanswered[0]}")

    # 2: the arithmetic. applied + declined + unanswered == the ledger.
    text = report(LEDGER, answers, problems)
    if "levers 3 · applied 1 · declined 1 · unanswered 1" not in text:
        failures.append("the counts line does not add up to the ledger")
    if "**unanswered**" not in text:
        failures.append("the unanswered row is not marked in the table")

    # 3: every decline is printed in full, with its class and its reason.
    if ("- **C2** (dark-pattern)" not in text
            or "the export is the reason people trust the tool" not in text):
        failures.append("a decline is not printed in full")

    # 4: a fully answered ledger is clean, and a dark-pattern decline passes
    # exactly like any other class.
    complete = ANSWERS + [{"id": "C3", "lever": "raise the annual plan",
                           "disposition": "declined", "reason": "no evidence yet",
                           "decline_class": "evidence"}]
    answers, problems = audit(LEDGER, complete)
    if problems:
        failures.append(f"a complete answer set produced {problems}")
    if "levers 3 · applied 1 · declined 2 · unanswered 0" not in report(
            LEDGER, answers, problems):
        failures.append("a complete answer set miscounts")

    # 5-10: the malformed answers, each one finding.
    cases = [
        ([{"id": "C1", "disposition": "maybe", "reason": "r"}], "disposition"),
        ([{"id": "C1", "disposition": "applied", "lands_in": "none",
           "reason": "r"}], "names nowhere it lands"),
        ([{"id": "C1", "disposition": "applied", "lands_in": "billing"}],
         "no reason given"),
        ([{"id": "C1", "disposition": "declined", "reason": "later"}],
         "decline_class"),
        ([{"id": "C1", "disposition": "declined", "reason": "later",
           "decline_class": "not-now"}], "decline_class"),
        ([{"id": "C9", "disposition": "applied", "lands_in": "x", "reason": "r"}],
         "the ledger does not carry"),
        ([{"disposition": "applied", "lands_in": "x", "reason": "r"}], "no id"),
    ]
    for found, marker in cases:
        hits = [p for p in problems_for(LEDGER[:1], found) if marker in p]
        if not hits:
            failures.append(f"{found}: no finding matching {marker!r}")

    # 11: the same lever answered twice is a finding, not a silent overwrite.
    twice = [ANSWERS[0], dict(ANSWERS[0], lands_in="somewhere else")]
    if not any("answered more than once" in p
               for p in problems_for(LEDGER[:1], twice)):
        failures.append("the same lever answered twice was accepted")

    # 12: a ledger id carried twice. One answer cannot dispose of two levers;
    # this used to report unanswered=1 and still exit 0.
    duplicated = [LEDGER[0], dict(LEDGER[0], lever="charge for storage too")]
    if not any("appears more than once in the ledger" in p
               for p in problems_for(duplicated, ANSWERS[:1])):
        failures.append("a duplicated ledger id was accepted, so an unanswered "
                        "lever can still pass")

    # 13: a value carrying a pipe cannot break the table it is rendered into.
    piped = [{"id": "C1", "lever": "a | b"}]
    if "| a \\| b |" not in report(piped, {}, []):
        failures.append("a pipe in a lever is not escaped")

    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)

        def write(name: str, text: str) -> str:
            path = home / name
            path.write_text(text, encoding="utf-8")
            return str(path)

        ledger_lines = "\n".join(json.dumps(e) for e in LEDGER)
        full = write("ledger.jsonl",
                     "# the evidence stage wrote this\n\n" + ledger_lines + "\n")
        one = write("one.jsonl", json.dumps(LEDGER[0]) + "\n")
        short = write("concept-short.json",
                      json.dumps({"commercial_findings": ANSWERS}))
        whole = write("concept-whole.json",
                      json.dumps({"commercial_findings": complete}))
        out = str(home / "decisions.md")

        # 14-15: the two verdicts, end to end. Comments and blank lines in the
        # ledger are skipped rather than counted as levers.
        if run_cli(["--ledger", full, "--concept", whole, "--report", out]) != 0:
            failures.append("a complete answer set did not exit 0")
        if "levers 3 · applied 1 · declined 2" not in Path(out).read_text(
                encoding="utf-8"):
            failures.append("the report file does not carry the counts")
        if run_cli(["--ledger", full, "--concept", short, "--report", out]) != 1:
            failures.append("an unanswered lever did not exit 1")
        if "**unanswered**" not in Path(out).read_text(encoding="utf-8"):
            failures.append("the report is not written when the check fails")

        # 16-17: unreadable and malformed input is exit 2, never exit 1 — a
        # missing file is not a research finding.
        for label, argv in (
                ("missing ledger", ["--ledger", str(home / "gone.jsonl"),
                                    "--concept", short]),
                ("missing concept", ["--ledger", one,
                                     "--concept", str(home / "gone.json")]),
                ("ledger line is not JSON",
                 ["--ledger", write("bad.jsonl", "{oops\n"), "--concept", short]),
                ("ledger entry with no id",
                 ["--ledger", write("noid.jsonl", '{"lever":"x"}\n'),
                  "--concept", short]),
                ("concept is not JSON",
                 ["--ledger", one, "--concept", write("bad.json", "{oops")]),
                ("concept is not an object",
                 ["--ledger", one, "--concept", write("arr.json", "[]")]),
                ("findings not an array",
                 ["--ledger", one,
                  "--concept", write("wrong.json",
                                     '{"commercial_findings": {"C1": "applied"}}')]),
                ("a finding is not an object",
                 ["--ledger", one,
                  "--concept", write("scalar.json",
                                     '{"commercial_findings": ["C1"]}')])):
            code = run_cli(argv + ["--report", out])
            if code != 2:
                failures.append(f"{label}: exit {code}, want 2")

        # 18: an empty ledger with no findings is a pass, not a crash.
        if run_cli(["--ledger", write("empty.jsonl", "\n# nothing\n"),
                    "--concept", write("none.json", "{}"),
                    "--report", out]) != 0:
            failures.append("an empty ledger did not exit 0")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", help="commercial-lever ledger JSONL")
    ap.add_argument("--concept", help="concept verdict JSON")
    ap.add_argument("--report", help="decisions report path (default stdout)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=18 failures={len(failures)}")
        return 1 if failures else 0

    # Checked here rather than by argparse's required=True so --self-test
    # needs no other flag.
    missing = [flag for flag, value in (("--ledger", args.ledger),
                                        ("--concept", args.concept))
               if not value]
    if missing:
        print(f"{NAME}: the following arguments are required: "
              f"{', '.join(missing)}", file=sys.stderr)
        return 2

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
