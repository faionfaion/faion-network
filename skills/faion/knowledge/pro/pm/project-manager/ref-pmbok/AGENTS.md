# PMBoK 7 and 8 Reference

## Summary

Quick-reference tables for PMBoK 7 (8 performance domains, 12 principles) and PMBoK 8 (7 domains, 6 principles), plus EVM formulae, estimation accuracy bands, risk response strategies, and RAG status thresholds. This is a constants module for agent system prompts — inject the relevant table to anchor terminology. Not a methodology for doing anything; pair with operational methodologies (WBS, risk register, stakeholder engagement).

## Why

PMBoK 6 (process groups + knowledge areas) is heavily over-represented in LLM training data. Agents default to "Integration Management" and "Quality Management" as domain names even when instructed to use PMBoK 7/8. Injecting the exact table from this reference into the system prompt forces the right vocabulary. EVM arithmetic on more than 5 rows drifts in LLMs — always compute in code.

## When To Use

- Ground-truthing PMBoK terminology in system prompts, sponsor decks, or certification content
- Quick-lookup of EVM formulae, risk strategies, estimation accuracy, RAG thresholds during status report generation
- Disambiguating PMBoK 6 vs 7 vs 8 vocabulary before generating any PM content
- Building a translation layer for teams migrating from one edition to another

## When NOT To Use

- As a standalone methodology to do anything — it is a reference; pair with operational methodologies
- For non-PMI frameworks (PRINCE2, IPMA, ISO 21500) — vocabulary overlaps but differs; a pure PMBoK lens distorts those frameworks
- For agile-only environments that have no baseline — EVM formulae are meaningless without a scope and cost baseline

## Content

| File | What's inside |
|------|---------------|
| `content/01-pmbok7-reference.xml` | Eight domains, twelve principles, EVM formulae, estimation accuracy bands, risk strategies, RAG thresholds |
| `content/02-pmbok8-delta.xml` | PMBoK 8 changes: six principles, seven domains, sustainability, AI appendix; agent gotchas for edition drift |

## Templates

| File | Purpose |
|------|---------|
| `templates/evm-calculator.py` | EVM calculator: SV, CV, SPI, CPI, EAC, ETC, VAC, RAG from BAC/PV/EV/AC inputs |
