# Code Review Basics

## Summary

A structured approach to examining code changes before merge: reviewer reads the diff plus touched files, categorizes findings using Conventional Comments labels (blocking/suggestion/nit/question/praise), and emits at most 20 comments prioritized correctness → security → maintainability → nits. PR size cap: 400 changed lines. Agent is never the sole approver on a merge to main.

## Why

Empirical studies (SmartBear) confirm that code review quality degrades past 400 LoC and 60 minutes. Conventional Comments labels let authors distinguish blockers from nits without ambiguity. Running linters/tests before the agent review eliminates duplicate findings and focuses LLM judgment on what static analysis cannot catch.

## When To Use

- Pre-review pass on every PR before a human reviewer is assigned.
- Self-review automation for agent-authored diffs before pushing.
- Mentoring junior contributors: agent leaves educational comments with explanations.
- Bulk review of mechanical PRs (dependabot, renovate) where breaking-change risk varies.

## When NOT To Use

- Architecture/design PRs needing product context the agent does not have — humans only.
- Security-sensitive merges where regulatory sign-off (PCI, HIPAA) is required — agent advises but cannot approve.
- Trivial single-line fixes already covered by lint + CI — agent comment is noise.
- Repos where rubber-stamping is already the failure mode — adding another approval signal worsens it.

## Content

| File | What's inside |
|------|---------------|
| `content/01-checklist.xml` | Six review dimensions: correctness, design, maintainability, testing, performance, security — each with concrete checks. |
| `content/02-comments.xml` | Conventional Comments label rules, good/bad examples per label, reviewer and author dos/don'ts, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-context.sh` | Fetch PR metadata, changed files, failing CI checks, and diff (truncated) for the agent. |
| `templates/review-prompt.txt` | Agent prompt: diff-scoped comments, Conventional Comments labels, max 20, JSON output. |
