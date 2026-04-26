# methodology_router.py — route a research question to the correct methodology
# Input:  a research question string
# Output: matched methodology name

KEYWORDS: dict[str, list[str]] = {
    "jtbd": ["why", "motivation", "hired", "fired", "switched", "accomplish", "trying to"],
    "persona": ["who", "segment", "type of user", "demographics", "behaviors"],
    "problem_validation": ["does this problem exist", "is it real", "how painful", "validate hypothesis"],
    "pain_mining": ["where", "complaints", "frustration", "reddit", "reviews", "forum"],
}


def route(question: str) -> str:
    q = question.lower()
    scores = {k: sum(1 for kw in kws if kw in q) for k, kws in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unclear — clarify the research question"


if __name__ == "__main__":
    print(route("Why do users switch to a competitor?"))         # → jtbd
    print(route("Who are our typical users?"))                   # → persona
    print(route("Is the invoice pain real for freelancers?"))    # → problem_validation
    print(route("What do people complain about on Reddit?"))     # → pain_mining
