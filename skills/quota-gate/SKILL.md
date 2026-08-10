---
name: quota-gate
description: >-
  Check rate-limit headroom before spawning agents on a long/batch run so a pool or fan-out
  doesn't burn the 5-hour or weekly ceiling. Use when running the ultimate-guide v8 pool, any
  multi-agent fan-out, or a long autonomous loop, and when the user asks "перевір квоту",
  "quota check", "are we close to the limit", "do we have headroom before I batch this".
  Returns GO / HOLD / UNKNOWN as an exit code. Has a FRESHNESS GUARD: a stale session-state
  file (statusline frozen during idle) returns UNKNOWN instead of trusting a possibly-frozen
  number — the fix for the time the pool sat on a stale "98%" for ~2 days.
---

# Quota Gate

A small dependency-free check that keeps long runs from exhausting the account rate limit.
Mirrors the faion pool's inline check, packaged as a script with exit codes, **plus a freshness
guard** this workspace specifically needs.

## Use it

```bash
python3 ~/.claude/skills/quota-gate/scripts/quota_gate.py; rc=$?
# rc=0 GO       dispatch normally
# rc=1 HOLD     at/over a threshold -> skip spawning this tick, keep the loop alive
# rc=2 UNKNOWN  no source / unreadable / STALE -> gate conservatively (low cap, heed warnings)
```

Thresholds match faion (override with flags): HOLD when **5-hour used ≥ 70%** OR **7-day used
> 94%**. The weekly ceiling is the hard backstop — burning it locks out work for days, so it
gates tighter. Override: `--five-hold`, `--seven-hold`.

## The freshness guard (why this version exists)

The faion statusline writes `/tmp/claude-session-state.json` only **while a session is actively
rendering**. During a long idle park (no turns firing) the file FREEZES. Trusting a frozen value
once made the pool sit on a stale `98%` for ~2 days. So the gate now checks the source's mtime:

- source older than `--max-age-min` (default **15** min) → **UNKNOWN**, "do not trust this number".
- On UNKNOWN, re-read after a live turn (a tool call refreshes the statusline), or gate
  conservatively (low cap). Pass `--max-age-min 0` to disable the guard.

This is the single concrete improvement over the source skill, which trusted the file's value
regardless of age.

## Source resolution

Reads, first existing wins: `$CLAUDE_SESSION_STATE` → `/tmp/claude-session-state.json` (the
faion statusline target on this machine) → `~/.claude/session-state.json`. JSON shape used:

```json
{"rate_limits": {"five_hour": {"used_percentage": 64}, "seven_day": {"used_percentage": 12}}}
```

## Where it's used

The ultimate-guide v8 pool tick should call this before each dispatch wave (gate-before-spawn,
rule 4 of `references/orchestration-doctrine.md`). Any future fan-out / autonomous-loop calls it
the same way.

## Related

- `references/orchestration-doctrine.md` — the four token-discipline rules for fan-out work
  (file-reference dispatch, thin orchestrator, bounded worker reports, gate-before-spawn).
- Memory `claude-quota-state-file`, `weekly-quota-throttle`, `quota-already-restored`.
