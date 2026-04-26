# Agent Integration — AI-Assisted Persona Building

## When to use
- You have existing user data (analytics, interview transcripts, survey responses, support tickets) to cluster
- You need to synthesize personas from multi-source data faster than manual affinity mapping allows
- A product team wants data-backed personas, not assumption-driven archetypes
- You are updating stale personas after a major product pivot or new market entry
- You are running a Jobs-to-be-Done (JTBD) framing exercise alongside persona creation

## When NOT to use
- You have zero real user data — AI will hallucinate plausible-sounding but false personas
- The product is in pure pre-discovery (no interviews, no analytics yet)
- Regulatory context prohibits feeding user data to third-party LLMs (HIPAA, GDPR special categories)
- The team needs only 1–2 archetypes from a single homogeneous user segment — manual synthesis is faster

## Where it fails / limitations
- AI clusters behavioral patterns but cannot infer motivation without interview quotes or qualitative input
- Quantified impact fields ("saves 3 hours/week") require actual measurement data; AI will fabricate numbers if none supplied
- Sentiment pattern extraction is unreliable for short text samples (<50 responses) — clusters degrade to noise
- Trigger analysis requires longitudinal data; single-point surveys produce flat, undifferentiated personas
- LLMs over-index on articulate user quotes; silent users who churn silently are systematically under-represented
- Persona freshness decays fast; AI-generated personas go stale as fast as their source data

## Agentic workflow
A Claude subagent ingests structured user data (CSV exports from analytics, JSON interview transcripts, survey CSVs), performs k-means-style behavioral segmentation via structured prompting, and outputs draft persona cards in JSON or Markdown. A second pass with a validation agent checks each persona for internal consistency and flags missing JTBD dimensions. Human researchers review, edit, and approve before personas enter any design system or decision process.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the structured synthesis pipeline end-to-end (data in → persona JSON out)
- General Claude subagent (Sonnet) — behavioral clustering and draft generation
- General Claude subagent (Haiku) — persona card formatting and documentation

### Prompt pattern
```
You are a UX research analyst. Given the following user interview transcripts and analytics segments,
identify 3–5 distinct behavioral clusters. For each cluster output:
- Cluster label
- Core JTBD statement (When [situation], I want to [motivation], So I can [outcome])
- Top 3 pain points with severity (High/Med/Low)
- Trigger events that activate product usage
- Representative verbatim quote
Output as JSON array. Do not invent data not present in the input.
```

```
You are reviewing persona drafts for internal consistency. For each persona check:
1. Is the JTBD statement consistent with the pain points listed?
2. Are the behavior patterns plausible given the demographics?
3. Flag any fields that appear fabricated rather than data-derived.
Output issues as a numbered list per persona.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` | Transform analytics JSON exports before feeding to LLM | `apt install jq` / jq.dev |
| `csvkit` | Convert survey CSV to normalized JSON for LLM input | `pip install csvkit` / csvkit.rtfd.io |
| `python-docx` / `pypdf` | Extract interview transcripts from Word/PDF files | `pip install python-docx pypdf` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS (qualitative research) | Partial — REST API for notes/tags | Export tags + themes as input to LLM clustering |
| Maze | SaaS (usability/surveys) | Yes — CSV/JSON export | Good survey data source for segmentation |
| Mixpanel / Amplitude | SaaS (analytics) | Yes — API / CSV export | Behavioral event data for cluster features |
| Notion | SaaS (docs) | Yes — API | Store validated persona cards; agents can read/update |
| Airtable | SaaS (structured DB) | Yes — REST API | Structured persona registry; agent-updatable |
| Atlas (Anthropic) | SaaS (LLM ops) | Yes | Track persona generation prompts for auditability |

## Templates & scripts
See `templates.md` for the 5-section persona card template (demographics, JTBD, pain points, triggers, quotes).

Inline preprocessing script (normalizes interview JSON for LLM input):
```python
import json, sys, pathlib

def normalize_interviews(paths: list[str]) -> list[dict]:
    records = []
    for p in paths:
        raw = json.loads(pathlib.Path(p).read_text())
        for segment in raw.get("segments", [raw]):
            records.append({
                "user_id": segment.get("user_id", "anon"),
                "quote": segment.get("transcript", ""),
                "tags": segment.get("tags", []),
                "session_date": segment.get("date", ""),
            })
    return records

if __name__ == "__main__":
    result = normalize_interviews(sys.argv[1:])
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

## Best practices
- Always supply real verbatim quotes as grounding material; forbid LLM from adding quotes not present in input
- Run two clustering passes: first by behavior (what users do), then by motivation (why they do it) — merge results manually
- Limit each persona to 1 core JTBD statement; multiple JTBDs signal the cluster should be split
- Version personas with a date and data source reference so staleness is visible
- Validate AI-generated quantified claims (time saved, frequency) against actual analytics before publishing
- Store persona JSON in a structured registry (Airtable, Notion DB) so agents can query and update incrementally
- Never use AI personas as the sole input for major product decisions — require at least 1 round of human interview validation

## AI-agent gotchas
- LLMs confidently hallucinate demographic details when given only behavioral data — require explicit "only use provided data" constraint in prompt
- Clustering quality degrades sharply with <30 data points per segment; instruct agent to flag thin clusters rather than force-fit
- Agent may merge two legitimately distinct segments if their surface language is similar — require explicit cluster-separation justification
- JTBD extraction requires first-person voice in input; passive/third-person interview notes produce weak statements — preprocess before feeding
- Iterative persona updates (new data → update existing personas) require the agent to receive the prior persona JSON explicitly; without it, the agent restarts clustering from scratch and produces inconsistent results
- Human-in-loop checkpoint required before personas enter design system or stakeholder decks

## References
- Clayton Christensen, "Competing Against Luck" (Jobs-to-be-Done framework)
- Nielsen Norman Group: https://www.nngroup.com/articles/persona/
- Dovetail Research Repository: https://dovetail.com
- Anthropic Claude API (structured output): https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs
