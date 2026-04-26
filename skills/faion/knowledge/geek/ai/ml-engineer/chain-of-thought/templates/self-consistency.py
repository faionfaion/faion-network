"""
Self-Consistency with majority voting.
Use for: high-stakes single decisions where 5x token cost is justified.
n_samples=5, temperature=0.7.
"""
import anthropic
from collections import Counter


def self_consistency(problem: str, n_samples: int = 5) -> dict:
    """
    Run N parallel CoT calls at temperature=0.7, return majority answer.
    Returns {"answer": str, "confidence": float, "agreement_rate": float}
    """
    client = anthropic.Anthropic()
    answers = []
    for _ in range(n_samples):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": (
                    f"Think step by step and solve:\n\n{problem}\n\n"
                    "Show your reasoning, then state your Final Answer on the last line."
                ),
            }],
        )
        text = response.content[0].text.strip()
        # Extract last line as the answer
        final_answer = text.split("\n")[-1].replace("Final Answer:", "").strip()
        answers.append(final_answer)

    counts = Counter(answers)
    top_answer, top_count = counts.most_common(1)[0]
    agreement_rate = top_count / n_samples

    return {
        "answer": top_answer,
        "confidence": agreement_rate,
        "agreement_rate": agreement_rate,
        "all_answers": answers,
        "requires_review": agreement_rate < 0.6,  # Escalate if < 60% agreement
    }
