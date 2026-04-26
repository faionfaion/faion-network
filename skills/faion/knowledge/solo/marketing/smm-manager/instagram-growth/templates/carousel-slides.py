"""
Generate a 10-slide Instagram carousel text outline from a topic, key points, and CTA.
Input: topic (str), key_points (list of str), cta (str)
Output: list of slide dicts with slide number, type, and text.

Usage (as module):
  from carousel_slides import carousel_slides
  slides = carousel_slides("Instagram growth", ["Post Reels daily", "Engage 30 min/day"], "Follow for weekly tips")
"""


def carousel_slides(topic: str, key_points: list[str], cta: str) -> list[dict]:
    """Produce a 10-slide carousel text outline."""
    slides = [
        {"slide": 1, "type": "Hook", "text": f"The complete guide to {topic}"},
        {"slide": 2, "type": "Promise", "text": f"In this carousel: {', '.join(key_points[:3])}"},
    ]
    for i, point in enumerate(key_points, start=3):
        slides.append({"slide": i, "type": "Value", "text": point})
        if len(slides) >= 9:
            break
    slides.append({
        "slide": len(slides) + 1,
        "type": "Summary",
        "text": "To recap: " + " | ".join(key_points[:5]),
    })
    slides.append({"slide": len(slides) + 1, "type": "CTA", "text": cta})
    return slides


if __name__ == "__main__":
    example = carousel_slides(
        "Instagram growth",
        ["Post Reels daily", "Engage 30 min/day", "Use DM triggers", "Track reach %, not followers"],
        "Follow for weekly growth tips",
    )
    for s in example:
        print(f"Slide {s['slide']} [{s['type']}]: {s['text']}")
