# Agent Integration — Research Workflows

Methodology covers three sequential research workflows orchestrated by the `faion-researcher` skill: **Idea Discovery**, **Product Research**, **Project Naming**. The workflows are state machines: gather context → run research agents one-by-one → write outputs to `.aidocs/product_docs/`. This file maps that pipeline to concrete subagents, CLI tools and SaaS APIs an LLM agent can drive.

## When to use

- Pre-spec stage of a new product/idea where `.aidocs/product_docs/market-research.md`, `competitive-analysis.md`, or `idea-validation.md` are missing.
- Solopreneur / one-engineer flow where an LLM acts as the entire research team, then hands off to `faion-sdd` or `faion-marketing-manager`.
- Naming / domain validation before reserving a brand and writing `constitution.md`.
- Refresh of stale research artifacts (>6 months old) before a major roadmap revision.

## When NOT to use

- Inside an active SDD task — research belongs in `backlog/<feature>/` discovery, not in execution.
- When the user has signed enterprise market data contracts (Gartner, IDC, Statista paid) — feed those reports directly to `faion-sdd` instead of re-deriving with web search.
- Tactical decisions inside a 30-minute window. Sequential execution requirement (`Run agents ONE BY ONE`) makes this multi-minute work, not interactive.
- After spec freeze — research findings that contradict signed-off spec must go through change management, not a research re-run.

## Where it fails / limitations

- **Sequential bottleneck.** README mandates `not parallel`. With 5 modules × 8-12 searches each in deep mode, total tool calls easily hit 50-60 — fragile to long sessions and rate limits.
- **Source citation rule** (`If data not found → write "Data not available"`) is routinely violated by LLMs that hallucinate plausible TAM numbers. Needs a hard validator post-step.
- **No scoring rubric for picking 3-5 ideas** in step 3 of Idea Discovery — left to user judgement, often skipped.
- **Domain check** in Project Naming relies on a `faion-domain-checker-agent` that has to call WHOIS/registrar APIs; if the agent silently fails, names get reserved that are already taken.
- **Mode selection (quick vs deep)** is binary, no in-between. Deep mode in WebSearch-only environments can exhaust context before synthesis.
- **Loop-back on rejection** (step 6 of Idea Discovery, step 5 of Naming) has no max-iteration guard — agents can loop forever if user keeps saying "no".

## Agentic workflow

Drive each workflow as a **deterministic state machine** in the orchestrator subagent. Use `AskUserQuestion` for the three branching points (context gathering, idea selection, mode selection). Spawn one research subagent per module via the `Task` tool, wait for completion, then move to the next. Persist intermediate state to `.aidocs/product_docs/<module>.md` after every step so a session crash resumes cleanly. Feed the final `executive-summary.md` to downstream agents (`faion-sdd`, `faion-marketing-manager`) as input.

### Recommended subagents

- `faion-research-agent` — Research orchestrator with 9 modes (ideas/market/competitors/pricing/niche/personas/pains/validate/names). One invocation per mode, sequential.
- `faion-domain-checker-agent` — Verifies `.com/.io/.co/GitHub/Twitter` availability for naming workflow. Must have network + registrar API access.
- `faion-marketing-manager` — Downstream consumer: turns `executive-summary.md` into a GTM Manifest.
- `faion-sdd` — Downstream consumer: turns `executive-summary.md` + `idea-validation.md` into `spec.md`.
- `faion-software-developer` — Final downstream node when research-to-build handoff is approved.
- General-purpose `Task` subagent — Use when no specialized research-agent is registered; pass the methodology's `llm-prompts.md` as system context.

### Prompt pattern

Orchestrator dispatch (Idea Discovery, step 4):

```
Run faion-research-agent in mode=pains for ideas: [<list>].
Constraints: cite every claim with URL. Output to .aidocs/product_docs/pain-points.md.
If a Reddit/forum/review claim cannot be sourced, write "Data not available" — do not infer.
Return only the file path on completion.
```

Synthesis prompt (after all modules complete):

```
Read .aidocs/product_docs/{market-research,competitive-analysis,user-personas,problem-validation,pricing-research}.md.
Produce executive-summary.md with: 1-paragraph TL;DR, top-3 risks, top-3 opportunities, recommended-next-step ∈ {gtm, spec, kill}.
Quote at least one source URL per section. Max 600 words.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` (Claude Code CLI) | Run subagents, AskUserQuestion, Task tool | https://docs.anthropic.com/en/docs/claude-code |
| `gh` | GitHub org/repo name availability for naming | `apt install gh` / https://cli.github.com |
| `whois` | Domain availability fallback when registrar API down | `apt install whois` |
| `dig` / `host` | DNS resolution check (taken vs parked vs registered) | bundled in `dnsutils` |
| `curl` + Cloudflare/Namecheap API | Real-time domain availability + price | https://api.namecheap.com/xml.response |
| `python-google-trends` (`pytrends`) | Trend signals for niche evaluation | `pip install pytrends` |
| `redditwarp` / `praw` | Pain-point mining from subreddits | `pip install praw` |
| `searxng` (self-hosted, port 8888 in this workspace) | Aggregated web search without API quotas | already running on nero-prod |
| `firecrawl` CLI | Crawl competitor sites + pricing pages, return markdown | `npm i -g firecrawl-cli` |
| `lynx -dump` | Cheap fallback for fetching landing pages when HTML clean | `apt install lynx` |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Anthropic Web Search | API tool inside Claude | Yes — native `WebSearch` tool | Default for Quick mode, 3-5 calls |
| Tavily | Search-as-API tuned for agents | Yes — REST + Python SDK | Best for Deep mode, returns LLM-ready summaries |
| Exa (formerly Metaphor) | Semantic search API | Yes — REST | Better than Tavily for academic / niche topics |
| Perplexity API | Cited answer engine | Yes — REST | Returns citations inline, saves a synthesis step |
| Firecrawl | Crawl + scrape API | Yes — REST + MCP server | Use to extract competitor pricing tables |
| Reddit API (OAuth) | Pain-point mining | Yes — REST, rate-limited 60/min | Critical for `mode=pains` |
| ProductHunt API | Competitor discovery | Yes — GraphQL | Free tier, good signal for `mode=competitors` |
| G2 / Capterra | Reviews + competitor matrix | Partially — no public API, scrape | Firecrawl works; respect ToS |
| SimilarWeb / Ahrefs | Traffic + keyword data | Paid API, agent-friendly | Use only when budget allocated |
| Statista | Market sizing | Paid, no usable API | Manual export only |
| Namecheap API | Domain availability + buy | Yes — XML API | Used by `faion-domain-checker-agent` |
| Cloudflare Registrar API | Domain registration | Yes — REST | At-cost domains, agent-driven buy |
| GitHub API | Org/repo handle availability | Yes — REST via `gh` | Required by naming workflow |
| Twitter/X API | Handle availability | Limited — paid tier needed since 2023 | `gh`-style HEAD check on `https://x.com/<handle>` is the cheap fallback |
| Google Trends (`pytrends`) | Trend evaluation | Yes — unofficial Python | Brittle, throttled — cache results |
| Hacker News Algolia API | Tech-trend mining | Yes — REST, no auth | Cheap signal for B2B-dev niches |

## Templates & scripts

The methodology's own `templates.md` and `examples.md` are empty — there is nothing to "see". Use the inline scripts below until those files are populated upstream.

Domain + handle availability batch check (≤50 lines bash):

```bash
#!/usr/bin/env bash
# usage: check-names.sh names.txt   (one candidate per line)
# outputs CSV: name,com,io,co,gh,x,score
set -euo pipefail
NAMES_FILE="${1:?names file required}"
echo "name,com,io,co,gh,x,score"
while IFS= read -r name; do
  [[ -z "$name" ]] && continue
  s=0
  for tld in com io co; do
    if whois "${name}.${tld}" 2>/dev/null | grep -qiE "no match|not found|no entries"; then
      eval "av_${tld}=1"; s=$((s + (tld == com ? 10 : tld == io ? 5 : 3)))
    else
      eval "av_${tld}=0"
    fi
  done
  gh_code=$(curl -sLo /dev/null -w "%{http_code}" "https://github.com/${name}")
  [[ "$gh_code" == "404" ]] && av_gh=1 && s=$((s+3)) || av_gh=0
  x_code=$(curl -sLo /dev/null -w "%{http_code}" "https://x.com/${name}")
  [[ "$x_code" == "404" ]] && av_x=1 && s=$((s+3)) || av_x=0
  echo "${name},${av_com},${av_io},${av_co},${av_gh},${av_x},${s}"
  sleep 1   # rate-limit politeness
done < "$NAMES_FILE"
```

Workflow state file (drop into `.aidocs/product_docs/_workflow-state.json`):

```json
{
  "workflow": "product-research",
  "modules": ["market", "competitors", "personas", "validation", "pricing"],
  "mode": "deep",
  "completed": [],
  "current": null,
  "outputs": {}
}
```

## Best practices

- **Write state before each step.** Persist `_workflow-state.json` after every module finishes; on resume, read it and skip done modules. Crash recovery without re-running paid API calls.
- **Cap searches per module.** Hard-stop at the README budgets (3-5 quick, 8-12 deep). Track count in the orchestrator, not the subagent — subagents lie about their own usage.
- **Pin source URLs in a separate `sources.md`.** Keep the synthesis files clean; an auditor or spec writer wants a flat URL list, not inline footnotes scattered across 5 files.
- **Force an "evidence row"** for every claim: `| Claim | Source URL | Quote | Date accessed |`. Validates the "no speculation" rule mechanically.
- **Cache web fetches by URL hash** for the duration of a workflow run — Deep mode often re-fetches the same competitor page across modes.
- **Two-pass naming.** Generate 20 candidates → filter to 5 with cheap `whois`/HEAD checks → run `faion-domain-checker-agent` only on the 5. README's all-at-once approach burns API quota.
- **Run `faion-marketing-manager` before `faion-sdd`** when go-to-market unknowns dominate; run `faion-sdd` first when feasibility is the larger risk. README presents them as parallel options — they are not.
- **Reject loop-back > 2 iterations.** If user rejects ideas twice, escalate (different prompt, different framework) rather than re-rolling the same generator.

## AI-agent gotchas

- **Hallucinated TAM/SAM/SOM.** LLMs fabricate market sizes confidently. Always require `≥3 independent URLs` for any number or write "Data not available".
- **Stale data.** Web search returns 2-3-year-old blog posts as if current. Reject any source older than 24 months for pricing/market data without explicit override.
- **Sequential rule violated by parallelism-loving agents.** Claude Code will eagerly batch tool calls. Enforce sequential by chaining Task calls in a single orchestrator turn, awaiting each.
- **`AskUserQuestion` ignored in headless / cron contexts.** The Idea Discovery and Naming workflows assume an interactive user. In automated pipelines (n8n, cron) the workflow stalls. Provide non-interactive mode that picks defaults.
- **Naming workflow false positives.** A 200 OK on `github.com/<name>` does not mean taken (could be an org page); a 404 does not mean free (could be reserved/squatted). Cross-check with `gh api users/<name>` and `whois`.
- **Domain registrar caching.** Namecheap returns "available" for ~5 minutes after a registration in some TLDs. Always re-check directly before the buy.
- **Loop without termination guard.** README's "loop back to step 2" has no exit. Wrap orchestrator with `max_iterations=3` or auto-exit to "kill" recommendation.
- **Agents lie about completion.** Subagents return "done" before writing the file. Orchestrator must `Read` the output file and check non-empty before advancing.
- **Cross-module contradictions.** `market-research.md` says TAM $2B; `competitive-analysis.md` quotes a competitor's $50M revenue claiming 60% share. Run a final `consistency-check` step before `executive-summary.md`.
- **Token blow-up at synthesis.** 5 modules × deep mode = 30-50k tokens. The summary subagent must be a separate session with only the 5 files in context, not the full search history.

## References

- Methodology README: `../README.md`
- Sibling: `../agent-invocation/README.md` (covers how to spawn `faion-research-agent`)
- Claude Code subagents: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code skills: https://docs.anthropic.com/en/docs/claude-code/skills
- Tavily Search API: https://docs.tavily.com
- Exa search API: https://docs.exa.ai
- Firecrawl: https://docs.firecrawl.dev
- Perplexity API: https://docs.perplexity.ai
- Reddit API (PRAW): https://praw.readthedocs.io
- Namecheap API: https://www.namecheap.com/support/api/intro/
- Cloudflare Registrar API: https://developers.cloudflare.com/registrar/
- ProductHunt API: https://api.producthunt.com/v2/docs
- HN Algolia API: https://hn.algolia.com/api
