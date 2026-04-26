"""
research-dispatch.py — Claude SDK dispatcher for multi-source synthesis.
Input:  question (str), raw_data (list[dict]) — each dict has keys: source, content
Output: str — markdown synthesis with citations
"""
import anthropic
import json

client = anthropic.Anthropic()


def research_dispatch(question: str, raw_data: list[dict]) -> str:
    """Synthesize multi-source research findings using Claude Sonnet."""
    prompt = f"""<synthesis_task>
<question>{question}</question>
<raw_data>{json.dumps(raw_data, indent=2)}</raw_data>
<instructions>
- Identify key themes
- Flag contradictions
- Note claims with single-source support
- Output markdown with citations
</instructions>
</synthesis_task>"""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
