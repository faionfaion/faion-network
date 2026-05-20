---
slug: mr-renovate-ai-handoff
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run Renovate (or Dependabot) for the deterministic 90% of dependency bumps — semver-safe patch and minor versions auto-merge once CI is green and Mend's Merge-Confidence score crosses the threshold.
content_id: "86217d03418851e8"
tags: [renovate, dependabot, auto-merge, dependency-management, ai-agent]
---
# Renovate Auto-Merge + AI Handoff for Breaking Updates

## Summary

**One-sentence:** Run Renovate (or Dependabot) for the deterministic 90% of dependency bumps — semver-safe patch and minor versions auto-merge once CI is green and Mend's Merge-Confidence score crosses the threshold.

**One-paragraph:** Run Renovate (or Dependabot) for the deterministic 90% of dependency bumps — semver-safe patch and minor versions auto-merge once CI is green and Mend's Merge-Confidence score crosses the threshold. Reserve LLM coding agents for the 10% where the bump introduces breaking API changes or vulnerability fixes that need code edits. GitHub shipped this exact split in April 2026: Dependabot detects the alert, you "Assign to Agent" (Copilot Coding Agent, Claude, Codex, Devin), and the agent opens a DRAFT PR with the version bump plus call-site edits plus test fixes. Multiple agents may be assigned in parallel; pick the strongest PR.

## Applies If (ALL must hold)

- Any repo with `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `composer.json` (Renovate covers all).
- Security-alert remediation where the patch is non-trivial — call-sites moved, API renamed, deprecated calls removed.
- Multi-language monorepos where a single Renovate config governs every ecosystem.
- Repos where you can budget for AI agent tokens on major-version PRs but want patch bumps to cost zero.

## Skip If (ANY kills it)

- Projects with manual release-train governance where every dependency bump is reviewed in a release meeting.
- Repos that pin all versions exactly and never auto-update — Renovate has no role.
- Patch bumps with all-green CI and high Merge-Confidence — let Renovate auto-merge; do not burn agent tokens.
- MAJOR-version bumps without explicit agent supervision — never auto-merge even with high Merge-Confidence.

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
