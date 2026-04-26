# AI Governance Documentation Templates

Ready-to-use templates for AI governance documentation.

## Template 1: Model Card

```markdown
# Model Card: [Model Name]

## Model Details

| Field | Value |
|-------|-------|
| Name | [Model Name] |
| Version | [X.Y.Z] |
| Type | [Classification/Regression/Generation/etc.] |
| Framework | [PyTorch/TensorFlow/Scikit-learn/etc.] |
| Release Date | [YYYY-MM-DD] |
| Owner | [Team/Individual] |
| Contact | [Email/Slack] |

## Intended Use

### Primary Use Cases
- [Use case 1]
- [Use case 2]

### Intended Users
- [User type 1]
- [User type 2]

### Out-of-Scope Uses
- [Prohibited use 1]
- [Prohibited use 2]

## Training Data

### Dataset Description
| Attribute | Value |
|-----------|-------|
| Source | [Data source] |
| Size | [Number of samples] |
| Date Range | [Start - End] |
| Preprocessing | [Summary of preprocessing steps] |

### Demographic Distribution
| Group | Percentage |
|-------|------------|
| [Group 1] | [X%] |
| [Group 2] | [Y%] |

### Data Quality
- Missing values: [X%]
- Outlier handling: [Method]
- Validation: [Process]

## Evaluation Data

| Attribute | Value |
|-----------|-------|
| Source | [Data source] |
| Size | [Number of samples] |
| Overlap with Training | [None/X%] |

## Performance Metrics

### Overall Performance
| Metric | Value |
|--------|-------|
| Accuracy | [X%] |
| Precision | [X%] |
| Recall | [X%] |
| F1 Score | [X] |
| AUC-ROC | [X] |

### Performance by Subgroup
| Group | Accuracy | Precision | Recall |
|-------|----------|-----------|--------|
| [Group 1] | [X%] | [X%] | [X%] |
| [Group 2] | [X%] | [X%] | [X%] |

## Fairness Analysis

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Disparate Impact | [X] | >0.8 | [PASS/FAIL] |
| Equal Opportunity Difference | [X] | <0.1 | [PASS/FAIL] |
| Statistical Parity | [X] | <0.1 | [PASS/FAIL] |

## Limitations

### Known Limitations
- [Limitation 1]
- [Limitation 2]

### Performance Degradation Conditions
- [Condition 1]: [Expected impact]
- [Condition 2]: [Expected impact]

## Ethical Considerations

### Potential Harms
- [Harm 1]: [Mitigation]
- [Harm 2]: [Mitigation]

### Human Oversight Requirements
- [Requirement 1]
- [Requirement 2]

## Deployment

### Infrastructure Requirements
- [Requirement 1]
- [Requirement 2]

### Monitoring
- Metrics tracked: [List]
- Alert thresholds: [List]
- Review frequency: [Frequency]

## Maintenance

### Update Schedule
- Retraining frequency: [Frequency]
- Evaluation frequency: [Frequency]

### Version History
| Version | Date | Changes |
|---------|------|---------|
| [X.Y.Z] | [Date] | [Summary] |

## References

- [Documentation link]
- [Research paper]
```

---

## Template 2: Data Sheet

```markdown
# Data Sheet: [Dataset Name]

## Motivation

### Purpose
Why was this dataset created?
[Description]

### Creators
Who created the dataset and on behalf of which entity?
[Names/Organization]

### Funding
Who funded the creation of the dataset?
[Funding source]

## Composition

### Data Types
| Type | Description | Format |
|------|-------------|--------|
| [Type 1] | [Description] | [Format] |
| [Type 2] | [Description] | [Format] |

### Instance Count
- Total instances: [Number]
- Training split: [Number]
- Validation split: [Number]
- Test split: [Number]

### Features
| Feature | Type | Description | Missing % |
|---------|------|-------------|-----------|
| [Feature 1] | [Type] | [Description] | [X%] |
| [Feature 2] | [Type] | [Description] | [X%] |

### Labels
| Label | Description | Distribution |
|-------|-------------|--------------|
| [Label 1] | [Description] | [X%] |
| [Label 2] | [Description] | [X%] |

### Sensitive Data
Does the dataset contain data that might be considered sensitive?
- [ ] Personal identifiable information (PII)
- [ ] Protected health information (PHI)
- [ ] Financial information
- [ ] Biometric data
- [ ] Location data

If yes, what safeguards are in place?
[Description of safeguards]

## Collection Process

### Collection Method
How was the data collected?
[Description]

### Collection Timeframe
When was the data collected?
[Date range]

### Sampling Strategy
What sampling strategy was used?
[Description]

### Data Sources
| Source | Type | Consent |
|--------|------|---------|
| [Source 1] | [Type] | [Yes/No/N/A] |
| [Source 2] | [Type] | [Yes/No/N/A] |

### Collectors
Who collected the data?
[Description]

## Preprocessing

### Cleaning Steps
| Step | Description | Records Affected |
|------|-------------|------------------|
| [Step 1] | [Description] | [Number] |
| [Step 2] | [Description] | [Number] |

### Transformations
| Transformation | Features | Rationale |
|----------------|----------|-----------|
| [Transform 1] | [Features] | [Rationale] |
| [Transform 2] | [Features] | [Rationale] |

### Raw Data
Is the raw data available?
[Yes/No - Location if yes]

## Uses

### Intended Uses
- [Use 1]
- [Use 2]

### Not Suitable For
- [Use 1]
- [Use 2]

### Prior Uses
Has this dataset been used before?
[Description]

## Distribution

### Access
How can the dataset be accessed?
[Description]

### License
Under what license is the dataset distributed?
[License type]

### Restrictions
Are there any restrictions on access or use?
[Description]

## Maintenance

### Maintainer
Who maintains the dataset?
[Name/Team]

### Update Frequency
How often is the dataset updated?
[Frequency]

### Version History
| Version | Date | Changes |
|---------|------|---------|
| [X.Y] | [Date] | [Summary] |

### Error Reporting
How can errors be reported?
[Process]
```

---

## Template 3: Risk Assessment

```markdown
# AI Risk Assessment: [System Name]

## System Overview

| Field | Value |
|-------|-------|
| System Name | [Name] |
| Version | [X.Y.Z] |
| Assessment Date | [YYYY-MM-DD] |
| Assessor | [Name] |
| Next Review | [YYYY-MM-DD] |

## Risk Classification

### EU AI Act Classification
| Question | Answer |
|----------|--------|
| Is the system used for prohibited purposes? | [Yes/No] |
| Does it fall under high-risk categories? | [Yes/No] |
| If high-risk, which category? | [Category] |
| Final classification | [Unacceptable/High/Limited/Minimal] |

### Internal Risk Rating
| Dimension | Score (1-5) | Justification |
|-----------|-------------|---------------|
| Impact on individuals | [Score] | [Justification] |
| Scale of deployment | [Score] | [Justification] |
| Autonomy level | [Score] | [Justification] |
| Data sensitivity | [Score] | [Justification] |
| Reversibility of decisions | [Score] | [Justification] |
| **Total Risk Score** | [Total/25] | |

## Risk Identification

### Technical Risks

| Risk ID | Risk Description | Likelihood | Impact | Risk Level |
|---------|-----------------|------------|--------|------------|
| TR-001 | [Description] | [H/M/L] | [H/M/L] | [Score] |
| TR-002 | [Description] | [H/M/L] | [H/M/L] | [Score] |

### Compliance Risks

| Risk ID | Risk Description | Likelihood | Impact | Risk Level |
|---------|-----------------|------------|--------|------------|
| CR-001 | [Description] | [H/M/L] | [H/M/L] | [Score] |
| CR-002 | [Description] | [H/M/L] | [H/M/L] | [Score] |

### Ethical Risks

| Risk ID | Risk Description | Likelihood | Impact | Risk Level |
|---------|-----------------|------------|--------|------------|
| ER-001 | [Description] | [H/M/L] | [H/M/L] | [Score] |
| ER-002 | [Description] | [H/M/L] | [H/M/L] | [Score] |

## Risk Mitigation

| Risk ID | Mitigation Strategy | Owner | Status | Due Date |
|---------|---------------------|-------|--------|----------|
| TR-001 | [Strategy] | [Owner] | [Status] | [Date] |
| CR-001 | [Strategy] | [Owner] | [Status] | [Date] |
| ER-001 | [Strategy] | [Owner] | [Status] | [Date] |

## Residual Risk

### Post-Mitigation Assessment

| Risk ID | Original Level | Residual Level | Acceptable? |
|---------|----------------|----------------|-------------|
| TR-001 | [Score] | [Score] | [Yes/No] |
| CR-001 | [Score] | [Score] | [Yes/No] |
| ER-001 | [Score] | [Score] | [Yes/No] |

### Unmitigated Risks

| Risk ID | Reason | Acceptance Authority |
|---------|--------|---------------------|
| [ID] | [Reason for non-mitigation] | [Authority] |

## Monitoring Plan

| Risk ID | Monitoring Method | Frequency | Trigger for Review |
|---------|-------------------|-----------|-------------------|
| TR-001 | [Method] | [Frequency] | [Trigger] |
| CR-001 | [Method] | [Frequency] | [Trigger] |

## Approvals

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Technical Lead | [Name] | [Date] | _________ |
| Compliance Officer | [Name] | [Date] | _________ |
| Business Owner | [Name] | [Date] | _________ |
```

---

## Template 4: Incident Report

```markdown
# AI Incident Report

## Incident Summary

| Field | Value |
|-------|-------|
| Incident ID | [INC-XXXX] |
| Date/Time Detected | [YYYY-MM-DD HH:MM UTC] |
| Date/Time Resolved | [YYYY-MM-DD HH:MM UTC] |
| Severity | [Critical/High/Medium/Low] |
| Status | [Open/Investigating/Resolved/Closed] |

## Affected System

| Field | Value |
|-------|-------|
| Model/System Name | [Name] |
| Version | [X.Y.Z] |
| Environment | [Production/Staging/Dev] |
| Region/Instance | [Region] |

## Incident Description

### What Happened
[Detailed description of the incident]

### Impact
- Users affected: [Number/Percentage]
- Decisions impacted: [Number]
- Business impact: [Description]
- Regulatory implications: [Description]

### Root Cause
[Root cause analysis]

## Timeline

| Time (UTC) | Event |
|------------|-------|
| [HH:MM] | [Event description] |
| [HH:MM] | [Event description] |
| [HH:MM] | [Event description] |

## Response Actions

| Action | Owner | Status | Completion Time |
|--------|-------|--------|-----------------|
| [Action 1] | [Owner] | [Status] | [Time] |
| [Action 2] | [Owner] | [Status] | [Time] |
| [Action 3] | [Owner] | [Status] | [Time] |

## Remediation

### Immediate Actions Taken
- [Action 1]
- [Action 2]

### Long-Term Fixes
| Fix | Owner | Due Date | Status |
|-----|-------|----------|--------|
| [Fix 1] | [Owner] | [Date] | [Status] |
| [Fix 2] | [Owner] | [Date] | [Status] |

## Notifications

| Stakeholder | Notified | Method | Time |
|-------------|----------|--------|------|
| [Stakeholder 1] | [Yes/No] | [Email/Call] | [Time] |
| [Stakeholder 2] | [Yes/No] | [Email/Call] | [Time] |

### Regulatory Notification Required?
- [ ] Yes - Authority: [Name], Deadline: [Date]
- [ ] No

## Lessons Learned

### What Went Well
- [Item 1]
- [Item 2]

### What Could Be Improved
- [Item 1]
- [Item 2]

### Action Items for Prevention
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action 1] | [Owner] | [Date] |
| [Action 2] | [Owner] | [Date] |

## Approvals

| Role | Name | Date |
|------|------|------|
| Incident Manager | [Name] | [Date] |
| Technical Lead | [Name] | [Date] |
| Compliance (if required) | [Name] | [Date] |
```

---

## Template 5: Audit Log Schema

```sql
-- Audit log table schema for AI decisions

CREATE TABLE ai_decision_audit (
    -- Identifiers
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trace_id UUID NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    inference_started_at TIMESTAMP WITH TIME ZONE,
    inference_completed_at TIMESTAMP WITH TIME ZONE,

    -- Request context
    request_id VARCHAR(100),
    session_id VARCHAR(100),
    user_id VARCHAR(100),  -- Anonymized
    client_ip_hash VARCHAR(64),  -- Hashed for privacy

    -- Input/Output
    input_hash VARCHAR(64) NOT NULL,  -- Hash of input for dedup
    input_features JSONB,  -- Anonymized features
    output_prediction JSONB NOT NULL,
    confidence_score DECIMAL(5,4),

    -- Explainability
    feature_attributions JSONB,  -- SHAP values
    decision_factors JSONB,  -- Top contributing factors

    -- Governance
    risk_level VARCHAR(20),
    human_review_required BOOLEAN DEFAULT FALSE,
    human_reviewed BOOLEAN DEFAULT FALSE,
    human_reviewer_id VARCHAR(100),
    human_review_decision VARCHAR(50),
    human_review_timestamp TIMESTAMP WITH TIME ZONE,

    -- Compliance
    consent_verified BOOLEAN,
    data_retention_date DATE,
    regulatory_flags JSONB,

    -- System metadata
    environment VARCHAR(20) NOT NULL,
    region VARCHAR(50),
    instance_id VARCHAR(100),

    -- Indexes
    INDEX idx_model_version (model_id, model_version),
    INDEX idx_created_at (created_at),
    INDEX idx_trace_id (trace_id),
    INDEX idx_human_review (human_review_required, human_reviewed)
);

-- Partitioning by month for retention management
CREATE TABLE ai_decision_audit_2025_01 PARTITION OF ai_decision_audit
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

---

## Template 6: Governance Policy Document

```markdown
# AI Governance Policy: [Organization Name]

## Document Control

| Field | Value |
|-------|-------|
| Version | [X.Y] |
| Effective Date | [YYYY-MM-DD] |
| Review Date | [YYYY-MM-DD] |
| Owner | [Role/Department] |
| Approver | [Role/Name] |

## Purpose

[Description of policy purpose]

## Scope

This policy applies to:
- [Scope item 1]
- [Scope item 2]

This policy does NOT apply to:
- [Exclusion 1]
- [Exclusion 2]

## Definitions

| Term | Definition |
|------|------------|
| AI System | [Definition] |
| High-Risk AI | [Definition] |
| Model Owner | [Definition] |

## Governance Principles

### Principle 1: [Name]
[Description]

### Principle 2: [Name]
[Description]

## Roles and Responsibilities

### AI Governance Board
- [Responsibility 1]
- [Responsibility 2]

### Model Owners
- [Responsibility 1]
- [Responsibility 2]

### ML Engineers
- [Responsibility 1]
- [Responsibility 2]

## Compliance Requirements

### Regulatory Compliance
| Regulation | Requirement | Owner |
|------------|-------------|-------|
| EU AI Act | [Requirement] | [Owner] |
| GDPR | [Requirement] | [Owner] |

### Internal Standards
- [Standard 1]
- [Standard 2]

## Procedures

### Model Registration
[Link to procedure]

### Risk Assessment
[Link to procedure]

### Deployment Approval
[Link to procedure]

### Incident Response
[Link to procedure]

## Enforcement

### Non-Compliance
[Consequences of non-compliance]

### Escalation Path
[Escalation process]

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| [X.Y] | [Date] | [Author] | [Summary] |
```
