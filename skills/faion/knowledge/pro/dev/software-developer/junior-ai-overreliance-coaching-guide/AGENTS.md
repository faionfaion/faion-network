---
slug: junior-ai-overreliance-coaching-guide
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A playbook for senior devs to spot AI-overreliance patterns during PR reviews and pairings, and to coach juniors back toward grounded engineering judgment.
content_id: "a590e66f852832d6"
tags: [mentorship,ai-assisted,review,pairing,junior,critical-thinking]
---
# Junior AI-Overreliance Coaching Guide

## Summary

**One-sentence:** A playbook for senior devs to spot AI-overreliance patterns during PR reviews and pairings, and to coach juniors back toward grounded engineering judgment.

**One-paragraph:** Juniors using AI assistants increasingly ship code they don't understand: APIs they never read, libraries they never compared, error handling they never thought about. This methodology gives senior devs a concrete pattern library of overreliance signals (mismatched naming, library-of-the-day, undefended exception flow, copy-pasted prompt artifacts, no-comment integration), a coaching conversation script that doesn't shame, and a delta-style review comment format that teaches. Mechanism: 6 detectable patterns, a "what-would-you-do-without-AI" conversation prompt, and a graduated intervention ladder (acknowledge → ask → block → escalate). Primary output: PR comments and pairing notes that move the junior from "AI suggested this" to "I chose this because…".

## Applies If (ALL must hold)

- team has ≥ 1 senior dev reviewing junior PRs
- juniors use Copilot / Cursor / Claude Code / similar AI assistants
- team has observed ≥ 1 incident traceable to undefended AI-generated code
- senior dev has bandwidth for occasional 30-min pairing sessions
- code review culture is established (not "approve and merge")

## Skip If (ANY kills it)

- single-dev team (no junior to coach)
- juniors don't use AI assistants — different coaching gap
- pure AI-prohibited environment (regulated industry) — escalate to policy
- team lead doesn't value engineering judgment over throughput
- juniors have &gt; 5 years experience labeled "junior" — title mismatch, not AI issue

## Prerequisites (must be true before starting)

- documented PR review norms in the team
- pairing slot calendar (recurring or ad-hoc)
- access to junior's PRs over last 4 weeks (pattern detection baseline)
- agreed-upon "coaching not punishing" tone with team lead
- escalation path to engineering manager when behavior persists

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/code-review-feedback` | Foundation for the coaching tone |
| `pro/dev/software-developer/refactoring-decisions` | Reference for "what to defend" in code |
| `geek/ai/claude-code/responsible-ai-usage` | Optional team-level usage policy |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pattern library, ask-not-tell, what-would-you-do-without-AI, delta review, escalation ladder | ~1000 |
| `content/02-output-contract.xml` | essential | Pairing note schema, PR comment format, escalation log | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (shaming, gaslighting, over-coaching, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pr_pattern_detector` | sonnet | Find AI-overreliance signals in diff |
| `comment_draft_in_voice` | sonnet | Tone-matched coaching comment |
| `pairing_outline_draft` | sonnet | 30-min session structure |
| `escalation_writeup` | sonnet | Manager escalation note when behavior persists |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-coaching-comment.md` | Delta-style coaching comment skeleton |
| `templates/pairing-session-script.md` | 30-min pairing outline |
| `templates/escalation-note.md` | Manager-level escalation when needed |
| `templates/pattern-library.md` | The 6 overreliance signals with examples |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/detect-ai-overreliance.py` | Scan PRs for the 6 signals | Pre-review |
| `scripts/coaching-progress-tracker.py` | Track per-junior signal-rate over time | Monthly review |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodology: `code-review-feedback`, `refactoring-decisions`
- external: [GitHub Copilot best practices](https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot) · [Codermetrics — engineering judgment](https://martinfowler.com/articles/codermetrics.html)
