# Agent Integration — Agent Invocation (faion-researcher)

Reference: `README.md` in this folder. This file covers how to drive the
`faion-researcher` invocation surface from Claude subagents and external CLIs.

## When to use

- Orchestrating a multi-stage research run (`ideas → pains → niche → market → competitors → pricing → personas → validate → names → domains`) where each stage's output feeds the next.
- A user asks "research X" and you need to pick the right mode (one of the 9 modes documented in README.md) without polluting the parent context with raw web search noise.
- Naming + domain check workflows where `names` mode must hand off to `faion-domain-checker-agent` for `.com/.io/.co/GitHub/Twitter` checks.
- You need the output to land deterministically in `.aidocs/product_docs/<file>.md` (one file per mode) so downstream skills like `faion-sdd` and `faion-product-manager` can consume it.

## When NOT to use

- One-off factual lookup (a single TAM number, a single competitor URL) — call `WebSearch` directly; spinning up a research subagent costs 10x more tokens.
- Internal codebase research — use `Grep`/`Glob`/`Agent` instead. The research agent is tuned for external web sources, not source code.
- Ideation that is purely creative (brand voice, copy variants) — use `brainstorm` (diverge/converge/review) instead of `mode: ideas`.
- The user's project already has fresh `market-research.md` / `competitive-analysis.md`. Re-running burns budget; read existing files first.

## Where it fails / limitations

- **Mode is not a real subagent type.** `subagent_type="faion-research-agent (mode: market)"` is a *naming convention* — Claude Code's `Task` tool only accepts the agent's actual `name` from the agent frontmatter. Pass the mode inside the `prompt` field, not the `subagent_type` string, or define one agent file per mode.
- **No native parallelism.** README warns "always run sequentially" — this is a hard constraint, not a preference. Parallel research mode invocations duplicate WebSearch quota and frequently hit rate limits on shared providers (Brave, Perplexity, Tavily).
- **Stale data.** `pricing` and `competitors` modes degrade fast (3–6 months). Never trust an output older than the last release of any cited competitor.
- **Hallucinated sources.** Without forced URL citation in the system prompt, models invent G2/Capterra slugs. Validate every URL with `WebFetch` before quoting.
- **Context blow-up.** A full 9-mode run with deep mode (8–12 searches each) emits 60–100k tokens of output. Pipe each mode through a summarizer agent or persist to disk and reload only the executive summary.

## Agentic workflow

Drive `faion-researcher` from a parent orchestrator that owns the mode sequence and writes outputs to `.aidocs/product_docs/`. The parent calls `Task` once per mode, passes the previous mode's output path in the prompt for context-passing, and waits for each `Task` to return before launching the next. For naming workflows, chain `mode: names` → `faion-domain-checker-agent` and discard names with `.com` taken or trademark conflicts before the user sees them. Keep each subagent's tool list minimal (Read, Write, WebSearch, WebFetch) so it cannot accidentally edit code or call shell.

### Recommended subagents

- `faion-research-agent` — Orchestrator implementing the 9 modes. One agent file per mode is cleaner than runtime mode dispatch (lets you tune `description`, `tools`, `model` per mode: `haiku` for data lookup, `sonnet` for pattern analysis, `opus` for strategic positioning per README.md table).
- `faion-domain-checker-agent` — Sonnet-tier; uses `WebFetch` against `whois.com`, `domains.google`, `github.com/<name>`, `twitter.com/<name>`. Returns availability table.
- `faion-sdd-executor-agent` (this repo, `agents/faion-sdd-executor-agent.md`) — Consumes finished research artifacts to produce `spec.md` / `design.md`. Not part of the research loop itself; downstream consumer.
- `password-scrubber-agent` (this repo) — Run before persisting any scraped content that may contain leaked tokens from forum dumps.

### Prompt pattern

```
Subagent prompt (mode: market):
"Research TAM/SAM/SOM for {product}. Geography: {geo}. Vertical: {vertical}.
Output to .aidocs/product_docs/market-research.md. Cite every figure with
[Source](URL). If a figure is unavailable, write 'Data not available' — do
not estimate. Read .aidocs/product_docs/idea-validation.md first if it
exists. Return only the absolute path of the file you wrote."
```

```
Subagent prompt (mode: names → domain check chain):
"Generate 15 names for {product_description}, tone={tone}. For each name,
immediately invoke Task(faion-domain-checker-agent, '{name}'). Drop any
name where .com is taken AND no premium acquirable, OR trademark conflict
exists (USPTO TESS lookup). Persist survivors to
.aidocs/product_docs/name-candidates.md sorted by score."
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | GitHub username/repo availability for naming mode | `apt install gh` · https://cli.github.com |
| `whois` | Direct domain lookup, faster than scraping registrars | `apt install whois` |
| `dig +short <name>.com NS` | Confirm domain has nameservers (parked vs taken) | iputils-host |
| `tldextract` (Python) | Parse domains from competitor URLs | `pip install tldextract` |
| `tavily-python` | Citation-quality search for `mode: market`/`competitors` | `pip install tavily-python` · https://tavily.com |
| `perplexity` API | High-citation answers for validate/pricing modes | https://docs.perplexity.ai |
| `firecrawl` CLI | Headless scrape of paywalled competitor docs | `npm i -g @mendable/firecrawl-js` |
| `wappalyzer` CLI | Detect competitor stack for `mode: competitors` | `npm i -g wappalyzer-cli` |
| `simfin` / `yfinance` | Public-company financials for TAM models | `pip install yfinance` |
| `op` (1Password CLI) | Pull research API keys from vault | https://developer.1password.com/docs/cli |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tavily Search API | SaaS | Yes — REST + Python SDK, returns citations as structured JSON | Best default for `WebSearch` replacement when running research at scale |
| Perplexity API | SaaS | Yes — `/sonar` endpoint returns answer+citations | Higher quality than raw search for `validate` mode |
| Exa.ai | SaaS | Yes — neural search, supports embeddings | Good for finding adjacent / similar companies in `competitors` |
| Firecrawl | SaaS + OSS | Yes — handles JS-rendered competitor sites | Fallback when `WebFetch` returns empty body |
| SimilarWeb API | SaaS | Partial — strict rate limits, expensive | Traffic estimates for `competitors`; usually overkill |
| Crunchbase API | SaaS | Yes — paid tier required | Funding data for `competitors`/`market` |
| Google Trends (`pytrends`) | OSS wrapper | Yes — unofficial, fragile | Search-volume signal for `validate` |
| Reddit API (PRAW) | OSS wrapper | Yes — rate limits OK with auth | Pain-point mining for `pains` mode |
| Hacker News Algolia API | SaaS (free) | Yes — no auth | Pain-point mining for `pains` mode |
| G2 / Capterra | SaaS (no public API) | Scrape-only — fragile | Use Firecrawl, expect breakage every quarter |
| USPTO TESS | Government | Yes — HTML scrape | Trademark conflict check for `names` mode |
| Domainr API | SaaS | Yes — domain availability across 500+ TLDs | Replaces multiple `whois` calls in `domain-check` |

## Templates & scripts

See `templates.md` for invocation skeletons. Inline below: a 40-line dispatcher that translates the README's "mode" convention into actual `Task` calls, with sequential execution and output-path tracking.

```bash
#!/usr/bin/env bash
# research-run.sh — drive faion-researcher modes sequentially.
# Usage: research-run.sh "<product description>" "ideas market competitors pricing"
set -euo pipefail

PRODUCT="$1"; shift
MODES="${*:-ideas market competitors personas validate pricing}"
OUT_DIR=".aidocs/product_docs"
mkdir -p "$OUT_DIR"

declare -A MODE_FILE=(
  [ideas]="idea-validation.md"
  [market]="market-research.md"
  [competitors]="competitive-analysis.md"
  [pains]="pain-points.md"
  [personas]="user-personas.md"
  [validate]="problem-validation.md"
  [niche]="niche-evaluation.md"
  [pricing]="pricing-research.md"
  [names]="name-candidates.md"
)

for mode in $MODES; do
  out="$OUT_DIR/${MODE_FILE[$mode]}"
  prior_args=""
  for prior in "$OUT_DIR"/*.md; do
    [ -f "$prior" ] && prior_args+=" --context $prior"
  done
  echo "[$(date -Is)] mode=$mode → $out"
  claude -p "Invoke faion-research-agent in mode '$mode' for product '$PRODUCT'. \
Read existing files in $OUT_DIR before starting. Write result to $out. \
Cite every claim. Output only the absolute path on success." \
    --output-format text > "$out.log" 2>&1
  test -s "$out" || { echo "FAIL mode=$mode"; exit 1; }
done
echo "OK research package → $OUT_DIR"
```

## Best practices

- One mode = one file = one Task call. Never bundle 2 modes in one prompt — output gets entangled and re-runs become impossible.
- Pass *file paths* of prior outputs to subsequent modes, not the file contents. The subagent re-Reads on demand. Saves 5–20k tokens per call.
- Pin a model per mode in the agent file frontmatter: `haiku` for `ideas`/`names`/`domain-check`, `sonnet` for `pains`/`personas`/`competitors`/`validate`, `opus` for `market`/`niche`/`pricing` (matches the agent-selection table in README.md).
- Run `pains` BEFORE `validate`. Validation without a pain inventory becomes self-confirmation. README's example sequences this correctly; preserve order.
- For `names` mode, generate 20 and let `faion-domain-checker-agent` filter to 5. Generating 5 directly yields zero survivors ~70% of the time.
- Every mode's output file MUST start with a 1-line provenance header: `<!-- generated: faion-research-agent mode=market on 2026-04-24 -->`. Lets `improver` audit staleness later.
- Keep `WebFetch` in the allowed-tools list — `WebSearch` alone returns snippets, and modes like `competitors` need full pricing pages.

## AI-agent gotchas

- **`subagent_type` string mismatch.** `Task(subagent_type="faion-research-agent (mode: market)")` does NOT route to a real agent — Claude Code resolves `subagent_type` against the literal `name:` in agent frontmatter. The README's pattern is pseudocode; you must either define `faion-research-market-agent` files OR pass mode inside the prompt and have one agent file dispatch internally.
- **Sequential constraint is enforced by quota, not by code.** Nothing prevents the parent from launching 9 parallel `Task` calls; you'll just get HTTP 429s mid-run, partial outputs, and a corrupt `.aidocs/product_docs/` state. Add an explicit semaphore in the orchestrator.
- **Hallucinated G2/Capterra/Trustpilot listings.** Models love to invent `g2.com/products/<plausible-slug>` URLs. Force a `WebFetch` round-trip before the URL appears in the output file; reject 404s.
- **Scope creep on `pains` mode.** Without a hard cap (e.g., "top 10 pains, ≥3 sources each, drop the rest") agents return 40+ pains, none well-sourced. Specify cap in the prompt.
- **Trademark check is a human-in-the-loop checkpoint.** USPTO TESS scraping is brittle and false-negatives cost real money. Surface the top 3 names back to the user with a `[ ] confirmed not-trademarked` checkbox before any domain purchase.
- **Pricing mode regional drift.** `Pricing for {product}` without geography returns US-defaults. The user is in EU/UA — always pass geography explicitly or the output is wrong by ~30%.
- **Persona fabrication.** `personas` mode without `pains.md` produces archetypes with invented quotes. Gate `personas` on `pains` existing, or require ≥1 real quote per persona with source URL.
- **Token overflow on `executive-summary`.** Reading all 9 mode files into one prompt blows past 200k tokens for verbose deep runs. Summarize each file to ≤2k tokens first, then synthesize.

## References

- This methodology's README: `./README.md` (sections: Agent Selection, Mode-Specific Invocations, Multi-Mode Workflows)
- Researcher SKILL.md: `../SKILL.md`
- Sibling skill `faion-research-agent` definition pattern: `agents/faion-sdd-executor-agent.md` (use as template for new research-agent files)
- Claude Code subagents: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code Task tool reference: https://docs.anthropic.com/en/docs/claude-code/agent-sdk
- Tavily citation-quality search: https://docs.tavily.com
- Perplexity Sonar API: https://docs.perplexity.ai/docs/getting-started
- Firecrawl: https://docs.firecrawl.dev
- USPTO TESS (trademark): https://tmsearch.uspto.gov
- Domainr API: https://domainr.com/docs/api
