# Code Quality Trends 2026

## Summary

A snapshot checklist of current quality standards for mainstream stacks (TypeScript 5/React 19/Next.js 15, Python 3.12+, Go, Rust) covering linting, type safety, testing coverage targets, performance budgets, and security practices. Treat as a configuration generator and audit driver, not a source of truth — refresh quarterly.

## Why

Stack best practices shift faster than teams track them. An agent using this snapshot can generate stack-matched lint configs, CI workflows, and coverage gates for new repos in one pass, and score existing repos against a current baseline. Without an explicit checklist, agents fall back on training-data defaults that may be 1–2 versions stale.

## When To Use

- Setting up a new repo: generate lint/format/test/CI configs matched to the detected stack.
- Quarterly tech-debt audit: compare repo against checklist, emit prioritized gap list.
- Onboarding a stack the team hasn't touched in 18+ months — surface what changed.
- Defining CI performance budgets (FCP, API p95 latency, error rate) from the benchmarks table.

## When NOT To Use

- Critical stack decisions requiring judgment about team skill, hiring, or vendor lock-in — checklist is descriptive, not normative.
- Late-stage products where a stack switch is prohibitively expensive — high adoption stats don't justify migration.
- Niche stacks (Elixir, Clojure, Zig) — the checklist is mainstream-biased.
- Real-time incident response — performance benchmarks are aspirational, not SLO replacements.

## Content

| File | What's inside |
|------|---------------|
| `content/01-stack-checklist.xml` | Per-stack quality gates: TypeScript strict mode, Python ruff/mypy, React RSC, coverage targets, security items. |
| `content/02-tooling-and-benchmarks.xml` | CLI tools index, performance benchmarks (FCP, API latency, error rate), AI tool routing table, known agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/detect-stack.sh` | Coarse stack classifier: reads manifests, emits lang/framework/version for the audit agent. |
| `templates/audit-prompt.txt` | Prompt for stack audit: output JSON array of {item, status, evidence, fix_command}. |
