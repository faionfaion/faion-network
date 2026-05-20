---
slug: ci-eval-gate-config
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Concrete CI configuration recipe for blocking PRs on LLM eval regression — baseline storage, threshold knobs, flaky-case handling, and an on-call override path.
content_id: "052005701a149f26"
tags: [sdlc-ai, eval, ci, llm, regression-gate, prompt-engineering, eval-harness]
---

# CI Eval Gate Config

## Summary

**One-sentence:** A drop-in CI configuration pattern that blocks PRs on LLM eval regression against a stored baseline, with explicit thresholds per metric, flaky-case quarantine, and a documented on-call override path.

**One-paragraph:** Most teams have an eval harness; few have it wired correctly into CI. The gaps are: where the baseline lives, how thresholds are set per metric, how flaky cases are handled without bypassing the gate, and who can override and how. Mechanism: baseline JSON committed to repo and updated only by reviewed PRs, per-metric threshold config (e.g., accuracy: drop &lt;= 2 pp tolerated, latency_p95: drop &lt;= 10% tolerated, cost_per_eval: max +5%), explicit flaky-case list with quarantine flag and re-evaluation date, on-call override path with named approver + audit log. Primary output: a CI step that runs evals on changed prompts / models / configs, compares to baseline, and produces a pass / changes-needed / override-applied decision.

## Applies If (ALL must hold)

- product has LLM components (prompts, agent flows, RAG, fine-tuned models) used in production OR pre-production
- eval harness exists and runs reproducibly OR can be created (see `geek/sdlc-ai/test-property-based-llm-invariants`)
- CI platform supports PR-blocking checks (GitHub Actions, GitLab CI, Buildkite, CircleCI)
- changes to prompts / models / configs are tracked in version control

## Skip If (ANY kills it)

- LLM use is exploratory / non-customer-facing — eval gate is overhead before signal exists
- no stable eval set yet — establish 50+ cases with stable ground truth first
- prompt changes happen outside the repo (UI-only prompt editor) — gate cannot see them; fix the workflow first
- single dev / pre-launch — manual eval-run discipline is faster than CI gate

## Prerequisites

- eval set with >= 50 cases, each with ground-truth labels or graded scoring
- one of: deterministic eval (BLEU, exact-match, JSON-schema-validity) OR LLM-as-judge with sufficient reliability data (Cohen's kappa >= 0.7 vs human labels)
- baseline JSON committed at known path (e.g., `.evals/baseline.json`)
- defined override approver(s) — typically tech lead + ML lead

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/eval-harness-construction` | Defines the eval set / scorer shape that this gate consumes |
| `geek/sdlc-ai/test-property-based-llm-invariants` | Provides invariant tests this gate runs alongside accuracy metrics |
| `geek/ai/ml-ops/baseline-snapshot-versioning` | Defines how baseline JSON is versioned and re-snapshotted after intentional model swaps |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: baseline-in-vcs, per-metric-thresholds, flaky-case-quarantine, override-with-named-approver, mandatory-cost-budget | ~1000 |
| `content/02-output-contract.xml` | essential | Gate output schema + override record schema + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (baseline-drift-via-feature-branch, judge-collusion, etc.) with detector + repair | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `changed_artifact_detection` | haiku | Walk PR diff, identify changed prompts / models / configs |
| `eval_run_orchestration` | haiku | Mechanical — invoke harness with changed artifacts |
| `metric_diff_vs_baseline` | sonnet | Compute per-metric deltas, classify within/over threshold |
| `flaky_case_diagnosis` | sonnet | When case fails inconsistently, decide quarantine vs investigate |
| `override_proposal_drafting` | sonnet | Draft override rationale when threshold breach is justified |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-baseline.json` | Baseline schema (per-case scores + aggregate metrics) |
| `templates/thresholds.yaml` | Per-metric threshold config |
| `templates/override-record.json` | Override approval record schema |
| `templates/ci-workflow.yml` | Drop-in GitHub Actions / GitLab CI workflow |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/run-eval-gate.py` | Orchestrates eval run + diff + decision | Every PR touching prompts / models / configs |
| `scripts/quarantine-case.py` | Adds case to flaky list with re-eval date | On confirmed flaky case |
| `scripts/audit-overrides.py` | Audits override history; flags chronic overrides | Monthly |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: `test-property-based-llm-invariants`, `test-golden-master-legacy-rewrite`, `gov-conventional-commits-enforced`
- external: [OpenAI Evals](https://github.com/openai/evals) · [Anthropic Eval Cookbook](https://docs.anthropic.com/en/docs/build-with-claude/evals) · [Promptfoo CI Integration](https://www.promptfoo.dev/docs/integrations/ci-cd/)
