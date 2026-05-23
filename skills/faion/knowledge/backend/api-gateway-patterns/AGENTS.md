# API Gateway Patterns

## Summary

**One-sentence:** Declarative gateway config (Kong, Envoy, Traefik, nginx) centralising TLS, JWT auth, rate limits, CORS, observability, and BFF fan-out for a backend fronted by one ingress.

**One-paragraph:** Without a gateway, every backend service duplicates TLS termination, auth middleware, rate-limit code, and CORS rules — drift becomes a CVE class. The methodology pins a GitOps-managed declarative config with explicit per-route timeouts, Redis-backed counters, JWT validation at the edge, and structured-log forwarding. Output is the gateway config artefact + the rollout plan. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals; the validator script enforces the output contract before the orchestrator accepts the artefact.

**Ефективно для:**

- API Gateway Patterns — fits when the triggering activity recurs and the artefact needs to be auditable.
- Solo operator who wants a fixed template instead of improvising under pressure.
- Downstream consumer (human reviewer or agent) who must sign off without re-deriving the reasoning.
- Recurring cycle (sprint, weekly, per-incident) rather than a one-off task.

## Applies If (ALL must hold)

- The triggering activity for `api-gateway-patterns` appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.
- Backend serves ≥3 services behind a single ingress OR external consumers.
- Operator has uptime requirements that justify centralising cross-cutting concerns.
- GitOps pipeline can apply gateway config declaratively (no UI edits in prod).

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).
- Single internal service with <100 RPS — gateway adds latency and ops cost without value.
- Serverless backend already fronted by a managed gateway (API Gateway, Cloud Run) — re-deploying nginx is duplicate work.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots, design-file ids | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-authentication]] | Auth mechanism the gateway enforces |
| [[api-rate-limiting]] | Rate-limit policy the gateway implements |

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
| `fill-api-gateway-patterns-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-api-gateway-patterns.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-gateway-patterns.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[api-authentication]]
- [[api-rate-limiting]]
- [[api-monitoring]]
- [[api-rest-design]]

## Decision tree

See `content/06-decision-tree.xml`. Routes (engine choice, plugin set, deployment shape) based on scale, ops budget, and existing infra. Every leaf cites a rule from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks any variant, and ties the chosen leaf to the rule the orchestrator must enforce.
