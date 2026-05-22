---
slug: prompt-changelog-discipline
tier: pro
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "7736c2de817bf675"
summary: A lightweight prompt-changelog convention that pairs every prompt edit with a hash, intent, eval delta, and rollback path so production-prompt regressions can be correlated back to a specific change in minutes rather than days.
tags: [prompts, changelog, observability, regression, ml-engineering, version-control]
---

# Prompt Changelog Discipline

## Summary

**One-sentence:** Couple every prompt edit to a structured changelog entry — intent, hash, eval delta, rollback path — so any production-quality regression can be traced to a specific edit within minutes rather than archaeological git-blame sessions.

**One-paragraph:** Prompts are code, but most teams treat them as configuration: edits land in PRs with messages like "tweak prompt" or "fix wording", and a regression a week later forces an hour of git-blame on a long YAML file. The discipline pins six fields per prompt edit: prompt-id, prompt-hash (content SHA), one-sentence intent, eval-suite delta (before vs after on a frozen eval), rollout flag (canary % or shadow), and rollback hash. Entries live in a single per-prompt `PROMPTS.changelog.md` next to the prompt artifact. Mechanism: pre-commit hook computes the hash, blocks commits without a changelog entry, eval runner attaches its delta to the entry, and a `prompt rollback` command reverts to a known-good hash. Primary output: a changelog file per prompt plus a per-deploy summary that ties prompt versions to model versions and to live eval scores.

## Applies If (ALL must hold)

- production system uses LLM prompts (Claude, OpenAI, Gemini, local) where output quality is customer-visible
- prompts live in version-controlled files (not in an LLM-Studio web UI without export)
- team has at least one frozen eval suite that the prompts are scored against
- team has experienced at least one prompt regression where the offending edit was hard to identify

## Skip If (ANY kills it)

- prompts are pure exploratory notebooks not in production — overhead not justified
- prompt edits are gated entirely behind LLMOps SaaS (Vellum, Pezzo) that already does changelog — adopt their format instead of duplicating
- no eval suite exists yet — establish the eval first (`geek/ai/ml-ops/evaluation-framework`); changelog without eval is just gossip
- team has fewer than 5 prompts and one engineer — the discipline overhead exceeds the regression risk

## Prerequisites

- prompts stored as files in a repo (one prompt = one file, or YAML map of prompt-id → prompt-text)
- a frozen eval suite that runs in CI (or at least nightly)
- agreement that prompt edits go through PRs, not via emergency hot-edit on the LLM gateway

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-ops/evaluation-framework` | Eval delta is the load-bearing field; no eval, no changelog discipline |
| `geek/ai/ml-engineer/prompt-engineering-evaluation` | Eval-suite construction is the upstream artifact |
| `geek/ai/ml-engineer/llm-observability` | Tying changelog entries to live observability signals closes the loop |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: one-prompt-one-file, hash on commit, intent + eval delta required, rollback hash, deploy-summary | ~900 |
| `content/02-output-contract.xml` | essential | Changelog entry schema, per-deploy summary schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: silent edit, eval-skipped, untracked rollback, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_intent_from_pr_description` | haiku | Lookup with simple summarization |
| `run_eval_and_attach_delta` | sonnet | Eval runner output parsing + delta computation |
| `propose_rollback_target_hash` | sonnet | Walks recent history, picks last known-good hash by eval score |
| `synthesize_deploy_summary` | sonnet | Cross-prompt synthesis at deploy time |

## Templates

| File | Purpose |
|------|---------|
| `templates/PROMPTS.changelog.md` | Skeleton with header + entry format |
| `templates/changelog-entry.yaml` | YAML form when prompts are stored in a YAML registry |
| `templates/deploy-summary.md` | Per-deploy summary table linking prompt versions to model version |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/prompt-hash.py` | Computes a stable content hash of the prompt file (after normalising whitespace) | Pre-commit hook |
| `scripts/changelog-required.py` | Blocks the commit if a prompt file changed without a matching changelog entry | Pre-commit hook |
| `scripts/prompt-rollback.py` | Reverts a prompt to a specified hash, opens an emergency PR with the diff | Incident response |

## Related

- parent skill: `geek/ai/ml-engineer/SKILL.md`
- peer methodologies: `geek/ai/ml-engineer/prompt-engineering-evaluation`, `geek/ai/ml-ops/evaluation-framework`, `geek/ai/ml-engineer/prompt-version-pinning-runbook`
- external: [Promptfoo eval framework] · [Microsoft LMOps team writeups on prompt versioning] · [Vellum / Pezzo / Helicone prompt-management docs] · [Anthropic prompt-engineering documentation chapter on iteration]
