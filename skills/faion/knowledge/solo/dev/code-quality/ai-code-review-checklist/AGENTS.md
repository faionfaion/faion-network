---
slug: ai-code-review-checklist
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "629ddeaf0b7f8f0f"
summary: Twelve-check rubric for reviewing AI-generated diffs (Copilot, Claude, Cursor) before merge — hallucinated APIs, silent-skip tests, convention drift, supply-chain risk.
tags: [code-review, ai-generated-code, copilot, claude, cursor, supply-chain]
---

# AI Code Review Checklist

## Summary

**One-sentence:** Twelve-check rubric for reviewing AI-generated diffs (Copilot, Claude, Cursor) before merge — hallucinated APIs, silent-skip tests, convention drift, supply-chain risk.

**One-paragraph:** Solves the dominant 2025-2026 PR-review failure mode: reviewer trusts the diff because it compiles and looks plausible, but it imports a non-existent package, deletes a failing test instead of fixing it, or adopts a pattern foreign to the codebase. Mechanism: a fixed 12-point checklist applied to any diff where ≥30% of new lines were AI-generated, with each check carrying a "block merge / request changes / approve with note" verdict. Primary output: a review decision plus a checklist trace recorded in the PR.

## Applies If (ALL must hold)

- pr_contains_ai_generated_diff == true (Copilot/Claude/Cursor commit signature, or author-disclosed)
- diff_size > 20 lines (smaller diffs use the generic code-review-process)
- target_branch is protected (main/master/production)
- reviewer is the author or a teammate doing human review (not just CI)

## Skip If (ANY kills it)

- diff is purely cosmetic (formatting, comments) — generic style review is enough
- diff is fully covered by deterministic codemod (jscodeshift, libcst output) — codemod review is different
- repo is a throwaway experiment without protected branches — overhead not justified
- AI generated only test data fixtures (no production code) — fixture review is different

## Prerequisites

- AGENTS.md / CLAUDE.md / CONVENTIONS.md present in repo root (the codebase conventions the AI was meant to follow)
- pre-commit hooks installed (linter, type-checker, secret scanner) — checklist assumes these run
- lockfile in repo (package-lock.json, poetry.lock, Cargo.lock, go.sum) — supply-chain check depends on it

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/code-quality/code-review-process` | Generic review fundamentals; this checklist layers AI-specific checks on top |
| `solo/dev/code-quality/tech-debt-management` | Provides "is this a debt deferral disguised as a fix?" framing for check 11 |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 12 checks with detector + verdict policy | ~1300 |
| `content/02-output-contract.xml` | essential | Review-decision schema and forbidden review patterns | ~600 |
| `content/03-failure-modes.xml` | essential | 6 reviewer failure modes specific to AI-generated diffs | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `static_checks_aggregation` | haiku | Pull together lint/type/test/lockfile signals; no judgment |
| `per-check_verdict` | sonnet | Bounded judgment per check; can read diff context |
| `cross-check_synthesis` | opus | Final merge/block decision integrating 12 verdicts + repo conventions |

## Templates

| File | Purpose |
|------|---------|

## Scripts

| File | Purpose |
|------|---------|

## Related

- parent skill: `solo/dev/code-quality/SKILL.md`
- peer methodologies: `solo/dev/code-quality/tech-debt-management`, `free/dev/code-quality/code-review-process`
- external: [GitHub Copilot review-resistance study (2024)](https://arxiv.org/abs/2404.10543) · [Stanford "Do Users Write More Insecure Code with AI Assistants?" (Perry et al., 2023)](https://arxiv.org/abs/2211.03622) · [Snyk supply-chain "slopsquatting" advisories (2025)] · [Anthropic Claude Code review guide](https://docs.anthropic.com/en/docs/claude-code)
