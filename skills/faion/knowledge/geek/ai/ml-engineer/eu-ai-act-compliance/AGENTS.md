# EU AI Act Compliance

## Summary

Framework for classifying AI systems under the EU AI Act risk tiers (prohibited / high / limited / minimal), generating required documentation (Article 11 technical file, model cards, conformity declarations), and implementing mandatory controls (risk management, bias testing, human oversight, audit logging). Applies from August 2024 with phased enforcement through 2027.

## Why

The EU AI Act imposes fines up to EUR 35M or 7% of global turnover for non-compliance. Risk classification determines which articles apply; incorrect classification — either under- or over-scoping — leads to either regulatory exposure or unnecessary engineering cost. Agents producing compliance drafts must cite specific articles and flag ambiguous cases for legal review.

## When To Use

- Building or deploying an AI system targeting EU users after August 2024
- Any system processing biometrics, employment decisions, credit scoring, education admissions, or critical infrastructure — all are Annex III high-risk
- Deploying a GPAI model (General Purpose AI) with >10^25 FLOPs training compute (systemic risk tier, Aug 2025 deadline)
- Integrating third-party LLM APIs where the provider's compliance does not cover downstream deployer obligations
- Conducting a pre-launch compliance gap analysis

## When NOT To Use

- Products deployed exclusively outside the EU with no EU users or EU-based processing
- Purely internal tools with no impact on individuals' rights or safety (minimal risk tier — no obligations)
- R&D activities exempt under Article 2(6) — lab testing does not require compliance
- Open-source models released without commercial intent may have reduced obligations (verify per Article 2(12))

## Content

| File | What's inside |
|------|---------------|
| `content/01-risk-classification.xml` | Risk tiers, Annex III categories, prohibited practices, penalty table |
| `content/02-compliance-checklist.xml` | Phase-by-phase checklist: GPAI (Aug 2025), high-risk (Aug 2026), deployer duties |
| `content/03-examples.xml` | Chatbot (limited), resume screener (high), deepfake labeling (limited) — code + antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-system-inventory.md` | Inventory table + detailed system record per system |
| `templates/technical-doc-article11.md` | Article 11 technical documentation skeleton |
| `templates/model-card.md` | EU AI Act-aligned model card with fairness metrics section |
| `templates/conformity-self-assessment.md` | Self-assessment checklist Articles 9-15 |
| `templates/prompt-risk-classification.txt` | LLM prompt for risk tier classification |
| `templates/prompt-bias-assessment.txt` | LLM prompt for bias analysis report |
