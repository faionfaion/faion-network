# Agent Integration — Customer Journey Mapping

## When to use
- Designing or redesigning a multi-step user flow (onboarding, checkout, support, offboarding)
- After collecting user interviews or analytics data that reveal pain points across touchpoints
- Before a product discovery sprint to align stakeholders on the current user experience
- When handoff problems appear between channels (web → email → app → support)
- Evaluating a new feature's impact on the broader experience, not just its own screen

## When NOT to use
- You have no research data — a purely imagined journey map has negative value (creates false consensus)
- The product is a single, isolated interaction with no multi-step journey
- You need to understand why users behave a certain way (use user interviews or usability testing instead)
- Stakeholders want quantitative evidence — journey maps are qualitative synthesis, not metrics

## Where it fails / limitations
- Maps go stale quickly; a map from last quarter may contradict current analytics
- The emotional arc (happy/sad scores) is often invented rather than observed, undermining credibility
- Cross-channel journeys are hard to validate without real omnichannel analytics (session replay only shows one channel)
- Maps created by one person without research become advocacy documents, not insight tools
- Service blueprint extensions (backstage processes) require organizational data agents cannot self-generate

## Agentic workflow
An agent can synthesize journey maps from structured research inputs: transcripts, support ticket exports, analytics funnel CSVs, and NPS comments. Feed the agent a corpus of evidence per stage, and it outputs a structured map (stage × row matrix). The agent identifies the emotional arc and pain-point clusters from sentiment in the source text. Human review is mandatory before the map is shared with stakeholders — the agent cannot validate whether emotional attributions match real user intent.

### Recommended subagents
- `faion-ux-researcher-agent` — scrapes and synthesizes research inputs (interviews, tickets, analytics exports) into stage-level summaries before the map is assembled
- `faion-usability-agent` — validates each touchpoint against heuristics to pre-annotate pain points

### Prompt pattern
```
Given the following user interview excerpts and support ticket summaries, produce a journey map
for the [persona] doing [journey]. Output a markdown table with rows:
Stages | Actions | Touchpoints | Thoughts | Emotions (1-5) | Pain Points | Opportunities
Base every cell on cited evidence from the input. If no evidence exists for a cell, write "no data".
```

```
Analyze the attached analytics funnel (CSV). For each drop-off step, infer likely user frustration
causes and list them as Pain Points. Cross-reference with the NPS verbatims provided.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` | Parse analytics JSON exports into stage-level summaries | `apt install jq` / jq.org |
| `csvkit` | Convert funnel CSVs to structured data for agent ingestion | `pip install csvkit` / csvkit.rtfd.io |
| `airtable-cli` | Push completed journey map rows to Airtable for team sharing | `npm i -g airtable-cli` / github.com/nicogalin/airtable-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Miro | SaaS | Partial — REST API for board creation, not visual layout | Good for collaborative workshops; agent can push text content via API, not draw swimlanes |
| FigJam | SaaS | No public API | Human-only authoring; agent prepares content, human pastes |
| Smaply | SaaS (journey-map-specific) | Partial — import CSV personas | Dedicated journey map tool with export; useful for final deliverable |
| Notion | SaaS | Yes — API can write table-structured maps | Agent can write and maintain maps as Notion databases with stage × row schema |
| Airtable | SaaS | Yes — full CRUD API | Best option for agent-maintained living journey maps with version history |
| Dovetail | SaaS | Partial — REST API for insights | Imports research data; agent can query tagged insights per stage |

## Templates & scripts
See `templates.md` for the full Journey Map and Stage Detail templates.

Inline helper — convert a funnel analytics CSV to stage summaries for agent input:
```python
import csv, sys, json

# Usage: python funnel_to_stages.py funnel.csv
# CSV columns: stage, sessions, drop_off_pct, avg_time_sec

def summarize(path):
    stages = []
    with open(path) as f:
        for row in csv.DictReader(f):
            stages.append({
                "stage": row["stage"],
                "sessions": int(row["sessions"]),
                "drop_off_pct": float(row["drop_off_pct"]),
                "avg_time_sec": int(row["avg_time_sec"]),
                "risk": "high" if float(row["drop_off_pct"]) > 30 else "normal"
            })
    print(json.dumps(stages, indent=2))

summarize(sys.argv[1])
```

## Best practices
- Scope narrowly: one persona + one journey per map. Combining two personas into one map hides differences.
- Cite sources per cell — every action, thought, and emotion must link to a research artifact (interview ID, ticket ID, analytics event).
- The emotional arc is the most valuable row: where it dips sharply is where to invest redesign effort.
- Run maps past the customer support team before finalizing — they see pain points daily that UX research misses.
- Treat maps as living documents: attach a "last validated" date and trigger a review when a major feature ships.
- Service blueprints extend journey maps to include backstage processes — if operational failures drive pain points, build the blueprint.
- Opportunities column should be tied to a backlog item or at least a hypothesis — a map without downstream action is waste.

## AI-agent gotchas
- Agents hallucinate emotions when no sentiment evidence exists in the corpus — always require "no data" as a valid cell value.
- Agents tend to smooth emotional arcs; real journeys have sharp dips. Prompt explicitly for variance.
- Without grounding data, agents produce generic journeys (Awareness → Purchase → Support) with no product-specific insight.
- Agents cannot observe users directly — journey maps based solely on agent inference must be treated as hypotheses, not findings.
- Stakeholder alignment on the map requires human facilitation; an agent-produced map sent cold to stakeholders often fails to create shared ownership.
- "Future state" maps generated by agents are design proposals, not research outputs — label them explicitly to avoid confusion.

## References
- https://www.nngroup.com/articles/journey-mapping-101/
- https://www.nngroup.com/articles/customer-journey-mapping/
- Mapping Experiences — Jim Kalbach (O'Reilly, 2nd ed.)
- This Is Service Design Doing — Stickdorn, Hormess, Lawrence, Schneider
- https://www.smaply.com/blog/journey-mapping-guide
