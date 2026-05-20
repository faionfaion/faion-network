---
slug: prompt-version-pinning-runbook
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2260845c88596445"
summary: A runbook for pinning prompt versions at the gateway: storage layout per environment, immutable version IDs, rollout (canary / shadow / 5/95 split), gateway-side enforcement, rollback in &lt; 60 seconds, and weekly A/B review.
tags: [prompts, version-pinning, llm-gateway, ab-testing, llm-agent, geek-tier]
---

# Prompt Version Pinning Runbook

## Summary

**One-sentence:** Pin prompt versions at the LLM gateway with immutable IDs, environment-scoped storage, canary / shadow rollout, gateway-side enforcement, and a 60-second rollback path — so prompt changes ship with the same discipline as schema migrations.

**One-paragraph:** Schema-version-pinning covers tool / output schemas; prompts also need a hardened pinning runbook. The geek-tier challenge is concrete: a multi-tenant agent platform with dozens of prompts, multiple environments, A/B experiments running constantly. Without pinning at the gateway, a new prompt version silently leaks into 100% of traffic at deploy. The runbook pins six choices: (1) storage layout — prompts are content-addressable objects (id + immutable version) in a registry per environment (`prod`, `staging`, `shadow`); (2) gateway-side enforcement — every LLM call carries the explicit `prompt_id @ version`, the gateway rejects unpinned calls; (3) rollout strategy per change — shadow (no traffic, eval only), canary (5%), guarded-flag (per-tenant), full; (4) rollback contract — `gateway rollback prompt_id` returns to last known-good in &lt; 60 sec, traffic shifts within 1 min; (5) weekly A/B review — at least one prompt under active comparison; (6) gateway audit log — every prompt version change is event-sourced for post-incident replay. Primary output: a working gateway with a `prompts/` registry, a per-environment lock file, and a `prompts ops` CLI.

## Applies If (ALL must hold)

- production system has ≥ 10 distinct LLM prompts and ≥ 100k LLM calls per day
- there is (or there can be) an LLM gateway / proxy in front of provider APIs (Helicone, Portkey, custom)
- team has at least one ML engineer dedicated to prompt operations
- there are multiple environments (prod, staging, optionally shadow) where prompt versions diverge

## Skip If (ANY kills it)

- prototype phase, single environment, no multi-tenant — pinning overhead exceeds the benefit; use `prompt-changelog-discipline` only
- prompts are stored entirely in a third-party LLM-Studio SaaS with no exportable lock file — adapt their primitives, do not roll your own
- no gateway is possible (compliance forbids it) — pinning happens at the client SDK with stricter discipline, but the runbook still applies
- &lt; 100k LLM calls per day — the ROI on full pinning kicks in at scale; smaller teams use a lighter version

## Prerequisites

- prompt-changelog-discipline already adopted (one file per prompt, hashes, eval)
- an LLM gateway exists OR can be added in 1-2 weeks (open-source or commercial)
- a frozen eval suite per prompt that runs in CI
- a feature-flag system for guarded rollouts (LaunchDarkly, Unleash, or a homegrown gate)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/prompt-changelog-discipline` | The hash + eval foundation; this runbook builds on it |
| `geek/ai/ml-engineer/llm-observability` | The audit trail and rollback logs live in the observability platform |
| `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` | Incident-response runbook format consumed during rollbacks |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: immutable IDs, gateway enforcement, rollout strategy per change, 60s rollback, weekly A/B review | ~900 |
| `content/02-output-contract.xml` | essential | Lock-file schema, gateway-event schema, rollback-receipt schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: silent version drift, unpinned client calls, rollback stuck, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate_lockfile_diff_for_release` | sonnet | Diff old vs new lock, surface prompt versions changing |
| `propose_rollout_strategy_per_change` | sonnet | Per-prompt bounded judgment from eval delta and traffic share |
| `incident_rollback_orchestration` | sonnet | Reads gateway state, picks rollback target, executes via CLI |
| `weekly_ab_review_synthesis` | opus | Cross-prompt synthesis of running comparisons |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompts.lock.yaml` | Per-environment lock file mapping prompt_id to immutable version |
| `templates/gateway-policy.yaml` | Gateway enforcement config (reject unpinned, allowed versions per env) |
| `templates/rollback-receipt.md` | Post-rollback artifact recording what was rolled back, by whom, when, why |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/prompts-ops.py` | CLI: `prompts pin`, `prompts canary`, `prompts rollback`, `prompts diff` | On every prompt rollout / rollback |
| `scripts/gateway-audit-export.py` | Pulls audit events for the past N days, summarises version transitions | Weekly |

## Related

- parent skill: `geek/ai/ml-engineer/SKILL.md`
- peer methodologies: `geek/ai/ml-engineer/prompt-changelog-discipline`, `geek/ai/llm-integration/structured-output-patterns`
- external: [Portkey LLM gateway docs] · [Helicone open-source proxy] · [LangChain Hub prompt versioning] · [Anthropic Workbench prompt versions docs] · [OpenAI Models endpoint versioning patterns]
