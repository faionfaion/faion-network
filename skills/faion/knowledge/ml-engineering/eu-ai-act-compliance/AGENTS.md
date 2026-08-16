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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/ai-governance-compliance` | Pre-classification governance — defines who owns the compliance artifact. |
| `pro/security/security` | Underlying security controls feed Article 15 robustness evidence. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules each with rationale + source — r1-r7 map the system to the Act, r8-r12 govern the pipeline that drafts the documentation (citation validation, human legal sign-off, immutable artefacts, re-classification trigger, GDPR parallel track). | ~1600 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check; carries reviewer_signoff and the model-card stub schema. | ~1000 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns with symptom/root-cause/fix — mis-classification, stripped citations, skipped GPAI docs, missing Article 50, hallucinated articles, classification drift, missing human gate, uninterpretable explanations, GDPR collision. | ~1500 |
| `content/04-procedure.xml` | essential | 8-step procedure: scope → classify → cite Articles → gap-analyse → generate evidence (model card, bias report, explainability) → document → legal review → register and monitor. | ~1100 |
| `content/05-examples.xml` | medium | Two worked examples: HR-screening tool → Annex III high-risk → Articles 9-15 obligations; credit-scoring agent through registration, including a caught hallucinated citation. | ~1300 |
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
| `templates/ai-system-inventory.md.j2` | Inventory row + per-system detailed record skeleton. |
| `templates/ai-system-inventory.md` | Inventory row + per-system detailed record skeleton. Generated from `templates/ai-system-inventory.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/conformity-self-assessment.md.j2` | Conformity self-assessment template (Article 43). |
| `templates/conformity-self-assessment.md` | Conformity self-assessment template (Article 43). Generated from `templates/conformity-self-assessment.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/model-card.md.j2` | GPAI model card (Article 53). |
| `templates/model-card.md` | GPAI model card (Article 53). Generated from `templates/model-card.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/prompt-bias-assessment.txt` | LLM prompt to draft Article 10 data-governance bias check. |
| `templates/prompt-risk-classification.txt` | LLM prompt to draft risk-tier classification. |
| `templates/technical-doc-article11.md.j2` | Article 11 technical documentation skeleton. |
| `templates/technical-doc-article11.md` | Article 11 technical documentation skeleton. Generated from `templates/technical-doc-article11.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eu-ai-act-compliance.py` | Validate that the compliance report matches the Article-citation schema. | Pre-merge of every compliance-draft PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-governance-compliance]] — sister methodology covering org-level model governance.
- [[llm-decision-framework]] — sits upstream; classifier output feeds the risk-budget node.
- [[mcp-security]] — Article 15 robustness inputs for MCP-mediated agent deployments.

## Decision tree

Risk-tier decision tree at `content/06-decision-tree.xml` decides which Articles apply BEFORE engineering invests in conformity work.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-bias-assessment.txt`

```text
-->

You are an AI fairness expert conducting bias assessment for EU AI Act Article 10 compliance.

System: {purpose}
Protected attributes in data: {attributes}
Decision type: {decision_type}
Evaluation results: {metrics}

Analyze:
1. Demographic parity — are outcomes equally distributed across groups?
2. Equal opportunity — do true positive rates differ?
3. Predictive equality — do false positive rates differ?
4. Intersectional effects — compounded impacts for multiple attributes?

Output JSON:
{
  "overall": "pass|fail|concerns",
  "findings": [
    {"metric": "...", "status": "pass|fail", "value": 0.0, "threshold": 0.0, "notes": "..."}
  ],
  "risks": "...",
  "recommendations": [],
  "monitoring_plan": "..."
}

Rules:
- Cite Article 10 for every data governance finding
- Flag disparities > 0.1 disparity score as high priority
- Distinguish between statistical disparity and causal bias
```

### `templates/prompt-risk-classification.txt`

```text
-->

You are an EU AI Act compliance expert. Classify the following AI system.

System description:
{system_description}

Steps:
1. Check Article 5 — does it match any prohibited practice?
2. Check Annex III — does the primary use case match any high-risk domain?
3. Check Article 50 — does it interact with humans or generate synthetic content?

Output JSON:
{
  "risk_tier": "prohibited|high|limited|minimal",
  "confidence": "low|medium|high",
  "prohibited_practices": [],
  "annex_iii_match": null,
  "article_50_applicable": false,
  "applicable_articles": [],
  "rationale": "...",
  "ambiguities_for_legal_review": []
}

Rules:
- Cite specific article numbers for every finding
- Never make a binding determination — flag ambiguities for legal review
- If systemic risk applies (GPAI > 10^25 FLOPs), note additional obligations
```
