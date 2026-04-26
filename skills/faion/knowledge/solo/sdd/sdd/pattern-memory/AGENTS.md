# Pattern Memory

## Summary

A system for capturing, storing, and retrieving proven solutions from development sessions so LLM agents apply consistent patterns across tasks and projects. Patterns are stored in `.aidocs/memory/patterns.md` with a confidence score (0.5 initial → 0.9+ proven), graduated by number of successful uses. High-confidence patterns (0.8+) are synced to `CLAUDE.md` for immediate availability in new sessions. The rule: capture when a non-obvious solution works in 2+ distinct contexts; never capture obvious best practices or one-off fixes.

## Why

Each task session starts fresh. Without an explicit pattern store, agents rediscover the same solutions independently, producing divergent naming conventions, inconsistent error handling, and duplicated utilities. Hierarchical memory (working → session → project → global) manages context limits while preserving cross-task learning. The Reflexion paper (Shinn et al., 2023) demonstrates that verbal reinforcement via retained examples measurably improves agent reliability on subsequent similar tasks.

## When To Use

- After a successful task execution where a non-obvious solution was applied — capture before the session ends
- When the same problem appears for the second time in a different context — that is a pattern, not a one-off
- Before starting a new task wave — inject high-confidence patterns (0.8+) into the task context header
- During CLAUDE.md maintenance: sync established patterns (0.9+) into the project rules file
- When onboarding a new agent session that lacks project history — load `patterns.md` as working memory

## When NOT To Use

- Capturing well-known best practices already in framework docs (e.g., "use async/await")
- One-off fixes specific to a single file or edge case
- Patterns with confidence below 0.5 (only one use, unverified) — capture as candidate, do not promote
- Project-specific configuration values (API keys, URLs) — those go in `.env`, not patterns

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | What a pattern is vs a code snippet; confidence levels; capture triggers; memory architecture |
| `content/02-lifecycle.xml` | Pattern discovery → capture → validation → establishment → maintenance; scoring formula; CLAUDE.md sync rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-entry.md` | Full PAT-XXX entry template with problem, solution, confidence, provenance |
| `templates/pattern-minimal.md` | Minimal quick-capture template for use during execution |
| `templates/patterns-file.md` | Structure for the main `.aidocs/memory/patterns.md` file |
| `templates/mistakes-file.md` | Structure for `.aidocs/memory/mistakes.md` anti-patterns log |
| `templates/prompt-extract.txt` | Prompts for post-task pattern extraction and periodic review |
| `templates/sync-patterns.sh` | Shell script syncing high-confidence patterns to CLAUDE.md |
