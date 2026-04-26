# BA Strategic Partnership

## Summary

A per-artifact stance reviewer that scores requirements documents on six axes (problem_clarity, outcome_orientation, evidence_grounding, enterprise_scope, partner_voice, kill_criterion) and rewrites order-taker language as outcome statements tied to a named OKR. Auto-blocks any artifact where any axis scores below 2 or kill_criterion scores below 1. This is a per-engagement behavior pattern — run it at intake and at spec-review gates, not as a quarterly portfolio loop.

## Why

BAs who accept requirements as-stated ("please add X") produce features disconnected from business outcomes. A lint-style rubric applied mechanically — quoting the order-taker phrase verbatim, classifying the failure mode, proposing a rewrite tied to a real OKR — shifts the BA posture without relying on individual judgment or managerial feedback cycles.

## When To Use

- Intake of a new requirement or "can you just add X" request — reframe as outcome before scope is locked
- Re-reading an existing requirements doc, user story, or PRD to detect order-taker language
- Onboarding a junior BA: run the stance rubric on their last 5 artifacts and produce coaching deltas
- Pre-meeting framing for stakeholder calls: draft 3 strategic questions to ask before accepting the stated requirement
- Spec review gate before a ticket goes to engineering — block if no problem statement, no outcome metric, no kill criterion

## When NOT To Use

- Quarterly portfolio-level opportunity mining — use the sibling `business-analyst/ba-strategic-partnership/`
- Modeling work (BPMN, use-case decomposition, traceability matrices) — wrong tool
- Live stakeholder dialogue — agent prepares, never speaks for the BA
- Trivial maintenance tickets (copy edits, dependency bumps) — overhead not justified

## Content

| File | What's inside |
|------|---------------|
| `content/01-stance-rubric.xml` | Six axes with scoring definitions, auto-block threshold, order-taker phrase patterns to scan for |
| `content/02-agentic.xml` | Stance-reviewer and intake-framer prompt patterns, subagents, AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/stance-review-schema.json` | Canonical JSON schema for stance reviewer output with auto-block logic |
| `templates/ba-frame.sh` | One-liner CLI: turns a stakeholder ask into 3 framing questions + strawman outcome |
