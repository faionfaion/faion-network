# Agent Integration — AI Governance and Compliance

## When to use
- Deploying AI in regulated industries: healthcare, HR, credit scoring, insurance (EU AI Act high-risk)
- Building multi-tenant SaaS where customer data is processed by AI models
- Any deployment in EU market where the AI Act applies (full enforcement 2026)
- Internal audit requirements demand traceable, immutable logs of every AI decision
- Organization has a CISO/legal team that needs documented AI risk posture

## When NOT to use
- Proof-of-concept or internal tool with no production traffic — governance overhead is disproportionate
- Minimal-risk AI (spam filter, recommendation engine with no legal/financial impact) — no formal governance required by EU AI Act
- Early-stage startup pre-revenue — lightweight logging suffices; formal governance adds process friction without regulatory necessity
- Team lacks ownership: governance without assigned DRI degrades into checkbox theater

## Where it fails / limitations
- Documentation without enforcement: governance frameworks fail when audit trail creation is decoupled from the deployment pipeline
- Bias metrics are domain-specific — generic bias tools (Fairlearn) produce misleading results if applied to the wrong fairness definition
- Explainability tools (SHAP, LIME) approximate explanations — they are not ground truth for model decisions
- ISO/IEC 42001 certification is expensive and slow (6-12 months); not appropriate for most solopreneur-scale projects
- EU AI Act risk classification is ambiguous at the edges — legal counsel required for borderline cases
- Governance platforms (DataRobot, Credo AI) are enterprise-priced; open-source stack requires significant integration effort

## Agentic workflow
A governance subagent runs as part of the MLOps pipeline, not as a one-off audit. On each model deployment event, it: validates that model documentation exists and is complete, checks the model registry for version and lineage metadata, runs a bias assessment script on a held-out eval set, logs the deployment event to an immutable audit trail (append-only store), and blocks the deployment if any gate fails. For EU AI Act compliance, it generates a conformity report template populated with model metadata. Human review is mandatory before any high-risk AI system goes live.

### Recommended subagents
- `faion-sdd-executor-agent` — drives compliance check sequence as SDD tasks with quality gates

### Prompt pattern
```
# Task: AI governance deployment gate
Given the model metadata and eval results below, assess compliance against
the EU AI Act risk tier and NIST AI RMF criteria. Output:
- risk_tier: unacceptable | high | limited | minimal
- gate_status: pass | fail
- blocking_issues: list of specific gaps (empty if pass)
- recommended_actions: list of remediation steps

Model metadata: {model_metadata}
Eval results: {eval_results}
Use case description: {use_case}
```

```python
# Minimal audit trail logger (append-only)
import json, datetime
from pathlib import Path

AUDIT_LOG = Path("audit/model_deployments.jsonl")

def log_deployment_event(
    model_id: str,
    action: str,  # "deploy" | "retire" | "eval_pass" | "eval_fail"
    metadata: dict,
    actor: str = "agent",
) -> None:
    AUDIT_LOG.parent.mkdir(exist_ok=True)
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "model_id": model_id,
        "action": action,
        "actor": actor,
        "metadata": metadata,
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fairlearn` | Bias assessment and mitigation | `pip install fairlearn` / fairlearn.org |
| `aif360` | IBM AI Fairness 360: comprehensive fairness metrics | `pip install aif360` / github.com/Trusted-AI/AIF360 |
| `shap` | SHAP model explainability | `pip install shap` / shap.readthedocs.io |
| `lime` | Local interpretable model-agnostic explanations | `pip install lime` / github.com/marcotcr/lime |
| `mlflow` | Model registry, lineage tracking, experiment logging | `pip install mlflow` / mlflow.org |
| `great-expectations` | Data quality validation (governance at data layer) | `pip install great-expectations` / greatexpectations.io |
| `evidently` | ML monitoring: drift, data quality, bias in production | `pip install evidently` / evidentlyai.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Weights & Biases | SaaS | Yes | Model registry + lineage; agent reads metrics via API |
| MLflow | OSS | Yes | Self-hosted; model registry; artifact storage |
| Credo AI | SaaS | Partial | EU AI Act alignment; policy workflows; REST API limited |
| DataRobot | SaaS | Partial | Enterprise MLOps + governance; API-accessible |
| Langfuse | OSS/SaaS | Yes | LLM observability; trace-level audit for LLM decisions |
| Braintrust | SaaS | Yes | Eval + audit trails for LLM-based systems |
| Evidently | OSS/SaaS | Yes | Production monitoring; drift + bias alerts via webhook |

## Templates & scripts
See `templates.md` for EU AI Act conformity report template and model card template.

Bias assessment gate (≤30 lines):

```python
from fairlearn.metrics import MetricFrame, demographic_parity_difference
from sklearn.metrics import accuracy_score
import pandas as pd

def bias_gate(
    y_true: list, y_pred: list, sensitive_features: list,
    max_dpd: float = 0.1
) -> dict:
    """Return gate result with demographic parity difference."""
    mf = MetricFrame(
        metrics=accuracy_score,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features,
    )
    dpd = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_features)
    passed = abs(dpd) <= max_dpd
    return {
        "gate_status": "pass" if passed else "fail",
        "demographic_parity_difference": round(float(dpd), 4),
        "threshold": max_dpd,
        "accuracy_by_group": mf.by_group.to_dict(),
    }
```

## Best practices
- Integrate governance as a deployment gate in CI/CD, not a post-hoc audit — prevention beats remediation
- Maintain a model inventory (spreadsheet or MLflow registry) with: model ID, use case, risk tier, data sources, DRI
- Use append-only audit logs — never update or delete past entries; immutability is a legal requirement for some jurisdictions
- Separate model documentation responsibility from model development — conflicts of interest produce rubber-stamp docs
- For EU AI Act high-risk systems: maintain a technical file (model card + training data description + eval results + risk assessment)
- Run bias assessments on your production data distribution, not a benchmark dataset
- Review governance metrics on a fixed cadence (monthly or per-deployment) not only on incidents

## AI-agent gotchas
- Governance agents must not self-approve their own deployments — the gate must be reviewed by a human for high-risk systems
- Bias metrics require a sensitive attribute column in the eval dataset; agents must verify this column exists before running assessment
- Audit log writes must be transactional — a crash mid-write creates a corrupt append; use atomic file writes
- Explainability outputs (SHAP values) are model-architecture-dependent; SHAP for transformers is approximate and slow
- EU AI Act "high-risk" classification triggers documentation requirements before deployment, not after — agent must block deployment if docs are incomplete
- Human-in-loop approval is legally mandated for EU AI Act high-risk system deployments — never auto-deploy without documented human sign-off

## References
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 (EU AI Act)
- https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf (NIST AI RMF)
- https://fairlearn.org/
- https://shap.readthedocs.io/
- https://mlflow.org/docs/latest/model-registry.html
- https://keyrus.com/us/en/insights/ai-in-2026-how-to-build-trustworthy-safe-and-governed-ai-systems-noram
