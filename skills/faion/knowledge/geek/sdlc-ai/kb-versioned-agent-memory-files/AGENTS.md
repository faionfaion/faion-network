# Versioned Agent-Memory Files (decisions / patterns / mistakes)

## Summary

Persist long-term agent memory as four committed Markdown files in `.aidocs/memory/` (or `.product/memory/`): `decisions.md` (key technical choices), `patterns.md` (proven implementations), `mistakes.md` (errors and the fix), and `session.md` (in-flight state). Every entry is appended (never edited or auto-overwritten by an LLM), every entry carries a date and a citation back to the commit, ticket, or transcript that produced it. Agents read the four files at session start; `session.md` is the only file that resets between sessions. The convention turns "agent memory" from a vendor-specific RAG black box into a reviewable, diff-able, code-reviewed artifact.

## Why

Vendor "memory" features (ChatGPT memory, Cursor memories, Devin knowledge) are opaque, non-portable, and silently rewrite themselves; they fail the basic SDLC requirement that any artifact driving production behaviour be code-reviewed. Committing memory as plain Markdown solves all three: portable across agent kinds (Claude Code, Codex, Cursor, aider read the same files), reviewable in PR diffs, and stable across forks. The four-file split (decisions / patterns / mistakes / session) maps to the empirical question categories agents need at session start: "what was already decided", "what works here", "what to avoid", "where am I right now" — and prevents the single-file failure mode where everything becomes a 5000-line Notion-export blob.

## When To Use

- Long-lived projects (>3 months) where agent context resets every session and rebuilds from scratch.
- Multi-agent setups (Claude Code + Codex + autoheal cron) that must share institutional knowledge.
- Teams where a human reviewer should approve every change to "what the agent believes about this codebase".
- Replacing vendor-specific memory features whose contents you cannot inspect or version.

## When NOT To Use

- One-shot agent invocations or short-lived feature branches — the four-file overhead is wasted.
- Highly volatile prototypes where today's "decision" is tomorrow's discard.
- Non-deterministic transient state (queue depths, in-flight ticket IDs) — those belong in a runtime store, not in versioned memory.

## Content

| File | What's inside |
|------|---------------|
| `content/01-four-file-split.xml` | The mandatory four-file split, the append-only rule, and the citation-required rule. |
| `content/02-session-reset-rule.xml` | How `session.md` resets between sessions and why the other three never do. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decisions.md` | Skeleton with one example entry and the required header schema. |
| `templates/patterns.md` | Skeleton for proven-implementation entries. |
| `templates/mistakes.md` | Skeleton for error-and-fix entries. |
| `templates/session.md` | Skeleton for in-flight state. |
