"""
Generate structured prompts for Adobe Firefly Services batch API.
Input: content_brief.json + brand_guide.json
Output: JSON array of batch generation payloads.
Usage: python batch-prompt-generator.py content_brief.json brand_guide.json
"""
import json
import sys


def generate_firefly_prompts(brief: dict, brand: dict) -> list:
    """
    Generate Firefly Services batch API payloads from a content brief and brand guide.
    Each asset in the brief produces one payload entry.
    """
    payloads = []
    style = brand.get("style", "clean, professional")
    color_desc = brand.get("color_palette_description", "")
    exclude = brand.get("exclude", "")

    for asset in brief.get("assets", []):
        subject = asset.get("subject", "")
        context = asset.get("context", "")
        content_class = asset.get("content_class", "photo")

        positive = f"{subject}, {style}, {color_desc}, {context}".strip(", ")
        negative = f"text, watermark, logo, low quality, blurry"
        if exclude:
            negative += f", {exclude}"
        if content_class == "illustration":
            negative += ", realistic photo, photography"

        payload = {
            "asset_id": asset.get("id", f"asset_{len(payloads)}"),
            "firefly_params": {
                "prompt": positive[:200],  # Firefly max prompt length
                "negativePrompt": negative[:200],
                "size": {
                    "width": asset.get("width", 1200),
                    "height": asset.get("height", 630),
                },
                "numVariations": asset.get("variants", 3),
                "contentClass": content_class,
                "styles": {"presets": [brand.get("style_preset", "photo")]},
            },
        }
        payloads.append(payload)

    return payloads


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python batch-prompt-generator.py <content_brief.json> <brand_guide.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        brief = json.load(f)
    with open(sys.argv[2]) as f:
        brand = json.load(f)

    batch = generate_firefly_prompts(brief, brand)
    print(json.dumps(batch, indent=2))
    print(f"\nGenerated {len(batch)} batch payload(s)")
    total_variants = sum(p["firefly_params"]["numVariations"] for p in batch)
    print(f"Estimated credit consumption: {total_variants} credits")
