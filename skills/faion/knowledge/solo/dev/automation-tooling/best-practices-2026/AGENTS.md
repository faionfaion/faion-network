---
slug: best-practices-2026
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Concrete 2026 baseline for TypeScript 5, React 19, Next.
content_id: "9d51bb92a40a964e"
tags: [typescript, react, python, code-quality, ai-assisted-dev]
---
# Software Development Best Practices 2026

## Summary

**One-sentence:** Concrete 2026 baseline for TypeScript 5, React 19, Next.

**One-paragraph:** Concrete 2026 baseline for TypeScript 5, React 19, Next.js 15, Python 3.13, and AI-assisted development. Provides triggers, checklists, paste-ready configs, and a verification procedure so an autonomous agent can audit or modernize a project without further guidance.

## Applies If (ALL must hold)

- Auditing whether a project's stack aligns with current standards (TS version, eslint config, Python tooling).
- Generating the standards section of CONTRIBUTING.md or AGENTS.md for a new project.
- Choosing which React 19 / Next.js 15 / Python 3.13 features to adopt in a modernization sprint.
- Defining an AI-assisted dev playbook: tool selection, prompt patterns, AI test generation guardrails.
- Reviewing a PR that touches tsconfig.json, pyproject.toml, eslint config, package.json engines, or Next.js fetch calls.

## Skip If (ANY kills it)

- Deep language-specific patterns (services, views, handlers) — see dev-methodologies-practices.
- Architecture decisions (monolith vs microservice) — see dev-methodologies-architecture.
- When the project has a stricter or newer house standard than this 2026 baseline — defer to that.
- One-shot bug fixes — load only the specific section, not the full hub.

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

- parent skill: `solo/dev/automation-tooling/`
