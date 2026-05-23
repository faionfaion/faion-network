# EU AI Act Compliance

## Summary

**One-sentence:** Produces an Article-cited EU AI Act risk classification + compliance gap report flagging Article 5 prohibitions, Annex III high-risk obligations, and Article 50 transparency duties.

**One-paragraph:** Produces an Article-cited EU AI Act risk classification + compliance gap report. Fines up to EUR 35M or 7% of global turnover. Article 5 prohibitions absolute since Feb 2025; GPAI obligations live since Aug 2025; Annex III high-risk obligations and Commission enforcement powers active Aug 2026. Mis-classification (under or over) drives regulatory exposure or unnecessary engineering cost. Every recommendation MUST cite specific Articles + Annexes.

**Ефективно для:** Compliance / ML lead готує draft pre-launch — закриває петлю між класифікацією ризику й конкретними статтями.

## Applies If (ALL must hold)

- Building or deploying an AI system targeting EU users after August 2024.
- System touches biometrics, employment, credit scoring, education admissions, or critical infrastructure (Annex III).
- Deploying a GPAI model trained with >10^25 FLOPs (systemic-risk tier).
- Integrating third-party LLM APIs where provider compliance does not cover downstream deployer obligations.
- Conducting pre-launch compliance gap analysis or drafting Article 11 technical documentation.

## Skip If (ANY kills it)

- Products deployed exclusively outside the EU with zero EU users and no EU-based processing.
- Purely internal tools with no impact on individuals' rights (minimal-risk tier).
- R&D activities exempt under Article 2(6).
- Open-source GPAI models released without commercial intent (verify per Article 2(12)).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| AI system inventory | markdown / yaml | platform engineering |
| Intended-use statement | markdown | product team |
| Training data summary | markdown / csv | ML team |
| Deployment region map | yaml | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/ai-governance-compliance` | Pre-classification governance — defines who owns the compliance artifact. |
| `pro/security/security` | Underlying security controls feed Article 15 robustness evidence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: scope → classify → cite Articles → gap-analyse → document → review. | ~700 |
| `content/05-examples.xml` | medium | Worked example: HR-screening tool → Annex III high-risk → Articles 9-15 obligations. | ~800 |
| `content/06-decision-tree.xml` | essential | Risk-tier branching: prohibited / high-risk / GPAI / limited / minimal. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-risk-tier` | sonnet | Structured judgement against Article 5 + Annex III + GPAI thresholds. |
| `draft-article-citations` | sonnet | Per-Article requirement mapping; accurate retrieval not deep reasoning. |
| `legal-review-handoff` | opus | Ambiguous edge cases — Opus surfaces genuine grey zones for legal counsel. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-system-inventory.md` | Inventory row + per-system detailed record skeleton. |
| `templates/conformity-self-assessment.md` | Conformity self-assessment template (Article 43). |
| `templates/model-card.md` | GPAI model card (Article 53). |
| `templates/prompt-bias-assessment.txt` | LLM prompt to draft Article 10 data-governance bias check. |
| `templates/prompt-risk-classification.txt` | LLM prompt to draft risk-tier classification. |
| `templates/technical-doc-article11.md` | Article 11 technical documentation skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eu-ai-act-compliance.py` | Validate that the compliance report matches the Article-citation schema. | Pre-merge of every compliance-draft PR. |

## Related

- [[ai-governance-compliance]] — sister methodology covering org-level model governance.
- [[llm-decision-framework]] — sits upstream; classifier output feeds the risk-budget node.
- [[mcp-security]] — Article 15 robustness inputs for MCP-mediated agent deployments.

## Decision tree

Risk-tier decision tree at `content/06-decision-tree.xml` decides which Articles apply BEFORE engineering invests in conformity work.
