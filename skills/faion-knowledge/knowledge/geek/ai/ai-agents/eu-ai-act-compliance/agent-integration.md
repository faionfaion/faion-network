# Agent Integration — EU AI Act Compliance

## When to use
- Deploying any AI system that operates in or serves users in the EU (regardless of where the provider is incorporated)
- Building chatbots, recommendation engines, or automated decision systems marketed in the EU
- Creating agent systems that touch biometrics, employment, credit, education, or critical infrastructure
- Conducting a GPAI (General-Purpose AI Model) integration where the model's training data or outputs are subject to copyright and transparency obligations
- Establishing a compliance audit pipeline before an August 2026 enforcement deadline

## When NOT to use
- Purely internal R&D tools with no user-facing deployment
- AI systems deployed exclusively outside EU jurisdictions with no EU data subjects
- Spam filters, games, or scientific research tools that fall in the "minimal risk" category and require no documentation beyond ordinary engineering practice
- Prototypes under active development not yet in production

## Where it fails / limitations
- EU AI Act risk classification is fact-specific — the same model can be high-risk in one context and limited-risk in another; automated classification tools are advisory only
- SHAP/LIME explainability is model-class specific; applying them to large transformer agents produces explanations that are technically valid but practically uninterpretable
- Conformity assessment documentation can be voluminous (hundreds of pages); generating it with an agent risks hallucinating regulatory requirements
- Member-state sandboxes and national competent authorities are not yet uniformly established (Q2 2026); compliance procedures vary by country
- Bias detection tools (Fairlearn, AI Fairness 360) measure proxy metrics; passing them does not guarantee actual fairness under the Act's definitions
- Penalties are enforced by national authorities who may interpret ambiguous provisions differently across EU member states

## Agentic workflow
A compliance subagent workflow runs in three sequential phases: (1) a classifier subagent reads the system description and produces a risk tier and applicable article list; (2) a documentation subagent generates model cards, data sheets, and a conformity assessment draft; (3) a reviewer subagent cross-checks the draft against the latest published EU AI Act text and flags gaps. Human legal review is mandatory before any produced document is submitted to a regulator.

### Recommended subagents
- `risk-classifier` — reads system description and outputs risk tier + applicable articles; uses Sonnet
- `doc-generator` — produces model card, data sheet, and conformity assessment draft from structured inputs; uses Sonnet
- `compliance-reviewer` — validates generated docs against Act text, flags missing sections; uses Opus
- `bias-checker` — runs Fairlearn/AI Fairness 360 on evaluation datasets and summarizes results; executes Python tools

### Prompt pattern
Risk classification:
```xml
<task>Classify this AI system under the EU AI Act risk framework.</task>
<system_description>{{system_description}}</system_description>
<deployment_context>{{context: country, domain, user_type}}</deployment_context>
<output_format>
{
  "risk_tier": "unacceptable|high|limited|minimal",
  "applicable_articles": ["list"],
  "rationale": "explanation",
  "requires_conformity_assessment": true|false
}
</output_format>
```

Document generation:
```xml
<task>Generate an EU AI Act model card for the following system.</task>
<risk_tier>{{tier}}</risk_tier>
<system_facts>{{structured_facts}}</system_facts>
<applicable_articles>{{articles}}</applicable_articles>
<instruction>Flag any fields where you lack sufficient information with [MISSING: reason].</instruction>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fairlearn` | Bias detection and mitigation for ML models | `pip install fairlearn` / fairlearn.org |
| `aif360` | AI Fairness 360 — bias metrics across protected attributes | `pip install aif360` / aif360.mybluemix.net |
| `shap` | SHAP explainability values for model decisions | `pip install shap` / shap.readthedocs.io |
| `lime` | Local interpretable model-agnostic explanations | `pip install lime` / github.com/marcotcr/lime |
| `presidio-analyzer` | PII detection for training data documentation | `pip install presidio-analyzer` / microsoft.github.io/presidio |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Credo AI | SaaS | Yes | AI governance platform; API for policy checks, model cards, audit trails |
| Holistic AI | SaaS | Yes | EU AI Act risk assessments and audit reports via API |
| DataRobot Governance | SaaS | Partial | Model monitoring, drift detection, compliance reporting |
| Arthur AI | SaaS | Yes | Real-time monitoring for bias, explainability, data drift |
| Weights & Biases | SaaS | Yes | Experiment tracking, model cards, audit logs — OSS-friendly |

## Templates & scripts
See `templates.md` for model card and conformity assessment document templates.

Automated bias report (≤30 lines):
```python
from fairlearn.metrics import MetricFrame, selection_rate
from sklearn.metrics import accuracy_score

def bias_report(y_true, y_pred, sensitive_features, output_path="bias_report.json"):
    mf = MetricFrame(
        metrics={"accuracy": accuracy_score, "selection_rate": selection_rate},
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )
    report = {
        "overall": mf.overall.to_dict(),
        "by_group": mf.by_group.to_dict(),
        "disparities": mf.difference().to_dict()
    }
    import json
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    return report
```

## Best practices
- Classify risk tier first — it determines the entire documentation burden; do not skip this step
- Store all compliance artifacts (model cards, bias reports, training data logs) in version-controlled storage with immutable history
- Automate bias checks on every model update; do not treat compliance as a one-time gate
- For chatbots and synthetic content, implement Article 50 disclosure banners before any user interaction begins
- Document data lineage for training sets, including copyright opt-out records (required for GPAI compliance from Aug 2025)
- Treat the generated documentation as a draft only; always have a human with legal competence review before regulatory submission
- Register high-risk systems in the EU AI Act database before deployment, not after

## AI-agent gotchas
- **Hallucinated regulatory requirements**: agents confidently generate compliance checklists that cite nonexistent articles. Always validate generated content against the official EU AI Act text (eur-lex.europa.eu).
- **Classification drift**: an agent system's risk tier can change as new features are added; build a re-classification trigger into the CI/CD pipeline.
- **Transparency disclosure**: if the compliance system itself is an AI agent, it is subject to the same transparency obligations it is documenting for others — disclose this in audit records.
- **Human-in-loop checkpoint**: no compliance document should be submitted to a regulator without explicit human legal review. The agent workflow must include a hard stop at this point.
- **Data subject rights**: if the agent processes personal data during compliance testing (e.g. running bias checks on real user data), GDPR data subject rights apply independently of the AI Act.

## References
- EU AI Act official text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
- EU AI Act compliance guide (2026): https://artificialintelligenceact.eu/
- Fairlearn: https://fairlearn.org/
- AI Fairness 360: https://aif360.mybluemix.net/
- Credo AI governance platform: https://www.credo.ai/
- Holistic AI risk management: https://www.holisticai.com/
