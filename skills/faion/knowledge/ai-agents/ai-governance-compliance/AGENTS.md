# AI Governance and Compliance

## Summary

**One-sentence:** Produces a governance pack for an AI system under EU AI Act / SOC2 / ISO 42001 — model card, bias audit report, explainability artefacts, human-oversight design, audit-log spec.

**One-paragraph:** Regulatory and enterprise-buyer pressure (EU AI Act, SOC 2, ISO 42001, MiCA) now require AI systems to ship with a documented governance pack. This methodology produces five named artefacts: a model card (provenance + intended use + limits), a bias audit report (demographic slices + statistical tests), explainability artefacts (SHAP/LIME or rule-based), a human-oversight design (when and how a human intervenes), and an audit-log spec (what is logged, retention, immutability). Output is one signed governance pack PMs and compliance officers can hand to auditors.

**Ефективно для:** Команд, які продають в Європу або в enterprise, і де на ревизії покупця питають «де ваш model card?»; pack за тиждень дає 5 артефактів — і відкриває контракти, які без них стоять у статусі «pending compliance review».

## Applies If (ALL must hold)

- AI system is or will be in production with external users.
- At least one of: EU market exposure, enterprise buyer with compliance gate, healthcare/finance/HR vertical, regulated industry.
- Named compliance owner exists.
- Bias audit data (demographic-tagged samples) is available or can be assembled.
- Model is not entirely third-party hosted with no introspection (otherwise governance pack is the provider's).

## Skip If (ANY kills it)

- Internal developer tooling with no external impact.
- Pure B2B passthrough where downstream customer holds the compliance burden.
- EU AI Act Annex III low-risk class: spam filters, public-content search, trivial recommenders.
- Prototype / pre-launch — implement before first paying customer, not before first demo.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Model identity | name + version + provider + training-data summary | ML team |
| Demographic-tagged sample set | jsonl with protected-attribute labels | QA / data |
| Explainability tooling | SHAP / LIME setup or rule trace | Eng |
| Human-oversight policy template | Markdown | Compliance |
| Audit log endpoint | URL + retention policy | Ops |
| Named compliance owner | handle / email | Legal / compliance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/eu-ai-act-compliance/AGENTS.md` | Sibling — risk classification feeds this pack. |
| `geek/ai/ai-agents/ai-feature-brief-extension-pack/AGENTS.md` | Hallucination policy anchors the human-oversight design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: model-card-required, bias-audit-statistical, explainability-typed, human-oversight-named, audit-log-immutable | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the governance pack manifest | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns | ~900 |
| `content/04-procedure.xml` | deep | 7-step procedure across the 5 artefacts | ~1300 |
| `content/05-examples.xml` | medium | Worked example: governance pack for a CV-screening AI | ~1100 |
| `content/06-decision-tree.xml` | essential | Risk-class → mandatory artefacts → ship/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_risk` | sonnet | Risk-class mapping requires regulatory judgment. |
| `draft_model_card` | sonnet | Structured artefact authoring. |
| `bias_audit_stats` | haiku | Mechanical statistical computation. |
| `explainability_draft` | sonnet | Pattern-match SHAP/LIME outputs to plain-English claims. |
| `legal_review` | opus | High-stakes cross-input synthesis with compliance vocabulary. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the governance pack manifest. |
| `templates/output.example.json` | Filled example. |
| `templates/model-card.md` | Markdown skeleton with EU AI Act + ISO 42001 fields. |
| `templates/bias-audit-report.md` | Markdown skeleton for statistical bias audit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the governance pack manifest. | After pack assembly, before auditor handoff. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[eu-ai-act-compliance]] — risk classification methodology.
- peer: [[ai-incident-postmortem-template]] — incidents feed the audit log.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) what is the EU AI Act risk class (Prohibited / High / Limited / Minimal)? (2) is there enterprise-buyer compliance gate? (3) is human oversight architecturally possible? Leaves point to "ship full pack", "ship abbreviated pack" (Limited / Minimal), or "escalate / refuse deployment" (Prohibited).
