"""
purpose: Self-consistency CoT — N parallel reasoning paths + majority vote + confidence.
consumes: prompt + N + LLM call + answer parser
produces: dict {final, votes, confidence}
depends-on: content/01-core-rules.xml; cot-techniques sibling
token-budget-impact: N x baseline CoT cost

Self-consistency CoT: N parallel reasoning paths, majority vote, confidence score.

Usage:
    answer, confidence = self_consistency("If a shirt costs $25 and is 20% off, price?")
    if confidence < 0.6:
        # Route to human review
        pass
"""
from collections import Counter
import anthropic

client = anthropic.Anthropic()


def self_consistency(problem: str, n: int = 5, temperature: float = 0.7) -> tuple[str, float]:
    """Run self-consistency: N parallel CoT paths, majority vote.

    Args:
        problem: The question or problem to solve.
        n: Number of reasoning paths to sample (3-7 recommended).
        temperature: Must be > 0 to get diverse paths. Min 0.6 for meaningful diversity.

    Returns:
        (majority_answer, confidence) where confidence = votes / n.
    """
    assert temperature >= 0.6, "temperature < 0.6 collapses diversity; use >= 0.6"

    answers = []
    for _ in range(n):
        msg = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"{problem}\n\nThink step by step. End with 'Answer: <value>'",
            }],
        )
        text = msg.content[0].text
        if "Answer:" in text:
            raw = text.split("Answer:")[-1].strip().split()[0].rstrip(".,;")
            answers.append(raw)

    if not answers:
        return "", 0.0
    top, count = Counter(answers).most_common(1)[0]
    return top, count / len(answers)
