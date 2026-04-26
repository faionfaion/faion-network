# Agent Integration — Agentic AI Product Development

## When to use
- Designing a new product feature where the core value proposition is autonomous action (e.g., auto-triage, auto-scheduling, auto-publishing)
- Shifting an existing reactive AI feature (user submits → model responds) to a proactive agentic one (agent monitors → acts without prompt)
- Defining acceptance criteria for agentic products: goal achievement rate, escalation rate, autonomy ratio
- Evaluating whether a candidate product use case justifies the cost and risk of agentic autonomy vs. a simpler assistant pattern
- Planning the human-in-the-loop model: which decisions the agent makes autonomously, which require human approval, and what triggers escalation
- Creating MVI (Minimum Viable Intelligence) scope instead of MVP when the product's core is an AI capability

## When NOT to use
- Building a simple AI-augmented tool where the user always initiates and reviews each step — use the standard AI-native product development pattern instead
- Agentic autonomy has no clear success metric — if you cannot define "did the agent achieve the goal?", do not build agentic
- Regulatory environment prohibits autonomous action (e.g., healthcare diagnosis, financial order execution without human approval) — use assistant pattern with mandatory human confirmation
- Team lacks observability infrastructure: without agent tracing, monitoring, and logging, production incidents are undebuggable
- Cost model does not support inference-heavy loops — agentic systems that call multiple models per task can cost 10–50x more than single-call AI features

## Where it fails / limitations
- Goal ambiguity causes agent loops: if the success condition is not machine-verifiable, agents may run forever or declare success prematurely
- Agentic products require significantly more monitoring infrastructure than traditional software — task queues, state persistence, retry logic, dead-letter handling
- User trust erodes quickly on visible errors; one bad autonomous action (deleted file, sent wrong email) is harder to recover from than a wrong suggestion
- 40% of agentic pilots fail to reach production due to underestimated edge case handling (Gartner 2026)
- Cost overruns are common: inference costs scale with autonomy depth (number of LLM calls per goal), not just user count
- Model capability gaps emerge at the boundary: the agent handles 85% of cases well, but the remaining 15% require domain knowledge the model does not have

## Agentic workflow
Use a product-design subagent to translate product goals into agentic workflow specs: define the goal state, enumerate autonomous actions the agent may take, specify the human-in-the-loop checkpoints, and produce an escalation matrix. A separate evaluation subagent benchmarks the resulting agentic system against the goal achievement rate and autonomy ratio targets before production launch. For ongoing iteration, a monitoring subagent tracks outcome metrics (not task completion) and flags when agent behavior drifts from the target autonomy profile.

### Recommended subagents
- `faion-mlp-agent` (mode: propose) — proposes WOW features that differentiate the agentic product from a simpler assistant implementation
- `goal-decomposer` — breaks a high-level product goal into machine-verifiable sub-goals with success/failure conditions
- `escalation-designer` — maps decision points to human-in-the-loop checkpoints, generates escalation matrix
- `mvi-scoper` — defines the Minimum Viable Intelligence scope: which agent capabilities are core, which are deferred

### Prompt pattern
```
You are designing an agentic AI product feature. Given the product goal below, produce:
1. Goal state definition (machine-verifiable success condition)
2. Autonomous actions the agent may take (exhaustive list)
3. Human-in-the-loop checkpoints (when must a human approve before the agent proceeds)
4. Escalation triggers (conditions that pause the agent and notify a human)
5. Failure modes and fallback behavior

Product goal: {goal}
User persona: {persona}
Constraints: {constraints}
```

```
Evaluate this agentic product design for production readiness:
- Goal achievement rate target: {target}%
- Autonomy ratio target: {autonomy_ratio} (fraction of cases handled without human intervention)
- Known failure modes: {failure_modes}

Identify gaps in the human-in-the-loop model and propose specific escalation rules.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude Agent SDK for building the agentic system itself | `pip install anthropic` / https://docs.anthropic.com/en/docs/agents |
| `langchain` | Agent orchestration, tool routing, memory | `pip install langchain` / https://python.langchain.com |
| `prefect` | Workflow orchestration with observability for agentic task pipelines | `pip install prefect` / https://docs.prefect.io |
| `temporal` | Durable workflow engine; critical for long-running agentic tasks with retry | https://temporal.io/docs |
| `langfuse` | LLM observability — trace agent calls, measure goal achievement | `pip install langfuse` / https://langfuse.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Claude API | SaaS | Yes | Claude Agent SDK supports tool use, multi-step reasoning |
| LangSmith | SaaS | Yes | Tracing and eval for LangChain-based agentic systems |
| Langfuse | OSS/SaaS | Yes | Self-hostable LLM observability; trace agentic loops |
| Prefect Cloud | SaaS | Yes | Orchestrate agentic task queues with retry, alerting |
| Temporal Cloud | SaaS | Yes | Durable workflow execution for long-running agents |
| Linear | SaaS | Yes (API) | Track agentic product tasks; integrates with CI/CD |
| PostHog | OSS/SaaS | Yes | Product analytics; track goal achievement rate and autonomy ratio in production |

## Templates & scripts
See `templates.md` for MVI scope canvas and agentic product spec templates.

Autonomy ratio calculator (for production monitoring):
```python
from dataclasses import dataclass

@dataclass
class AgentRunMetrics:
    total_tasks: int
    autonomous_completions: int
    human_escalations: int
    failures: int

def autonomy_ratio(m: AgentRunMetrics) -> float:
    """Fraction of tasks completed without human intervention."""
    if m.total_tasks == 0:
        return 0.0
    return m.autonomous_completions / m.total_tasks

def goal_achievement_rate(m: AgentRunMetrics) -> float:
    """Fraction of tasks that reached the success state."""
    if m.total_tasks == 0:
        return 0.0
    return (m.autonomous_completions + m.human_escalations) / m.total_tasks
```

## Best practices
- Define the success condition in machine-verifiable terms before writing any agent code — if you cannot write a unit test for "did the agent succeed?", the goal is too ambiguous for agentic design
- Start with autonomy ratio 0.5 (50% autonomous) and raise the target incrementally as you validate each failure mode; do not target 100% autonomy in v1
- Track goal achievement rate, not task completion rate — an agent can complete 100% of tasks and achieve 0% of goals if the tasks are wrong
- Build the human escalation path before the happy path; the escalation path is what prevents catastrophic failures
- Model selection matters for cost: use Haiku for routine agentic steps, Sonnet for reasoning checkpoints, Opus only for novel edge cases where the agent is genuinely uncertain
- Instrument every agent decision with a trace ID so you can replay and debug individual failures in production

## AI-agent gotchas
- Goal drift: agents optimizing for a proxy metric (e.g., "task completed" instead of "user satisfied") will achieve the metric while missing the goal — define the goal at the outcome level, not the action level
- Tool call loops: agents stuck in retry loops (tool fails, agent retries, tool fails again) can exhaust rate limits and burn budget in minutes — implement a maximum retry count and a circuit breaker at the orchestration layer
- Human-in-the-loop checkpoint: any autonomous action that is irreversible (send email, delete data, charge payment, publish content) must require human approval in v1, even if the long-term target is full autonomy
- Agentic systems expose new attack surfaces: prompt injection via tool outputs (e.g., a web page that contains instructions to the agent) is a real threat; validate and sanitize all tool outputs before passing them back to the model

## References
- https://docs.anthropic.com/en/docs/agents (Claude Agent SDK)
- https://www.gartner.com/en/articles/what-is-agentic-ai (Gartner on agentic AI, 40% pilot stat)
- https://temporal.io/docs (durable workflow execution)
- https://langfuse.com/docs (LLM observability for agentic systems)
- https://prefect.io/docs (workflow orchestration)
