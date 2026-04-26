# VUI Market Context

## Summary

VUI market context is reference content for grounding voice-product strategy in current adoption data and platform tradeoffs. It covers voice assistant usage statistics, smart speaker penetration, platform comparison (Alexa, Google Assistant, Siri, Bixby, custom LLM-VUI), and developer access surfaces. Numbers must be stamped with source year and geographic scope — they go stale within 6-12 months.

## Why

Platform selection decisions and stakeholder primers require concrete, sourced adoption figures, not anecdote. The methodology provides a canonical stat schema and a refresh pattern so agents can pull current numbers on demand rather than relying on stale hardcoded values. LLM-native voice agents (ChatGPT Voice, Claude voice) have reshaped the landscape since 2024 and now constitute a fifth platform category bypassing skill stores.

## When To Use

- Strategy phase of a voice-product proposal: ground the deck in current adoption stats and platform tradeoffs.
- Platform-selection decision: compare Alexa vs Google vs Siri vs custom LLM-VUI for target geos.
- Investor/stakeholder primers: a one-page market context sourced from canonical references.
- Quarterly brief refresh: pull current numbers on demand instead of relying on stale README values.

## When NOT To Use

- Implementation work — this is descriptive market context, not a how-to methodology.
- Platform already locked by contract — re-justification is not useful.
- Real-time competitive intelligence — use a market-research methodology with monitoring loops.

## Content

| File | What's inside |
|------|---------------|
| `content/01-market-stats.xml` | Adoption statistics schema (metric, value, year, source, geo), platform comparison table, stat refresh rules. |
| `content/02-platform-comparison.xml` | Developer access, supported locales, monetization, user reach, LLM integration openness per platform. |

## Templates

| File | Purpose |
|------|---------|
| `templates/refresh-script.py` | Python script: calls Claude with web_search tool to refresh stat list; stamps refreshed_at date. |
