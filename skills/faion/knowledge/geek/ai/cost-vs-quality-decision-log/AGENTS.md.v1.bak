---
slug: cost-vs-quality-decision-log
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "770baf9e0eae1f96"
summary: A persistent log of LLM cost-vs-quality trades so the same compromises don't get re-considered every quarter — pairs with the Pareto template to record the decision after the analysis.
tags: [cost-optimization, decision-log, llm-eval, ml-ops, geek-ai]
---
# Cost-vs-Quality Decision Log

## Summary

**One-sentence:** A persistent append-only log of every cost-vs-quality trade made on LLM-powered features — so the same decisions don't get re-litigated every quarter, and reversals are made with full context.

**One-paragraph:** ML engineers running production LLM pipelines repeatedly cut cost: dropped opus to sonnet, shortened a system prompt, reduced top-k retrieval, switched from per-call to batched. Each trade is made in a Slack thread, lost to git history's noise, then re-considered six months later from scratch — usually arriving at the same conclusion (or worse, the opposite, undoing the savings). This methodology pins a single log file with one append-only row per decision: what was changed, expected quality impact, observed cost saving, rollback trigger, and review-after date. The log is the institutional memory for the cost knob. Paired with `cost-quality-pareto-template` (which runs the eval), the log records the outcome.

## Applies If (ALL must hold)

- The team operates LLM features in production with measurable monthly cost.
- More than one cost knob is in play (model, prompt size, retrieval count, caching, batch size).
- The team has experienced "we already tried that" cycles (re-considering rejected trades).
- Weekly or monthly cost review is a standing ritual.

## Skip If (ANY kills it)

- Single-call, single-config pipeline — there's nothing to log.
- Pre-prototype where the right answer is rapid iteration without overhead.
- Architecture decision records (ADRs) already cover this dimension — extend the ADR format instead.
- Solo developer with full memory of every trade — log is overhead; revisit at team-size 2+.

## Prerequisites

- A repo or wiki space where the log lives (markdown file under version control preferred).
- Monthly cost data per LLM-powered feature.
- Quality dimensions defined per feature (correctness, faithfulness, etc.).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/cost-quality-pareto-template` | Paired methodology — Pareto produces the decision, this log records it. |
| `geek/ai/ml-ops/ml-model-monitoring` | Quality monitoring provides the observed-impact data for log entries. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: append-only, decision tied to feature, rollback trigger, review-after, link to Pareto | ~900 |
| `content/02-output-contract.xml` | essential | Log entry shape; required fields; status lifecycle | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: re-litigation, missing baseline, retroactive entries | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-log-entry` | sonnet | Bounded fill from decision context |
| `quality-impact-summary` | sonnet | Read monitoring data, summarize observed delta |
| `re-litigation-detector` | sonnet | Scan recent slack/discussions for repeat trades |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-log.md` | Append-only log skeleton with header + row format |
| `templates/log-entry.md` | One-entry template with all required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/log-review-overdue.py` | Surface entries past their review-after date | Weekly |

## Related

- parent skill: `geek/ai/ml-ops/`
- peer methodology: `cost-quality-pareto-template`, `ml-model-monitoring`, `prompt-caching-strategy`
- external: [Architecture Decision Records (Nygard)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · [FinOps Foundation cost-control patterns](https://www.finops.org/)
