"""
triangulate.py — Claude SDK triangulator for TAM/SAM/SOM.
Input:  market_def (str), top_down_data (str), bottom_up_data (str)
Output: dict with tam/sam/som (low/mid/high), confidence, gap_driver, assumptions
Flags divergence >2x between the two paths.
"""
import anthropic
import json

client = anthropic.Anthropic()


def triangulate_market(
    market_def: str,
    top_down_data: str,
    bottom_up_data: str,
) -> dict:
    prompt = f"""<triangulation>
<market>{market_def}</market>
<top_down_findings>{top_down_data}</top_down_findings>
<bottom_up_findings>{bottom_up_data}</bottom_up_findings>
<instructions>
1. Compute TAM/SAM/SOM for each path independently.
2. If estimates differ by more than 2x, identify which assumption drives the gap.
3. Output JSON:
   {{
     "tam": {{"low": 0, "mid": 0, "high": 0, "unit": "USD billions"}},
     "sam": {{"low": 0, "mid": 0, "high": 0}},
     "som": {{"low": 0, "mid": 0, "high": 0}},
     "confidence": "low|medium|high",
     "gap_driver": "string or null",
     "assumptions": ["list of one-line assumptions"]
   }}
</instructions>
</triangulation>"""
    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(r.content[0].text)
