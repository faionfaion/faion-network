# jtbd_parser.py — extract JTBD statement components from raw interview notes
# Input:  free-form interview notes as a string
# Output: situation, action, outcome components
import re


def parse_jtbd(text: str) -> dict:
    """Extract When/I want/So I can from raw interview notes."""
    patterns = {
        "situation": r"(?:when|whenever|after)\s+(.+?)(?:\.|,|I want)",
        "action": r"(?:I want(?:ed)? to|need to)\s+(.+?)(?:\.|,|so)",
        "outcome": r"(?:so (?:I|that I) can|in order to)\s+(.+?)(?:\.|$)",
    }
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        result[key] = match.group(1).strip() if match else "NOT FOUND"
    return result


if __name__ == "__main__":
    notes = (
        "When I finish a project, I want to send a professional invoice quickly "
        "so I can get paid faster."
    )
    parsed = parse_jtbd(notes)
    print(f"Situation: {parsed['situation']}")
    print(f"Action:    {parsed['action']}")
    print(f"Outcome:   {parsed['outcome']}")
