# Extreme Programming (XP)

## Summary

Agile methodology built on 5 values (communication, simplicity, feedback, courage, respect) and 12 practices (TDD, pair programming, collective ownership, CI, small releases, YAGNI). The concrete rule: if a practice is good, take it to its logical extreme — if testing is good, test everything first (TDD); if reviews help, review all code via pairing. "Done" means: tests pass, no TODOs, CHANGELOG updated.

## Why

XP produces high code quality by closing the feedback loop at every level: unit tests catch regressions in seconds, CI catches integration issues in minutes, small releases catch product misalignment in days. The AI-era adaptation treats Claude as navigator in Red-Green-Refactor: human writes the failing test, Claude proposes the minimal green implementation, human approves the refactor.

## When To Use

- Solo developer using Claude as the pair — TDD, simple design, small releases map cleanly to agentic loops
- Small team (2-12) with churning requirements where customer feedback is accessible
- Greenfield product where coding standards and CI can be enforced from day one
- Codebases that already have high test coverage (XP feedback loops only work with a fast, trusted suite)

## When NOT To Use

- Compliance-heavy domains (medical, aerospace) requiring big upfront design and signed change controls
- Distributed async-only teams unable to do real-time pairing or daily sync (use Kanban/async Scrum)
- Projects without an accessible customer or PM proxy (on-site customer practice collapses)
- Maintenance-mode systems where pace is dictated by external SLAs, not iterations

## Content

| File | What's inside |
|------|---------------|
| `content/01-practices.xml` | 12 XP practices with descriptions; simple design rules; planning game format; CI rules |
| `content/02-solo-and-ai.xml` | Solo XP adaptations; AI-as-pair pattern; agentic TDD workflow; gotchas for LLM pairing |

## Templates

| File | Purpose |
|------|---------|
| `templates/xp-navigator-prompt.txt` | Red-Green-Refactor prompt for Claude-as-navigator pairing session |
| `templates/pre-push-hook.sh` | Pre-push hook enforcing "never break the build" (pytest + ruff) |
