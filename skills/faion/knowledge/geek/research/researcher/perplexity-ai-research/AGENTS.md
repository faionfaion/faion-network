# Perplexity AI for Research

## Summary

A workflow for using Perplexity Pro Search to synthesize cited multi-source research answers. Sonnet decomposes a research question into atomic sub-queries; Haiku executes each Pro Search call; Sonnet synthesizes results and flags conflicting or low-confidence claims. Human reviews flagged items before findings enter any downstream pipeline.

## Why

Claude alone lacks live web data; Perplexity returns citations alongside synthesis. Decomposing compound questions into atomic sub-queries (one fact per query) produces higher-quality answers than asking everything at once. Requiring confidence ratings (H/M/L) based on source count forces honest calibration.

## When To Use

- Fast synthesis of a research question requiring 5+ web sources simultaneously.
- Market sizing, competitive landscape, or trend research where citations matter.
- Fact-checking a specific claim with primary source validation.
- When the question requires live web data (post-knowledge-cutoff events, current pricing, recent funding).

## When NOT To Use

- When primary source documents (PDFs, internal databases) are required — Perplexity only searches the public web.
- For confidential competitive research — queries leak strategic intent via Perplexity's servers.
- When a single authoritative source is available directly — fetch it with a targeted HTTP call.
- For strategy or product decisions requiring reasoned tradeoffs — Perplexity retrieves, does not reason.

## Content

| File | What's inside |
|------|---------------|
| `content/01-method.xml` | Perplexity capabilities, usage stats, query strategies by research type, limitations. |
| `content/02-agent-workflow.xml` | Atomic sub-query decomposition pipeline, prompt patterns, gotchas, best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/perplexity-research.py` | Python: batch Pro Search queries via Perplexity REST API with citation extraction. |
| `templates/query-decompose-prompt.txt` | Prompt for decomposing a research question into atomic Perplexity sub-queries. |
