# purpose: Sprint-level agentic product metrics tracker.
# consumes: SprintAgentMetrics dataclass (total / autonomous / escalated / failed).
# produces: dict with autonomy_ratio, goal_achievement_rate, failure_rate, escalation_rate.
# depends-on: dataclasses (stdlib).
# token-budget-impact: zero — code only.
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
