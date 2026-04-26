# Code Review Cycle

## Summary

A structured human-AI collaboration for code review running as a 3-step pipeline: (1) AI pre-screen flags style, anti-patterns, and missing tests; (2) parallel review agents (Claude + cross-model) produce structured BLOCK/WARN/NOTE finding lists; (3) a merge step deduplicates findings and produces a unified report. Humans address BLOCK items; reflexion feeds review findings back into `patterns.md` and `mistakes.md`. AI assists but never replaces human judgment on business logic, architecture decisions, and security context.

## Why

Over 30% of senior developers now ship mostly AI-generated code, and PRs are 18% larger on average. Change failure rates increase 30% when AI output exceeds human verification capacity. AI pre-screening cleans up style issues before human review, reducing review fatigue. A separate review model catches blind spots the generation model cannot — the model that wrote the code is unreliable for reviewing its own output.

## When To Use

- After any SDD task execution, before marking the task done — run AI pre-screen + human spot-check
- When PRs consistently exceed 300 lines — AI pre-review reduces noise before human review
- Setting up a multi-model review pipeline (write with Claude, review with a separate model)
- Integrating SDD reflexion: post-review findings feed into `patterns.md` and `mistakes.md`
- After detecting a spike in change failure rates — add AI review as a quality gate in CI/CD

## When NOT To Use

- Single-file configuration changes — linter is sufficient
- Trivial one-line bug fixes — peer review + merge is faster
- First pass in a new codebase where patterns are not yet established — establish patterns first
- When the human reviewer has deep domain knowledge and AI review produces high false positives

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Review type taxonomy, AI assistance levels (L1/L2/L3), multi-model strategy, AI tool comparison table |
| `content/02-workflow.xml` | Step-by-step review pipeline, SDD integration (task completion checkpoints), reflexion learning loop |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-review.txt` | Prompts for AI pre-screen, independent code review, and finding merge/deduplication |
