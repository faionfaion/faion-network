# Design Document Examples

## Summary

Concrete, worked design document examples for user authentication and related features. Provides a reference AD (Architecture Decision) format with FR traceability tables, file change tables, and component breakdowns that agents use as few-shot structural references when generating or reviewing design.md files.

## Why

Abstract templates alone do not calibrate output quality. Agents injected with a correctly structured example produce designs that match the expected AD format, FR coverage table, and file change table. The authentication example also demonstrates the decision-making narrative: alternatives table with explicit rejection reasons, consequences with trade-offs, and traceability to FR/NFR identifiers.

## When To Use

- Generating a new design.md for a user-identity or auth-related feature — inject the auth example as few-shot context.
- Reviewing a generated design.md for structural gaps — compare AD format, FR coverage, and file table against the example.
- Onboarding a new design-writing agent that needs a calibration reference before its first real feature.
- Teaching the AD alternatives-and-rejection pattern when an agent produces shallow "alternatives" sections.

## When NOT To Use

- Copying example task names, file paths, or technology choices (JWT, bcrypt cost 12) into a real project without checking the constitution — examples encode defaults, not decisions.
- Frontend component hierarchy examples (RegisterForm props) in backend-only or non-React projects.
- Treating example file structures as required layouts rather than illustrative patterns.
- Running examples through automated tooling that expects live code — they are documentation artifacts, not executable code.

## Content

| File | What's inside |
|------|---------------|
| `content/01-auth-design-example.xml` | Full authentication system AD example: email validation, password hashing, token storage, JWT vs session auth, connection pooling — each as a complete AD with context, decision, rationale, alternatives, consequences, and FR traces. |
| `content/02-structure-and-patterns.xml` | File structure table, file change table, FR coverage validator script, rules for using examples as structural references. |

## Templates

| File | Purpose |
|------|---------|
| `templates/fr-coverage-check.py` | Script to verify every FR-X from spec appears in design's FR coverage table. |

## Scripts

none
