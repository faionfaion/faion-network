# EU AI Act Documentation Templates

Ready-to-use templates for compliance documentation.

## Template 1: AI System Inventory

```markdown
# AI System Inventory

| ID | System Name | Description | Risk Level | Provider/Deployer | Status |
|----|-------------|-------------|------------|-------------------|--------|
| AI-001 | Customer Chatbot | Support automation | Limited | Deployer | Active |
| AI-002 | Resume Screener | Candidate filtering | High | Provider | Planning |
| AI-003 | Fraud Detection | Transaction monitoring | High | Deployer | Active |

## Detailed System Records

### AI-001: Customer Chatbot

| Field | Value |
|-------|-------|
| **System ID** | AI-001 |
| **Name** | Customer Service Chatbot |
| **Description** | AI-powered customer support assistant |
| **Risk Classification** | Limited (Article 50) |
| **Role** | Deployer |
| **Provider** | [Vendor Name] |
| **Deployment Date** | YYYY-MM-DD |
| **Business Owner** | [Name] |
| **Technical Owner** | [Name] |
| **Data Categories** | Customer queries, conversation logs |
| **Geographic Scope** | EU |
| **Users Affected** | ~50,000/month |
| **Compliance Status** | In Progress |
| **Last Review Date** | YYYY-MM-DD |
| **Next Review Date** | YYYY-MM-DD |

**Transparency Measures:**
- [ ] AI disclosure message implemented
- [ ] Human escalation available
- [ ] User consent mechanism

**Notes:**
[Additional compliance notes]
```

---

## Template 2: Risk Classification Assessment

```markdown
# Risk Classification Assessment

**System:** [System Name]
**Date:** YYYY-MM-DD
**Assessor:** [Name]

## 1. Initial Screening

### Prohibited Practices Check (Article 5)

| Practice | Applicable? | Evidence |
|----------|-------------|----------|
| Social scoring | No | System does not score based on social behavior |
| Exploitation of vulnerabilities | No | Not targeting vulnerable groups |
| Real-time biometric identification | No | No biometric processing |
| Emotion recognition in workplace | No | No emotion detection |
| Biometric categorization | No | No categorization by protected attributes |

**Result:** [ ] Contains prohibited practice (STOP) [x] Proceed to risk assessment

### High-Risk Check (Annex III)

| Domain | Applicable? | Justification |
|--------|-------------|---------------|
| Biometrics | [ ] Yes [x] No | |
| Critical infrastructure | [ ] Yes [x] No | |
| Education | [ ] Yes [x] No | |
| Employment | [x] Yes [ ] No | Used in hiring process |
| Essential services | [ ] Yes [x] No | |
| Law enforcement | [ ] Yes [x] No | |
| Migration/border | [ ] Yes [x] No | |
| Justice | [ ] Yes [x] No | |

**Result:** [x] High-risk [ ] Not high-risk

### Limited Risk Check (Article 50)

| Characteristic | Applicable? |
|---------------|-------------|
| Interacts directly with humans | [x] Yes [ ] No |
| Generates synthetic content | [ ] Yes [x] No |
| Emotion recognition | [ ] Yes [x] No |
| Biometric categorization | [ ] Yes [x] No |

## 2. Final Classification

**Risk Level:** HIGH

**Applicable Articles:** 9, 10, 11, 12, 13, 14, 15, 17, 43

**Compliance Deadline:** August 2026

## 3. Required Actions

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Implement risk management system | [Name] | YYYY-MM-DD | Not Started |
| Create technical documentation | [Name] | YYYY-MM-DD | Not Started |
| Establish bias testing | [Name] | YYYY-MM-DD | Not Started |
| Design human oversight | [Name] | YYYY-MM-DD | Not Started |
| Conduct conformity assessment | [Name] | YYYY-MM-DD | Not Started |

## 4. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Assessor | | | |
| Technical Lead | | | |
| Legal/Compliance | | | |
| Business Owner | | | |
```

---

## Template 3: Technical Documentation (Article 11)

```markdown
# Technical Documentation
## [System Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Classification:** HIGH-RISK AI SYSTEM

---

## 1. General Description

### 1.1 System Identification

| Field | Value |
|-------|-------|
| System Name | |
| Version | |
| Provider | |
| Intended Purpose | |
| Geographic Scope | |

### 1.2 Intended Purpose

[Detailed description of what the system is designed to do]

### 1.3 Intended Users

[Description of who will use the system and how]

### 1.4 Prohibited Uses

[Explicit list of uses the system is NOT designed for]

---

## 2. System Architecture

### 2.1 High-Level Architecture

[Architecture diagram or description]

### 2.2 Components

| Component | Description | Technology |
|-----------|-------------|------------|
| | | |

### 2.3 External Dependencies

| Dependency | Purpose | Provider |
|------------|---------|----------|
| | | |

---

## 3. Development Process

### 3.1 Design Methodology

[Description of design and development approach]

### 3.2 Training Data

| Aspect | Description |
|--------|-------------|
| Data sources | |
| Data volume | |
| Time period | |
| Data quality measures | |
| Bias mitigation | |

### 3.3 Model Architecture

| Parameter | Value |
|-----------|-------|
| Model type | |
| Parameters | |
| Training compute | |
| Training duration | |

### 3.4 Validation and Testing

| Test Type | Description | Results |
|-----------|-------------|---------|
| Unit tests | | |
| Integration tests | | |
| Bias testing | | |
| Robustness testing | | |
| User acceptance | | |

---

## 4. Performance Metrics

### 4.1 Accuracy Metrics

| Metric | Value | Threshold |
|--------|-------|-----------|
| Accuracy | | |
| Precision | | |
| Recall | | |
| F1 Score | | |

### 4.2 Fairness Metrics

| Metric | Value | Threshold |
|--------|-------|-----------|
| Demographic parity | | |
| Equal opportunity | | |
| Predictive equality | | |

### 4.3 Performance Boundaries

[Description of conditions where performance may degrade]

---

## 5. Risk Management

### 5.1 Identified Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

### 5.2 Residual Risks

[Description of risks that remain after mitigation]

### 5.3 Monitoring Plan

[How risks will be monitored in production]

---

## 6. Human Oversight

### 6.1 Oversight Mechanisms

[Description of human oversight capabilities]

### 6.2 Intervention Procedures

[How humans can intervene or override]

### 6.3 Training Requirements

[Training required for human overseers]

---

## 7. Logging and Traceability

### 7.1 Events Logged

| Event | Data Captured | Retention |
|-------|---------------|-----------|
| | | |

### 7.2 Audit Trail

[How audit trail is maintained]

---

## 8. Cybersecurity

### 8.1 Security Measures

| Measure | Description |
|---------|-------------|
| Data encryption | |
| Access control | |
| Adversarial robustness | |
| Secure deployment | |

### 8.2 Vulnerability Management

[Process for identifying and addressing vulnerabilities]

---

## 9. Changes and Updates

### 9.1 Change Log

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| | | | |

### 9.2 Update Procedures

[Process for updating the system]

---

## 10. Appendices

### A. Test Reports
### B. Training Data Documentation
### C. Model Cards
### D. Incident Reports
```

---

## Template 4: Model Card

```markdown
# Model Card: [Model Name]

## Model Details

| Field | Value |
|-------|-------|
| **Model Name** | |
| **Version** | |
| **Type** | Classification / Regression / Generation / etc. |
| **Architecture** | |
| **Parameters** | |
| **Developer** | |
| **Release Date** | |
| **License** | |

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

### Data Sources
| Source | Records | Time Period |
|--------|---------|-------------|
| | | |

### Data Processing
[Description of preprocessing, filtering, augmentation]

### Known Limitations
- [Limitation 1]
- [Limitation 2]

## Evaluation

### Metrics

| Metric | Test Set | Production |
|--------|----------|------------|
| Accuracy | | |
| Precision | | |
| Recall | | |

### Disaggregated Evaluation

| Subgroup | Accuracy | Precision | Recall |
|----------|----------|-----------|--------|
| | | | |

### Fairness Assessment

| Metric | Value | Acceptable Range |
|--------|-------|------------------|
| Demographic Parity | | |
| Equal Opportunity | | |

## Limitations and Risks

### Known Limitations
- [Limitation with mitigation]

### Potential Risks
- [Risk with mitigation]

### Failure Modes
- [Failure mode and handling]

## Recommendations

### Best Practices
- [Recommendation 1]
- [Recommendation 2]

### Human Oversight
- [Oversight requirement]

## EU AI Act Compliance

| Requirement | Status | Notes |
|-------------|--------|-------|
| Risk classification | Completed | [Classification] |
| Technical documentation | Completed | [Link] |
| Bias testing | Completed | [Results] |
| Human oversight | Implemented | [Description] |

---

**Last Updated:** YYYY-MM-DD
**Next Review:** YYYY-MM-DD
```

---

## Template 5: Conformity Self-Assessment

```markdown
# EU AI Act Conformity Self-Assessment

**System:** [Name]
**Date:** YYYY-MM-DD
**Assessor:** [Name]

## Checklist

### Article 9: Risk Management

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| Risk management system established | [ ] | |
| Risks identified and analyzed | [ ] | |
| Risk estimation for intended use | [ ] | |
| Risk estimation for misuse | [ ] | |
| Mitigation measures implemented | [ ] | |
| Testing completed | [ ] | |

### Article 10: Data Governance

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| Training data documented | [ ] | |
| Data quality verified | [ ] | |
| Bias examined and addressed | [ ] | |
| Data governance practices documented | [ ] | |

### Article 11: Technical Documentation

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| System description complete | [ ] | |
| Design specifications documented | [ ] | |
| Development process recorded | [ ] | |
| Monitoring capabilities described | [ ] | |

### Article 12: Record-Keeping

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| Automatic logging enabled | [ ] | |
| Events traceable | [ ] | |
| Retention period defined | [ ] | |

### Article 13: Transparency

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| Instructions for use provided | [ ] | |
| Capabilities documented | [ ] | |
| Limitations disclosed | [ ] | |

### Article 14: Human Oversight

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| Oversight capability designed | [ ] | |
| Human intervention enabled | [ ] | |
| Override mechanism available | [ ] | |

### Article 15: Accuracy, Robustness, Cybersecurity

| Requirement | Compliant | Evidence |
|-------------|-----------|----------|
| Accuracy levels appropriate | [ ] | |
| Robustness measures implemented | [ ] | |
| Cybersecurity controls in place | [ ] | |

## Declaration

I declare that this AI system meets the requirements of the EU AI Act.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Provider Representative | | | |

## Supporting Documents

- [ ] Technical Documentation
- [ ] Risk Management Report
- [ ] Test Results
- [ ] Model Card
- [ ] Training Data Summary
```

---

## Template 6: Incident Report

```markdown
# AI System Incident Report

## Incident Summary

| Field | Value |
|-------|-------|
| **Incident ID** | INC-YYYY-NNN |
| **System** | [System Name] |
| **Date Detected** | YYYY-MM-DD HH:MM |
| **Date Reported** | YYYY-MM-DD |
| **Severity** | Critical / High / Medium / Low |
| **Status** | Open / Under Investigation / Resolved / Closed |

## Incident Description

### What Happened
[Detailed description of the incident]

### Impact
- Users affected: [Number]
- Decisions impacted: [Number]
- Duration: [Time period]

### Root Cause
[Analysis of why the incident occurred]

## Response

### Immediate Actions
1. [Action taken]
2. [Action taken]

### Corrective Actions
1. [Planned correction]
2. [Planned correction]

### Preventive Measures
1. [Measure to prevent recurrence]
2. [Measure to prevent recurrence]

## Regulatory Notification

| Question | Answer |
|----------|--------|
| Serious incident under AI Act? | Yes / No |
| Authority notification required? | Yes / No |
| Authority notified? | Yes / No |
| Notification date | YYYY-MM-DD |

## Timeline

| Date | Time | Event |
|------|------|-------|
| | | Incident occurred |
| | | Incident detected |
| | | Initial response |
| | | Root cause identified |
| | | Corrective action implemented |
| | | Incident resolved |

## Lessons Learned

[Key takeaways and improvements]

## Sign-Off

| Role | Name | Date |
|------|------|------|
| Incident Manager | | |
| Technical Lead | | |
| Compliance Officer | | |
```

---

*ML Engineer Methodology - faion-network*
