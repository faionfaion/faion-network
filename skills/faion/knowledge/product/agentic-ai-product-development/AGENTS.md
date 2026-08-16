# Agentic AI Product Development

## Summary

**One-sentence:** A product methodology for designing and shipping autonomous AI systems — agents that act toward a goal without user-triggering each step — replacing MVP with MVI (Minimum Viable Intelligence) and pinning machine-verifiable goal states, enumerated autonomous actions, escalation-first design, and a behavioural-regression hook.

**One-paragraph:** Traditional AI feature specs describe behaviour in natural language ("the agent will handle complex cases") and are not implementable. Agentic products require a different success-metric model (goal-achievement-rate, autonomy-ratio, cost-per-task) and a different failure model (edge-case recovery paths, behavioural regression on model bumps). About 40% of agentic pilots fail to productionize — the failure point is rarely the model and almost always the absence of a production-grade escalation path. This methodology pins the spec to five testable rules and turns it into an executable contract: machine-verifiable goal state, escalation written BEFORE the happy path, enumerated autonomous actions with triggers, behavioural regression mandated on every model bump, and agentic unit metrics (goal-achievement-rate, autonomy-ratio, cost-per-task) as primaries.

**Ефективно для:** AI PM, який запускає першого автономного агента в продакшен і хоче, щоб 40%-pilot-graveyard минула повз.

## Applies If (ALL must hold)

- The core delivery mechanism is an autonomous agent (not a user-triggered single model call).
- The product has access to enough operational data to define a machine-verifiable goal state.
- A named human role exists to receive escalations.
- The team has engineering maturity to monitor agentic pipelines (logs, traces, behavioural test suite).
- Stakeholders accept that primary metrics will be agentic unit metrics, not engagement.

## Skip If (ANY kills it)

- The use case is a conversational copilot — use `ai-native-product-development` instead.
- Success criteria require a human judge ("does this feel good?") — agentic systems need machine-verifiable success.
- Regulatory constraints require human review of every output before reaching users (then it's not agentic, it's assistive).
- Organisation lacks the monitoring stack to detect behavioural drift.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Operational dataset | log / DB query | telemetry store |
| Goal-state predicate definition | YAML | product spec draft |
| Escalation role + on-call | role + person | ops / support roster |
| Behavioural test set | jsonl | QA / eval engineering |
| Cost model per model tier | YAML | finance + AI eng |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/product/product-manager/agents` | Sibling on agent-as-product patterns. |
| `geek/product/product-manager/ai-feature-de-risking` | Feeds the escalation + behavioural-regression sections. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: machine-verifiable goal, escalation-first, enumerated actions, behavioural regression, agentic unit metrics | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~1000 |
| `content/06-decision-tree.xml` | essential | Agentic-or-copilot gate + escalation-ready branch | ~320 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_spec_skeleton` | haiku | Section fill from feature_name + goal + persona. |
| `enumerate_actions` | sonnet | Per-action judgment: trigger conditions, harm thresholds. |
| `design_escalation_path` | opus | Strategic design — cross-domain reasoning over regulator + harm + cost. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-spec-writer.txt` | Prompt template for spec writer (6-section draft). |
| `templates/prompt-spec-reviewer.txt` | Prompt template for spec reviewer (gap list with severity). |
| `templates/sprint-metrics.py` | Computes autonomy_ratio / goal_achievement_rate / failure_rate from sprint task counts. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agentic-ai-product-development.py` | Validate a filled spec against the output contract (goal predicate, escalation-first, action triggers, agentic metrics). | Before stakeholder sign-off and before any deploy. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-native-product-development]] — conversational-copilot sibling for non-autonomous AI products.
- [[ai-feature-de-risking]] — peer methodology for shipping AI features safely.
- [[agents]] — agent-as-product subagent patterns.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first asks: is this autonomous OR copilot? If copilot → route to `ai-native-product-development`. If autonomous, check whether goal state is machine-verifiable AND escalation can be defined. If either fails → block. Otherwise → emit the spec using the rule set.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-spec-writer.txt`

```text
You are a product manager writing a spec for an agentic AI feature.

Feature: {feature_name}
Product goal: {goal}
Target persona: {persona}

Produce the following sections:
1. Goal state (machine-verifiable: how do we know the agent succeeded?)
2. Autonomous actions (what can the agent do without user approval?)
3. Human-in-the-loop checkpoints (which actions require approval, and why?)
4. Escalation triggers (what conditions pause the agent and alert a human?)
5. Success metrics (goal achievement rate, autonomy ratio, cost-per-task targets)
6. Failure modes and recovery plan
```

### `templates/prompt-spec-reviewer.txt`

```text
Review this agentic product spec for production readiness:
{spec_text}

Flag: ambiguous goal states, missing escalation triggers, undefined failure recovery,
underspecified human-in-the-loop model, autonomous actions without triggering conditions.

Return a structured list of gaps with severity (blocking / warning) and suggested fix for each.
```

### `templates/sprint-metrics.py`

```python
"""Sprint-level agentic product metrics tracker.

Input: task counts per sprint period.
Output: autonomy_ratio, goal_achievement_rate, failure_rate.
"""
from dataclasses import dataclass


@dataclass
class SprintAgentMetrics:
    period: str
    total_tasks: int
    autonomous: int   # completed without human intervention
    escalated: int    # required human review but reached goal
    failed: int       # did not reach goal state


def sprint_summary(m: SprintAgentMetrics) -> dict:
    if m.total_tasks == 0:
        return {}
    return {
        "period": m.period,
        "autonomy_ratio": round(m.autonomous / m.total_tasks, 3),
        "goal_achievement_rate": round(
            (m.autonomous + m.escalated) / m.total_tasks, 3
        ),
        "failure_rate": round(m.failed / m.total_tasks, 3),
        "escalation_rate": round(m.escalated / m.total_tasks, 3),
    }
```
