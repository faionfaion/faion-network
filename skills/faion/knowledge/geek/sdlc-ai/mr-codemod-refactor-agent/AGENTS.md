# Codemod-First Refactor Agent

## Summary

Cross-cutting refactors (Angular 17→20, AI SDK 5→6, rename `User.email`→`User.contact`) are codemods, not chat conversations. Use AST-aware tools (jscodeshift, ts-morph, libcst, semgrep, codemod.com / Hypermod) to do the deterministic 95% of edits, then let an LLM finish the long-tail (string templates, tests, docstrings, README snippets) that AST cannot reach. Open ONE PR per logical group of changes — not one per file. Multi-agent stacks (Architect → Migration → Validator) generate the PR with summary plus risk notes.

## Why

LLMs alone produce inconsistent renames at 100+ call sites: variant casing slips through, string templates get rewritten incorrectly, and import paths drift. Codemods are deterministic on AST — the rename is exact and re-runnable. The remaining 5% (where AST has no signal) is exactly where an LLM is strong. Combining the two collapses a multi-day manual refactor into a reviewable single PR with codemod summary plus AI-written body, while keeping the AST log as audit. AI SDK 5→6, Angular major upgrades, and OpenAI's Agents SDK migration cookbook all ship as codemods specifically because the LLM-only path failed in their own evals.

## When To Use

- Framework upgrades that ship breaking renames (Angular, React, Next.js, Vue, AI SDK).
- API renames or deprecation removals across >100 call-sites.
- Lint-rule rollouts where every existing violation must be auto-fixed (TS strict mode flip, ESLint rule).
- Schema migrations where the field rename touches code, tests, fixtures, and docs in lockstep.

## When NOT To Use

- Small renames (<20 sites) — IDE rename refactor is faster and safer; codemod overhead is not justified.
- Semantic refactors where the type signature stays but the BEHAVIOUR changes — codemods don't see behaviour.
- Refactors that require staged rollout across multiple deploys — split into staged PRs first.
- Generated code where the source-of-truth is not the file being changed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-codemod-first-rule.xml` | AST tools do 95%, LLM does the long-tail; one PR per logical group. |
| `content/02-multi-agent-validator.xml` | Architect/Migration/Validator split; codemod log as audit; CI gate on idempotence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rename-property.ts` | jscodeshift codemod renaming `user.email` → `user.contact` repo-wide. |
| `templates/migration-pr-body.md` | PR body skeleton with codemod stats, risk, manual-touch list. |
