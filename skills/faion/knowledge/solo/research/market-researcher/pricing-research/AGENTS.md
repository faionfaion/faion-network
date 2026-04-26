# Pricing Research

## Summary

Six-step pricing framework: quantify value delivered, build a competitor pricing matrix, apply Van
Westendorp price sensitivity (4 questions), choose a billing model, design tier structure with
feature distribution, and validate via real sales. Output: recommended price bands with model
rationale, not a single number to hard-code.

## Why

Pricing set without research produces underpricing (leaving margin on the table) or overpricing
(losing customers) and wrong model selection (subscription when one-time fits). The Van Westendorp
method produces an acceptable price range from real respondents; the value-based ceiling (10-20%
capture of value delivered) provides an upper bound independent of competitor anchoring. Agents
fabricate both if given insufficient real data.

## When To Use

- Pre-launch: validating tier structure and price points before publishing pricing page.
- Quarterly pricing review after a market shift (new competitors, new category entrants).
- Pivoting model (one-time to subscription, freemium to paid trial).
- Setting enterprise/custom price floor for first sales call.

## When NOT To Use

- Fewer than 50 paying customers — talk to them directly; agent output is confabulation at this scale.
- B2B enterprise contract negotiation — relationship/procurement-driven, not formula-driven.
- Heavily regulated pricing (insurance, prescription, utility) — agent will not know jurisdiction rules.
- Marketplace/two-sided pricing — supply-and-demand dynamics need real telemetry, not survey output.

## Content

| File | What's inside |
|------|---------------|
| `content/01-value-and-competitors.xml` | Value metric types, capture-rate formula, competitor matrix structure, analysis rules. |
| `content/02-van-westendorp.xml` | VW 4-question method, optimal-point interpretation, simplified interview alternative. |
| `content/03-models-and-tiers.xml` | Billing model selection table, 3-tier design rules, feature distribution pattern. |
| `content/04-gotchas.xml` | Fabrication risks, capture-rate priors, annual-discount math, human-in-loop checkpoints. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pricing-report.md` | Full Pricing Research Report with value, competitor, VW, and recommendation sections. |
| `templates/pricing-quick-check.md` | Quick pricing check for low-stakes decisions. |
| `templates/prompt-competitor-scrape.txt` | Agent prompt for extracting normalized pricing matrix from competitor URLs. |
| `templates/prompt-value-model.txt` | Agent prompt for computing value-based price ceiling from interview transcripts. |
