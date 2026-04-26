# Golden-Master Corpus for AI-Driven Legacy Rewrites

## Summary

When you ask a coding agent to rewrite a 5000-line legacy module, you have no spec — you have *current behaviour*. Capture inputs and outputs of the current implementation from production traffic, fixtures, or a fuzzer into a committed corpus of `(input, expected_output)` pairs; the agent's rewrite passes only when it reproduces every pair, byte-for-byte, or each diff is explicitly approved row-by-row. This is the only test that scales to AI-driven rewrites of untested legacy: it is the spec the legacy never had, captured automatically, and it gives the agent a deterministic GREEN signal that does not depend on human ability to read the old code.

## Why

Legacy code's "spec" is its observed behaviour, including its bugs. Hand-written unit tests around legacy ossify the developer's *interpretation* of behaviour, so they miss exactly the edge cases the agent will trip over. A golden-master corpus encodes behaviour empirically: capture once, replay forever. The diff workflow forces every behavioural change to be *named* — either an accepted bugfix or an unintended regression. Without it, agents tend to "tidy" semantics silently, and untested legacy leaves no way to catch the drift before production. The pattern predates LLMs (Michael Feathers, "Working Effectively with Legacy Code") but becomes load-bearing when the rewrite author is an agent with no domain memory.

## When To Use

- Rewriting a legacy module/service with poor or no test coverage that an agent will touch.
- Cross-language ports (Python → Rust, PHP → Go) where preserving exact output is the success criterion.
- Library upgrades where vendor changelogs hint at behavioural shifts (date parsing, timezone, locale).
- Any "I don't trust the existing tests but I do trust production" rewrite.
- Refactoring a deterministic transformer (parser, formatter, exporter) under agent control.

## When NOT To Use

- Greenfield code with no prior behaviour to preserve — write unit tests against the spec instead.
- Pervasive nondeterminism without normalization (timestamps, UUIDs, random IDs, ORDER BY-less queries).
- Tiny modules under ~200 LOC where targeted unit tests are cheaper than capture infrastructure.
- Stateful interactive flows (UI, multiplayer game tick) where I/O shape isn't a function of input alone.

## Content

| File | What's inside |
|------|---------------|
| `content/01-capture-corpus.xml` | How to capture the corpus from production traffic, fixtures, or a fuzzer; normalization rules. |
| `content/02-replay-and-diff-gate.xml` | The replay test, byte-for-byte assertion, and the row-by-row diff approval workflow. |

## Templates

| File | Purpose |
|------|---------|
| `templates/golden_master_test.py` | Pytest replay test asserting parity over a JSONL corpus. |
| `templates/capture_corpus.py` | Capture script that wraps the legacy callable, normalizes IDs/timestamps, writes JSONL. |
