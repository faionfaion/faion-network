# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Claude prompt caching with cache_control header.
The static system prompt prefix must be >=2048 tokens to activate caching.
Place ALL dynamic content AFTER the cached static prefix.
"""
import anthropic

client = anthropic.Anthropic()

# Static system prompt (must be >=2048 tokens to activate cache)
STATIC_SYSTEM_PROMPT = """You are an expert analyst. [... 2000+ tokens of static context ...]"""


def analyze_with_cache(user_query: str) -> str:
    """
    Call Claude with prompt caching on the static system prompt.
    Second and subsequent calls with the same prefix pay cache read cost (~10% of full input).
    """
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": STATIC_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # Cache this prefix
            }
        ],
        messages=[{"role": "user", "content": user_query}],
    )

    # Check if cache was used
    usage = response.usage
    cache_hit = hasattr(usage, "cache_read_input_tokens") and usage.cache_read_input_tokens > 0

    return response.content[0].text
