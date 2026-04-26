# Specification Examples: Basic

## Summary

Condensed spec format for MVP features with clear, well-understood requirements. Reduces the full spec-structure v2.0 to five minimum sections: Problem Statement, User Stories (max 3), Functional Requirements (Must only), Acceptance Criteria (1 happy path + 1 error), Out of Scope. Typical size: 1100–1650 tokens.

## Why

Full spec-structure v2.0 adds overhead (detailed personas, NFR tables, open questions) that is unjustified for simple CRUD operations or well-known patterns. The condensed format preserves traceability (FR → US → AC) while eliminating sections that carry no new information at MVP scope. Because the condensed spec fits in 1-2k tokens, agents can include it in full context without budget pressure.

## When To Use

- MVP features with clear requirements (≤ 5 FRs, ≤ 3 User Stories).
- Simple CRUD operations or well-known patterns (auth, registration, forms).
- Small team, fast iteration environment.
- Proof of concept or rapid prototyping.

## When NOT To Use

- Features with multiple user personas and complex business rules — use `spec-structure` full v2.0 instead.
- Regulated domains (payments, healthcare, legal) where traceability completeness is non-negotiable.
- Features with more than 5 User Stories or 10 Functional Requirements.
- Security-sensitive features where at least an unauthorized-access AC is required (condensed ACs are too thin).

## Content

| File | What's inside |
|------|---------------|
| `content/01-condensed-spec.xml` | Complete authentication example as a condensed spec; rules for what to include and skip; token estimation table. |
| `content/02-writing-rules.xml` | Rules for concise FR language, traceability, AC format, Out of Scope discipline; antipatterns to reject. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-size-check.sh` | Bash script: counts US, FR, AC in a spec file and warns when counts exceed condensed-format thresholds. |
