# Agent Integration — AI Research Tool Categories

## When to use
- Selecting the right research tool for a specific research phase before starting a project
- Building a reusable tool-selection decision tree for recurring research workflows
- Auditing an existing research stack against coverage gaps by phase
- Onboarding a new agent to a research pipeline by mapping tasks to approved tools

## When NOT to use
- When you already know the tool for the job — skip categorization overhead
- When the research budget is fixed and only one or two tools are available
- When tool categories are stable and don't change — this methodology is most valuable during tool procurement or pipeline design, not execution

## Where it fails / limitations
- Tool categories shift quickly; a 2025 category map is partially obsolete by 2026 as new entrants merge categories
- "Agent-friendly" ratings require direct API testing; vendor claims diverge from actual API reliability
- Mid-market tools (Looppanel, Dovetail) sit across multiple categories (interview + sentiment + synthesis), causing classification ambiguity
- Budget tiers are approximate; enterprise pricing is negotiated and not public

## Agentic workflow
A Haiku agent handles classification: given a research task description, it maps the task to a phase (exploration, competitor intel, interview analysis, etc.) and returns the recommended tool set with rationale. A Sonnet agent handles comparison: given two or three candidate tools for the same phase, it evaluates them against agent-friendliness, cost, and coverage. Tool selection should happen once per project at planning time, not per research query.

### Recommended subagents
- `faion-sdd-executor-agent` — drives tool-selection tasks embedded in a project spec

### Prompt pattern
```
<tool_selection>
  <task>Competitive landscape sweep for AI note-taking tools, B2B segment, 2026</task>
  <phase>competitor-intel</phase>
  <constraints>
    <budget>mid</budget>
    <api_required>true</api_required>
    <timeline>3 days</timeline>
  </constraints>
  <output>Ranked tool list with: tool name, phase fit, API available (yes/no), cost tier, notes</output>
</tool_selection>
```

```
<tool_comparison>
  <candidates>["Crayon", "Contify", "Klue"]</candidates>
  <criteria>["real-time updates", "API access", "NLP query support", "pricing"]</criteria>
  <output_format>markdown table</output_format>
</tool_comparison>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytrends` | Google Trends — exploration phase | `pip install pytrends` |
| `serpapi` | Structured search results — exploration + competitor | `pip install google-search-results` |
| `anthropic` SDK | Classification and comparison reasoning | `pip install anthropic` |
| `requests` | Call Perplexity API, Contify webhooks | stdlib-adjacent, no install needed |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity | SaaS | Yes — REST API | Exploration + synthesis |
| Crayon | SaaS | Partial — webhooks | Competitor intel; requires manual competitor setup |
| Klue | SaaS | Partial | Competitor intel; better NLP than Crayon for query |
| Contify | SaaS | Partial — REST API | Competitor + market news monitoring |
| Looppanel | SaaS | Partial — export only | Interview analysis; no live query API |
| Dovetail | SaaS | Partial — export only | Interview + sentiment synthesis |
| Qualtrics | SaaS | Yes — REST API | Survey collection and analysis |
| SurveyMonkey | SaaS | Yes — REST API | Survey analysis with AI insights |
| Brandwatch | SaaS | Partial — REST API | Social sentiment; complex OAuth |
| Miro AI | SaaS | No | Synthesis board; not scriptable |
| Synthetic Users | SaaS | Yes — REST API | Synthetic research for early validation |
| Viewpoints.ai | SaaS | Yes — REST API | Simulated user panels |
| Google Trends | Free | Yes — `pytrends` | Exploration; B2C proxy only |

## Templates & scripts
See `templates.md` for a tool-selection matrix template. Inline phase-mapper:

```python
import anthropic

client = anthropic.Anthropic()

PHASE_MAP = {
    "exploration": ["Perplexity", "Claude", "Google Trends"],
    "competitor-intel": ["Crayon", "Klue", "Contify", "AlphaSense"],
    "interview-analysis": ["Looppanel", "Dovetail", "Insight7"],
    "survey-analysis": ["Qualtrics", "SurveyMonkey AI"],
    "sentiment": ["Brandwatch", "Sprout Social"],
    "synthesis": ["Miro AI", "Condens", "EnjoyHQ"],
    "synthetic-research": ["Synthetic Users", "Viewpoints.ai"],
}

def recommend_tools(task_description: str, budget: str = "mid") -> str:
    phase_list = "\n".join(f"- {p}: {', '.join(t)}" for p, t in PHASE_MAP.items())
    prompt = f"""<tool_selection>
<task>{task_description}</task>
<budget>{budget}</budget>
<phases>{phase_list}</phases>
<output>JSON: {{"phase": "...", "recommended_tools": [...], "rationale": "..."}}</output>
</tool_selection>"""
    r = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.content[0].text
```

## Best practices
- Lock tool selection per project at spec time; changing tools mid-project invalidates cross-phase data consistency
- Test API reliability on a 10-query sample before committing a tool to a production pipeline
- For synthetic research tools (Synthetic Users, Viewpoints.ai), treat outputs as directional signals only — not replacements for real user data
- Maintain a team-level approved-tools registry with API key status and rate-limit budgets; agents should reference this, not discover tools ad hoc
- Prefer tools with webhook/push over polling; polling adds latency and hits rate limits faster in multi-agent setups

## AI-agent gotchas
- Agents will recommend tools outside the approved list if not given a constrained tool registry; always pass the approved list explicitly
- "Agent-friendly" from vendor marketing often means "has an API" — not "reliable for programmatic use at scale"; test before production
- Interview-analysis tools require human-uploaded content; agents cannot conduct or ingest interviews without a preprocessing step
- Competitor intel tools (Crayon, Klue) need a one-time human configuration of competitor entities; agents cannot bootstrap this from scratch
- Synthetic research tools produce biased outputs if the simulated persona pool is too narrow; agents must be given demographic constraints

## References
- [Looppanel Product Research Tools](https://www.looppanel.com/blog/product-research)
- [Userlytics AI Platforms Guide 2026](https://www.userlytics.com/resources/blog/7-best-ai-powered-user-research-platforms-in-2026-complete-buyers-guide/)
- [Crayon Competitive Intelligence](https://www.crayon.co/)
- [Contify CI Tools](https://www.contify.com/resources/blog/best-competitive-intelligence-tools/)
- [Synthetic Users](https://www.syntheticusers.com/)
- [NN/g AI Research](https://www.nngroup.com/articles/research-with-ai/)
