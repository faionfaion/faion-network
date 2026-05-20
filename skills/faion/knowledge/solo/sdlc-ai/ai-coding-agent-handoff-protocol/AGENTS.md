---
slug: ai-coding-agent-handoff-protocol
tier: solo
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Spec → AI-agent task → human review discipline that stops vibe-coded breakage by enforcing a written hand-off contract, a bounded change scope, and a mandatory diff-review gate before merge.
content_id: 0dee031f6876288f
---

# AI Coding Agent Handoff Protocol

## Summary
A protocol for solo SaaS builders working with Claude Code / Cursor / Copilot agents that turns "vibe coding" into a repeatable spec → agent → review loop. Outcome: every agent-authored change starts from a written spec, ships within an explicit scope fence, and is gated by a human diff review before merge — so production never receives a change the human did not at least skim.

## Applies If
- You use a coding agent (Claude Code, Cursor, Copilot) for non-trivial changes
- You are the sole reviewer of your code (no other engineer to catch agent drift)
- You have shipped at least one agent-induced bug to production
- You work on a codebase with users / revenue / compliance stakes

## Skip If
- You are exploring throwaway prototypes with no production target
- You have a second engineer who reviews every PR (use standard PR rubric)
- The change is a one-off script you will delete before end of day
- You have not yet used an AI coding agent (start with pair-with-ai-agent-protocol first)

## Content
See `content/01-core-rules.xml`.

## Related
- [[pair-with-ai-agent-protocol]]
- [[ai-prompt-as-commit-artifact]]
- [[context-window-curation-for-coding-agents]]
- [[ai-over-reliance-self-audit]]
