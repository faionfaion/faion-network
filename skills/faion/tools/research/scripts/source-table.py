#!/usr/bin/env python3
"""source-table.py — turn a JSONL of research claims into a markdown evidence
table, a gaps report and a commercial-lever ledger, and fail the run when a
load-bearing claim carries no source or a money lever carries no name.

Input JSONL, one object per line:
    {"claim": "...", "url": "https://...", "date": "2026-08-11",
     "confidence": "high", "load_bearing": true,
     "commercial": true, "lever": "..."}
  - claim       required, non-empty string
  - url         optional in the schema, REQUIRED for a load-bearing claim
  - date        optional, YYYY-MM-DD (anything else is reported as a gap)
  - confidence  optional string (high/medium/low) or number 0..1
  - load_bearing  optional bool, default true — set false for colour/context
  - commercial  optional bool, default false — true when the claim names
                something that could move what the product earns
  - lever       required when commercial is true: the action the claim
                implies, in the product's own terms, not the claim restated

Output: markdown table to --out (default stdout), gaps report to --report,
        the ledger of commercial levers to --levers, one summary line on
        stdout.
Exit:   0 every load-bearing claim sourced and every lever named · 1 at
        least one is not · 2 unreadable or malformed input.

Why: a research arm that cites nothing loses to one that cites everything.
The measured gap on the run this encodes was 108 sourced URLs against 0.
The ledger exists for the second measured gap: the pipeline found the
levers that decide revenue, sourced them, and then shipped without them —
so every tagged lever leaves here with an id a later stage must answer.
Zero model calls.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
from pathlib import Path

NAME = "source-table"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://\S+$", re.I)


def esc(text: str) -> str:
    """Make a value safe inside a markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def confidence_str(value) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        return ""
    if isinstance(value, (int, float)):
        return f"{value:g}"
    return str(value).strip()


def run_cli(argv: list[str]) -> int:
    """main() over a fixed argv, output swallowed. The gate's whole value is
    its exit code, so --self-test asserts on the code the caller sees rather
    than on the counters behind it."""
    saved = sys.argv
    sys.argv = [NAME] + argv
    try:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return main()
    finally:
        sys.argv = saved


# One claim per failure this gate exists to catch, plus the two shapes that
# must pass. `example.com` is an RFC 2606 reserved name; nothing here is fetched.
SOURCED = ('{"claim": "Edge cached a three-day-old bundle", '
           '"url": "https://blog.example.com/cdn", "date": "2026-08-11", '
           '"confidence": "high"}')
COLOUR = ('{"claim": "The team calls it the ghost deploy", '
          '"load_bearing": false, "confidence": "low"}')
UNSOURCED = '{"claim": "Most teams never check the edge", "confidence": "high"}'
LEVERED = ('{"claim": "Rivals charge for the purge API", '
           '"url": "https://docs.example.com/pricing", "date": "2026-08-11", '
           '"confidence": "medium", "commercial": true, '
           '"lever": "keep purge in the free tier and price the audit"}')
LEVERLESS = ('{"claim": "Rivals charge for the purge API", '
             '"url": "https://docs.example.com/pricing", "confidence": "medium", '
             '"commercial": true}')


def self_test() -> list[str]:
    """Prove the gate against inline fixtures written to a temporary directory:
    what fails, what passes, and that the gaps report names the offender."""
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        table, gaps, levers = (str(home / "table.md"), str(home / "gaps.md"),
                               str(home / "levers.jsonl"))

        def run(lines: list[str], extra: list[str] | None = None) -> int:
            path = home / "claims.jsonl"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return run_cli(["--in", str(path), "--out", table, "--report", gaps,
                            "--levers", levers] + (extra or []))

        def text(path: str) -> str:
            return Path(path).read_text(encoding="utf-8")

        # 1: a fully sourced set passes, and nothing is written to the ledger
        # when nothing is tagged commercial.
        code = run(["# a comment line", "", SOURCED, COLOUR])
        if code != 0:
            failures.append(f"a fully sourced set exited {code}, want 0")
        if text(levers).strip():
            failures.append("the ledger is not empty when nothing is tagged")
        rows = re.findall(r"^\| \d+ \|", text(table), re.M)
        if len(rows) != 2:
            failures.append(f"the table holds {len(rows)} rows for 2 claims")
        if "[link](https://blog.example.com/cdn)" not in text(table):
            failures.append("a sourced claim is not linked in the table")

        # 2: an unsourced load-bearing claim fails, and the gaps report names
        # the claim rather than only counting it.
        code = run([SOURCED, UNSOURCED])
        if code != 1:
            failures.append(f"an unsourced load-bearing claim exited {code}, want 1")
        report = text(gaps)
        if "UNSOURCED (load-bearing)" not in report:
            failures.append("the gaps report does not flag the unsourced claim")
        if "Most teams never check the edge" not in report:
            failures.append("the gaps report does not name the offending claim")
        if "L2 claim 2" not in report:
            failures.append("the gaps report does not carry the input line number")
        if "**missing**" not in text(table):
            failures.append("the table does not mark the unsourced row")

        # 3: colour is allowed to be unsourced. A gate that fails on context
        # gets every claim marked load-bearing to shut it up.
        if run([SOURCED, COLOUR]) != 0:
            failures.append("an unsourced colour claim failed the gate")
        if "not load-bearing" not in text(gaps):
            failures.append("an unsourced colour claim is not reported at all")

        # 4: a commercial claim with no lever fails — the second measured gap
        # this tool exists for.
        code = run([SOURCED, LEVERLESS])
        if code != 1:
            failures.append(f"a commercial claim with no lever exited {code}, want 1")
        if "COMMERCIAL, NO LEVER" not in text(gaps):
            failures.append("the gaps report does not flag the unnamed lever")

        # 5: a commercial claim marked colour fails too — money is load-bearing
        # by definition, and this is the cheapest way to dodge check 4.
        code = run([SOURCED, LEVERLESS[:-1] + ', "load_bearing": false}'])
        if code != 1:
            failures.append(f"a commercial colour claim exited {code}, want 1")
        if "COMMERCIAL BUT MARKED COLOUR" not in text(gaps):
            failures.append("a commercial claim marked colour is not flagged")

        # 6: a levered claim passes and lands in the ledger with an id, which
        # is what lever-check reads back.
        if run([SOURCED, LEVERED, LEVERED]) != 0:
            failures.append("a fully levered set did not pass")
        entries = [json.loads(line) for line in text(levers).splitlines() if line]
        if [e["id"] for e in entries] != ["C1", "C2"]:
            failures.append(f"ledger ids are not C1..Cn in input order: {entries}")
        if entries and (entries[0]["lever"] !=
                        "keep purge in the free tier and price the audit"
                        or not entries[0]["url"]):
            failures.append("the ledger entry does not carry the lever and source")
        if "C1 keep purge" not in text(table):
            failures.append("the table does not show the lever id")

        # 7: --require-date is off by default and fatal when asked for.
        undated = ('{"claim": "Purge is rate limited to 1000/day", '
                   '"url": "https://docs.example.com/limits", "confidence": "high"}')
        if run([undated]) != 0:
            failures.append("a missing date failed the gate without --require-date")
        if run([undated], ["--require-date"]) != 1:
            failures.append("--require-date did not fail an undated claim")
        if "NO DATE (load-bearing)" not in text(gaps):
            failures.append("--require-date does not name the undated claim")

        # 8: a url that is not http(s) is not a source. Treating it as one is
        # how `www.example.com` and `see the appendix` pass as evidence.
        code = run(['{"claim": "Bare host", "url": "www.example.com", '
                    '"confidence": "high"}'])
        if code != 1:
            failures.append(f"a non-http url exited {code}, want 1")
        if "url is not http(s)" not in text(gaps):
            failures.append("a non-http url is not reported")

        # 9: a malformed date is a gap, not a silent pass into the table.
        if run([SOURCED[:-1].replace('"date": "2026-08-11"', '"date": "Aug 2026"')
                + "}"]) != 0:
            failures.append("a malformed date failed the gate on its own")
        if "date not YYYY-MM-DD" not in text(gaps):
            failures.append("a malformed date is not reported")

        # 10: a pipe in a claim cannot break the table it is rendered into.
        if run(['{"claim": "a | b", "url": "https://example.com/x", '
                '"confidence": "high"}']) != 0:
            failures.append("the escaping fixture did not pass")
        if "| a \\| b |" not in text(table):
            failures.append("a pipe in a claim is not escaped")

        # 11-16: input the tool must refuse outright, exit 2 — a caller must
        # never read 'I could not parse this' as 'your research is fine'.
        for label, lines in (
                ("not JSON", ["{oops"]),
                ("not an object", ['"just a string"']),
                ("empty claim", ['{"claim": "   ", "url": "https://example.com/x"}']),
                ("no claim key", ['{"url": "https://example.com/x"}']),
                ("non-bool commercial",
                 ['{"claim": "x", "url": "https://example.com/x", '
                  '"commercial": "yes"}']),
                ("no claims at all", ["# only a comment"])):
            code = run(lines)
            if code != 2:
                failures.append(f"{label}: exit {code}, want 2")
        if run_cli(["--in", str(home / "gone.jsonl"), "--out", table]) != 2:
            failures.append("an unreadable input did not exit 2")
        if run_cli(["--out", table]) != 2:
            failures.append("a missing --in did not exit 2")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="infile", help="claims JSONL path ('-' for stdin)")
    ap.add_argument("--out", help="markdown table path (default stdout)")
    ap.add_argument("--report", help="gaps report path (default stderr when gaps exist)")
    ap.add_argument("--levers", help="commercial-lever ledger path (JSONL); "
                                     "written whenever given, empty when nothing is tagged")
    ap.add_argument("--title", default="Evidence table", help="H2 heading for the table")
    ap.add_argument("--require-date", action="store_true",
                    help="also fail when a load-bearing claim has no valid date")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=16 failures={len(failures)}")
        return 1 if failures else 0

    # Checked here rather than by argparse's required=True so --self-test
    # needs no other flag.
    if not args.infile:
        print(f"{NAME}: the following arguments are required: --in",
              file=sys.stderr)
        return 2

    try:
        raw = sys.stdin.read() if args.infile == "-" else Path(args.infile).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"source-table: cannot read input: {exc}", file=sys.stderr)
        return 2

    claims = []
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"source-table: line {lineno}: bad JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(obj, dict):
            print(f"source-table: line {lineno}: not a JSON object", file=sys.stderr)
            return 2
        text = str(obj.get("claim") or "").strip()
        if not text:
            print(f"source-table: line {lineno}: empty or missing 'claim'", file=sys.stderr)
            return 2
        if "commercial" in obj and not isinstance(obj["commercial"], bool):
            print(f"source-table: line {lineno}: 'commercial' must be a bool",
                  file=sys.stderr)
            return 2
        obj["_lineno"] = lineno
        claims.append(obj)

    if not claims:
        print("source-table: no claims in input", file=sys.stderr)
        return 2

    rows = []
    gaps: list[str] = []
    ledger: list[dict] = []
    sourced = 0
    unsourced = 0
    missing_conf = 0
    missing_date = 0
    undated_load_bearing = 0
    unnamed_levers = 0

    for i, c in enumerate(claims, 1):
        text = str(c["claim"]).strip()
        url = str(c.get("url") or "").strip()
        date = str(c.get("date") or "").strip()
        conf = confidence_str(c.get("confidence"))
        load_bearing = c.get("load_bearing", True) is not False
        tag = "yes" if load_bearing else "no"
        commercial = c.get("commercial", False) is True
        lever = str(c.get("lever") or "").strip()

        if url and not URL_RE.match(url):
            gaps.append(f"- L{c['_lineno']} claim {i}: url is not http(s): `{esc(url)}`")
            url = ""
        if url:
            sourced += 1
        elif load_bearing:
            unsourced += 1
            gaps.append(f"- L{c['_lineno']} claim {i}: **UNSOURCED (load-bearing)** — {esc(text)}")
        else:
            gaps.append(f"- L{c['_lineno']} claim {i}: unsourced (not load-bearing) — {esc(text)}")
        if not conf:
            missing_conf += 1
            gaps.append(f"- L{c['_lineno']} claim {i}: no confidence — {esc(text)}")
        if date and not DATE_RE.match(date):
            gaps.append(f"- L{c['_lineno']} claim {i}: date not YYYY-MM-DD: `{esc(date)}`")
            date = ""
        if not date:
            missing_date += 1
            if args.require_date and load_bearing:
                undated_load_bearing += 1
                gaps.append(f"- L{c['_lineno']} claim {i}: **NO DATE (load-bearing)** — {esc(text)}")

        if commercial and not load_bearing:
            unnamed_levers += 1
            gaps.append(f"- L{c['_lineno']} claim {i}: **COMMERCIAL BUT MARKED "
                        f"COLOUR** — a claim that moves what the product earns "
                        f"is load-bearing by definition — {esc(text)}")
        if commercial and not lever:
            unnamed_levers += 1
            gaps.append(f"- L{c['_lineno']} claim {i}: **COMMERCIAL, NO LEVER** "
                        f"— name the action this claim implies — {esc(text)}")
        lever_id = ""
        if commercial and lever:
            lever_id = f"C{len(ledger) + 1}"
            ledger.append({"id": lever_id, "lever": lever, "claim": text,
                           "url": url, "date": date, "confidence": conf})

        source = f"[link]({url})" if url else "**missing**"
        rows.append(f"| {i} | {esc(text)} | {source} | {esc(date) or '—'} | "
                    f"{esc(conf) or '—'} | {tag} | "
                    f"{(lever_id + ' ' + esc(lever)).strip() if commercial else '—'} |")

    table = [f"## {args.title}", "",
             "| # | Claim | Source | Date | Confidence | Load-bearing | Commercial lever |",
             "|---|-------|--------|------|------------|--------------|------------------|",
             *rows, ""]
    table_text = "\n".join(table)

    if args.out:
        Path(args.out).write_text(table_text, encoding="utf-8")
    else:
        print(table_text)

    if args.levers:
        Path(args.levers).write_text(
            "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in ledger),
            encoding="utf-8")

    failed = unsourced > 0 or undated_load_bearing > 0 or unnamed_levers > 0
    if gaps:
        report_text = "## Evidence gaps\n\n" + "\n".join(gaps) + "\n"
        if args.report:
            Path(args.report).write_text(report_text, encoding="utf-8")
        else:
            print(report_text, file=sys.stderr)

    print(f"source-table: claims={len(claims)} sourced={sourced} "
          f"unsourced_load_bearing={unsourced} missing_confidence={missing_conf} "
          f"missing_date={missing_date} commercial={len(ledger)} "
          f"unnamed_levers={unnamed_levers} -> {args.out or 'stdout'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
