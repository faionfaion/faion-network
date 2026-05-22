# purpose: Pydantic model for 3-axis rubric + LLM-as-judge structured output
# consumes: tracer instance, agent runs, eval-set tasks
# produces: OTel spans / eval-report rows conforming to content/02-output-contract.xml
# depends-on: 01-core-rules.xml (three-axis-required, otel-genai-semconv, tool-span-required, hash-not-paste, ci-eval-gate)
# token-budget-impact: instrumentation overhead < 1ms / span; eval-report ~200 tokens / run
from pydantic import BaseModel

class EvalRubric(BaseModel):
    outcome_score_0_to_1: float    # task-success
    trajectory_score_0_to_1: float # path optimality
    resource_score_0_to_1: float   # 1 - normalized_cost

def score_run(trace) -> EvalRubric:
    outcome = score_outcome_with_judge(trace.final_answer, trace.goal)
    trajectory = 1 - min(1, (trace.steps - optimal_steps) / 10)
    resource = 1 - min(1, trace.total_cost / max_acceptable_cost)
    return EvalRubric(
        outcome_score_0_to_1=outcome,
        trajectory_score_0_to_1=trajectory,
        resource_score_0_to_1=resource,
    )
