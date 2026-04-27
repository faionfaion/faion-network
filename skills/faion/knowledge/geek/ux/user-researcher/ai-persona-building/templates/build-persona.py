"""
Lightweight persona generation: user_type + data_points + jtbd → persona card Markdown.
Input: JSON on stdin with keys: user_type (str), data_points (list[str]), jtbd (str).
Output: persona card Markdown printed to stdout.
"""
import anthropic
import json
import sys

SYSTEM = (
    "You are a UX researcher. Create data-backed user personas. "
    "Only use provided data. Mark all inferred fields as [INFERRED — needs validation]. "
    "Output a persona card, not a user story."
)


def build_persona(user_type: str, data_points: list[str], jtbd: str) -> str:
    client = anthropic.Anthropic()
    points = "\n".join(f"- {d}" for d in data_points)
    prompt = (
        f"User type: {user_type}\n"
        f"Data points:\n{points}\n"
        f"JTBD: {jtbd}\n\n"
        "Output a persona card with sections: Name/Role, Demographics, Goals, "
        "Pain Points, Behavior Patterns, Trigger Events, Representative Quote. "
        "Mark any field not directly supported by the data points as [INFERRED — needs validation]."
    )
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


if __name__ == "__main__":
    spec = json.loads(sys.stdin.read())
    print(build_persona(spec["user_type"], spec["data_points"], spec["jtbd"]))
