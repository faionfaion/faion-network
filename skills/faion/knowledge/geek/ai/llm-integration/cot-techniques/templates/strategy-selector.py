# CoT strategy selection heuristic
# Usage: strategy = select_cot_strategy(problem_text)
# Returns: "zero_shot" | "tree_of_thoughts" | "least_to_most"

def select_cot_strategy(problem: str) -> str:
    """Select CoT strategy based on problem keywords and length.

    Heuristic only — benchmark on your problem class before hardcoding.
    Always try zero_shot first; only escalate if it fails.
    """
    KWS_BRANCHING = {"choose", "compare", "which", "options", "alternative",
                     "best", "versus", "tradeoff"}
    KWS_SEQUENTIAL = {"step", "before", "depends", "order", "first", "then",
                      "sequence", "pipeline", "migration"}

    words = set(problem.lower().split())

    if KWS_BRANCHING & words:
        return "tree_of_thoughts"
    if (KWS_SEQUENTIAL & words) or len(problem) > 500:
        return "least_to_most"
    return "zero_shot"
