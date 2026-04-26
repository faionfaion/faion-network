# Renovate Auto-Merge + AI Handoff for Breaking Updates

## Summary

Run Renovate (or Dependabot) for the deterministic 90% of dependency bumps — semver-safe patch and minor versions auto-merge once CI is green and Mend's Merge-Confidence score crosses the threshold. Reserve LLM coding agents for the 10% where the bump introduces breaking API changes or vulnerability fixes that need code edits. GitHub shipped this exact split in April 2026: Dependabot detects the alert, you "Assign to Agent" (Copilot Coding Agent, Claude, Codex, Devin), and the agent opens a DRAFT PR with the version bump plus call-site edits plus test fixes. Multiple agents may be assigned in parallel; pick the strongest PR.

## Why

LLM agents are wasted on patch-version bumps that Renovate already merges deterministically; conversely, Renovate alone cannot handle major-version bumps that require call-site rewrites and test updates. Splitting the work along the semver boundary (and Merge-Confidence threshold) keeps cost, latency, and risk all within budget. Mend Merge-Confidence is published per package across 90+ ecosystems; combining it with branch protection and an agent label gives a deterministic fast-path with a safe escalation lane.

## When To Use

- Any repo with `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `composer.json` (Renovate covers all).
- Security-alert remediation where the patch is non-trivial — call-sites moved, API renamed, deprecated calls removed.
- Multi-language monorepos where a single Renovate config governs every ecosystem.
- Repos where you can budget for AI agent tokens on major-version PRs but want patch bumps to cost zero.

## When NOT To Use

- Projects with manual release-train governance where every dependency bump is reviewed in a release meeting.
- Repos that pin all versions exactly and never auto-update — Renovate has no role.
- Patch bumps with all-green CI and high Merge-Confidence — let Renovate auto-merge; do not burn agent tokens.
- MAJOR-version bumps without explicit agent supervision — never auto-merge even with high Merge-Confidence.

## Content

| File | What's inside |
|------|---------------|
| `content/01-renovate-split.xml` | Semver split rules, Merge-Confidence threshold, agent-fixable label hand-off. |

## Templates

| File | Purpose |
|------|---------|
| `templates/renovate.json` | Renovate config with patch/minor auto-merge plus major→`agent-fixable` rule. |
| `templates/dependabot-handoff.yml` | GitHub workflow that assigns Dependabot alerts to a coding agent on label. |
