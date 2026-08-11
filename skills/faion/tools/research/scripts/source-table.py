#!/usr/bin/env python3
"""source-table.py — turn a JSONL of research claims into a markdown evidence
table plus a gaps report, and fail the run when a load-bearing claim carries
no source.

Input JSONL, one object per line:
    {"claim": "...", "url": "https://...", "date": "2026-08-11",
     "confidence": "high", "load_bearing": true}
  - claim       required, non-empty string
  - url         optional in the schema, REQUIRED for a load-bearing claim
  - date        optional, YYYY-MM-DD (anything else is reported as a gap)
  - confidence  optional string (high/medium/low) or number 0..1
  - load_bearing  optional bool, default true — set false for colour/context

Output: markdown table to --out (default stdout), gaps report to --report,
        one summary line on stdout.
Exit:   0 every load-bearing claim sourced · 1 at least one unsourced ·
        2 unreadable or malformed input.

Why: a research arm that cites nothing loses to one that cites everything.
The measured gap on the run this encodes was 108 sourced URLs against 0.
Zero model calls.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="infile", required=True, help="claims JSONL path ('-' for stdin)")
    ap.add_argument("--out", help="markdown table path (default stdout)")
    ap.add_argument("--report", help="gaps report path (default stderr when gaps exist)")
    ap.add_argument("--title", default="Evidence table", help="H2 heading for the table")
    ap.add_argument("--require-date", action="store_true",
                    help="also fail when a load-bearing claim has no valid date")
    args = ap.parse_args()

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
        obj["_lineno"] = lineno
        claims.append(obj)

    if not claims:
        print("source-table: no claims in input", file=sys.stderr)
        return 2

    rows = []
    gaps: list[str] = []
    sourced = 0
    unsourced = 0
    missing_conf = 0
    missing_date = 0
    undated_load_bearing = 0

    for i, c in enumerate(claims, 1):
        text = str(c["claim"]).strip()
        url = str(c.get("url") or "").strip()
        date = str(c.get("date") or "").strip()
        conf = confidence_str(c.get("confidence"))
        load_bearing = c.get("load_bearing", True) is not False
        tag = "yes" if load_bearing else "no"

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

        source = f"[link]({url})" if url else "**missing**"
        rows.append(f"| {i} | {esc(text)} | {source} | {esc(date) or '—'} | "
                    f"{esc(conf) or '—'} | {tag} |")

    table = [f"## {args.title}", "",
             "| # | Claim | Source | Date | Confidence | Load-bearing |",
             "|---|-------|--------|------|------------|--------------|",
             *rows, ""]
    table_text = "\n".join(table)

    if args.out:
        Path(args.out).write_text(table_text, encoding="utf-8")
    else:
        print(table_text)

    failed = unsourced > 0 or undated_load_bearing > 0
    if gaps:
        report_text = "## Evidence gaps\n\n" + "\n".join(gaps) + "\n"
        if args.report:
            Path(args.report).write_text(report_text, encoding="utf-8")
        else:
            print(report_text, file=sys.stderr)

    print(f"source-table: claims={len(claims)} sourced={sourced} "
          f"unsourced_load_bearing={unsourced} missing_confidence={missing_conf} "
          f"missing_date={missing_date} -> {args.out or 'stdout'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
