# Agent Integration — Web Scraping

## When to use
- Sites without an API where you need product/price/listing data on a schedule.
- Research workflows: gather a corpus of pages for an LLM to summarize or fine-tune on.
- Monitoring: track changes to a competitor pricing page, regulator publication, status board.
- Aggregating content from JS-rendered SPAs that `curl` can't see.
- One-off backfills of public data into a dataset.

## When NOT to use
- The site offers an official API or RSS — use it. Cheaper, more reliable, ToS-clean.
- Targets where ToS forbid scraping and you have no fair-use defense.
- Authenticated account data of users who didn't consent.
- Data behind hard anti-bot walls (Cloudflare Turnstile interactive, Akamai bot manager) without a stealth budget.
- Sub-second latency requirements; scraping is inherently slow.

## Where it fails / limitations
- DOM churn: a marketing redesign breaks every selector. Brittle without role/text-based locators or tolerant parsers.
- Rate limits + IP blocks: agents that scrape too fast get the whole subnet banned.
- Cloudflare/PerimeterX/DataDome detect Playwright/Puppeteer signatures (`navigator.webdriver`, missing fonts, JS challenge timing).
- Pagination bugs: infinite scroll without dedup yields duplicate rows; agents miss the "newHeight === previousHeight" edge.
- Captchas: solving them programmatically is gray-area legally and brittle.
- Charset / encoding issues: BeautifulSoup vs lxml parser produces different trees.
- Schema drift over time silently corrupts datasets — needs a hash/snapshot diff per run.

## Agentic workflow
A scrape agent: (1) fetches with `curl -I` to confirm SSR vs JS-render; (2) for SSR uses `httpx`+`selectolax`/`BeautifulSoup`, for JS uses Playwright; (3) extracts with role/text locators; (4) writes to a versioned dataset (`raw/<date>/<source>.jsonl`); (5) runs a schema validation step; (6) on schema drift, raises a human review issue. Add polite delays, robots.txt check, and User-Agent identification. Use `faion-sdd-executor-agent` to gate dataset commits on schema validation pass.

### Recommended subagents
- `faion-sdd-executor-agent` — gates the scraper run as a quality task with schema-validation step.
- A composed `browser-agent` (per CLAUDE.md "Used by: faion-browser-agent") for Playwright-driven scrapes.

### Prompt pattern
```
Source: <URL>. Content: <product table | article list | etc.>.
Step 1: curl -sI <URL> — report content-type, server, set-cookie, status.
Step 2: curl -s <URL> | grep -E '<table|<article' — confirm SSR.
   If empty → JS-rendered, use Playwright with role-based locators.
   Else → httpx + selectolax with CSS selectors.
Step 3: Output schema as Pydantic / Zod. Validate every row. Drop invalid; log count.
Step 4: Save to raw/<YYYY-MM-DD>/<source>.jsonl. Commit dataset separately from code.
```

```
Detect schema drift: compare today's raw/<date>/<source>.jsonl
to last good run (git diff). If new fields → flag for review.
If existing fields disappear in > 5% of rows → fail and stop.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` / `httpx` (CLI) | SSR-only fetches; HTTP/2 + async | `pip install httpx[cli]` |
| `selectolax` | Fast lxml-based HTML parsing | `pip install selectolax` |
| `parsel` | Scrapy's selector lib, standalone | `pip install parsel` |
| `playwright` | JS-rendered scraping | see playwright-automation/ |
| `scrapy` | Full crawler framework with pipelines | `pip install scrapy` |
| `puppeteer-extra-plugin-stealth` | Bypass naive bot detection | `npm i puppeteer-extra puppeteer-extra-plugin-stealth` |
| `crawl4ai` | LLM-friendly scraping (markdown output) | `pip install crawl4ai` |
| `playwright-stealth` | Stealth for Playwright | `pip install playwright-stealth` |
| `firecrawl` (self-host) | Markdown-first scrape API | https://github.com/mendableai/firecrawl |
| `htmlq` | jq for HTML | `cargo install htmlq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Firecrawl | SaaS + OSS | Yes — REST API | Returns LLM-ready markdown; agent-first. |
| Browserbase | SaaS | Yes — Playwright CDP | Stealth profiles + residential proxies. |
| Bright Data Web Scraper | SaaS | Yes — API | Datasets-as-a-service; expensive. |
| ScraperAPI | SaaS | Yes — single endpoint | Handles proxies + JS rendering. |
| ScrapingBee | SaaS | Yes — REST | Simple GET wrapper, JS option. |
| Apify | SaaS + OSS | Yes — Actor API | Reusable scraper "actors"; agentic-friendly. |
| Crawlbase | SaaS | Yes — REST | Captcha solving included. |
| Reader by Jina | SaaS | Yes — `r.jina.ai/<url>` | Free LLM-readable text from any URL. |
| ZenRows | SaaS | Yes — REST | Anti-bot bypass focus. |

## Templates & scripts
See `templates.md` for full pagination/scroll handlers. Polite SSR scraper (≤50 lines):

```python
# polite_scrape.py
import asyncio, hashlib, json, time
from pathlib import Path
import httpx
from selectolax.parser import HTMLParser
from urllib.robotparser import RobotFileParser

UA = "ResearchBot/1.0 (+contact@example.com)"
DELAY = 1.5  # seconds between requests

async def fetch(client: httpx.AsyncClient, url: str) -> str:
    r = await client.get(url, headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    return r.text

def parse(html: str) -> list[dict]:
    tree = HTMLParser(html)
    rows = []
    for card in tree.css("article.item"):
        title = card.css_first("h2")
        price = card.css_first(".price")
        if title and price:
            rows.append({"title": title.text(strip=True),
                         "price": price.text(strip=True)})
    return rows

async def main(urls: list[str], out: Path):
    rp = RobotFileParser(); rp.set_url(urls[0].rsplit('/', 3)[0] + "/robots.txt"); rp.read()
    out.parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(http2=True) as client:
        with out.open("w") as f:
            for u in urls:
                if not rp.can_fetch(UA, u):
                    continue
                html = await fetch(client, u)
                for row in parse(html):
                    row["_source"] = u
                    row["_hash"] = hashlib.sha1(html.encode()).hexdigest()[:10]
                    f.write(json.dumps(row) + "\n")
                await asyncio.sleep(DELAY)

if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[2:], Path(sys.argv[1])))
```

## Best practices
- Check `robots.txt` and respect it; cache the result for the run.
- Identify yourself: descriptive User-Agent with contact email. Reduces ban risk.
- Throttle: 1-3 RPS minimum for small sites; jitter the delay.
- Cache pages locally during dev (`requests-cache` or filesystem) so iteration doesn't re-hit the target.
- Snapshot raw HTML alongside parsed JSON; lets you re-parse without re-scraping.
- Write parsers tolerant of missing fields — return `None` rather than crashing.
- Validate with Pydantic/Zod and log validation errors to a separate stream.
- Schedule with cron + a dead-letter table; never silently fail.
- For LLM consumption, prefer `firecrawl`/`r.jina.ai` markdown over raw HTML — saves 70%+ tokens.

## AI-agent gotchas
- Agents skip robots.txt unless explicitly told. Make it the first step.
- LLMs hallucinate site selectors that "feel right" (`.product-card`) when the actual class is `.css-1abc23`. Always inspect first.
- "Just retry on failure" loops without backoff get IPs banned in minutes.
- Login flows: agents commit cookies/tokens. Add `auth.json`, `cookies.json` to `.gitignore` template.
- Encoding: Asian-language sites often `gb2312` or `Shift_JIS`; agents assume utf-8 and silently corrupt.
- Pagination: agents stop at "next button gone" but miss infinite-scroll. State the layout in the prompt.
- Legal: agents don't reason about ToS. Human-in-loop checkpoint required for any commercial-data scrape.
- Use Reader (`r.jina.ai`) or Firecrawl when the agent only needs the text — it bypasses 90% of brittle-selector failures.

## References
- robots.txt spec — https://www.rfc-editor.org/rfc/rfc9309.html
- Scrapy docs — https://docs.scrapy.org/
- Firecrawl — https://github.com/mendableai/firecrawl
- Jina Reader — https://jina.ai/reader/
- "Scraping at scale" — Zyte (Scrapy) blog — https://www.zyte.com/blog/
- Sibling: `playwright-automation/`, `puppeteer-automation/`, `browser-automation-overview/`.
