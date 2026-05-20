---
slug: security-sast
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: SAST analyzes source code before execution to identify vulnerabilities early ("shift-left" security).
content_id: "ab238253e2494d74"
tags: [sast, semgrep, codeql, security, cicd]
---
# Static Application Security Testing (SAST) in CI/CD

## Summary

**One-sentence:** SAST analyzes source code before execution to identify vulnerabilities early ("shift-left" security).

**One-paragraph:** SAST analyzes source code before execution to identify vulnerabilities early ("shift-left" security). Integrate Semgrep, CodeQL, or SonarQube into every PR pipeline and block on CRITICAL+HIGH findings only; expose MEDIUM/LOW as informational at first, then tighten over time.

## Applies If (ALL must hold)

- Any project that ships code to production — SAST is the minimum viable security gate.
- Wiring SAST into a PR check so developers get feedback before merge.
- Custom rule authoring for domain-specific patterns (e.g., hardcoded secrets, SQL interpolation).
- Generating SARIF for GitHub Advanced Security / GitLab Code Quality.

## Skip If (ANY kills it)

- Replacing DAST — SAST cannot find runtime vulnerabilities (auth bypass, business logic, SSRF).
- Greenfield exploration with fluid requirements — false-positive volume will drown the team before rules are tuned.
- One-off scripts or scratch repos — overhead exceeds value.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
