# Agent Integration — AI Governance and Compliance

## When to use
- Deploying AI systems in EU markets where the AI Act applies (effective August 2024, tiered enforcement through 2027)
- Building high-risk AI applications: recruitment, credit scoring, biometric ID, medical diagnostics, law enforcement tools
- Any product that makes consequential automated decisions affecting natural persons
- When organizational policies require documented model cards, bias audits, or explainability reports
- Preparing for enterprise sales where buyers require SOC 2 / ISO 42001 compliance evidence
- Audit trail requirements: financial services, healthcare, public sector AI deployments

## When NOT to use
- Internal developer tooling with no external user impact — overhead exceeds benefit
- Pure B2B APIs where the downstream customer handles their own compliance
- Low-risk AI (EU AI Act Annex III exclusions): spam filters, AI-powered search on public content, simple recommendation engines with no legal/financial effect
- Prototype / research phase — implement governance before production launch, not before first demo

## Where it fails / limitations
- SHAP/LIME explainability degrades for LLM-based systems — feature attribution methods designed for tabular ML do not apply to transformer architectures
- Bias detection tools (Fairlearn, AI Fairness 360) require labeled demographic data that is often unavailable or illegal to collect in EU jurisdictions (GDPR conflict)
- Model cards document a model at a point in time; they go stale after fine-tuning or prompt updates — versioning is manual unless automated in CI
- EU AI Act "human oversight" requirement is vague — "meaningful oversight" is not defined technically, leaving compliance scope to interpretation
- Automated bias monitoring in production requires ground-truth labels to measure outcome disparity; these are rarely available in real-time
- AI Act conformity assessments for high-risk systems require a Notified Body review — no automated tooling replaces this for Category 3 systems

## Agentic workflow
Use a governance-checker subagent as a gate in the deployment pipeline: it reads model card templates, runs bias checks against a held-out validation set, generates an explainability report using SHAP on a sample, and outputs a structured compliance checklist with pass/fail per criterion. A separate audit-logger subagent wraps production inference calls, recording input hashes, model version, decision output, and confidence scores to an append-only audit log. Human review is triggered when the audit log shows anomalies (decision reversal rate > threshold, protected-attribute correlation spike).

### Recommended subagents
- `compliance-checker` — runs pre-deployment checklist: model card completeness, bias metrics, documentation audit
- `audit-logger` — wraps every inference call, records structured log entry (immutable, timestamped)
- `explainability-reporter` — generates SHAP/LIME report for a sampled batch, flags top feature contributions
- `drift-monitor` — compares production input distribution against training distribution weekly; alerts on divergence

### Prompt pattern
```
You are a compliance audit agent. Review the following AI system configuration and produce a structured compliance report.

System info:
- Model: {model_name} v{version}
- Use case: {use_case}
- Affected population: {population}
- EU AI Act risk category: {risk_category}

Check each item and return JSON:
{
  "model_card_complete": bool,
  "bias_audit_done": bool,
  "human_oversight_mechanism": str | null,
  "data_governance_documented": bool,
  "gaps": [str]
}
```

```python
# Minimal audit log entry structure
import hashlib, time, json

def log_inference(model_id: str, input_data: dict, output: dict) -> dict:
    entry = {
        "ts": time.time(),
        "model_id": model_id,
        "input_hash": hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest(),
        "output": output,
        "schema_version": "1.0",
    }
    append_to_audit_log(entry)  # write-once store
    return entry
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fairlearn` | Bias mitigation and fairness metrics | `pip install fairlearn` / https://fairlearn.org/ |
| `aif360` | AI Fairness 360: bias detection, mitigation algorithms | `pip install aif360` / https://aif360.readthedocs.io/ |
| `shap` | Model explainability (SHAP values) | `pip install shap` / https://shap.readthedocs.io/ |
| `lime` | Local interpretable model explanations | `pip install lime` / https://github.com/marcotcr/lime |
| `evidently` | Data/model drift monitoring, bias reports | `pip install evidently` / https://www.evidentlyai.com/ |
| `captum` | PyTorch attribution methods (Integrated Gradients) | `pip install captum` / https://captum.ai/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hugging Face Model Cards | SaaS/OSS | Yes | Standard model card format; API for programmatic card creation |
| Evidently Cloud | SaaS | Yes | Automated drift + bias monitoring; webhook alerts for agent triggers |
| Credo AI | SaaS | Partial | Governance platform; API for policy checks; enterprise-focused |
| Weights & Biases | SaaS | Yes | Track model versions, bias metrics per experiment; good audit trail |
| MLflow | OSS | Yes | Model registry with metadata; tag compliance status per model version |
| AWS Audit Manager | SaaS | Partial | Evidence collection for cloud-deployed models; integrates with CloudTrail |

## Templates & scripts
See `templates.md` for model card and bias report templates.

Minimal Fairlearn bias check:
```python
from fairlearn.metrics import MetricFrame, demographic_parity_difference
from sklearn.metrics import accuracy_score

def run_bias_check(y_true, y_pred, sensitive_features) -> dict:
    mf = MetricFrame(
        metrics={"accuracy": accuracy_score},
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features,
    )
    dpd = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_features)
    return {
        "accuracy_by_group": mf.by_group.to_dict(),
        "demographic_parity_difference": float(dpd),
        "pass": abs(dpd) < 0.1,  # EU AI Act threshold: no official number, 0.1 is industry convention
    }
```

## Best practices
- Version every model card as code — store in the same repo as the model, require PR review for changes
- Run bias checks on stratified validation sets, not production data, to avoid GDPR issues with real user data
- Implement data lineage from raw source to training set — required for EU AI Act Article 10 data governance documentation
- Separate audit logs from application logs — use append-only storage (S3 + Object Lock, Worm drives) to prevent tampering
- Define "human oversight" concretely in your system design: a dashboard showing AI decisions counts only if humans act on it within a defined SLA
- For EU high-risk systems: document the Fundamental Rights Impact Assessment (FRIA) before deployment, not after

## AI-agent gotchas
- Agents generating compliance reports using LLMs can hallucinate passing scores — always validate generated reports against ground-truth metrics computed from actual data
- SHAP computation on LLM outputs is not meaningful for black-box APIs (GPT-4, Claude) — use behavioral testing (perturbation analysis) instead
- Human-in-the-loop checkpoint: any agent that auto-approves a model for production based on compliance metrics must have a human sign-off step — automated green lights are insufficient for high-risk AI Act categories
- Drift alerts from monitoring agents should not trigger automatic model rollback without human review — automated rollback can itself introduce compliance violations if the prior version had known issues

## References
- EU AI Act text: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
- Fairlearn documentation: https://fairlearn.org/v0.10/user_guide/
- Hugging Face model cards: https://huggingface.co/docs/hub/model-cards
- AI Fairness 360: https://aif360.readthedocs.io/en/stable/
- ISO/IEC 42001 (AI management systems): https://www.iso.org/standard/81230.html
- NIST AI RMF: https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf
