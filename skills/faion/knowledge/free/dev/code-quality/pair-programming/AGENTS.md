# Pair Programming

## Summary

A practice where two developers share a single workstation — one drives (types), one navigates (reviews and steers). Roles switch every 15–30 minutes. Three main styles: driver-navigator (classic), ping-pong (TDD-alternating), strong-style (navigator must verbalize every idea before it reaches the keyboard). With agents the same styles apply; the style must be declared explicitly at session start.

## Why

Studies show pair programming reduces bug escape rates, accelerates knowledge transfer, and lowers bus-factor risk. The navigator catches errors in real time that would otherwise survive to review. Strong-style pairing is particularly effective for onboarding and for preventing a solo agent from silently over-engineering.

## When To Use

- Complex or unfamiliar code where a second perspective catches assumptions.
- Knowledge transfer: onboarding a new team member or cross-training on an unfamiliar module.
- Critical business logic that benefits from real-time review.
- Debugging a hard-to-reproduce issue.
- Agent acting as navigator: rubber-duck escalation with questions and edge-case prompts.
- TDD ping-pong: agent writes one failing test, human makes it pass, human writes next test.

## When NOT To Use

- Simple, well-specified, mechanical tasks — agent is overhead; delegate directly.
- Tasks where deliberate struggle is the goal (interview prep, learning by doing) — agent removes useful friction.
- Regulatory code requiring two human sign-offs; agent can advise but cannot fill the human-approver role.
- Long architectural debates — agent sycophantically agrees; use `faion-brainstorm` instead.
- Sessions longer than 90–120 minutes without breaks; context degrades for both agent and human.

## Content

| File | What's inside |
|------|---------------|
| `content/01-styles.xml` | Driver-navigator, ping-pong, strong-style, tour-guide: rules, flow, best-for. |
| `content/02-agent-workflow.xml` | Agent-specific rules: declare style upfront, session journal, gotchas (sycophancy, scope creep, strong-style violation). |

## Templates

| File | Purpose |
|------|---------|
| `templates/strong-style-prompt.txt` | System prompt constraining agent to navigator-only (no Edit/Write tools). |
| `templates/pingpong-prompt.txt` | TDD ping-pong entry prompt with turn-tracking rules. |
| `templates/pair-journal.sh` | Session journal script that survives agent compaction. |
