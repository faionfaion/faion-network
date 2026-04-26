# Agent Integration — Customer Journey Mapping

## When to use
- Before a major product redesign to document the baseline experience and identify the biggest pain points
- When multiple teams own different parts of the experience and no one sees the full picture
- When support data or NPS verbatims indicate friction but the location within the journey is unclear
- When entering a new market segment and the team needs to understand how a different persona experiences the product
- When preparing a cross-functional workshop to align stakeholders on experience priorities

## When NOT to use
- As the first UX activity on a new product — there is no journey to map without research; build the research foundation first
- When the goal is to fix a specific UI element — journey mapping is for systemic problems across stages, not individual screens
- When the team cannot access real user research (interviews, analytics, support data) — a map built from assumptions is a fiction document, not a research artifact
- When no stakeholder has authority to act on the findings — maps without committed owners produce posters, not change

## Where it fails / limitations
- Journey maps are snapshots; customer behavior changes faster than maps are updated — stale maps get cited in decisions they no longer support
- Emotion curves are often added as decoration rather than derived from research; teams draw what they expect users to feel, not what research reveals
- Maps collapse the diversity of user experiences into a single persona path, masking segment-level differences that matter for prioritization
- The workshop format creates false consensus — participants agree on the map in the room but interpret priorities differently when they return to their teams
- B2B journey maps are especially unreliable because the "user" (the person doing the task) and the "decision-maker" (who defines success) are different people

## Agentic workflow
A Claude subagent is effective at two stages: (1) synthesizing raw research inputs (interview transcripts, support ticket summaries, analytics event sequences) into a structured journey map draft, and (2) generating the opportunity prioritization section from a completed map by scoring pain points against impact and frequency. The agent produces a Markdown or JSON draft that a designer then visualizes; the visual design of the map is a human task. Emotion curve data must come from research, not from the agent — the agent should flag where emotion data is missing rather than inferring it.

### Recommended subagents
- Any general-purpose Claude subagent (Opus preferred) — synthesize research into map stages, identify pain points, generate opportunity prioritization
- `faion-sdd-executor-agent` — convert prioritized opportunities into implementation tasks after the map is validated

### Prompt pattern
```
You are a UX researcher synthesizing customer journey data. Given the research inputs below, produce a structured journey map in JSON.

Output schema per stage:
{
  "stage": "string",
  "user_goal": "string",
  "actions": ["string"],
  "touchpoints": ["string"],
  "thoughts": ["string"],
  "emotions": "string | null (null if no research data)",
  "pain_points": [{ "description": "string", "evidence": "string", "severity": "high|medium|low" }],
  "opportunities": ["string"]
}

Persona: [description]
Journey scope: [start] to [end]
Research inputs:
- Interview summaries: [text]
- Support ticket themes: [text]
- Analytics drop-off points: [text]
- Survey verbatims: [text]
```

```
You are prioritizing opportunities from a customer journey map. For each opportunity below, score it on:
- user_impact: 1–5 (how much it improves user experience)
- frequency: 1–5 (how many users encounter this friction)
- effort: 1–5 (engineering complexity, 5 = highest effort)
- priority_score: (user_impact * frequency) / effort

Return sorted by priority_score descending with a brief rationale for the top 5.

Opportunities: [list from journey map]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-js` | Generate journey map diagrams as code (text → SVG) | `npm i -g @mermaid-js/mermaid-cli` / [mermaid.js.org](https://mermaid.js.org) |
| `python-docx` / `openpyxl` | Export journey map data from Python to Word/Excel for stakeholder sharing | `pip install python-docx openpyxl` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Miro | SaaS | Yes — REST API | Journey map templates; agents can create boards and add sticky notes via API |
| FigJam | SaaS | Partial | Journey map templates; limited API for automation |
| Smaply | SaaS | Partial — export | Dedicated journey mapping tool; exports to PDF/image; no write API |
| UXPressia | SaaS | Partial — export | Journey + persona + impact map; CSV export; no write API |
| Confluence | SaaS | Yes — REST API | Agents can publish structured journey map Markdown to Confluence pages via API |
| Hotjar | SaaS | Yes — API | Session recordings and heatmaps provide evidence for specific journey stages |

## Templates & scripts
See `README.md` for Journey Map and Stage Detail templates.

Script — generate a Mermaid journey diagram from a JSON map:
```python
#!/usr/bin/env python3
"""
Usage: python journey_to_mermaid.py map.json > diagram.mmd
Then: mmdc -i diagram.mmd -o journey.svg
"""
import json, sys

def to_mermaid(map_data):
    persona = map_data.get("persona", "User")
    lines = ["journey", f'  title {persona} Journey']
    for stage in map_data["stages"]:
        lines.append(f'  section {stage["stage"]}')
        for action in stage.get("actions", [])[:3]:
            lines.append(f'    {action[:40]}: 5: {persona}')
    return "\n".join(lines)

if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    print(to_mermaid(data))
```

## Best practices
- Ground every emotion score in a research quote or observation — if you cannot cite evidence, mark emotion as unknown and note it as a research gap
- Map the current state before designing the future state — teams that jump to future state skip the diagnostic step and miss the real problems
- Limit stages to 5–8 — more than 8 stages signals the scope is too broad or the stage boundaries are not meaningful
- Share the draft map with 2–3 research participants for a "member check" before using it to drive decisions — they often correct assumptions that felt obvious internally
- Date every journey map version — maps without dates get treated as current truth long after they are outdated
- Link each pain point to a specific metric (NPS score, drop-off rate, support ticket volume) so prioritization is quantified, not just directional

## AI-agent gotchas
- Agents will invent emotion data if research inputs are thin or absent — explicitly instruct the agent to set emotions to null and flag gaps rather than infer
- Journey maps synthesized from only one data type (e.g., only interview transcripts) miss what other sources would reveal; agents should note which stages lack multi-source validation
- When agents process long interview transcripts, they tend to over-weight the most dramatic moments rather than the most frequent ones; ask for frequency counts alongside pain point descriptions
- Agents cannot determine journey stage boundaries from raw data — the stage definition is a human decision that must be provided before synthesis
- Future-state journey maps generated entirely by an agent without grounding in research produce aspirational fiction; require the agent to cite which current-state problems each future-state improvement addresses

## References
- [Journey Mapping 101 — NNG](https://www.nngroup.com/articles/journey-mapping-101/)
- [Mapping Experiences — Jim Kalbach (O'Reilly)](https://www.oreilly.com/library/view/mapping-experiences/9781491923528/)
- [When and How to Create Customer Journey Maps — NNG](https://www.nngroup.com/articles/customer-journey-mapping/)
- [Miro Journey Map Templates](https://miro.com/templates/customer-journey-map/)
- [This Is Service Design Doing — Stickdorn et al.](https://www.thisisservicedesigndoing.com/)
