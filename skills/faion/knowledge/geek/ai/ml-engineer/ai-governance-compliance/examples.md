# AI Governance Implementation Examples

Real-world patterns and case studies for AI governance implementation.

## Example 1: Credit Scoring Model Governance

### Context

Financial institution deploying ML model for credit risk assessment.

**Risk Level:** High (EU AI Act), regulated industry

### Governance Implementation

```yaml
Model Registration:
  id: credit-score-v2.3.1
  risk_level: high
  business_owner: Risk Management
  technical_owner: ML Platform Team
  regulatory_classification: EU AI Act Article 6(2)

Documentation:
  model_card: docs/model-cards/credit-score-v2.3.1.md
  data_sheet: docs/datasheets/credit-features-2024.md
  risk_assessment: docs/risk/credit-model-risk-v2.md
  conformity_assessment: docs/compliance/eu-ai-act-credit.md
```

### Bias Monitoring Setup

```python
from fairlearn.metrics import MetricFrame
from sklearn.metrics import accuracy_score, selection_rate

# Define protected attributes
protected_features = ['gender', 'age_group', 'ethnicity']

# Calculate fairness metrics
metric_frame = MetricFrame(
    metrics={
        'accuracy': accuracy_score,
        'selection_rate': selection_rate,
    },
    y_true=y_test,
    y_pred=predictions,
    sensitive_features=test_data[protected_features]
)

# Check disparate impact ratio
for feature in protected_features:
    rates = metric_frame.by_group['selection_rate']
    min_rate = rates.min()
    max_rate = rates.max()
    disparate_impact = min_rate / max_rate if max_rate > 0 else 0

    if disparate_impact < 0.8:
        alert_compliance_team(
            model_id='credit-score-v2.3.1',
            feature=feature,
            disparate_impact=disparate_impact
        )
```

### Audit Trail Configuration

```python
# Langfuse integration for decision logging
from langfuse import Langfuse

langfuse = Langfuse()

def score_application(application_data: dict) -> dict:
    trace = langfuse.trace(
        name="credit-scoring",
        metadata={
            "model_version": "v2.3.1",
            "application_id": application_data['id'],
            "timestamp": datetime.utcnow().isoformat()
        }
    )

    # Record input features (anonymized)
    trace.span(
        name="input-features",
        input=anonymize_pii(application_data)
    )

    # Model inference
    score = model.predict(application_data)

    # Record output with explanation
    trace.span(
        name="model-output",
        output={
            "score": score,
            "decision": "approved" if score > threshold else "denied",
            "shap_values": get_shap_explanation(application_data),
            "top_factors": get_top_factors(application_data)
        }
    )

    return {"score": score, "trace_id": trace.id}
```

### Human Review Queue

```python
# Escalation rules for human review
ESCALATION_RULES = {
    "borderline_score": lambda s: 0.45 < s < 0.55,
    "high_amount": lambda app: app['loan_amount'] > 100000,
    "first_time_applicant": lambda app: app['credit_history_months'] < 6,
    "override_request": lambda app: app.get('override_requested', False)
}

def needs_human_review(application: dict, score: float) -> bool:
    for rule_name, rule_fn in ESCALATION_RULES.items():
        if rule_name == "borderline_score":
            if rule_fn(score):
                return True
        else:
            if rule_fn(application):
                return True
    return False
```

---

## Example 2: Healthcare Diagnostic AI

### Context

Medical imaging AI for radiology assistance (lung nodule detection).

**Risk Level:** High (medical device), FDA/CE-marked

### Model Card Structure

```markdown
# Model Card: Lung Nodule Detection v3.1

## Model Details
- **Name:** LungScan-AI
- **Version:** 3.1.0
- **Release Date:** 2025-09-15
- **Type:** Convolutional Neural Network (3D U-Net variant)
- **Modality:** CT scans

## Intended Use
- **Primary:** Assist radiologists in detecting lung nodules
- **Users:** Licensed radiologists, trained technicians
- **Environment:** Hospital PACS integration
- **NOT for:** Primary diagnosis without radiologist review

## Training Data
- **Source:** 5 academic medical centers (de-identified)
- **Volume:** 50,000 CT scans, 180,000 annotated nodules
- **Demographics:** Age 35-85, 52% male, multi-ethnic
- **Annotation:** Board-certified radiologists (3x consensus)

## Performance Metrics
| Metric | Overall | Nodules <6mm | Nodules 6-8mm | Nodules >8mm |
|--------|---------|--------------|---------------|--------------|
| Sensitivity | 94.2% | 88.1% | 96.3% | 98.7% |
| Specificity | 91.8% | 89.2% | 93.1% | 95.4% |
| AUC | 0.967 | 0.932 | 0.971 | 0.989 |

## Limitations
- Performance degrades on motion-artifact scans
- Not validated for pediatric populations
- Requires specific CT protocols (see technical docs)
- May miss ground-glass nodules in certain orientations

## Ethical Considerations
- Human radiologist must verify all findings
- Not for use as sole diagnostic criterion
- Regular bias monitoring across demographics
```

### Continuous Monitoring Dashboard

```python
# Prometheus metrics for model monitoring
from prometheus_client import Counter, Histogram, Gauge

# Decision metrics
predictions_total = Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_version', 'prediction_class']
)

inference_latency = Histogram(
    'model_inference_seconds',
    'Inference latency',
    ['model_version']
)

# Drift metrics
data_drift_score = Gauge(
    'model_data_drift',
    'Data drift score (KL divergence)',
    ['model_version', 'feature']
)

# Fairness metrics
subgroup_accuracy = Gauge(
    'model_subgroup_accuracy',
    'Accuracy by demographic group',
    ['model_version', 'demographic', 'group']
)

# Alert thresholds
DRIFT_THRESHOLD = 0.15
ACCURACY_DROP_THRESHOLD = 0.05
```

---

## Example 3: HR Resume Screening

### Context

AI-assisted resume screening for initial candidate filtering.

**Risk Level:** High (employment decisions), anti-discrimination laws

### Bias Prevention Architecture

```python
class FairResumeScreener:
    def __init__(self, model, protected_attributes):
        self.model = model
        self.protected_attributes = protected_attributes
        self.calibrator = None

    def preprocess(self, resume_text: str) -> dict:
        """Remove potentially biasing information."""
        # Redact names (correlated with demographics)
        text = self.redact_names(resume_text)

        # Remove graduation years (age proxy)
        text = self.normalize_dates(text)

        # Standardize institution names
        text = self.normalize_institutions(text)

        return self.extract_features(text)

    def predict_with_fairness(self, features: dict) -> dict:
        """Score with post-processing fairness correction."""
        raw_score = self.model.predict(features)

        # Apply calibrated threshold per group if needed
        if self.calibrator:
            adjusted_score = self.calibrator.adjust(
                raw_score,
                features.get('inferred_group')
            )
        else:
            adjusted_score = raw_score

        return {
            'raw_score': raw_score,
            'adjusted_score': adjusted_score,
            'fairness_adjustment': raw_score - adjusted_score
        }

    def audit_batch(self, predictions: list, actuals: list,
                    demographics: list) -> dict:
        """Run fairness audit on batch of decisions."""
        from aif360.metrics import BinaryLabelDatasetMetric

        metrics = {}
        for attr in self.protected_attributes:
            dataset = self.create_aif360_dataset(
                predictions, actuals, demographics, attr
            )
            metric = BinaryLabelDatasetMetric(
                dataset,
                privileged_groups=[{attr: 1}],
                unprivileged_groups=[{attr: 0}]
            )
            metrics[attr] = {
                'statistical_parity': metric.statistical_parity_difference(),
                'disparate_impact': metric.disparate_impact(),
                'equal_opportunity': metric.equal_opportunity_difference()
            }
        return metrics
```

### Adverse Impact Analysis Report

```markdown
# Adverse Impact Analysis - Resume Screening

## Period: Q4 2025

### Selection Rates by Group

| Group | Applications | Selected | Rate | vs. Baseline |
|-------|--------------|----------|------|--------------|
| Overall | 10,000 | 2,500 | 25.0% | - |
| Male | 5,500 | 1,400 | 25.5% | +2% |
| Female | 4,500 | 1,100 | 24.4% | -2% |
| Age 20-35 | 6,000 | 1,550 | 25.8% | +3% |
| Age 35-50 | 3,000 | 750 | 25.0% | 0% |
| Age 50+ | 1,000 | 200 | 20.0% | -20% |

### Four-Fifths Rule Analysis

| Comparison | Impact Ratio | Status |
|------------|--------------|--------|
| Female/Male | 0.96 | PASS (>0.8) |
| Age 50+/Age 20-35 | 0.78 | REVIEW (borderline) |

### Remediation Actions
1. Review feature weights for experience years
2. Audit training data for age-related patterns
3. Implement age-blind scoring pilot
```

---

## Example 4: Customer Service Chatbot

### Context

LLM-powered chatbot handling customer inquiries.

**Risk Level:** Limited (transparency required)

### Transparency Implementation

```python
class GovernedChatbot:
    def __init__(self, llm_client, guardrails):
        self.llm = llm_client
        self.guardrails = guardrails

    def respond(self, user_message: str, context: dict) -> dict:
        # Transparency disclosure
        if context.get('first_message', True):
            disclosure = (
                "I'm an AI assistant. I can help with general questions "
                "but for complex issues, I can connect you with a human agent."
            )
        else:
            disclosure = None

        # Generate response with guardrails
        response = self.guardrails.invoke(
            llm=self.llm,
            messages=[{"role": "user", "content": user_message}],
            config={
                "prohibited_topics": ["medical_advice", "legal_advice"],
                "pii_handling": "mask",
                "escalation_triggers": ["speak to human", "complaint", "lawsuit"]
            }
        )

        # Log for audit
        self.audit_log.record(
            session_id=context['session_id'],
            input=user_message,
            output=response['content'],
            guardrails_triggered=response.get('triggered_guardrails', []),
            escalated=response.get('escalated', False)
        )

        return {
            "disclosure": disclosure,
            "response": response['content'],
            "escalated": response.get('escalated', False)
        }
```

### Content Policy Enforcement

```yaml
# Guardrails configuration
policies:
  prohibited_content:
    - discriminatory_language
    - harmful_advice
    - competitor_recommendations
    - unauthorized_commitments

  escalation_triggers:
    keywords:
      - "speak to manager"
      - "legal action"
      - "file complaint"
      - "unsubscribe"
    sentiment_threshold: -0.7

  pii_protection:
    detect_and_mask:
      - credit_card
      - ssn
      - email
      - phone
    action: mask_in_logs

  quality_thresholds:
    min_confidence: 0.7
    max_response_length: 500
    required_source_citation: false
```

---

## Example 5: Model Retirement Process

### Context

Decommissioning legacy fraud detection model.

### Retirement Checklist

```markdown
# Model Retirement: Fraud-Detect-v1.8

## Pre-Retirement

- [x] Replacement model validated (Fraud-Detect-v2.0)
- [x] Performance comparison documented
- [x] Stakeholder sign-off obtained
- [x] Regulatory notification (if required)

## Data Retention

- [x] Training data archived (7-year retention)
- [x] Model artifacts preserved
- [x] Decision logs exported
- [x] Audit trail closed out

## Transition

- [x] Traffic routing updated
- [x] Monitoring disabled
- [x] Alerts decommissioned
- [x] API endpoints deprecated (30-day notice)

## Documentation

- [x] Retirement date: 2025-12-01
- [x] Reason: Replaced by improved model
- [x] Final performance metrics captured
- [x] Lessons learned documented

## Post-Retirement

- [ ] 30-day observation period
- [ ] Archive model artifacts to cold storage
- [ ] Update model inventory
- [ ] Close governance record
```

### Retirement Automation

```python
def retire_model(model_id: str, replacement_id: str):
    """Automated model retirement workflow."""

    # Validate replacement is ready
    assert model_registry.get_status(replacement_id) == "production"

    # Archive model artifacts
    archive_path = f"s3://models-archive/{model_id}/"
    model_registry.archive(model_id, archive_path)

    # Export audit logs
    audit_logs = audit_service.export(
        model_id=model_id,
        format="parquet",
        destination=f"s3://audit-archive/{model_id}/"
    )

    # Update governance record
    governance_db.update(
        model_id=model_id,
        status="retired",
        retirement_date=datetime.utcnow(),
        replacement_id=replacement_id,
        archive_location=archive_path,
        audit_archive=audit_logs['location']
    )

    # Notify stakeholders
    notify_stakeholders(
        event="model_retirement",
        model_id=model_id,
        replacement_id=replacement_id
    )

    # Schedule deletion (after retention period)
    scheduler.schedule(
        task="delete_model_artifacts",
        model_id=model_id,
        execute_at=datetime.utcnow() + timedelta(days=2555)  # 7 years
    )
```
