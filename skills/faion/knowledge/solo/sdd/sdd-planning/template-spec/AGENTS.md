# Template: Specification

## Summary

A fill-in-the-blanks template for spec.md — the document that answers "WHAT are we building and WHY?" Sections: Reference Documents, Overview, Problem Statement (Who/Problem/Impact/Solution/Metric), User Personas, User Stories (As a/I want/So that), Functional Requirements table (FR-X with MoSCoW), Non-Functional Requirements table (NFR-X with targets), Acceptance Criteria (Given-When-Then), Out of Scope table, Assumptions and Constraints, and Dependencies.

## Why

Without a standard template, specs written by different agents or humans diverge in structure, omit sections (especially Out of Scope and NFRs), and produce untraceable requirements. A shared template ensures every FR has a US reference, every AC has a Given-When-Then form, and every spec explicitly states what is NOT being built — preventing scope creep when design begins.

## When To Use

- Starting any new feature that will be executed by a subagent — the template enforces the FR/AC structure the executor needs.
- When a stakeholder provides fuzzy requirements and you need a structured artifact to validate understanding.
- Before writing design.md — spec must exist and be approved first.
- Generating spec drafts from user interviews, chat logs, or product briefs.

## When NOT To Use

- Hot-fixes and patches — spec overhead exceeds value for changes under ~2 hours of work.
- Pure infrastructure tasks with no user-facing behavior.
- Research spikes where requirements are deliberately undefined.

## Content

| File | What's inside |
|------|---------------|
| `content/01-template-rules.xml` | Rules for using the template: fill order, required sections, what belongs in spec vs design, MoSCoW on FRs and NFRs, status gate (Draft → Review → Approved before design begins), anti-patterns. |
| `content/02-checklist.xml` | Phase-by-phase checklist for filling each template section with quality gates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Complete spec.md template with all required sections and placeholder text. |
| `templates/spec-trace-check.sh` | Bash script to verify every FR-X referenced in spec has a corresponding US and AC entry. |
