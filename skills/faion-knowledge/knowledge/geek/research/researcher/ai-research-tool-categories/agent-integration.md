# Agent Integration — AI Research Tool Categories

## When to use
- Planning a research stack at the start of a new project or research sprint
- Selecting tools for a specific research phase (discovery → synthesis → validation)
- Budget-scoping a research operation (free vs. mid vs. enterprise tier)
- Onboarding a new researcher who needs a tool landscape overview
- Choosing the right tool per research question type before committing to a SaaS contract

## When NOT to use
- As a substitute for evaluating whether a specific tool fits your data privacy requirements — always check data processing agreements
- When the research question is fully addressable with a single tool already in use — tool sprawl has a coordination cost
- For purely qualitative synthesis tasks where Claude alone suffices — no additional tooling needed

## Where it fails / limitations
- The tool landscape changes rapidly; this category map can be 6-12 months stale without active maintenance
- Budget tiers vary by team size, geography, and negotiation; "mid" for one team is "enterprise" for another
- Tool API availability does not equal agent suitability — many SaaS tools have APIs that are poorly documented or rate-limited for automation
- No single tool covers all research phases well; the map forces choosing a stack, not a silver bullet

## Agentic workflow
An agent uses this category map as a decision tree: given a research phase and budget, it selects 1-2 tools per phase and outputs a stack recommendation with integration notes. For agent-driven research pipelines, the agent prioritizes tools with REST APIs and structured output (JSON) over tools that produce only human-readable dashboards. The agent then reads phase-specific methodology files (e.g., `ai-interview-analysis`, `synthetic-users`) for execution details.

### Recommended subagents
- `faion-sdd-executor-agent` — can be extended with tool-selection as a planning step before execution
- General Claude subagent (Sonnet) — stack recommendation from phase + budget inputs
- General Claude subagent (Haiku) — tool lookup and data retrieval from selected tools

### Prompt pattern
```
I am running a [research type: discovery / validation / competitive] research sprint.
Budget tier: [free / mid / enterprise].
Research phase: [exploration / interviews / synthesis / competitive intel].
Team size: [1 researcher / small team / large team].

Recommend a tool stack. For each tool:
- Name and category
- Why it fits this phase
- API availability (yes/no)
- One thing to watch out for
Format as a markdown table.
```

```
Given this research question: "[question]"
Which tool category is most appropriate and why?
Options: Exploration | Competitor Intel | User Interviews |
Survey Analysis | Sentiment | Synthesis | Synthetic Research.
Return: category, top 2 tools, and the specific capability needed.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Perplexity MCP | Exploration phase: cited web synthesis | MCP server, perplexity.ai/api |
| SimilarWeb CLI (unofficial) | Competitor traffic estimates | similarweb.com/developer |
| Google Trends (pytrends) | Trend exploration, free tier | `pip install pytrends` / github.com/GeneralMills/pytrends |
| Brandwatch CLI | Sentiment monitoring (enterprise) | brandwatch.com/developer |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity Pro | SaaS | Yes (API) | Exploration phase; best cited synthesis for free/mid |
| Claude / ChatGPT | SaaS | Yes (API) | Exploration + synthesis; calculation assistance; no live data |
| Crayon | SaaS | Yes (API) | Competitor intel; feature and messaging tracking |
| Klue | SaaS | Partial | Competitor intel; battlecards; enterprise contract required |
| Contify | SaaS | Partial | Competitor intel; news monitoring with API |
| AlphaSense | SaaS | Partial | Competitor intel + market sizing; financial filings |
| Looppanel | SaaS | Partial (API beta) | User interviews; transcription + insight tagging |
| Dovetail | SaaS | Yes (API) | User interviews + synthesis; repository with API |
| User Interviews | SaaS | No | Participant recruitment; no agent-accessible analysis layer |
| Qualtrics | SaaS | Yes (API) | Survey analysis; enterprise AI layer (Qualtrics AI) |
| SurveyMonkey AI | SaaS | Partial | Survey analysis; AI summaries; limited API for analysis output |
| Brandwatch | SaaS | Yes (API) | Sentiment monitoring; social listening |
| Sprout Social | SaaS | Yes (API) | Sentiment + social; stronger on publishing than analysis |
| Miro AI | SaaS | No | Synthesis / affinity mapping; no export API for AI outputs |
| Condens | SaaS | Yes (API) | Synthesis; research repository with structured tagging |
| EnjoyHQ (by UserZoom) | SaaS | Partial | Synthesis repository; enterprise |
| Synthetic Users | SaaS | Yes (API) | Synthetic research; profile + response simulation |
| Viewpoints.ai | SaaS | Partial | Synthetic research; concept validation |
| Google Trends | Free | Yes (unofficial pytrends) | Trend exploration; relative volume only |

## Templates & scripts
See `templates.md` for a research stack selection worksheet.

Tool selection decision script:
```python
# tool_selector.py
PHASE_MAP = {
    "exploration": ["Perplexity Pro", "Claude", "Google Trends"],
    "competitor_intel": ["Crayon", "Klue", "AlphaSense"],
    "interviews": ["Looppanel", "Dovetail", "AssemblyAI"],
    "survey": ["Qualtrics", "SurveyMonkey AI"],
    "sentiment": ["Brandwatch", "Sprout Social"],
    "synthesis": ["Dovetail", "Condens", "EnjoyHQ"],
    "synthetic": ["Synthetic Users", "Viewpoints.ai"],
}

BUDGET_FILTER = {
    "free": {"Perplexity Pro", "Claude", "Google Trends"},
    "mid": {"Perplexity Pro", "Claude", "Looppanel", "Dovetail", "Condens",
            "SurveyMonkey AI", "AssemblyAI", "Synthetic Users"},
    "enterprise": set(PHASE_MAP["exploration"] + PHASE_MAP["competitor_intel"] +
                      PHASE_MAP["interviews"] + PHASE_MAP["survey"] +
                      PHASE_MAP["sentiment"] + PHASE_MAP["synthesis"] +
                      PHASE_MAP["synthetic"]),
}

def recommend(phase: str, budget: str) -> list[str]:
    phase_tools = set(PHASE_MAP.get(phase, []))
    budget_tools = BUDGET_FILTER.get(budget, set())
    return list(phase_tools & budget_tools)

print(recommend("interviews", "mid"))
# ['Looppanel', 'Dovetail']
```

## Best practices
- Pick one canonical repository tool (Dovetail or Condens) and funnel all research outputs there; fragmented insights across tools is the primary cause of research debt
- Prefer tools with REST APIs that return structured JSON for any phase where agents need to consume output
- Free/mid stacks cover 80% of solopreneur research needs; enterprise tools add breadth for competitive intelligence, not depth for user research
- Audit your tool stack annually; the AI research tooling market consolidates rapidly and pricing changes affect stack viability
- Never use more than 3 tools per research sprint; coordination overhead exceeds analytical benefit beyond that

## AI-agent gotchas
- "Agent-friendly" in the services table means a structured API exists; it does not mean the API is designed for automation — always check rate limits and output formats before building a pipeline
- Many SaaS research tools process data on third-party servers; for B2B user research with NDA constraints, verify data processing agreements before piping transcripts through them
- Tool-selection agents tend to recommend the most well-known tools, not the most API-accessible; always verify API availability independently before committing
- Human checkpoint at tool selection stage: the agent recommends, the researcher confirms — wrong tool choice is expensive to reverse mid-sprint

## References
- https://www.nngroup.com/articles/research-with-ai/
- https://www.userlytics.com/resources/blog/7-best-ai-powered-user-research-platforms-in-2026-complete-buyers-guide/
- https://www.producttalk.org/ (Teresa Torres on continuous discovery tools)
- https://www.crayon.co/
- https://dovetail.com/
- https://looppanel.com/
