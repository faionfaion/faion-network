# Market Sizing with AI

## Summary

AI-assisted TAM/SAM/SOM estimation via top-down and bottom-up triangulation.
Run both methods independently using separate Perplexity and web-search calls,
document every assumption, then triangulate: if both paths agree within 2x,
confidence is defensible; if not, flag the divergence and identify the assumption
driving the gap. Output a structured estimate with confidence ranges, not point numbers.

## Why

TAM/SAM/SOM estimates built from a single research path are finger-in-the-air numbers.
Triangulating two independent methods — one from industry reports down, one from
customer counts up — increases confidence and forces explicit assumption logging.
AI tools confuse TAM, SAM, and SOM if not defined in the prompt; the structured
prompt pattern in the templates eliminates this ambiguity.

## When To Use

- Producing TAM/SAM/SOM estimates to support a go/no-go decision or investor deck
- Triangulating market size when no single authoritative report exists
- Stress-testing existing market estimates by running independent top-down and bottom-up paths
- Automating recurring market-size updates as part of a research cadence

## When NOT To Use

- When the investor or client requires named analyst reports (Gartner, IDC) — AI cannot substitute these
- Highly novel markets with less than 12 months of public data — AI extrapolates from unreliable proxies
- Regulated contexts (IPO prospectus, SEC filing) where every number needs traceable sourcing
- When the market boundary is contested — AI anchors to the most common framing without flagging ambiguity

## Content

| File | What's inside |
|------|---------------|
| `content/01-method.xml` | Top-down + bottom-up triangulation rules, tool table, checklist |
| `content/02-agentic-patterns.xml` | Orchestrator prompt, gotchas, CLI/SaaS table |

## Templates

| File | Purpose |
|------|---------|
| `templates/triangulate.py` | Claude SDK triangulator: runs two paths, flags >2x divergence |
| `templates/market-sizing-prompt.txt` | XML prompt for market sizing task |
