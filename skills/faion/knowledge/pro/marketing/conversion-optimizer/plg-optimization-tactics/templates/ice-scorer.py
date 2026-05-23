# purpose: ICE-scoring for PLG tactic backlog; bucket() returns priority queue
# consumes: list[Tactic] with impact / confidence / ease (1-10) + metric + baseline
# produces: ranked Tactic list per content/02-output-contract.xml schema
# depends-on: content/01-core-rules.xml (rule baseline-required)
# token-budget-impact: ~400 tokens when loaded as context
"""
ice-scorer.py — ICE scoring for PLG tactic backlog.

Agents emit Tactic(...) instances from each tactic-catalog section,
then call rank() to produce a prioritized test queue.

ICE = Impact + Confidence + Ease (each 1-10).
Bucket thresholds are calibrated for quarterly sprint planning.
"""
from dataclasses import dataclass


@dataclass
class Tactic:
    name: str
    impact: int       # 1-10: expected lift on target metric
    confidence: int   # 1-10: evidence strength (own data > industry > guess)
    ease: int         # 1-10: inverse cost (eng + design weeks; 10 = hours)
    metric: str       # which metric this tactic moves (required)
    baseline: float   # current value of that metric (required; rejects if 0)

    @property
    def ice(self) -> int:
        return self.impact + self.confidence + self.ease

    def bucket(self) -> str:
        if self.ice >= 24:
            return "test_now"
        if self.ice >= 18:
            return "this_quarter"
        if self.ice >= 12:
            return "if_capacity"
        return "backlog"


def rank(tactics: list[Tactic]) -> list[Tactic]:
    """Return tactics sorted by ICE descending. Raises on missing baseline."""
    for t in tactics:
        if t.baseline <= 0:
            raise ValueError(f"Tactic '{t.name}' has no baseline — reject (rule baseline-required).")
    return sorted(tactics, key=lambda t: t.ice, reverse=True)
