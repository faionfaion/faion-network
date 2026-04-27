"""Generate Content Reel-compatible JSON data file.

Output: JSON string → paste into Content Reel > Custom Data in Figma.
"""
import json


def generate_content_reel_data(names: list[str], emails: list[str]) -> str:
    """Produce Content Reel-compatible JSON for user profile content."""
    entries = [
        {"Name": n, "Email": e, "Avatar": f"https://i.pravatar.cc/150?u={e}"}
        for n, e in zip(names, emails)
    ]
    return json.dumps({"data": entries}, indent=2)


# Review names for i18n/diversity before using in stakeholder-facing designs.
sample = generate_content_reel_data(
    names=["Alice Martin", "Bob Chen", "Carla Rossi"],
    emails=["alice@co.com", "bob@co.com", "carla@co.com"],
)
print(sample)
