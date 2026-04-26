"""
Keyword-based signal classifier for post-interview note processing.
Input: list of statement strings from interview notes.
Output: list of dicts with statement and matched signal types.

Signal types:
  PROBLEM       — interviewee describes pain or friction
  CURRENT_SOL   — interviewee describes what they use now
  COMMITMENT    — interviewee offers time, reputation, or money
  RED_FLAG      — hypothetical language, predicts unreliable signal
  COMPLIMENT    — positive but non-committal (discard for validation)
"""

SIGNAL_KEYWORDS: dict[str, list[str]] = {
    "PROBLEM": ["struggle", "hard", "frustrating", "pain", "waste", "annoying", "broken", "hate"],
    "CURRENT_SOL": ["I use", "we use", "currently", "right now", "we pay", "we spend", "we rely"],
    "COMMITMENT": ["introduce", "pilot", "deposit", "beta", "send you", "schedule", "sign", "prepay"],
    "RED_FLAG": ["would", "might", "probably", "I think I'd", "generally", "usually I'd"],
}


def classify_statement(statement: str) -> list[str]:
    lower = statement.lower()
    matched = [
        signal
        for signal, keywords in SIGNAL_KEYWORDS.items()
        if any(kw in lower for kw in keywords)
    ]
    return matched if matched else ["COMPLIMENT"]


def classify_interview(statements: list[str]) -> list[dict]:
    return [
        {"statement": s, "signals": classify_statement(s)}
        for s in statements
    ]
