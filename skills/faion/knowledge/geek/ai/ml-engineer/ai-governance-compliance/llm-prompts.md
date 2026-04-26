# LLM Prompts for AI Governance Tasks

Prompts for automating governance documentation and analysis.

## Model Card Generation

### Generate Model Card from Training Artifacts

```
You are an AI governance specialist. Generate a comprehensive model card based on the following training artifacts.

## Training Information
Model Name: {{model_name}}
Model Type: {{model_type}}
Framework: {{framework}}
Training Dataset: {{dataset_description}}
Training Date: {{training_date}}

## Performance Metrics
{{metrics_json}}

## Feature Information
{{feature_descriptions}}

## Instructions
Generate a model card following the Hugging Face model card format. Include:

1. **Model Details** - Name, version, type, framework, release date
2. **Intended Use** - Primary use cases, intended users, out-of-scope uses
3. **Training Data** - Dataset description, size, demographics if applicable
4. **Evaluation** - Metrics with context, subgroup performance if available
5. **Limitations** - Known limitations and failure modes
6. **Ethical Considerations** - Potential harms, mitigations, human oversight needs
7. **How to Use** - Basic usage instructions
8. **Citation** - How to cite if applicable

Be specific and avoid generic statements. Flag any missing information that should be documented.
```

### Generate Data Sheet

```
You are a data governance specialist. Generate a datasheet for the following dataset.

## Dataset Information
Name: {{dataset_name}}
Source: {{data_source}}
Collection Period: {{date_range}}
Size: {{sample_count}} samples
Features: {{feature_list}}

## Collection Method
{{collection_description}}

## Instructions
Generate a datasheet following the "Datasheets for Datasets" format (Gebru et al.). Include:

1. **Motivation** - Purpose, creators, funding
2. **Composition** - What instances represent, total count, splits, features, labels, missing data, sensitive data
3. **Collection Process** - How data was collected, who collected it, sampling strategy
4. **Preprocessing** - Cleaning, transformations, raw data availability
5. **Uses** - Intended uses, inappropriate uses, prior uses
6. **Distribution** - How accessed, license, restrictions
7. **Maintenance** - Who maintains, update frequency, error reporting

Be precise about limitations and potential biases in the data.
```

---

## Risk Assessment

### EU AI Act Risk Classification

```
You are an EU AI Act compliance specialist. Classify the following AI system according to the EU AI Act risk categories.

## System Description
Name: {{system_name}}
Purpose: {{purpose}}
Domain: {{domain}}
Users: {{user_types}}
Decision Impact: {{decision_impact}}

## Functionality
{{functionality_description}}

## Instructions
Analyze this system against EU AI Act criteria and provide:

1. **Risk Classification**: Unacceptable / High / Limited / Minimal

2. **Reasoning**: Explain why this classification applies, referencing specific EU AI Act articles

3. **If High-Risk**:
   - Which Annex III category it falls under
   - Required conformity assessment type
   - Key compliance requirements

4. **If Limited Risk**:
   - Transparency obligations that apply

5. **Recommendations**: What governance measures are needed for compliance

Be specific and cite EU AI Act articles where applicable.
```

### Comprehensive Risk Assessment

```
You are an AI risk management specialist. Conduct a risk assessment for the following AI system.

## System Information
Name: {{system_name}}
Description: {{description}}
Deployment Context: {{context}}
Users: {{users}}
Data Processed: {{data_types}}

## Current Controls
{{existing_controls}}

## Instructions
Identify and assess risks across these categories:

1. **Technical Risks**
   - Model performance degradation
   - Data quality issues
   - System failures
   - Security vulnerabilities

2. **Compliance Risks**
   - Regulatory non-compliance
   - Documentation gaps
   - Audit failures

3. **Ethical Risks**
   - Bias and discrimination
   - Privacy violations
   - Transparency issues
   - Unintended consequences

For each risk:
- Risk ID (TR-XXX, CR-XXX, ER-XXX)
- Description
- Likelihood (High/Medium/Low)
- Impact (High/Medium/Low)
- Risk Score
- Recommended mitigation

Prioritize risks by score and provide actionable mitigation strategies.
```

---

## Bias Analysis

### Fairness Metrics Interpretation

```
You are an AI fairness specialist. Interpret the following fairness metrics and provide recommendations.

## Model Information
Model: {{model_name}}
Task: {{task_type}}
Protected Attributes: {{protected_attributes}}

## Fairness Metrics
{{metrics_json}}

## Instructions
Analyze these fairness metrics and provide:

1. **Metric Interpretation**
   - What each metric means in context
   - Whether values indicate bias
   - Comparison to industry thresholds (4/5ths rule, etc.)

2. **Bias Assessment**
   - Overall fairness assessment
   - Most concerning disparities
   - Affected groups

3. **Root Cause Hypotheses**
   - Potential causes of observed bias
   - Training data issues
   - Feature engineering concerns

4. **Recommendations**
   - Immediate actions
   - Long-term improvements
   - Monitoring suggestions

Be specific about which disparities require attention and why.
```

### Bias Audit Report Generation

```
You are an AI ethics auditor. Generate a bias audit report based on the following analysis results.

## Audit Information
Model: {{model_name}}
Audit Period: {{period}}
Auditor: {{auditor}}

## Statistical Analysis
{{statistical_results}}

## Subgroup Performance
{{subgroup_metrics}}

## Instructions
Generate a formal bias audit report including:

1. **Executive Summary**
   - Key findings
   - Overall bias risk rating
   - Critical issues requiring immediate attention

2. **Methodology**
   - Fairness definitions used
   - Metrics calculated
   - Thresholds applied

3. **Findings by Protected Attribute**
   - Detailed analysis for each attribute
   - Statistical significance
   - Practical significance

4. **Compliance Assessment**
   - Four-fifths rule analysis
   - Equal opportunity assessment
   - Regulatory compliance status

5. **Recommendations**
   - Prioritized action items
   - Owners and timelines
   - Monitoring requirements

6. **Appendix**
   - Detailed metric tables
   - Methodology details

Format as a professional audit document suitable for regulatory submission.
```

---

## Explainability

### Generate Decision Explanation

```
You are an AI explainability specialist. Generate a human-readable explanation for the following model decision.

## Decision Context
Model: {{model_name}}
Prediction: {{prediction}}
Confidence: {{confidence}}

## Feature Values
{{feature_values}}

## SHAP Values
{{shap_values}}

## Instructions
Generate an explanation suitable for {{audience}} (technical/non-technical/regulatory):

1. **Plain Language Summary**
   - What the model predicted
   - Confidence level in context

2. **Key Factors**
   - Top 3-5 factors that influenced the decision
   - Direction of influence (positive/negative)
   - Relative importance

3. **Counterfactual**
   - What would need to change for a different outcome
   - Minimum changes required

4. **Confidence Context**
   - What the confidence score means
   - When to trust/question this prediction

5. **Limitations**
   - Factors the model cannot consider
   - Situations where this explanation may not apply

Adjust technical depth based on the specified audience.
```

---

## Compliance Documentation

### Generate Conformity Assessment

```
You are an EU AI Act compliance specialist. Generate a conformity assessment document for the following high-risk AI system.

## System Information
Name: {{system_name}}
Provider: {{provider}}
Category: {{annex_iii_category}}
Version: {{version}}

## System Description
{{description}}

## Existing Documentation
- Model Card: {{model_card_summary}}
- Risk Assessment: {{risk_assessment_summary}}
- Testing Results: {{testing_summary}}

## Instructions
Generate a conformity assessment document addressing EU AI Act requirements:

1. **System Identification**
   - Unique identifier
   - Version and configuration
   - Intended purpose

2. **Risk Management System** (Article 9)
   - Risk identification methodology
   - Evaluation and mitigation measures
   - Residual risk assessment

3. **Data Governance** (Article 10)
   - Training data description
   - Data quality measures
   - Bias examination results

4. **Technical Documentation** (Article 11)
   - Documentation completeness checklist
   - Gaps identified

5. **Record-Keeping** (Article 12)
   - Logging capabilities
   - Traceability measures

6. **Transparency** (Article 13)
   - User information provision
   - Disclosure mechanisms

7. **Human Oversight** (Article 14)
   - Oversight measures
   - Override capabilities

8. **Accuracy and Robustness** (Article 15)
   - Performance metrics
   - Robustness testing results

9. **Conformity Declaration**
   - Compliance statement
   - Responsible parties

Flag any gaps requiring remediation before deployment.
```

### Generate Audit Response

```
You are an AI governance specialist responding to a regulatory audit. Generate responses to the following audit questions.

## Audit Context
Auditor: {{auditor}}
Audit Type: {{audit_type}}
System: {{system_name}}

## Audit Questions
{{questions}}

## Available Documentation
{{documentation_list}}

## Instructions
For each audit question, provide:

1. **Direct Answer**
   - Clear, factual response
   - Reference specific documentation

2. **Evidence**
   - Document names and sections
   - Specific metrics or data points
   - Dates and version numbers

3. **Supporting Context**
   - Additional relevant information
   - Process descriptions
   - Governance measures

4. **Gaps Identified**
   - Any areas requiring follow-up
   - Remediation plans if applicable

Use precise language. Avoid speculation. If information is unavailable, state clearly what documentation would be needed.
```

---

## Monitoring and Alerting

### Generate Drift Analysis Report

```
You are an MLOps monitoring specialist. Analyze the following drift detection results and provide recommendations.

## Model Information
Model: {{model_name}}
Baseline Period: {{baseline_period}}
Current Period: {{current_period}}

## Drift Metrics
### Feature Drift
{{feature_drift_metrics}}

### Prediction Drift
{{prediction_drift_metrics}}

### Performance Drift
{{performance_metrics}}

## Instructions
Analyze drift patterns and provide:

1. **Drift Summary**
   - Overall drift severity (Low/Medium/High/Critical)
   - Most affected features/predictions
   - Trend direction

2. **Root Cause Analysis**
   - Likely causes of observed drift
   - External factors (seasonality, data source changes)
   - Model-related factors

3. **Impact Assessment**
   - Effect on model performance
   - Business impact estimation
   - Compliance implications

4. **Recommendations**
   - Immediate actions (if critical)
   - Investigation priorities
   - Retraining considerations
   - Monitoring adjustments

5. **Timeline**
   - When drift became significant
   - Projected trajectory if uncorrected

Include specific threshold comparisons and statistical significance.
```

### Generate Incident Summary

```
You are an AI incident response specialist. Generate an incident summary for the following AI system incident.

## Incident Information
Incident ID: {{incident_id}}
System: {{system_name}}
Detection Time: {{detection_time}}
Severity: {{severity}}

## Incident Details
{{incident_description}}

## Timeline
{{event_timeline}}

## Actions Taken
{{response_actions}}

## Instructions
Generate a structured incident summary including:

1. **Executive Summary**
   - One paragraph overview
   - Key impact metrics
   - Current status

2. **Incident Description**
   - What happened
   - How it was detected
   - Systems affected

3. **Impact Analysis**
   - Users/decisions affected
   - Business impact
   - Regulatory implications

4. **Root Cause**
   - Technical root cause
   - Contributing factors
   - Prevention gaps

5. **Response Effectiveness**
   - What worked well
   - What could improve
   - Response time analysis

6. **Remediation Status**
   - Immediate fixes
   - Long-term fixes
   - Prevention measures

7. **Lessons Learned**
   - Key takeaways
   - Process improvements
   - Documentation updates

Format for both technical and executive audiences.
```

---

## Governance Review

### Model Approval Assessment

```
You are an AI governance reviewer. Assess this model for production deployment approval.

## Model Information
Name: {{model_name}}
Version: {{version}}
Purpose: {{purpose}}
Requestor: {{requestor}}

## Documentation Provided
- Model Card: {{model_card_status}}
- Data Sheet: {{datasheet_status}}
- Risk Assessment: {{risk_assessment_status}}
- Test Results: {{test_results}}
- Fairness Analysis: {{fairness_status}}

## Performance Metrics
{{metrics}}

## Instructions
Conduct a governance review and provide:

1. **Documentation Completeness**
   - Checklist of required documents
   - Status of each (Complete/Partial/Missing)
   - Critical gaps

2. **Technical Assessment**
   - Performance adequacy
   - Robustness concerns
   - Scalability considerations

3. **Compliance Assessment**
   - Regulatory alignment
   - Policy compliance
   - Audit readiness

4. **Risk Assessment**
   - Key risks identified
   - Mitigation adequacy
   - Residual risk acceptance

5. **Fairness Assessment**
   - Bias testing completeness
   - Concerning disparities
   - Mitigation effectiveness

6. **Recommendation**
   - APPROVE / APPROVE WITH CONDITIONS / REJECT
   - Conditions if applicable
   - Required follow-up

Be specific about approval conditions and rejection reasons.
```
