# Agent Integration — Naming and Domains

## When to use
- Pre-launch: locking name + domain + core social handles in one batch.
- Rebrand / sub-product launch: testing 20+ candidates against availability and trademark.
- Naming a project where domain availability is the binding constraint (no .com → no go).
- Generating localized variants (UA/RU/EN/DE) of a brand for multi-region launch.

## When NOT to use
- You already have an established brand — naming agents will not improve mature trademarks.
- Highly regulated industries (pharma, finance) where naming triggers regulator review — manual lawyer step required.
- Internal/code-name only — domain check is wasted effort.

## Where it fails / limitations
- LLM naming is heavily mode-collapsed: same prompt ⇒ "Lify, Spark, Loop, Flux, Atlas, Nova, Pulse" repeatedly. Diversity requires explicit anti-patterns in the prompt.
- Domain availability: WHOIS/RDAP rate-limits agents fast; some TLDs (.io, .ai) need authenticated registrar APIs.
- Trademark check via USPTO TESS is non-trivial — agents miss similar marks (phonetic, design); never substitute for an attorney.
- Pronunciation/cultural pitfalls: agent-generated names like "Krapp", "Pschitt", "Sega" (Italian "sega" = saw/handjob) — needs L1 speaker review.
- Premium domain pricing fluctuates; scraped prices stale within weeks.

## Agentic workflow
Pipeline: (1) `name-generator` agent produces 30-50 candidates from brief (attributes, keywords, anti-patterns). (2) `availability-checker` agent runs WHOIS/RDAP + GitHub + npm + Twitter handle checks in parallel; returns matrix. (3) `trademark-prefilter` agent runs USPTO TESS basic search and flags risky candidates — human attorney required for final clearance. (4) Human shortlist + human pronunciation/cultural review with native speakers. Generation is throwaway-cheap; rerun until 3 viable candidates pass all gates.

### Recommended subagents
- `name-generator` — sonnet, applies 7 strategies (descriptive/invented/compound/metaphor/portmanteau/alliteration/acronym), enforces anti-pattern list.
- `availability-checker` — haiku, parallel WHOIS + handle lookups via tools.
- `trademark-prefilter` — sonnet, USPTO TESS WebFetch; outputs risk band only, NOT clearance.
- `cultural-checker` — sonnet, multi-language profanity / negative-meaning audit. Confirm with humans.

### Prompt pattern
```
Brief:
  attributes: [simple, fast, trustworthy]
  keywords: [tasks, workflow, automation]
  anti-patterns: NO [-ly, -ify, -hub, AI-, smart-, .ai TLD, Spark, Atlas, Nova]
  length: 5-10 chars
  pronunciation: 2 syllables max
Generate 30 candidates across 7 strategies. Return JSON:
[{name, strategy, reasoning, expected_pronunciation}]
```

```
Candidates: [list of 30]
For each, check in parallel:
  .com, .io, .co, .app TLDs
  GitHub org, npm package, PyPI package
  Twitter/X, LinkedIn company URL slug
  USPTO TESS basic search
Return matrix; rank by # of green checks.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `whois` | TLD availability check | system |
| `rdap-client` | Modern WHOIS replacement | `pip install whoisit` |
| `dnstwist` | Find typo-squat/similar registered domains | `pip install dnstwist` |
| `namecheap-api-cli` | Bulk availability + price | https://www.namecheap.com/support/api/ |
| `gh api` | GitHub org/repo namespace check | https://cli.github.com |
| `npm view <name>` | npm package namespace | bundled with npm |
| `python -m pip index` | PyPI namespace probe | pip |
| `claude` + WebFetch | TESS, premium-domain pricing | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Namecheap API | SaaS | Yes (XML) | Bulk availability + price; free dev key with low limits. |
| Porkbun API | SaaS | Yes (JSON) | Cheaper TLDs (.dev, .app); modern REST. |
| Cloudflare Registrar | SaaS | Yes (API v4) | At-cost pricing; agent-driven registration straightforward. |
| GoDaddy / Dynadot | SaaS | API yes | More TLDs but pricier; rate-limited. |
| Namechk | SaaS | Scrape only | One-shot multi-handle check; UI-first. |
| USPTO TESS | Free gov | WebFetch only | US trademark database; no public API; HTML-form-driven. |
| EUIPO eSearch | Free gov | Limited | EU trademark; clunkier than TESS. |
| Brandbucket / Squadhelp | SaaS | Browse only | Premium-name marketplace; agents can't bid. |
| Sedo / Afternic | SaaS | Limited | Aftermarket pricing; price-discovery only. |
| Wayback Machine | Free | Yes | Check if a "parked" domain ever had real product. |
| Google Translate API | SaaS | Yes | Cheap multi-language meaning audit; not perfect. |

## Templates & scripts
See `templates.md` for Naming Brief and Domain Check Report. Bulk availability runner:

```bash
#!/usr/bin/env bash
# check-names.sh — read names.txt, output matrix.csv
set -euo pipefail
NAMES=${1:?names.txt required}
OUT=~/names/$(date +%F).csv
mkdir -p ~/names
echo "name,com,io,co,app,gh,npm,pypi,twitter" > "$OUT"

while IFS= read -r name; do
  com=$(whois "$name.com" | grep -qi "no match\|not found" && echo Y || echo N)
  io=$(whois "$name.io" | grep -qi "no match\|not found" && echo Y || echo N)
  co=$(whois "$name.co" | grep -qi "no match\|not found" && echo Y || echo N)
  app=$(whois "$name.app" | grep -qi "no match\|not found" && echo Y || echo N)
  gh=$(curl -s -o /dev/null -w "%{http_code}" "https://github.com/$name" \
       | grep -q 404 && echo Y || echo N)
  npm=$(npm view "$name" 2>/dev/null >/dev/null && echo N || echo Y)
  pypi=$(curl -s -o /dev/null -w "%{http_code}" \
         "https://pypi.org/pypi/$name/json" | grep -q 404 && echo Y || echo N)
  tw=$(curl -s -o /dev/null -w "%{http_code}" "https://twitter.com/$name" \
       | grep -q 404 && echo Y || echo N)
  echo "$name,$com,$io,$co,$app,$gh,$npm,$pypi,$tw" >> "$OUT"
  sleep 1  # rate-limit politeness
done < "$NAMES"

column -t -s, "$OUT"
```

## Best practices
- **.com is still king** for B2B; .io for devtools; .ai for ML products only if budget tolerates premium. Skip .xyz/.tech for serious brands.
- **Trademark > availability**: a free .com that infringes is worse than a paid premium that's clear.
- **5-10 character sweet spot**: short → premium-priced; long → unmemorable.
- **Pronunciation test live**: get 5 humans to say the name from text alone. If 2+ stumble, drop it.
- **Negative-space check**: Google "[name] meaning" + native speakers in target markets — agents miss culturally negative associations.
- **Reserve handles before announcing**: GitHub org, npm/PyPI, Twitter, LinkedIn — even if unused, reserve in same hour as registering domain.
- **Don't chase parked premiums**: if a domain has been parked >5 years and asking price is >$5k for a non-revenue project, walk away.
- **Avoid hyphens, numbers, and ambiguous letters (l/I/1, O/0)** — kill memorability, hurt voice spelling.

## AI-agent gotchas
- LLM naming defaults to "fluffy startup-y" register: -ly, -ify, -ai, Hub, Loop, Spark. Forbid in prompt.
- Phonetic similarity to existing brands isn't caught by string match — agent will offer "Slock" thinking Slack is taken.
- Domain WHOIS responses vary by registry — "no match" / "not found" / "no entries" / "AVAILABLE". Agent regex misses some; verify 2-3 patterns.
- Some TLDs deny WHOIS to non-authenticated clients (.de needs DENIC TCP); agents falsely report "available".
- USPTO TESS HTML changes ~yearly — scrape will break; prefer WebFetch with current selector probing.
- **Human-in-loop checkpoint**: trademark clearance MUST end at human attorney. Agent output is informational risk band, not legal advice.
- Domains "available" by WHOIS may be reserved (premium tier) at registrar — always confirm at the registrar API, not just WHOIS.
- Cultural meaning checks need native L1 speakers; Google Translate misses slang/profanity.
- Price scraping is stale fast — re-fetch within 48h of registration decision.

## References
- Igor Naming — "The Power of Naming" (https://www.igorinternational.com/process/)
- Crew naming guide (Marty Neumeier) — "The Brand Gap"
- USPTO TESS — https://tmsearch.uspto.gov
- ICANN domain registry data — https://lookup.icann.org
- Paul Graham — "Naming a Startup" essay
- Practical Trademark Manual — Nolo Press
