# Agent Integration — Idea Generation

## When to use
- Solopreneur stuck on "what to build" with skills inventory but no candidate list.
- Need to generate 20-50 candidates fast across 7 frameworks (skills, pain mining, productized service, unbundling, market stacking, own problems, job substitution).
- Pre-niche-evaluation step: produce raw idea pool that downstream `niche-evaluation` will score.
- Refresh of stale roadmap: feed weekly capture template into agent on cron.

## When NOT to use
- You already have a validated idea with paying customers — skip to `pricing-research` or `mvp-scoping`.
- You're generating ideas without skills/constraints; agents will produce generic, ungrounded lists.
- You need novel scientific/research ideas — LLMs converge on consensus; use literature-driven discovery instead.

## Where it fails / limitations
- LLM idea generation is **mode-collapsed**: same prompt → same 30 ideas across solopreneur literature. Add randomized seed terms (Reddit thread URL, weekly news digest) to break this.
- Agents hallucinate "market sizes" and "successful examples" — never trust unverified numbers; pipe each idea through niche-evaluation with real data.
- No personal-fit signal: agent doesn't know your skill depth, only what you list. Output skews toward what's lexically common in training data (SaaS), undercounting service/info-product opportunities.
- Pain-point mining via Reddit/forums requires actual scraping; without WebFetch the agent fabricates plausible complaints.

## Agentic workflow
Drive with two-pass diverge/converge: pass 1 generates 30+ raw ideas across all 7 frameworks against a skills+constraints brief, pass 2 deduplicates and scores against the 5-criterion matrix. Use `faion-brainstorm` skill for the diverge phase (multi-agent perspectives) and a single converge agent for scoring. Capture into the `Idea Discovery Session` template, then hand top 3 to `niche-evaluation` agent. Run weekly on a schedule against a fresh inputs file (your week's pains + scraped Reddit).

### Recommended subagents
- `faion-brainstorm` skill — diverge phase, multi-perspective idea generation (already in repo).
- Custom `idea-generator` subagent — sonnet, sole job: framework-by-framework expansion of one skill+constraint brief into 30 candidates.
- Custom `idea-scorer` subagent — sonnet, applies 5-criterion matrix, returns ranked CSV.
- `faion-niche-evaluator` (downstream) — handoff for top 3.

### Prompt pattern
```
Brief: {skills}, {domains}, {constraints}, {time_budget}, {capital}
For each of 7 frameworks (skills inventory, pain mining, job substitution,
productized service, unbundling, market stacking, own problems), produce
4 candidate ideas. For each: problem, audience, rough solution.
Return JSON: [{framework, name, problem, audience, solution}]
```

```
Inputs: {30 ideas JSON}
Score each on Market(20%), Personal Fit(25%), Competition(15%),
Monetization(20%), Speed-to-MVP(20%). Return top 5 sorted desc with
reasoning per criterion. No fabricated market sizes — flag any number
you can't cite.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `glow` / `bat` | Render idea reports in terminal | `brew install glow` / `cargo install bat` |
| `gum choose` | Interactive idea picker | `brew install gum` |
| `pup` / `htmlq` | Scrape Reddit/HN for pain mining | `cargo install htmlq` |
| `claude` (Claude Code) | Drive subagents | https://docs.anthropic.com/en/docs/claude-code |
| `jq` | Parse/filter idea JSON | system pkg manager |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reddit JSON API | Free | Yes | `https://reddit.com/r/{sub}/top.json?t=month` — pain mining source. Rate-limited; needs auth header. |
| Hacker News Algolia API | Free | Yes | `hn.algolia.com/api/v1/search` — competitor signal, complaints, "Show HN". |
| Exploding Topics | SaaS | Partial | Trend signal; UI-first, scrape with Playwright. |
| Indie Hackers | Free | Yes | Public revenue/idea data; scrapeable for productized-service patterns. |
| Product Hunt API | Free tier | Yes | GraphQL API; lists recently launched ideas (anti-pattern: avoid duplicates). |
| Google Trends (`pytrends`) | OSS lib | Yes | Validate idea direction; unofficial Python wrapper. |
| Upwork/Fiverr | SaaS | Scrape only | Job-substitution framework needs gig listings; no idea-friendly API. |
| Notion / Obsidian | Note tool | Yes (MCP/Notion API) | Persist idea register, weekly capture template. |

## Templates & scripts
See `templates.md` for Discovery Session and Weekly Capture. Minimal driver:

```bash
#!/usr/bin/env bash
# weekly-idea-run.sh — cron @weekly
set -euo pipefail
WEEK=$(date +%Y-W%V)
OUT=~/ideas/$WEEK
mkdir -p "$OUT"
# 1. Pull pains
for sub in startups SaaS Entrepreneur smallbusiness; do
  curl -sH "User-Agent: idea-bot/1.0" \
    "https://reddit.com/r/$sub/top.json?t=week&limit=50" \
    > "$OUT/$sub.json"
done
# 2. Brief
cat > "$OUT/brief.md" <<EOF
Skills: $(cat ~/ideas/skills.txt)
Pains week: $(jq -r '.data.children[].data.title' "$OUT"/*.json | head -30)
EOF
# 3. Diverge → converge
claude -p "$(cat ~/prompts/idea-diverge.txt) $(cat $OUT/brief.md)" \
  > "$OUT/30-ideas.json"
claude -p "$(cat ~/prompts/idea-score.txt) $(cat $OUT/30-ideas.json)" \
  > "$OUT/top5.md"
```

## Best practices
- **Seed with constraints, not goals**: "I have 10h/week, $0 budget, Python + B2B SaaS background" beats "find me a billion-dollar idea".
- **Run weekly, archive monthly**: ideas compound. Most useful idea at month 3 is rarely the one from week 1.
- **Score independently from generation**: same agent that generated will rationalize bad ideas. Use second context.
- **Personal fit > market**: a 4.0-fit/3-market idea ships; a 2-fit/5-market idea dies. Override the weighted total when fit < 3.
- **Cap scoring at 5 candidates**: scoring 30 is theatre. Filter to top-by-gut, then score rigorously.
- **Disambiguate framework-stacking**: market-stacking + unbundling generates the same idea twice. Dedupe by audience+problem, not by name.

## AI-agent gotchas
- LLMs systematically over-rate "Speed to MVP" — they think everything is 2 weeks. Hard-code: any idea touching auth/billing/integrations = minimum M.
- Pain-point mining without source URLs is fabrication. Force agents to return `evidence: [{url, quote}]` per idea or reject.
- Mode collapse on "AI-powered X" — explicitly forbid prefixes/suffixes (AI, smart, intelligent, GPT) in the prompt to force diverse framing.
- **Human-in-loop checkpoint**: never let an agent autonomously commit to building. The decision after scoring is a founder decision; agent's job ends at ranked list with evidence.
- Agent confidence is meaningless on novelty — there's no training-data signal for "is this actually new". Always cross-check top idea against Indie Hackers / Product Hunt / Google manually.
- LLM-generated TAM/SAM numbers are confabulation. Extract them as `unverified_claim` and require a citable source before they enter the scorecard.

## References
- Rob Walling — "Start Small, Stay Small" (productized service framework origin)
- Indie Hackers community — https://www.indiehackers.com/products
- Y Combinator Request for Startups — https://www.ycombinator.com/rfs (idea seed, not idea source)
- Justin Welsh — "Diary of a Solopreneur" (market-stacking patterns)
- Anthropic — multi-agent diverge/converge in Claude Code (faion-brainstorm reference)
