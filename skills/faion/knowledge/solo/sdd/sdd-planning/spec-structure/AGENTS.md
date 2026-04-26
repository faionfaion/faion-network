# Specification Structure

## Summary

Full spec structure v2.0 for features with 3+ user personas or 8+ functional requirements. The spec answers WHAT and WHY — never HOW. Mandatory sections: Overview, Problem Statement, User Personas, User Stories, Functional Requirements (FR-X with SMART criteria and MoSCoW priority), Non-Functional Requirements, Acceptance Criteria (Given-When-Then), Out of Scope, Assumptions, Dependencies. Typical size: 500–1200 tokens.

## Why

Incomplete or ambiguous requirements cause the largest rework in the SDD lifecycle. A structured spec with full FR/AC traceability enables multi-agent executors to verify coverage mechanically (every FR traces to a US, every AC traces to an FR). The two-pass writing process (backbone first, then body) prevents agents from conflating requirements discovery with requirements writing, which produces better-scoped documents.

## When To Use

- Features with 3+ user personas or 8+ functional requirements.
- Features requiring formal stakeholder sign-off where completeness is auditable.
- Complex integrations where NFRs (performance, security, scalability) must be contracted before design begins.
- When the spec feeds into a multi-agent executor pipeline and full FR/AC traceability is required.

## When NOT To Use

- MVP features under 5 FRs — use `spec-examples-basic` condensed format instead.
- Internal tooling or developer-only features where user persona sections add no value.
- Features on a known pattern (nth CRUD endpoint) where all structural decisions are inherited.
- When spec or design doc is still in draft; writing full spec too early wastes tokens when requirements shift.

## Content

| File | What's inside |
|------|---------------|
| `content/01-spec-structure.xml` | Spec v2.0 section-by-section rules; two-pass writing process; document hierarchy table (spec vs design vs impl-plan). |
| `content/02-quality-gates.xml` | Quality gate checklist (Completeness, Clarity, Consistency, Context); common quality failures and fixes; NFR numeric target rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-quality-gate.sh` | Bash script: checks presence of all required spec sections and returns PASS or FAIL with gap list. |
