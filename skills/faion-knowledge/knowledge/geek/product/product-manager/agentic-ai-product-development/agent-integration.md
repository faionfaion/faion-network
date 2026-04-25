# Agent Integration — Agentic AI Product Development (Product Manager)

## When to use
- Writing product specs for features where the core delivery mechanism is an autonomous agent (not a user-triggered model call)
- Defining success metrics for agentic products: goal achievement rate, escalation rate, autonomy ratio, cost-per-task
- Prioritizing agentic features in the roadmap: deciding which use cases have the goal clarity and data access to support autonomous action
- Creating the MVI (Minimum Viable Intelligence) scope document for an agentic product launch
- Documenting the human-in-the-loop model for stakeholders: what the agent does autonomously, what requires human approval, and why
- Educating product teams on the difference between "AI-assisted" (user triggers, model helps) and "agentic" (agent acts toward a goal)

## When NOT to use
- The use case is a conversational assistant or copilot — use the ai-native-product-development methodology instead
- Success criteria cannot be defined without a human judge (e.g., "does this feel good?") — agentic systems need machine-verifiable success conditions
- The organization lacks the engineering maturity to build and monitor agentic pipelines; pushing the product spec ahead of infrastructure capability leads to failed launches
- Regulatory constraints require a human to review every AI-generated output before it reaches users or systems of record

## Where it fails / limitations
- MVI framing focuses on "intelligence level," but what intelligence means for a specific product is rarely obvious — teams spend too long debating the definition instead of shipping
- Cost range ($50K–$500K+ for enterprise agentic) is a rough guide; actual cost depends heavily on the number of LLM calls per task and the per-token cost of the models chosen
- 40% of agentic pilots fail to productionize — the failure point is usually not the model, but the lack of an error recovery path when the agent hits an edge case
- Model selection tables age quickly; the right model for cost management today may not be the right choice in 6 months
- Agentic products require a different type of A/B testing: you are testing goal achievement rate, not click-through rate, and the feedback loop is longer

## Agentic workflow
Use a product-spec subagent to draft the agentic product requirements document (goal state definition, autonomous actions list, escalation matrix, success metrics). Feed the draft to a review subagent that checks for ambiguous goal definitions, missing failure modes, and gaps in the human-in-the-loop model. A separate subagent generates the MVI scope canvas by applying the "intelligence level vs. feature count" framework: which capabilities are core intelligence, which are deferred to v2.

### Recommended subagents
- `faion-mlp-agent` (mode: propose) — proposes WOW features that create product differentiation beyond the baseline MVI
- `faion-mvp-scope-analyzer-agent` — adapts MVP scope analysis to MVI scope; useful for understanding competitor agentic feature sets
- `spec-reviewer` — checks agentic product spec for: machine-verifiable goal state, complete autonomous action list, human-in-the-loop model, escalation triggers, and rollback plan
- `mvi-scoper` — applies the MVI framework: maps each proposed capability to an intelligence tier (core / value-add / deferred)

### Prompt pattern
```
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

```
Review this agentic product spec for production readiness:
{spec_text}

Flag: ambiguous goal states, missing escalation triggers, undefined failure recovery,
underspecified human-in-the-loop model. Return a structured list of gaps.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude Agent SDK — the underlying runtime for agentic products built on Claude | `pip install anthropic` / https://docs.anthropic.com/en/docs/agents |
| `langfuse` | Observability for agentic products; track goal achievement and escalation rates | `pip install langfuse` / https://langfuse.com |
| `temporal` | Durable workflow engine — the infrastructure layer most agentic products need | https://temporal.io |
| `linear` (API) | Issue and roadmap tracking; agentic product specs live here | https://linear.app/docs/graphql |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Claude as the reasoning engine for the agentic product |
| Langfuse | OSS/SaaS | Yes | Production observability: trace each agent task, measure outcome metrics |
| Temporal Cloud | SaaS | Yes | Durable execution for long-running agentic workflows with reliable retry |
| PostHog | OSS/SaaS | Yes | Product analytics: track goal achievement rate as a product metric |
| Linear | SaaS | Yes (API) | Roadmap and spec management for agentic feature backlog |
| Notion | SaaS | Partial | Spec documentation; lacks structured review workflow for agentic specs |

## Templates & scripts
See `templates.md` for the MVI scope canvas and agentic product spec template.

Autonomy ratio target tracker (for sprint reviews):
```python
from dataclasses import dataclass

@dataclass
class SprintAgentMetrics:
    period: str
    total_tasks: int
    autonomous: int       # completed without human intervention
    escalated: int        # required human review
    failed: int           # did not reach goal state

def sprint_summary(m: SprintAgentMetrics) -> dict:
    if m.total_tasks == 0:
        return {}
    return {
        "period": m.period,
        "autonomy_ratio": round(m.autonomous / m.total_tasks, 3),
        "goal_achievement_rate": round((m.autonomous + m.escalated) / m.total_tasks, 3),
        "failure_rate": round(m.failed / m.total_tasks, 3),
        "cost_efficiency": "track separately via langfuse",
    }
```

## Best practices
- Write the escalation path before the happy path in the spec — the happy path is optimistic; the escalation path is what prevents production disasters
- Define "intelligence level" in concrete, testable terms: "the agent handles 80% of inbound support tickets without human review" is better than "the agent is smart"
- Use cost-per-task as the primary efficiency metric for agentic products, not cost-per-user — agentic systems scale with task volume, not seat count
- Involve engineering in MVI scoping before the spec is finalized; the intelligence level you can achieve is constrained by what the current model can reliably do
- Version the agentic product's behavior: when the underlying model changes, test whether the goal achievement rate and autonomy ratio hold — document the acceptable regression threshold

## AI-agent gotchas
- Product specs that describe agentic behavior in natural language ("the agent will handle complex cases") are not implementable; every autonomous action must be enumerated explicitly with its triggering conditions
- Human-in-the-loop checkpoint: any spec for an agentic product in a regulated domain (finance, health, legal) must explicitly call out which outputs require human sign-off before action — this cannot be left as an implementation detail
- Model capability drift: when the model provider updates a model, the agentic product's behavior may change without a code release — build behavioral regression tests that run on every model update
- Agentic product demos often use cherry-picked inputs; success in a controlled demo does not imply a viable goal achievement rate across real production traffic — require a 100-task pilot on real data before committing to the roadmap

## References
- https://docs.anthropic.com/en/docs/agents (Claude Agent SDK)
- https://www.gartner.com/en/articles/what-is-agentic-ai (Gartner 40% pilot stat, MVI concept)
- https://temporal.io/docs (durable workflow for agentic infrastructure)
- https://langfuse.com/docs (agentic observability)
- https://linear.app/docs/graphql (roadmap integration)
