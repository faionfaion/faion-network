# Agentic AI Product Operations

## Summary

**One-sentence:** An ops-readiness methodology for autonomous agentic AI products that pins five preconditions before the agent takes production traffic: a machine-verifiable goal predicate, daily-budgeted autonomous actions, a pre-launch escalation runbook, an agentic-ops dashboard (goal-achievement-rate / autonomy-ratio / cost-per-task / escalation-rate / regression status), and a behavioural-regression hook on every model bump.

**One-paragraph:** Reactive AI features (user submits → model responds) can be operated like normal SaaS. Autonomous agentic AI systems cannot — they act without prompt, have non-trivial blast radius, and silently regress on provider model updates. This methodology pins the ops-side counterpart of `geek/product/product-manager/agentic-ai-product-development`: budgets per autonomous action, escalation runbook written BEFORE traffic shifts, agentic unit metrics surfaced on the ops dashboard, and an automated regression test set that holds traffic until green. Output: an ops-readiness JSON the launch gate validates.

**Ефективно для:** ops / SRE, який пускає першого автономного агента в продакшен і не хоче, щоб баг у trigger дав 1000 refunds за 30 хв.

## Applies If (ALL must hold)

- An autonomous agentic AI feature is being launched OR is already in production but lacks ops-readiness.
- Observability infrastructure exists (agent tracing, prompt logging, cost telemetry).
- The team has the cost model to support inference-heavy loops.
- A named ops owner exists for the runbook.
- Provider model identifiers can be pinned in config.

## Skip If (ANY kills it)

- Simple AI-augmented tool where user initiates and reviews each step — use the AI-native ops pattern instead.
- No clear agent success metric — if "did the agent achieve the goal?" cannot be defined, do not operate agentic.
- Regulatory environment prohibits autonomous action (healthcare diagnosis, financial order execution without human approval).
- No observability stack — production incidents will be undebuggable.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Goal predicate | YAML | product spec from PM-side methodology |
| Action budgets | YAML | ops + finance |
| On-call rota | YAML | ops roster |
| Dashboard panels | URLs | ops tooling |
| Behavioural test set | jsonl | eval engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/product/product-manager/agentic-ai-product-development` | PM-side counterpart that authors the spec this ops-readiness pack operates. |
| `geek/product/product-manager/ai-feature-de-risking` | Provides the behavioural-regression eval set this methodology hooks into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: goal predicate, escalation runbook pre-launch, budgeted actions, regression on model bump, agentic metrics on dashboard | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~950 |
| `content/06-decision-tree.xml` | essential | Ops-ready gate with per-precondition branches | ~340 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `runbook_draft` | sonnet | Per-agent runbook with SLA / channel / role. |
| `budget_calibration` | sonnet | Calibrate daily budgets from historical task volume. |
| `regression_set_synthesis` | opus | Cross-task behavioural-test design. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ops-readiness.yaml` | Ops-readiness pack schema (goal + actions + runbook + dashboard + regression). |
| `templates/escalation-runbook.md` | Escalation runbook skeleton (role + channel + SLA + triggers). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-ai-product-development.py` | Validate ops-readiness pack against the contract (predicate, budgets, runbook pre-launch, dashboard wired, regression hook). | Launch-gate; pre-production. |

## Related

- [[ai-native-product-development]] — sibling ops methodology for non-autonomous AI-native products.
- [[ai-feature-de-risking]] — peer methodology providing the regression test set.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` checks five preconditions: goal predicate set, every action has a daily budget, runbook is pre-launch, dashboard is wired with agentic metrics, regression hook is set. Any failure → block launch. All green → route traffic.
