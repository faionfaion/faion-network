#!/usr/bin/env python3
"""
Interview transcript tagger using Anthropic SDK.
Input (stdin): plain text interview transcript
Output (stdout): JSON with per-turn labels and overall hierarchy level score.
Requires: anthropic (pip install anthropic), ANTHROPIC_API_KEY env var set.
Usage: cat interview.txt | python3 transcript-tagger.py
"""
import json
import sys
import anthropic

SYSTEM = """Tag each turn in the transcript as one of:
- COMPLIMENT: flattery about the idea ("great idea", "love this")
- HYPOTHETICAL: future/conditional intent ("I would", "I'd probably", "might use")
- GENERIC: non-specific broad claims ("everyone", "nobody does this well")
- SPECIFIC_PAST: concrete past experience with evidence
- COMMITMENT: actual commitment with type (time|reputation|money) and strength 1-5

For each turn return:
{speaker, text_excerpt (max 100 chars), label, hierarchy_level (1-5), quote_evidence}

Hierarchy levels:
1 = user paid for a solution
2 = user committed (signed up, LOI, time investment)
3 = user engaged with prototype
4 = user expressed strong interest
5 = user said they have the problem

Return a JSON object with:
{turns: [...], overall_hierarchy_level: 1-5, commitment_count: int, red_flag_count: int}"""

transcript = sys.stdin.read()
if not transcript.strip():
    print(json.dumps({"error": "empty transcript"}))
    sys.exit(1)

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    system=SYSTEM,
    messages=[{"role": "user", "content": transcript}],
)

print(response.content[0].text)
