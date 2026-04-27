"""
Generate minimal APL list card JSON for Amazon Echo Show.
Input: title (str), items (list of dicts with 'label' and optional 'speech'), spoken_summary (str).
Output: APL document dict (serialize to JSON for deployment).
"""
import json


def make_apl_card(title: str, items: list[dict], spoken_summary: str) -> dict:
    """Generate a minimal APL 1.9 list card for Echo Show."""
    return {
        "type": "APL",
        "version": "1.9",
        "document": {
            "type": "APL",
            "mainTemplate": {
                "item": {
                    "type": "Container",
                    "items": [
                        {"type": "Text", "text": title, "style": "textStyleHeading"},
                        {
                            "type": "Sequence",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": item["label"],
                                    "speech": item.get("speech", item["label"]),
                                }
                                for item in items
                            ],
                        },
                    ],
                }
            },
        },
        "datasources": {"spoken_summary": spoken_summary},
    }


if __name__ == "__main__":
    card = make_apl_card(
        title="Pasta Recipes",
        items=[
            {"label": "Spaghetti Bolognese"},
            {"label": "Cacio e Pepe"},
        ],
        spoken_summary="I found 2 pasta recipes.",
    )
    print(json.dumps(card, indent=2))
