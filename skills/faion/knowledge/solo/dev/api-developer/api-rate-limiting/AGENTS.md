---
slug: api-rate-limiting
tier: solo
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Rate-limit config: sliding window OR token bucket OR fixed window, tier-based quotas, per-endpoint limits, standard Retry-After + RateLimit-* headers, Redis backend for distributed deployments.
content_id: "12123b7262155c24"
complexity: medium
produces: config
est_tokens: 4200
tags: [api-developer, rate-limiting, scaling, redis, performance]
---
# API Rate Limiting

## Summary

**One-sentence:** Rate-limit config: sliding window OR token bucket OR fixed window, tier-based quotas, per-endpoint limits, standard Retry-After + RateLimit-* headers, Redis backend for distributed deployments.

**One-paragraph:** Naive rate limits (per-IP counter in process memory) break under multi-instance deployment and starve legitimate users behind shared NATs. The methodology pins the algorithm choice (sliding window default, token bucket for burst-tolerant APIs), per-tier quotas, per-endpoint multipliers, standard headers, and a Redis-backed counter for distributed deployments. Output is the rate-limit config artefact + the rollout plan. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- API Rate Limiting — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `api-rate-limiting` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- API exposed to external callers OR untrusted internal consumers.
- Operator has Redis (or equivalent) for distributed counters.
- Tier-based quotas exist OR will exist within 6mo.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Internal API behind a service mesh with already-authenticated peers and no abuse risk.
- Static-asset CDN already enforcing edge rate limits — duplicating at origin adds noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-authentication]] | Caller identity the limit attaches to |
| [[api-monitoring]] | Metrics surfacing 429 rate and per-key consumption |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-api-rate-limiting-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-api-rate-limiting.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-rate-limiting.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[api-authentication]]
- [[api-monitoring]]
- [[api-gateway-patterns]]
- [[api-rest-design]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (algorithm, backend, tier shape) based on burst tolerance, deployment topology, and quota model. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
