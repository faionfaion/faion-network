# Agent Integration — AI Research Tools (market-researcher)

## When to use
- Building or auditing the tool stack for a market research pipeline
- Deciding which AI tool handles which stage of a multi-step market research project
- Replacing manual research workflows (Google → read → summarize) with agent-driven equivalents
- Onboarding a new agent to an existing research pipeline by matching task types to tools

## When NOT to use
- When a single tool already covers the full research scope — no need to evaluate alternatives
- Proprietary or regulated research contexts requiring auditable, non-AI sources
- When the research team lacks API access to the candidate tools — tool integration requires provisioned credentials before agents can use them
- One-off ad hoc queries where tool overhead exceeds the research value

## Where it fails / limitations
- No single AI tool covers all stages; agents that try to use one tool for everything produce shallow, biased results
- Tool quality for market research degrades sharply outside English-language content
- Competitor analysis tools (Crayon, Klue) require 2-4 weeks of initial setup before producing useful signals; agents cannot bootstrap this
- Interview analysis tools (Looppanel, Dovetail) only operate on pre-uploaded transcripts — agents cannot conduct interviews
- AI tools reflect the training cutoff or crawl date of their underlying data; freshness of results must be explicitly verified

## Agentic workflow
Use a two-layer agent structure: an orchestrator (Sonnet) selects the right tool for each research stage based on the task type and available tool credentials, then dispatches sub-queries to stage-specific tools (Perplexity for exploration, AlphaSense export for filings, SerpAPI for structured results). The orchestrator merges outputs and flags gaps where no tool produced coverage. A human checkpoint validates the merged output before the synthesis step.

### Recommended subagents
- `faion-sdd-executor-agent` — drives tool-dispatched research tasks in a structured pipeline

### Prompt pattern
```
<research_pipeline>
  <topic>AI research tools market, 2026</topic>
  <stages>
    <stage name="exploration" tool="perplexity">Broad landscape: who are the players, what are the use cases?</stage>
    <stage name="competitor-intel" tool="serpapi">Recent news, funding, product launches for top 5 players</stage>
    <stage name="trend" tool="google-trends">Search volume trends for key terms over 12 months</stage>
    <stage name="synthesis" tool="claude-sonnet">Merge stage outputs into a structured report with source registry</stage>
  </stages>
  <output>Markdown report, source registry, coverage gaps list</output>
</research_pipeline>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytrends` | Google Trends — trend signal | `pip install pytrends` |
| `serpapi` | Structured search results | `pip install google-search-results` |
| `anthropic` SDK | Orchestration and synthesis | `pip install anthropic` |
| `httpx` | Async API calls to Perplexity, Contify | `pip install httpx` |
| `pandas` | Tabulate and merge multi-tool outputs | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity Pro | SaaS | Yes — REST API | Exploration and cited synthesis |
| ChatGPT API | SaaS | Yes — REST API | General synthesis; weaker citations than Perplexity |
| Claude API | SaaS | Yes — REST API | Best for structured output and multi-step reasoning |
| Crayon | SaaS | Partial — webhooks | Competitor intel; manual setup required |
| Klue | SaaS | Partial | Competitor intel; better NLP querying |
| Contify | SaaS | Partial — REST | Competitor + market news |
| Brandwatch | SaaS | Partial — REST | Social sentiment; complex setup |
| Sprout Social | SaaS | Partial — REST | Social sentiment; more accessible API |
| Statista AI | SaaS | No — export only | Market data reports |
| CB Insights | SaaS | Partial — export | Company and funding data |
| Exploding Topics | SaaS | Yes — REST | Emerging trend signals |
| Looppanel | SaaS | Partial — export | Interview analysis |
| Dovetail | SaaS | Partial — export | Interview and UX research synthesis |

## Templates & scripts
See `templates.md` for multi-stage research brief and synthesis templates. Inline stage dispatcher:

```python
import anthropic, os
from typing import Literal

client = anthropic.Anthropic()

STAGE_TOOLS = {
    "exploration": "perplexity",
    "competitor-intel": "serpapi",
    "trend": "google-trends",
    "interview-analysis": "dovetail-export",
    "synthesis": "claude-sonnet",
}

def select_tool(task_type: str) -> str:
    tool = STAGE_TOOLS.get(task_type)
    if not tool:
        raise ValueError(f"Unknown task type: {task_type}. Valid: {list(STAGE_TOOLS)}")
    return tool

def orchestrate_research(topic: str, stages: list[dict]) -> str:
    stage_summary = "\n".join(
        f"- {s['name']} ({select_tool(s['name'])}): {s['query']}" for s in stages
    )
    prompt = f"""<research_orchestration>
<topic>{topic}</topic>
<stages>{stage_summary}</stages>
<instruction>For each stage, generate the optimal query for the assigned tool.
Output JSON: [{{"stage": "...", "tool": "...", "query": "...", "expected_output": "..."}}]
</instruction>
</research_orchestration>"""
    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.content[0].text
```

## Best practices
- Assign exactly one primary tool per research stage; avoid having the same tool cover multiple stages, as this hides coverage gaps
- Verify tool credentials and rate limits at the start of each pipeline run; failed tool calls silently missing from results are a common failure mode
- Document which tool produced each finding in the output; reviewers need this to assess credibility
- Run the tool stack on a known-answer test case before live research to validate API reliability
- Use Exploding Topics for emerging market research before committing to Crayon/Klue setup; trend signals often reveal whether a market is worth deep competitive analysis

## AI-agent gotchas
- Agents default to Claude or ChatGPT for all stages when not given explicit tool assignments; this produces citation-poor results for competitive and market data stages
- Rate limit errors from one tool will propagate silently unless the orchestrator handles exceptions per-tool
- Tool outputs have different schemas; the synthesis step must normalize before merging (Perplexity returns citations as URLs, SerpAPI returns structured JSON, Google Trends returns DataFrames)
- "AI tool" in 2026 means both AI-native tools (Perplexity, Elicit) and legacy tools with AI features bolted on (Statista AI, SurveyMonkey AI); their reliability for agent pipelines differs significantly
- Agents will hallucinate tool capabilities if given tool names without explicit API documentation; always include the API reference in the agent's context

## References
- [Perplexity API](https://docs.perplexity.ai/)
- [SerpAPI Docs](https://serpapi.com/search-api)
- [Exploding Topics API](https://explodingtopics.com/api)
- [CB Insights Platform](https://www.cbinsights.com/)
- [NN/g AI Research Tools](https://www.nngroup.com/articles/research-with-ai/)
- [Dovetail Platform](https://dovetail.com/)
