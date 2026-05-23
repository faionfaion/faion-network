# purpose: Pre-existing template carried into the generative-ui-design methodology
# consumes: See content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml for produces=spec
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

"""Generate multiple UI variants via Claude API in a single batch.

Input:  screen_brief   — description of the screen to generate
Output: variant_*.tsx  — one React file per variant style
"""
import anthropic

client = anthropic.Anthropic()

VARIANTS = ["minimal", "warm-approachable", "information-dense"]


def generate_ui_variant(screen_brief: str, variant_style: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate a React functional component for: {screen_brief}.\n"
                    f"Style: {variant_style}. Mobile-first. WCAG AA. Tailwind CSS.\n"
                    "Output only the component code, no explanation.\n"
                    "Add comment: // AI-generated — review before production"
                ),
            }
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    brief = "email verification screen, step 2 of onboarding"
    for style in VARIANTS:
        code = generate_ui_variant(brief, style)
        filename = f"variant_{style.replace('-', '_')}.tsx"
        with open(filename, "w") as f:
            f.write(code)
        print(f"Written: {filename}")
