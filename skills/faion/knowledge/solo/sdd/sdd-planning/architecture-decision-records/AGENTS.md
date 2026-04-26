# Architecture Decision Records (ADR)

## Summary

A single-file document (Nygard format) that captures one architectural decision — its context, the decision made, alternatives considered with rejection reasons, and consequences (positive, negative, neutral). ADRs live in `docs/adr/NNN-title.md`, are numbered sequentially from 001, and transition through statuses: Proposed → Accepted → Deprecated/Superseded. New ADRs amend, never edit, existing Accepted ones.

## Why

Architecture decisions made today are invisible to new team members and to agents working months later. Without ADRs, the same debates recur; production incidents lack design context; and agents generating new code may contradict existing architectural choices they cannot see. Storing ADRs co-located with code in version control gives agents file-system access to the full decision history during code generation and review.

## When To Use

- Before committing to a tech stack choice that will be hard to reverse (database, framework, auth strategy).
- After a production incident that exposes a design weakness — capture the fix decision.
- Anytime two or more viable alternatives were seriously considered.
- At the start of a new feature with meaningful architectural surface (new service, new API contract, new data model).

## When NOT To Use

- Trivial implementation details (which library function to call, naming conventions).
- Decisions that will certainly be revisited within 1-2 weeks — too early, no context yet.
- Configuration values that belong in docs, not decision records.
- When there was only one realistic option — no choice means no ADR needed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-adr-format.xml` | Nygard format sections (Context, Decision, Alternatives, Consequences); status lifecycle; best practices (immutable by default, active voice, under 400 words); antipatterns. |
| `content/02-agentic-workflow.xml` | Agent workflow for writing ADRs from spec/design context; "Proposed" gate rule; ADR compliance review pattern; gotchas (hallucinated alternatives, immutability, index cost). |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-template.md` | Nygard ADR skeleton with all required sections and field descriptions. |
| `templates/adr-status.sh` | Bash script: lists all ADRs in docs/adr/ with their status line for quick index review. |
