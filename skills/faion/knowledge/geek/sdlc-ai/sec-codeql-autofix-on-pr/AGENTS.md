---
slug: sec-codeql-autofix-on-pr
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every GitHub repository enables Code Scanning with CodeQL on `push` and `pull_request`.
content_id: "9d718239fd5c56b9"
tags: [codeql, sast, security, github, copilot-autofix]
---
# CodeQL + Copilot Autofix as the PR-time SAST Gate

## Summary

**One-sentence:** Every GitHub repository enables Code Scanning with CodeQL on `push` and `pull_request`.

**One-paragraph:** Every GitHub repository enables Code Scanning with CodeQL on `push` and `pull_request`. PRs that introduce a new CodeQL alert MUST be blocked from merge by a required check. Copilot Autofix runs automatically on alerts and posts an AI-generated patch as a PR suggestion that a human accepts, edits, or rejects — never auto-merge. For ecosystems CodeQL does not cover (Bash, Dockerfile, Terraform/HCL, PHP), enable AI-powered detections in the same Code Scanning pipeline so the gate is uniform across the stack.

## Applies If (ALL must hold)

- Any GitHub-hosted repository with executable code (public OSS gets it free; private repos need GitHub Advanced Security or Copilot Enterprise).
- Any repo with HTTP, auth, deserialization, SQL/NoSQL, or template rendering surface.
- Polyglot repos where shell, Dockerfile, Terraform or PHP also need SAST coverage via the AI detections lane.
- Agent-driven feature work — agents read SARIF via `gh api` and treat new alerts as merge blockers.

## Skip If (ANY kills it)

- Repositories not hosted on GitHub — use Semgrep or SonarQube instead; the Autofix loop is GitHub-specific.
- Pure documentation, asset, or notebook repositories with no executable surface — overhead exceeds value.
- Throwaway experimental branches that will never be merged — do not waste minutes on Code Scanning runs there.
- Mass-renaming refactors that legitimately churn thousands of lines — schedule a one-shot baseline reset, not per-PR Autofix.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
