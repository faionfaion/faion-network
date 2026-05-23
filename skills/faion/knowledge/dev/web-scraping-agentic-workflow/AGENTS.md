# Web Scraping — Agentic Workflow

## Summary

**One-sentence:** End-to-end agentic scrape pipeline: probe SSR vs JS-render, pick tool, extract with schema, write versioned JSONL, detect drift — emits a per-run report artefact.

**One-paragraph:** Letting an LLM agent run a scrape end-to-end is one of the highest-leverage automations for a solo dev. It is also one of the easiest to get silently wrong: agents skip robots.txt, fabricate selectors, pick Playwright for SSR pages, and accept malformed rows. This methodology pins the order: (1) curl probe to confirm SSR vs JS-render; (2) tool choice (httpx + selectolax for SSR, Playwright for JS, managed Firecrawl / r.jina.ai for clean text); (3) extraction with role/text locators not guessed classes; (4) Pydantic/Zod validation row-by-row; (5) versioned JSONL store under `raw/YYYY-MM-DD/source.jsonl`; (6) schema-drift alarm at &gt;5% field disappearance. The artefact is a scrape-run report (rows extracted, rows invalid, drift score, tool, run id) the agent emits at end of run.

**Ефективно для:**

- Solo / outsource dev scraping 1+ source per day and wanting LLM autonomy bounded by a deterministic report.
- AI agent (Claude Code, GPT-4-turbo) instructed to scrape — needs the order locked-in so it doesn't pick Playwright for static HTML.
- Multi-source pipelines where schema drift across sources is the cost of doing business.
- Cost optimisation: managed services (Firecrawl) saves 70% tokens vs raw-HTML feed.

## Applies If (ALL must hold)

- A named target source exists with a defined URL pattern.
- robots.txt allows scraping OR a legal exception applies.
- A schema (Pydantic / Zod / JSON Schema) is defined for the rows you want.
- You can write to a local / blob store partitioned by date.

## Skip If (ANY kills it)

- The source provides an official API — use it, don't scrape.
- robots.txt forbids scraping AND no legal exception — stop.
- One-off scrape with no recurrence — quick-and-dirty is acceptable; this methodology is for repeat runs.
- Source returns rate-limited 429 even at low rates — see `web-scraping-resilience` first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target URL pattern | string | task brief |
| Row schema | Pydantic / Zod / JSON Schema | repo |
| Bot User-Agent + contact email | string | team config |
| Storage path or bucket | URL | infra |
| robots.txt cache (per run) | text | URL |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/web-scraping-element-extraction` | Step 3 of this workflow — extraction details. |
| `solo/dev/automation-tooling/web-scraping-pagination` | Step 3.5 — pagination handling. |
| `solo/dev/automation-tooling/web-scraping-resilience` | Step ∞ — production-grade resilience. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: probe-first, tool-by-render-mode, locator-roles, validate-rows, versioned-JSONL, drift-alarm, run-the-checklist + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for scrape-run report + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: Playwright on SSR, fabricated selectors, skipped robots.txt, drift ignored | 700 |
| `content/04-procedure.xml` | medium | 6-step procedure: probe → tool → extract → validate → store → drift | 700 |
| `content/05-examples.xml` | reference | Worked example: scraping a news listing across 30 days with drift caught at day 18 | 600 |
| `content/06-decision-tree.xml` | essential | Tree: render mode? → tool → drift? → emit verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `probe-render-mode` | haiku | curl -I + small payload heuristic; deterministic. |
| `extract-with-locators` | sonnet | Bounded judgment on role/text vs class selectors. |
| `cluster-drift` | sonnet | Grouping disappeared fields into root-cause clusters. |

## Templates

| File | Purpose |
|------|---------|
| `templates/web-scraping-agentic-workflow.json` | JSON Schema for the scrape-run report artefact. |
| `templates/scrape-run-report.md` | Markdown skeleton authors fill at end-of-run. |
| `templates/agent-prompt.md` | Prompt skeleton for an LLM scrape agent (forces robots.txt + tool order). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-web-scraping-agentic-workflow.py` | Validate a scrape-run report JSON against schema + drift rule. | At end of each scrape run, before promoting raw → curated. |

## Related

- [[web-scraping-element-extraction]] — inner extraction step.
- [[web-scraping-pagination]] — pagination handling.
- [[web-scraping-resilience]] — rate-limit + retry + anti-detection.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks render mode (SSR / JS / managed) and routes to the matching tool. It then walks: locator strategy (roles/text vs classes), validation rate (rows_valid / rows_seen ≥ 0.9), drift score (disappeared fields ≤ 5%). Leaves emit `promote`, `block-validation-low`, `block-drift-high`, or `block-tool-mismatch`, each referencing a rule in `01-core-rules.xml`.
