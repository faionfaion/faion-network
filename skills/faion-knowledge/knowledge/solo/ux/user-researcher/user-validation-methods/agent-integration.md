# Agent Integration — User Validation Methods

## When to use
- Running a structured discovery sprint that needs multiple validation lenses in sequence: JTBD → persona → problem validation → pain mining
- When a single methodology is insufficient and a combined workflow is needed (e.g., build personas, then validate the top pain point per persona)
- Onboarding a new team member to the full research toolkit via a single entry point
- Agent orchestration: routing a research task to the correct sub-methodology based on the question type

## When NOT to use
- When one specific methodology already answers the question — go to that methodology's agent-integration.md directly
- As a substitute for running any individual methodology thoroughly — this file coordinates, not replaces
- When no qualitative data exists yet — start with pain-point-mining, not the combined workflow

## Where it fails / limitations
- This file contains four methodology summaries (JTBD, persona-building, problem-validation, pain-point-mining); each summary is thinner than the standalone methodology file
- Agents prompted from this file will produce shallower outputs than agents prompted from a dedicated methodology file
- The combined workflow creates sequencing risk: persona-building before pain validation leads to premature segmentation

## Agentic workflow
This file is best used as a router: an agent reads the methodology summaries, identifies which sub-methodology answers the user's current question, and then applies that sub-methodology's prompt pattern. For full integration guidance on each sub-methodology, the agent should load the dedicated `agent-integration.md` from the relevant directory.

Canonical routing logic:
- "What is the user trying to accomplish?" → JTBD
- "Who is the user?" → Persona Building
- "Does this problem really exist and matter?" → Problem Validation
- "Where do users express frustration online?" → Pain Point Mining

### Recommended subagents
- `faion-sdd-executor-agent` — run coordinated multi-methodology research tasks
- Any general Claude subagent — route research questions, run combined discovery workflows

### Prompt pattern
```
You are a user research coordinator. Given the following research question, identify which methodology applies:
- JTBD: understanding user motivation and switching behavior
- Persona Building: segmenting users into distinct archetypes
- Problem Validation: verifying a specific problem hypothesis with evidence
- Pain Point Mining: discovering unknown frustrations from public sources

Research question: <paste>
Output: methodology name + one-paragraph explanation of how to apply it.
```

```
Run a combined validation workflow for the following hypothesis:
Step 1 (Pain Mining): Search Reddit and G2 for complaints matching this pain: <pain>
Step 2 (Problem Validation): Score evidence against validation hierarchy (paid/committed/engaged/stated)
Step 3 (JTBD): Draft a job statement: "When [situation], I want to [action], so I can [outcome]"
Output: findings per step + overall recommendation (PROCEED / PIVOT / KILL).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| PRAW | Reddit mining for pain-point-mining step | `pip install praw` / praw.readthedocs.io |
| Whisper | Transcribe interviews for JTBD step | `pip install openai-whisper` |
| Typeform API | Deploy problem validation surveys | developer.typeform.com |
| Notion API | Store personas, job statements, validation reports | developers.notion.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes (REST API) | Central store for interview transcripts, persona notes, and JTBD findings |
| Notion | SaaS | Yes (API) | Cross-methodology research database; link personas to job statements |
| Airtable | SaaS | Yes (REST API) | Track validation evidence rows with methodology type column |
| Typeform | SaaS | Yes (REST API) | Run surveys for persona validation and problem frequency checks |

## Templates & scripts
See the templates embedded in `README.md` for: JTBD Canvas, Persona Template, Problem Validation Report, and Pain Point Mining Report.

Inline script — methodology router:
```python
# methodology_router.py — route a research question to the correct methodology
KEYWORDS = {
    "jtbd": ["why", "motivation", "hired", "fired", "switched", "accomplish", "trying to"],
    "persona": ["who", "segment", "type of user", "demographics", "behaviors"],
    "problem_validation": ["does this problem exist", "is it real", "how painful", "validate hypothesis"],
    "pain_mining": ["where", "complaints", "frustration", "reddit", "reviews", "forum"],
}

def route(question: str) -> str:
    q = question.lower()
    scores = {k: sum(1 for kw in kws if kw in q) for k, kws in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unclear — clarify the research question"

print(route("Why do users switch to a competitor?"))  # → jtbd
print(route("Who are our typical users?"))             # → persona
print(route("Is the invoice pain real for freelancers?"))  # → problem_validation
```

## Best practices
- Run methodologies in this order for new product discovery: pain mining → problem validation → JTBD → persona
- Do not run persona-building before problem validation — personas become anchors that bias problem framing
- JTBD and persona are complementary: JTBD explains motivation; persona explains context; use both
- Each methodology should produce an artifact (pain log, validation report, job statement, persona card) — agents must output structured artifacts, not free-form summaries
- Review artifacts across methodologies for contradictions — contradictions are the most valuable signal

## AI-agent gotchas
- Agents prompted from this combined file tend to conflate methodology outputs — instruct them to label each section with the methodology name
- Pain mining and JTBD have opposite biases: pain mining surfaces negatives; JTBD surfaces aspirations. Both are needed for a complete picture
- Human checkpoint: after each methodology step, the researcher must review the artifact before the agent proceeds to the next step
- Persona-building by an agent without interview data produces stereotypes; always provide raw interview excerpts as input
- Do not use JTBD output as a problem validation substitute — job statements describe motivation, not evidence of market demand

## References
- Dedicated agent-integration files for each sub-methodology in adjacent directories:
  - `jobs-to-be-done/agent-integration.md`
  - `problem-validation/agent-integration.md`
  - `pain-point-research/agent-integration.md`
  - `user-interviews-methods/agent-integration.md`
- Rob Fitzpatrick, "The Mom Test" (momtestbook.com)
- Clayton Christensen, "Competing Against Luck" — JTBD
- Erika Hall, "Just Enough Research" (A Book Apart)
