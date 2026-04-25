# Agent Integration — Jobs to Be Done (JTBD)

## When to use
- Repositioning a product that has low conversion despite apparent feature completeness
- Designing a new product category where obvious competitors don't exist yet
- Understanding why customers churn when they "should" be satisfied
- Rewriting positioning copy to speak to motivation, not to features
- Planning a switching campaign by mapping forces of progress for a competitor's customers

## When NOT to use
- Usability testing: JTBD explains why someone hired the product; usability testing explains why the product failed on the job
- Quantitative feature prioritization: JTBD is qualitative and requires synthesis, not voting
- When you have fewer than 5 recent switcher interviews — the framework needs pattern recognition across cases
- When the product is purely utilitarian with no emotional or social component (rare; most products have all three)

## Where it fails / limitations
- Agents cannot conduct JTBD timeline interviews — the method requires live follow-up probing
- LLM-generated job statements are plausible but untested; every statement must be validated with actual customers
- Forces analysis (push/pull/habit/fear) requires nuanced qualitative judgment that LLMs conflate into shallow lists
- JTBD does not tell you what to build — it tells you what customers are trying to do; the solution design step remains human
- Applying JTBD to B2B is complex: multiple stakeholders have different jobs; agents tend to collapse these into one

## Agentic workflow
An agent can synthesize JTBD job statements from raw interview transcripts, draft the forces analysis matrix for a given product switch, and generate job maps for complex workflows. The most effective pattern is a two-pass synthesis: first the agent extracts raw quotes indexed by JTBD timeline stage, then a second pass refines quotes into structured job statements. Human review is mandatory before any job statement is used for strategic decisions.

### Recommended subagents
- `faion-sdd-executor-agent` — execute JTBD research tasks in an SDD context
- Any general Claude subagent — synthesize interview transcripts into job statements, generate job maps

### Prompt pattern
```
You are a JTBD analyst. Given the following interview transcript from a recent product switcher,
extract:
1. The triggering situation (what changed in their life/work)
2. The functional job (what they needed to get done)
3. The emotional job (how they wanted to feel)
4. The social job (how they wanted to be perceived)
5. Forces: push (old pain), pull (new appeal), habit (comfort with old), fear (anxiety about new)
Output as structured JTBD statement: "When [situation], I want to [action], so I can [outcome]"
Transcript: <paste>
```

```
Map the following job into stages using the 8-stage job map framework:
(Define → Locate → Prepare → Confirm → Execute → Monitor → Modify → Conclude)
For each stage: Customer goals, Current pain points, Opportunity for product to help.
Job: <paste job statement>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Dovetail (API) | Store and query tagged interview transcripts | dovetail.com/api |
| Notion API | Maintain job statement library | developers.notion.com |
| Whisper (local) | Transcribe JTBD interviews from audio | `pip install openai-whisper` |
| NVivo / Atlas.ti | Professional qualitative coding (desktop) | nvivo.com / atlasti.com (no CLI) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes (REST API) | Upload transcripts, create tags for JTBD stages, query insights |
| Notion | SaaS | Yes (API) | Store job canvas documents, link to interview notes |
| Airtable | SaaS | Yes (REST API) | Track job statements and forces across customer segments |
| Maze | SaaS | Partial (REST API) | Run unmoderated JTBD concept tests |
| UserTesting | SaaS | No | No public API; recordings proprietary |
| Miro | SaaS | Partial (API) | Create job map boards programmatically |

## Templates & scripts
See `templates.md` for the Job Statement Template, JTBD Interview Template, and Job Map Template.

Inline script — JTBD statement parser:
```python
# jtbd_parser.py — extract JTBD statements from raw notes
import re

def parse_jtbd(text):
    """Extract When/I want/So I can from raw interview notes."""
    patterns = {
        "situation": r"(?:when|whenever|after)\s+(.+?)(?:\.|,|I want)",
        "action": r"(?:I want(?:ed)? to|need to)\s+(.+?)(?:\.|,|so)",
        "outcome": r"(?:so (?:I|that I) can|in order to)\s+(.+?)(?:\.|$)",
    }
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        result[key] = match.group(1).strip() if match else "NOT FOUND"
    return result

notes = "When I finish a project, I want to send a professional invoice quickly so I can get paid faster."
parsed = parse_jtbd(notes)
print(f"Situation: {parsed['situation']}")
print(f"Action:    {parsed['action']}")
print(f"Outcome:   {parsed['outcome']}")
```

## Best practices
- Interview recent switchers, not long-tenured customers — switchers remember the decision; loyal customers have rationalized it
- Ask "what did you use before?" before asking about the current product — previous solution reveals the job better than the new one
- The non-obvious competitor is often the most important: a task manager competes with sticky notes and email as much as with Trello
- Build one job statement per customer segment; a single product can be hired for different jobs by different segments
- Validate job statements back to interviewees: "Does this capture what you were trying to do?" — a 1-sentence job statement is easy to test
- Do not conflate solution and job: "I want to use Notion" is not a job; "I want to capture and organize thoughts so I never lose an idea" is a job

## AI-agent gotchas
- LLMs tend to generate generic job statements ("complete tasks efficiently") — instruct the agent to use the specific language from the transcript
- The forces model requires tension analysis: push and pull must outweigh habit and fear for switching to occur; agents often list forces without assessing the balance
- Do not use an agent to generate job statements without transcripts — synthetic JTBD is fiction
- Human checkpoint: product/strategy decisions based on JTBD must be reviewed by someone who has spoken to real customers
- Agents excel at the Locate and Execute stages of the job map (most structured) and struggle with Define and Confirm (most ambiguous)

## References
- Clayton Christensen, "Competing Against Luck" — foundational JTBD book
- Bob Moesta & Chris Spiek, "Demand-Side Sales 101" — JTBD applied to sales and switching interviews
- Alan Klement, "When Coffee and Kale Compete" (wkalc.com) — free online; JTBD forces model
- https://jtbd.info/ — community and resource hub
- https://www.producttalk.org/2016/08/opportunity-solution-tree/ — Teresa Torres on integrating JTBD with product discovery
