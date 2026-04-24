# AI Governance Compliance Checklist

Verification checklist for AI governance and regulatory compliance.

## Pre-Deployment Checklist

### Model Documentation

- [ ] **Model Card** - Purpose, architecture, training data, performance metrics
- [ ] **Data Sheet** - Data sources, collection methods, preprocessing steps
- [ ] **Risk Assessment** - Identified risks and mitigation strategies
- [ ] **Intended Use** - Approved use cases and known limitations
- [ ] **Version History** - Changes from previous versions documented

### Bias and Fairness

- [ ] **Fairness Metrics** - Calculated across protected attributes
- [ ] **Bias Testing** - Run Fairlearn or AI Fairness 360 analysis
- [ ] **Disparate Impact** - Ratio within acceptable threshold (>0.8)
- [ ] **Subgroup Performance** - Verified across demographic groups
- [ ] **Mitigation Applied** - Documented bias correction methods

### Explainability

- [ ] **Feature Attribution** - SHAP values computed for key features
- [ ] **Local Explanations** - LIME available for individual predictions
- [ ] **Global Interpretability** - Overall model behavior documented
- [ ] **User-Facing Explanations** - Plain language explanations ready
- [ ] **Decision Factors** - Key drivers identified and documented

### Data Governance

- [ ] **Data Lineage** - Full traceability from source to model
- [ ] **Consent Verification** - Legal basis for data use confirmed
- [ ] **PII Handling** - Personal data properly anonymized/pseudonymized
- [ ] **Retention Policy** - Data retention period defined and enforced
- [ ] **Data Quality** - Quality metrics meet thresholds

### Security

- [ ] **Access Controls** - RBAC configured for model access
- [ ] **Encryption** - Data at rest and in transit encrypted
- [ ] **Vulnerability Scan** - No critical vulnerabilities found
- [ ] **Inference Security** - Input validation and rate limiting
- [ ] **Model Security** - Protected against extraction attacks

### Human Oversight

- [ ] **Review Process** - Human review for high-stakes decisions
- [ ] **Escalation Path** - Clear escalation for edge cases
- [ ] **Override Capability** - Humans can override AI decisions
- [ ] **Feedback Loop** - Mechanism for human feedback collection
- [ ] **Training** - Operators trained on appropriate use

---

## EU AI Act Compliance (High-Risk Systems)

### Risk Classification

- [ ] **Risk Level Determined** - System classified per EU AI Act
- [ ] **High-Risk Justification** - If applicable, rationale documented
- [ ] **Prohibited Use Check** - Confirmed no prohibited applications

### Technical Documentation

- [ ] **System Description** - Detailed technical specification
- [ ] **Training Methodology** - Algorithms and techniques documented
- [ ] **Training Data Description** - Datasets, selection, preparation
- [ ] **Validation Data** - Separate validation datasets used
- [ ] **Performance Metrics** - Accuracy, precision, recall documented
- [ ] **Known Limitations** - Boundaries of system performance

### Quality Management

- [ ] **QMS Implemented** - Quality management system in place
- [ ] **Process Controls** - Development processes documented
- [ ] **Change Management** - Modification procedures defined
- [ ] **Testing Procedures** - Comprehensive test protocols

### Conformity Assessment

- [ ] **Self-Assessment** - Internal conformity check completed
- [ ] **Third-Party Audit** - If required, external assessment done
- [ ] **CE Marking** - Conformity marking applied (if applicable)
- [ ] **EU Declaration** - Declaration of conformity prepared

### Transparency

- [ ] **User Notification** - Users informed of AI interaction
- [ ] **Capability Disclosure** - System capabilities clearly stated
- [ ] **Limitation Disclosure** - Known limitations communicated
- [ ] **Instructions for Use** - Clear guidance provided

### Registration

- [ ] **EU Database Entry** - Registered in EU AI database (if required)
- [ ] **National Authority** - Notified relevant national authority
- [ ] **Authorized Representative** - EU rep designated (if non-EU)

---

## Audit Trail Checklist

### Logging Requirements

- [ ] **Decision Logs** - All predictions/decisions recorded
- [ ] **Timestamp** - UTC timestamps for all events
- [ ] **Input Data** - Inputs for each decision stored
- [ ] **Output Data** - Model outputs recorded
- [ ] **User Context** - User/session identifiers logged
- [ ] **Model Version** - Version used for each decision

### Training Audit

- [ ] **Dataset Version** - Training data version recorded
- [ ] **Hyperparameters** - All parameters documented
- [ ] **Random Seeds** - Seeds for reproducibility
- [ ] **Training Duration** - Start/end times logged
- [ ] **Hardware Environment** - GPU/CPU specs recorded
- [ ] **Framework Versions** - Library versions captured

### Deployment Audit

- [ ] **Deployment Date** - When model went live
- [ ] **Deployer Identity** - Who approved deployment
- [ ] **Configuration** - Production config captured
- [ ] **Previous Version** - What version was replaced
- [ ] **Rollback Plan** - Documented rollback procedure

### Monitoring Audit

- [ ] **Performance Metrics** - Regular metric snapshots
- [ ] **Drift Detection** - Data/concept drift logged
- [ ] **Alerts** - All triggered alerts recorded
- [ ] **Incidents** - Incident reports filed
- [ ] **Remediation** - Actions taken documented

---

## Periodic Review Checklist

### Monthly Review

- [ ] **Performance Trending** - KPIs reviewed for degradation
- [ ] **Alert Analysis** - All alerts investigated
- [ ] **Feedback Review** - User feedback analyzed
- [ ] **Drift Assessment** - Data drift metrics checked

### Quarterly Review

- [ ] **Bias Re-assessment** - Fairness metrics recalculated
- [ ] **Documentation Update** - Model card current
- [ ] **Compliance Check** - Regulatory changes assessed
- [ ] **Risk Review** - Risk assessment updated

### Annual Review

- [ ] **Full Audit** - Comprehensive governance audit
- [ ] **Regulatory Alignment** - All regulations reviewed
- [ ] **Policy Update** - Governance policies refreshed
- [ ] **Training Refresh** - Team training updated
- [ ] **Vendor Review** - Third-party AI systems assessed

---

## Incident Response Checklist

### Detection

- [ ] **Incident Identified** - Issue clearly defined
- [ ] **Severity Classified** - Impact level determined
- [ ] **Stakeholders Notified** - Relevant parties informed
- [ ] **Evidence Preserved** - Logs and data secured

### Response

- [ ] **Containment** - Issue contained (rollback if needed)
- [ ] **Root Cause** - Investigation initiated
- [ ] **Impact Assessment** - Affected users/decisions identified
- [ ] **Remediation Plan** - Fix strategy developed

### Resolution

- [ ] **Fix Implemented** - Correction deployed
- [ ] **Verification** - Fix effectiveness confirmed
- [ ] **Communication** - Affected parties notified
- [ ] **Documentation** - Incident report completed

### Post-Incident

- [ ] **Lessons Learned** - Review conducted
- [ ] **Process Improvement** - Preventive measures identified
- [ ] **Policy Update** - Procedures updated if needed
- [ ] **Training Update** - Team knowledge refreshed

---

## Vendor/Third-Party AI Checklist

### Due Diligence

- [ ] **Vendor Assessment** - Governance practices reviewed
- [ ] **Compliance Certifications** - ISO 27001, SOC 2, etc.
- [ ] **AI-Specific Certs** - ISO 42001 or equivalent
- [ ] **Data Processing** - DPA/SCC in place
- [ ] **Sub-processor List** - Third parties disclosed

### Contractual Requirements

- [ ] **Audit Rights** - Right to audit vendor
- [ ] **Compliance Obligations** - Regulatory requirements specified
- [ ] **Incident Notification** - Breach notification terms
- [ ] **Data Deletion** - End-of-contract data handling
- [ ] **Liability Allocation** - AI-related liability addressed

### Ongoing Monitoring

- [ ] **Performance SLAs** - Metrics tracked
- [ ] **Compliance Updates** - Vendor compliance monitored
- [ ] **Version Changes** - Model updates reviewed
- [ ] **Security Assessments** - Regular security checks
