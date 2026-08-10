#!/usr/bin/env python3
"""
Quota gate — decide GO / HOLD / UNKNOWN before spawning more agents on a long run.

Adapted from victoriafaion's quota-gate (itself adapted from the faion pool's
inline check), with one critical addition this workspace needs: a FRESHNESS
GUARD. The faion statusline writes /tmp/claude-session-state.json only while a
session is actively rendering. During a long idle park (no turns firing) the
file FREEZES — and a frozen value was trusted as live, which once made the pool
sit on a stale "98%" for ~2 days. So: if the source file is older than
--max-age-min, we return UNKNOWN instead of pretending the number is current.

Source resolution (first existing wins):
  1. $CLAUDE_SESSION_STATE                (explicit override)
  2. /tmp/claude-session-state.json       (faion statusline target)
  3. ~/.claude/session-state.json

Expected JSON shape (only the fields used):
  {"rate_limits": {"five_hour":  {"used_percentage": <num>, "resets_at": <epoch?>},
                   "seven_day": {"used_percentage": <num>, "resets_at": <epoch?>}}}

Exit codes (so callers can branch in bash):
  0  GO       — under both thresholds AND source is fresh
  1  HOLD     — at/over a threshold (source fresh); pause spawning, keep ticking
  2  UNKNOWN  — no source, unreadable, or STALE; caller should gate conservatively

Thresholds default to faion's: HOLD if 5h used >= 70% OR 7d used > 94% (the
weekly ceiling is the hard backstop — burning it locks out work for days).
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path


def find_source(explicit):
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    env = os.environ.get("CLAUDE_SESSION_STATE")
    if env:
        candidates.append(Path(env))
    candidates.append(Path("/tmp/claude-session-state.json"))
    candidates.append(Path.home() / ".claude" / "session-state.json")
    for p in candidates:
        try:
            if p.is_file():
                return p
        except OSError:
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=None, help="explicit path to session-state JSON")
    ap.add_argument("--five-hold", type=float, default=70.0)
    ap.add_argument("--seven-hold", type=float, default=94.0)
    ap.add_argument("--max-age-min", type=float, default=15.0,
                    help="source older than this (minutes) -> UNKNOWN (freshness guard). "
                         "0 disables the guard.")
    args = ap.parse_args()

    src = find_source(args.source)
    if src is None:
        print("UNKNOWN no session-state source found. Gate conservatively: "
              "low --cap, heed in-session limit warnings.")
        return 2

    # Freshness guard — the fix this workspace exists for.
    if args.max_age_min > 0:
        try:
            age_min = (time.time() - src.stat().st_mtime) / 60.0
        except OSError as e:
            print(f"UNKNOWN cannot stat {src} ({e}). Gate conservatively.")
            return 2
        if age_min > args.max_age_min:
            print(f"UNKNOWN source {src} is STALE ({age_min:.0f}m old > "
                  f"{args.max_age_min:.0f}m). The statusline hasn't refreshed it — "
                  f"do NOT trust this number. Re-read after a live turn, or gate "
                  f"conservatively (low cap).")
            return 2

    try:
        data = json.loads(src.read_text(encoding="utf-8"))
        rl = data["rate_limits"]
        five = float(rl["five_hour"]["used_percentage"])
        seven = float(rl["seven_day"]["used_percentage"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError) as e:
        print(f"UNKNOWN source {src} present but unreadable/unexpected shape ({e}). "
              f"Gate conservatively.")
        return 2

    hold = five >= args.five_hold or seven > args.seven_hold
    state = "HOLD" if hold else "GO"
    print(f"{state} 5h={five:.0f}% (hold>={args.five_hold:.0f}) "
          f"7d={seven:.0f}% (hold>{args.seven_hold:.0f}) fresh src={src}")
    return 1 if hold else 0


if __name__ == "__main__":
    sys.exit(main())
