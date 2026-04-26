# build-persona.py — Transcript clustering → persona JSON with citation IDs
# Input: interviews/*.json (each with fields: id, transcript)
# Output: persona.json with {clusters[], primary_persona{...}, negative_persona{...}}
# Usage: python build-persona.py
# Requires: pip install anthropic

import json
from pathlib import Path

import anthropic

client = anthropic.Anthropic()

transcripts = [
    json.loads(p.read_text())
    for p in sorted(Path("interviews").glob("*.json"))
]

prompt = f"""
Inputs: {json.dumps(transcripts)[:80000]}

Task:
1. Cluster utterances by: Goals, Frustrations, Behaviours, Information Sources.
   For each cluster:
   - one-sentence pattern (customer language, no solutions)
   - supporting INT-ID list
   - 3 verbatim quotes (exact text, do not paraphrase)

2. Propose ONE primary persona using ONLY clusters with >=4 supporting interviews.
   Fields: name_label, role, goals[], frustrations[], buying_trigger (verbatim + INT-ID),
   quote (verbatim + INT-ID), falsification_clause.

3. Propose ONE negative persona: profile, reasons[], identifying_signals[], evidence[].

Forbidden:
- Inventing demographics, jobs, or quotes not present in the input.
- Proposing more than one primary persona without explicit instruction.
- Using any INT-ID not in the provided transcripts.

Output: JSON with fields {{clusters[], primary_persona{{}}, negative_persona{{}}}}.
"""

msg = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=8000,
    messages=[{"role": "user", "content": prompt}],
)

output_path = Path("persona.json")
output_path.write_text(msg.content[0].text)
print(f"Persona written to {output_path}")
