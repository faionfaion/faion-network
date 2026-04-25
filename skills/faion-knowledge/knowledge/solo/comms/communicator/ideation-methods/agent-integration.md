# Agent Integration — Ideation Methods

## When to use
- SCAMPER: improving an existing product, feature, or process by systematically applying 7 transformation lenses
- Mind Mapping: visualizing a complex topic's structure before writing a spec, planning a launch, or preparing a presentation
- Starbursting: generating the full question set for a new project, feature, or decision before committing to an approach
- Combining methods: SCAMPER → idea shortlist → Mind Map to show relationships → Starbursting to validate unknowns

## When NOT to use
- When the problem is fully defined and the solution is constrained — structured ideation adds noise, not signal
- SCAMPER applied to services with strict regulatory requirements (medical, financial) — "Eliminate" and "Reverse" lenses can produce ideas that are immediately non-viable, wasting evaluation cycles
- Mind Mapping as a communication artifact for stakeholders who expect linear docs — the format is for generative thinking, not presentation
- Starbursting when the project timeline requires immediate action; generating 30+ questions delays execution

## Where it fails / limitations
- SCAMPER agent runs tend to produce thin output for "Put to Other Uses" and "Reverse" lenses — these require more lateral thinking than LLMs reliably provide in a single pass
- Mind Mapping generated as text (nested bullets) loses the spatial-connection benefit of the visual format; the relationships between branches are the value, not the node content
- Starbursting generates questions but cannot answer them — the output is an unknown inventory, not a resolution
- Combining methods sequentially (SCAMPER → Mind Map → Starbursting) produces long multi-step outputs; context length and coherence degrade across steps
- 5-10 minutes "per SCAMPER lens" is a human timing assumption — agents generate all 7 lenses in one pass, which reduces cross-lens inspiration

## Agentic workflow
For SCAMPER: agent receives a product/service description and applies all 7 lenses in a structured batch, producing 3-5 ideas per lens. A second pass scores the full list by novelty × feasibility and returns a top-10 shortlist. For Starbursting: agent receives an idea and generates 5 questions per 5W+H category (30 total), then ranks the top 10 by decision-criticality. For Mind Mapping: agent produces a nested JSON structure (parseable by Miro/Obsidian importers) rather than ASCII art.

### Recommended subagents
- General Claude Opus call — SCAMPER "Reverse" and "Put to Other Uses" lenses; lateral thinking quality matters
- General Claude Sonnet call — Starbursting question generation and Mind Map JSON structure; structured output task
- `faion-brainstorm` — when combining all three methods in a full ideation sprint with review gate

### Prompt pattern
SCAMPER structured pass:
```
Apply SCAMPER to: <PRODUCT_SERVICE_DESCRIPTION>.
For each lens (S/C/A/M/P/E/R), generate exactly 4 ideas.
Format per lens:
**[LENS NAME]**
1. [idea]
2. [idea]
3. [idea]
4. [idea]
No explanations inline. No overlap between lenses.
```

Starbursting question bank:
```
Generate a Starbursting question bank for: <IDEA>.
5 questions per category: WHO / WHAT / WHERE / WHEN / WHY / HOW.
Prioritize questions where the answer is genuinely unknown and decision-critical.
Output: table with columns [Category | Question | Why it matters].
```

Mind Map as structured JSON (Miro-importable):
```
Generate a mind map for: <TOPIC> as JSON.
Schema: {"center": "topic", "branches": [{"name": "branch", "children": ["sub1", "sub2"]}]}
Maximum 6 branches, 4 children per branch.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `xmind-cli` | Import JSON mind map to XMind format | https://xmind.app/developer/ |
| `markmap-cli` | Convert markdown mind maps to interactive HTML | `npm install -g markmap-cli` |
| `miro-api` (Node SDK) | Programmatic Miro board creation from SCAMPER/Starbursting output | `npm install @mirohq/miro-api` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Miro | SaaS | Partial — REST API | Create sticky notes, frames, and basic shapes via API; mind map layout is manual |
| MindMeister | SaaS | Yes — REST API | Full mind map CRUD via API; best for automated map creation |
| XMind | OSS/SaaS | Via JSON import | No REST API; import via `.xmind` file format |
| Whimsical | SaaS | No public API | Human-only; best design quality |
| Obsidian | OSS | Via MCP or file write | Write markdown files with `[[wikilinks]]` for mind-map-style connections |
| Notion | SaaS | Yes — REST API | Store SCAMPER worksheets and Starbursting outputs as database items |

## Templates & scripts
See `templates.md` for the SCAMPER Worksheet and Starbursting Template.

SCAMPER idea scorer (novelty × feasibility):
```python
def score_scamper_ideas(ideas: list[dict]) -> list[dict]:
    """
    ideas: list of {"lens": str, "idea": str, "novelty": int, "feasibility": int}
    novelty/feasibility: 1-5 integer ratings (human-assigned or LLM-estimated)
    Returns sorted by combined score descending.
    """
    for idea in ideas:
        idea["score"] = idea["novelty"] * idea["feasibility"]
    return sorted(ideas, key=lambda x: x["score"], reverse=True)
```

Markmap quick render:
```bash
# Convert a markdown mind map to interactive HTML
echo "# Product Launch
## Team
### Roles
### Hiring
## Marketing
### Channels
### Content" | markmap --no-open - > mindmap.html
```

## Best practices
- Run SCAMPER lens-by-lens with separate prompts if quality is low in a batch pass; "Reverse/Rearrange" and "Put to Other Uses" benefit most from isolated focus.
- Starbursting output should be ranked by "what happens if we don't know the answer?" — questions with unknown, high-consequence answers are the most valuable; low-stakes knowns are noise.
- For Mind Mapping, generate the JSON structure and import into a visual tool rather than working in ASCII — spatial layout is where the value is.
- Combine SCAMPER + Starbursting: run SCAMPER to generate ideas, then Starbursting to generate questions about the top-scored ideas. This surfaces viability unknowns early.
- Store SCAMPER worksheets per product version; re-running SCAMPER on the same product 6 months later with new constraints often surfaces different high-value ideas.

## AI-agent gotchas
- SCAMPER "Eliminate" lens produces ideas that are trivially obvious ("remove the manual step") or that break the core product ("remove the login"); add a filter for "ideas that eliminate the product's primary value" before scoring.
- Agents will reuse ideas across SCAMPER lenses (e.g., "subscription model" appearing under both Modify and Reverse); enforce uniqueness across lenses in the prompt.
- Starbursting generates 30 questions but LLMs rank them by interestingness to the model, not decision-criticality for the project; human must re-rank by actual stakes.
- Mind Map JSON output often has too-flat structures (all ideas as direct children of center) or too-deep (5+ levels); specify max depth and max breadth in the prompt.
- Human checkpoint required: the top-10 Starbursting questions must be reviewed before research or development begins — LLMs will sometimes surface "interesting" questions that are actually irrelevant to the decision at hand.

## References
- Eberle, B. (1996). SCAMPER: Creative Games and Activities for Imagination Development. Prufrock Press.
- Buzan, T. (1974). Use Both Sides of Your Brain. Dutton.
- Stanford d.school Methods: https://dschool.stanford.edu/resources
- MindMeister API: https://www.mindmeister.com/api
- Markmap docs: https://markmap.js.org
