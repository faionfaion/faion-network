# purpose: SelfCorrectionLoop — generate → verify with different model → regenerate; cap + escalate.
# consumes: self-correction-config.json + generator + verifier + chunks + audit_log
# produces: verified answer OR escalation with full trace
# depends-on: content/01-core-rules.xml r1, r2
# token-budget-impact: 1+N generator calls + N verifier calls; N capped at max_corrections
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class SelfCorrectionConfig:
    max_corrections: int = 2
    generator_model: str = "opus"
    verifier_model: str = "sonnet"
    max_ungrounded_claims: int = 2
    audit_trace: bool = True


@dataclass
class SelfCorrectionLoop:
    config: SelfCorrectionConfig
    generate: Callable[[str, list[dict], list[str] | None], str]
    verify: Callable[[str, list[dict]], dict]  # returns {"ungrounded": int, "feedback": list[str]}
    audit_log: Callable[[dict], None]

    def __post_init__(self) -> None:
        # rule r1: distinct verifier
        if self.config.verifier_model == self.config.generator_model:
            raise ValueError("verifier_model must differ from generator_model (rule r1)")
        # rule r2: cap + audit
        if self.config.max_corrections > 3:
            raise ValueError("max_corrections cap is 3 (rule r2)")
        if not self.config.audit_trace:
            raise ValueError("audit_trace must be true (rule r2)")

    def run(self, query: str, chunks: list[dict]) -> dict[str, Any]:
        trace: list[dict] = []
        feedback: list[str] | None = None
        for i in range(self.config.max_corrections + 1):
            answer = self.generate(query, chunks, feedback)
            verdict = self.verify(answer, chunks)
            trace.append({"iter": i, "answer": answer, "verdict": verdict})
            if verdict["ungrounded"] <= self.config.max_ungrounded_claims:
                self.audit_log({"query": query, "trace": trace, "result": "verified"})
                return {"answer": answer, "needs_human_review": False, "trace": trace}
            feedback = verdict.get("feedback", [])
        # cap reached
        self.audit_log({"query": query, "trace": trace, "result": "escalated"})
        return {"answer": None, "needs_human_review": True, "trace": trace}
