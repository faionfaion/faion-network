# Agent Integration — AI Research Tools (researcher)

## When to use
- Automating multi-source literature reviews or competitive landscape sweeps
- Driving a structured research workflow where each stage maps to a different tool
- Building a research pipeline that needs citation tracking and source verification
- Producing synthesis reports from heterogeneous sources (news, academic, market data)

## When NOT to use
- Primary source collection requiring human judgment (expert interviews, observation studies)
- Legally sensitive research where AI hallucination risk is unacceptable
- Real-time data that requires live API access beyond what the tools expose
- Tasks where source provenance must be court-admissible or regulatory-grade

## Where it fails / limitations
- AI tools summarize public-web content; paywalled academic or proprietary data requires separate subscriptions
- Citation quality varies: Perplexity cites URLs, but Claude/ChatGPT can hallucinate references
- Competitor intel tools (Crayon, Klue) update on crawl schedules, not real-time; gaps of hours to days
- Interview analysis tools (Looppanel, Dovetail) require human-uploaded transcripts; agents cannot conduct interviews
- No tool triangulates across all stages autonomously; human curation between stages is mandatory

## Agentic workflow
Deploy a Claude subagent as an orchestrator that runs stages sequentially: it forms queries, invokes web-search or Perplexity API, receives raw results, and hands off to a synthesis step. Use Haiku for mechanical query-dispatch and Sonnet for multi-source synthesis. Opus is reserved for validation of critical data points where hallucination risk is high. A human checkpoint between "broad exploration" and "deep research" prevents propagating low-quality seeds downstream.

### Recommended subagents
- `faion-sdd-executor-agent` — drives structured research tasks defined in SDD specs
- `nero-sdd-executor-agent` — same pattern, NERO-side orchestration

### Prompt pattern
```
<research_task>
  <question>What are the top 5 AI-native research tools for market sizing in 2026?</question>
  <sources>perplexity, web-search</sources>
  <output_format>JSON with fields: tool, use_case, pricing, agent_api_available</output_format>
  <verify>cross-reference at least 2 sources per tool claim</verify>
</research_task>
```

```
<synthesis_task>
  <raw_findings>{{findings_json}}</raw_findings>
  <instruction>Identify contradictions. Flag any claim supported by fewer than 2 sources.
  Output structured markdown report.</instruction>
</synthesis_task>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `perplexity-cli` (unofficial) | Query Perplexity API from shell | `pip install perplexity-python` / [docs](https://docs.perplexity.ai/) |
| `claude` (Anthropic CLI) | Drive Claude for synthesis | `pip install anthropic` / [docs](https://docs.anthropic.com/en/api) |
| `serpapi` | Google/Bing structured results | `pip install google-search-results` / [docs](https://serpapi.com/) |
| `exploding-topics-api` | Trend signal extraction | REST API, docs at explodingopics.com/api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity Pro | SaaS | Yes — REST API | Best for cited multi-source synthesis |
| AlphaSense | SaaS | Partial — export-only | Strong for SEC filings, earnings calls |
| Crayon | SaaS | Partial — webhook triggers | Competitive intel; no natural-language query API |
| Brandwatch | SaaS | Partial — REST API | Social sentiment; complex auth setup |
| Statista | SaaS | No | Data download only; agent must parse PDFs |
| Google Trends | Free | Yes — `pytrends` library | Rate-limited; useful for trend signals |
| Dovetail | SaaS | Partial — CSV export | Requires human-uploaded transcripts |

## Templates & scripts
See `templates.md` for research-brief and synthesis-report templates. Inline dispatcher:

```python
import anthropic, json, os

client = anthropic.Anthropic()

def research_dispatch(question: str, raw_data: list[dict]) -> str:
    """Synthesize multi-source research findings."""
    prompt = f"""<synthesis_task>
<question>{question}</question>
<raw_data>{json.dumps(raw_data, indent=2)}</raw_data>
<instructions>
- Identify key themes
- Flag contradictions
- Note claims with single-source support
- Output markdown with citations
</instructions>
</synthesis_task>"""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

## Best practices
- Assign tool to stage, not to question: use Perplexity for exploration, AlphaSense for industry filings, Dovetail for interview synthesis
- Document which AI tool produced each claim in the final report; reviewers need this for trust calibration
- Run top-down and bottom-up research paths independently before merging, to avoid anchoring bias from first result
- Set iteration budgets per stage (e.g., max 3 Perplexity queries for exploration) to control cost and scope creep
- Verify any statistic cited by an AI tool against the linked primary source before including in deliverables

## AI-agent gotchas
- Perplexity API results differ from the web UI; test both for coverage gaps before committing to API-only flow
- Claude and ChatGPT can fabricate plausible-sounding citations; always validate URLs before recording as sources
- Crayon and Klue require human setup (competitor list configuration) before agents can pull meaningful signals
- Synthesis agents lose track of source attribution when chaining multiple tool calls; pass source metadata explicitly through every step
- Rate limits on free-tier tools (Google Trends, SerpAPI) will silently truncate results; add explicit error handling

## References
- [Perplexity API Docs](https://docs.perplexity.ai/)
- [AlphaSense Research Platform](https://www.alphasense.com/)
- [NN/g AI Research Tools Review](https://www.nngroup.com/articles/research-with-ai/)
- [Anthropic Claude API](https://docs.anthropic.com/en/api/getting-started)
- [SerpAPI](https://serpapi.com/)
- [Exploding Topics](https://explodingtopics.com/)
