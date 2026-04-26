"""LLM architecture decision scoring matrix."""
from dataclasses import dataclass
from typing import Literal


@dataclass
class TaskProfile:
    """Profile of a task to route to the right LLM architecture."""
    example_count: int            # labeled training examples available
    knowledge_changes: bool       # does the knowledge update frequently?
    latency_budget_ms: int        # acceptable p50 latency
    monthly_calls: int            # expected API calls per month
    accuracy_required: float      # 0.0-1.0 required accuracy
    privacy_required: bool        # must not send data to 3rd party


def score_approach(profile: TaskProfile) -> dict[str, float]:
    """Score each approach 0-10 for this task profile."""
    scores: dict[str, float] = {
        "prompt_engineering": 0.0,
        "rag": 0.0,
        "fine_tuning": 0.0,
        "raft": 0.0,
    }

    # Prompt engineering: fast, no infra, limited by model capability
    scores["prompt_engineering"] = 8.0
    if profile.accuracy_required > 0.90:
        scores["prompt_engineering"] -= 3.0
    if profile.example_count > 100:
        scores["prompt_engineering"] -= 1.0

    # RAG: good for knowledge-intensive, frequently changing data
    scores["rag"] = 6.0
    if profile.knowledge_changes:
        scores["rag"] += 3.0
    if profile.example_count < 500:
        scores["rag"] += 1.0
    if profile.latency_budget_ms < 500:
        scores["rag"] -= 2.0

    # Fine-tuning: best for stable patterns, high volume, style/format
    scores["fine_tuning"] = 5.0
    if profile.example_count >= 1000:
        scores["fine_tuning"] += 3.0
    if profile.knowledge_changes:
        scores["fine_tuning"] -= 4.0
    if profile.monthly_calls > 100_000:
        scores["fine_tuning"] += 2.0
    if profile.privacy_required:
        scores["fine_tuning"] += 1.0

    # RAFT: combines RAG + fine-tuning for domain synthesis
    scores["raft"] = 4.0
    if profile.example_count >= 500 and profile.knowledge_changes:
        scores["raft"] += 4.0
    if profile.accuracy_required > 0.95:
        scores["raft"] += 2.0

    return {k: max(0.0, min(10.0, v)) for k, v in scores.items()}


def recommend(profile: TaskProfile) -> str:
    """Return the recommended approach for this task profile."""
    scores = score_approach(profile)
    return max(scores, key=lambda k: scores[k])
