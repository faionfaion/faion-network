# purpose: measure interviewer word-share + flag dominance windows
# consumes: transcript = list of {"speaker": str, "text": str}
# produces: dict[speaker, ratio] + list of dominated window start indices
# depends-on: stdlib only
# token-budget-impact: 0 (runs locally, no LLM call)


def speaker_ratio(transcript: list[dict]) -> dict[str, float]:
    """
    Measure word-share per speaker from a labeled transcript.

    Input:
        transcript: list of {"speaker": "INTERVIEWER"|"INTERVIEWEE", "text": "..."}

    Output:
        dict mapping speaker name to word-share float (0.0 to 1.0)

    Rule: if ratio["INTERVIEWER"] > 0.20 in any 3-turn window, flag as dominated.
    """
    from collections import defaultdict
    counts: dict[str, int] = defaultdict(int)
    for turn in transcript:
        counts[turn["speaker"]] += len(turn["text"].split())
    total = sum(counts.values()) or 1
    return {k: round(v / total, 3) for k, v in counts.items()}


def check_dominance(transcript: list[dict], window: int = 3) -> list[int]:
    """
    Return start indices of 3-turn windows where INTERVIEWER word-share > 20%.
    """
    dominated = []
    for i in range(len(transcript) - window + 1):
        window_turns = transcript[i:i + window]
        ratio = speaker_ratio(window_turns)
        if ratio.get("INTERVIEWER", 0) > 0.20:
            dominated.append(i)
    return dominated


# Usage example:
# transcript = [
#     {"speaker": "INTERVIEWER", "text": "How does that affect your team?"},
#     {"speaker": "INTERVIEWEE", "text": "It slows everything down..."},
# ]
# print(speaker_ratio(transcript))
# print(check_dominance(transcript))
