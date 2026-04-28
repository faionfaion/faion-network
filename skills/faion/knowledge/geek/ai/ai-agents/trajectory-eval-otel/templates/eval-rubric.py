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
