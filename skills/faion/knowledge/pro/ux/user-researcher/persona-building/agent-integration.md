# Agent Integration — Persona Building

## When to use
- After running ≥10 customer interviews and the team needs a shared archetype to anchor product / marketing / sales decisions.
- A pivot or new market entry where the prior persona is stale and a fresh data-driven build is required.
- Pre-positioning a launch — to align messaging across landing page, ads, and onboarding.
- Internal alignment when product and sales describe customers in incompatible terms.
- Annual or post-pivot review of an existing persona library.

## When NOT to use
- Before any real research — fictional personas are worse than none.
- Where the audience is well-understood from quantitative data alone (analytics, CRM cohorts) and the team needs segments, not personas.
- For one-off campaigns where a single value-prop test would be cheaper.
- When team capacity is so small that the persona will not be referenced again — opportunity cost.
- For B2B enterprise sales with named accounts; account-based artefacts (ICPs, buyer maps) outperform personas.

## Agentic workflow
Use agents to extract patterns from interview transcripts, support tickets, and sales-call notes; cluster utterances by goals, frustrations, behaviours; produce candidate personas the team validates. Keep validation human (recognition tests with real customers); agents draft and refresh, humans ratify and prioritise. Pair persona output with the explicit data sources behind every claim — no claim without a citation back to interview ID, ticket ID, or analytics segment.

### Recommended subagents
- `faion-persona-builder-agent` — primary owner per `README.md`. Drives interview-pattern extraction and template fill.
- `faion-brainstorm` — diverges on candidate persona names + headlines, converges on memorable yet specific options.
- A `pattern-clusterer` subagent: takes JSON-tagged interview snippets and clusters by goals/frustrations/behaviours, emitting affinity tables.
- A `validator` subagent that compares persona predictions ("they would buy if X") against actual cohort behaviour from analytics.

### Where it fails / limitations
- LLM-generated personas trend toward stereotypes ("Marketing Mary, 35, lives in Brooklyn, drinks oat milk") that look polished but predict nothing.
- Persona-quote synthesis can drift into invented language; require quotes pulled verbatim from transcripts with source IDs.
- Demographic tropes overshadow goals/frustrations when models are not constrained.
- "Negative persona" is often skipped; agents must produce one or explicitly justify omission.
- Personas freeze; without a refresh cadence, decisions made in year 1 keep echoing in year 3 against a different reality.

### Prompt pattern
"Given the attached 14 interview transcripts (`INT-001..014`), cluster utterances about Goals, Frustrations, Buying Behaviour, and Information Sources. Propose at most 2 primary personas and 1 negative persona. For every bullet in each persona, cite the supporting interview IDs. Never invent demographic detail not present in the transcripts."

"Validate the proposed primary persona against analytics cohort `cohort_id=42` (CSV attached). For each behavioural claim, mark Confirmed / Contradicted / No-data."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Whisper / WhisperX | Transcribe interview audio | https://github.com/m-bain/whisperX |
| AssemblyAI / Deepgram | Hosted transcription + diarisation | https://www.assemblyai.com / https://deepgram.com |
| Dovetail / Marvin / Notably API | Pull tagged interviews | https://developers.dovetail.com |
| Notion / Airtable API | Persona repo CRUD | https://developers.notion.com / https://airtable.com/developers |
| `gpt-researcher` (OSS) | Literature scan for industry archetypes | https://github.com/assafelovic/gpt-researcher |
| Hugging Face `bertopic` | Topic clustering on transcripts | `pip install bertopic` |
| Posthog / Amplitude APIs | Behavioural validation against cohorts | https://posthog.com / https://amplitude.com/docs/apis |
| Anthropic / OpenAI SDKs | Pattern extraction calls | https://docs.anthropic.com |
| Streamlit | Quick persona viewer for stakeholders | `pip install streamlit` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Dovetail | SaaS | Yes (REST + AI) | Tagged-evidence source for personas |
| Marvin / EnjoyHQ | SaaS | Yes (REST) | Repo + AI summarisation |
| Notably | SaaS | Yes (AI-native) | Persona templates built-in |
| UserPersona.dev / Personas.app | SaaS | Limited | Light tools for solos, weak APIs |
| Xtensio / HubSpot Make My Persona | SaaS | Limited | Templates only, low API surface |
| Otter.ai / Fireflies.ai | SaaS | Yes (REST) | Sales-call transcription source |
| Gong / Chorus | SaaS | Yes (REST) | Sales-call goldmine for B2B personas |
| Zendesk / Intercom | SaaS | Yes (REST) | Support-ticket pattern source |
| Posthog | SaaS / OSS | Yes (REST) | Behavioural cohorts to validate |
| Reddit / Discord (with consent) | SaaS | Yes | Lifestyle / language-pattern source |

## Templates & scripts
See `templates.md` for full / lean / negative persona templates and `examples.md` for two worked examples.

Inline pattern extractor (Anthropic + transcripts → grouped JSON):

```python
# build_persona.py — clusters utterances and drafts persona JSON
import json, anthropic
from pathlib import Path

client = anthropic.Anthropic()
transcripts = [json.loads(p.read_text()) for p in Path("interviews").glob("*.json")]

prompt = f"""
Inputs: {json.dumps(transcripts)[:80000]}
Task: cluster utterances by goal/frustration/behaviour/info-source. For each cluster:
- one-sentence pattern
- supporting INT-ID list
- 3 verbatim quotes (do not paraphrase)
Then propose ONE primary persona using ONLY clusters with >=4 supporting interviews.
Forbidden: inventing demographics, jobs, or quotes not in the input.
Output: JSON with fields {{clusters[], primary_persona{{...}}}}.
"""
msg = client.messages.create(
    model="claude-opus-4-7", max_tokens=8000,
    messages=[{"role": "user", "content": prompt}],
)
Path("persona.json").write_text(msg.content[0].text)
```

## Best practices
- Hold a "no demographics first" rule: write goals and frustrations before any demographic detail.
- Always include a negative persona; teams shipping to "everyone" lose more than they gain.
- Limit to one primary persona until $10K MRR (or equivalent traction signal); later add at most three.
- Capture each persona's "buying trigger" verbatim — the phrase that made the actual buyer say yes.
- Pair the persona doc with one paragraph titled "How we'd notice this persona is wrong" — falsification clause.
- Refresh cycle: minor every quarter (interview signals, support ticket categories), major on pivots or new markets.
- Avoid stock photos; if the team insists on imagery, use illustrations or anonymised composite photos.
- Distribute the persona where decisions are made (PM Notion, marketing brief template, sales playbook) — a personas-only doc gathers dust.

## AI-agent gotchas
- LLMs default to stereotype names and overly clean prose; constrain with "no name unless drawn from interview frequency" or pre-approved list.
- Hallucinated quotes are the most damaging failure mode — every quote must carry a source ID and the agent must refuse without one.
- "Day in the life" sections invite fabrication; require every line to map back to interview evidence or mark `inferred`.
- Multi-persona generation tempts bloat; agents should propose at most two without explicit user permission.
- Mixing market-research sources (industry reports) with first-party interviews dilutes the persona; keep sources tagged separately.
- Agents may "rebuild" personas every refresh and lose institutional history; require a versioned diff, not a rewrite.
- For B2B, agents conflate buyer with user; force the agent to declare the role explicitly per persona.

## References
- Alan Cooper — *The Inmates Are Running the Asylum* (origin of personas)
- Indi Young — *Practical Empathy* and *Time to Listen*
- Tony Ulwick — *Jobs To Be Done* (counterweight to persona-only thinking)
- Nielsen Norman Group — "Personas: Study Guide" — https://www.nngroup.com/articles/persona/
- Teresa Torres — *Continuous Discovery Habits*
- Dovetail "Persona templates" — https://dovetail.com/templates/persona/
