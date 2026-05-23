# Junior AI-Overreliance Coaching Guide

## Summary

**One-sentence:** Playbook for senior devs to spot AI-overreliance patterns during reviews/pairings and coach juniors back toward grounded engineering judgment.

**One-paragraph:** Juniors using AI assistants increasingly ship code they don't understand: APIs they never read, libraries they never compared, error handling they never thought about. This methodology gives senior devs a concrete pattern library of overreliance signals (mismatched naming, library-of-the-day, undefended exception flow, copy-pasted prompt artifacts), a coaching conversation script that doesn't shame, and a delta-style review comment format that teaches. Primary output: PR comments and pairing notes that move the junior from "AI suggested this" to "I chose this because…".

**Ефективно для:**

- PR review коли junior pull-request виглядає 'занадто рівно' — багато patterns одночасно без обґрунтування.
- Pairing-сесії, де junior копіює AI-вихід без переказу 'що це робить'.
- Виявлення library-of-the-day: вибрана незнайома команді бібліотека без compare-rationale.
- Coaching без shaming: дельта-формат review-коментарів ('я б очікував', 'що про X').

## Applies If (ALL must hold)

- Junior dev (≤2 years) actively uses AI assistant (Copilot / Claude / Cursor) on production code.
- Senior is responsible for the junior's PRs / pairing growth.
- Codebase has consistent conventions the AI does not always honor.
- Recent PRs show signal of overreliance (e.g. style break, unfamiliar lib, no error handling).

## Skip If (ANY kills it)

- Junior is already evaluating AI suggestions critically (cite reasons, compare APIs) — apply normal review.
- Code is genuinely written by senior + AI is editor-only autocomplete — no overreliance risk.
- Senior lacks bandwidth for coaching — flag to manager, do not silently rewrite.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | git diff | GitHub/GitLab |
| Junior context | tenure + AI tools used | team page |
| Project conventions | CONTRIBUTING.md / lint rules | repo |

## Assumes Loaded

none — methodology is self-contained.

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: signal-six-patterns, ask-not-tell, graduated-intervention, what-without-ai, no-rewrite-without-explanation | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for playbook-step + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan-pr-for-signals` | sonnet | Pattern detection across diff. |
| `draft-delta-comment` | opus | Tone + framing decisions are high-judgment. |
| `detect-shaming-phrases` | haiku | Mechanical regex against shame-vocabulary list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-coaching-comment.md` | Delta-format PR coaching comment template (one signal per bullet, one what-without-AI question) |
| `templates/_smoke-test.md` | Minimal viable filled-in version of pr-coaching-comment.md |
| `templates/six-signals-checklist.md` | Quick scan checklist mapping diff observations → named signal |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-junior-ai-overreliance-coaching-guide.py` | Validate the coaching artefact against the schema | Pre-commit when committing review templates |

## Related

- [[junior-ai-pairing-protocol]]
- [[java-spring-boot]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
