# Modern BA Framework

## Summary

Select one primary BA reference framework (BABOK v3, BA Standard 2025, IREB CPRE, PMI-PBA, BCS Diploma, SAFe BA, Agile Extension to BABOK v2, SWEBOK v4) for an engagement before producing any artifact. Score candidates on regulatory fit, team maturity, vocabulary overlap, tooling support, and agile friendliness. Persist the decision as `ba-framework-decision.md` with a vocabulary glossary. This selection is upstream of all routing decisions — pick the rulebook before picking the plays.

## Why

LLMs default to BABOK because it is the most tokenized BA reference in training data. Without a structured selection step, non-IIBA shops (IREB, PMI, BCS) never get the appropriate framework, terminology skew accumulates across artifacts, and regulated programs fail audit because deliverable vocabulary does not match the contracted standard.

## When To Use

- Onboarding a BA or agent into an unfamiliar org where the "BA standard" is unclear or contested
- Procurement or RFP responses naming a specific standard — deliverable vocabulary must match exactly
- Regulated industries (pharma GxP, banking BCBS 239, automotive ASPICE) where requirements artifacts are auditable
- Multi-vendor programs where each vendor uses a different BA dialect — normalize to one canonical vocabulary
- Hybrid agile/waterfall portfolios requiring a documented bridge between BABOK and Scrum/SAFe ceremonies
- Building an internal BA competency matrix or training curriculum anchored to a published syllabus

## When NOT To Use

- Team already has a working BA practice with a known reference — re-selection is rework theatre
- Solo founder or 1-2 person product — continuous discovery + plain user stories beats any framework overhead
- Pure UX or growth work — use `ux-researcher/` and `conversion-optimizer/` methodologies
- One-shot tactical analysis (single ticket clarification) — overhead not justified
- Org explicitly anti-IIBA — pick Agile Extension or skip to product-discovery methodologies

## Content

| File | What's inside |
|------|---------------|
| `content/01-frameworks.xml` | Candidate framework catalog (8 frameworks), selection scoring criteria, known limitations of the README's descriptive tables |
| `content/02-agentic.xml` | Selector and audit prompt patterns, subagent roles, AI gotchas, mandatory human checkpoints |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-framework-select.sh` | Scaffold a ba-framework-decision.json for a feature with all scoring fields |
