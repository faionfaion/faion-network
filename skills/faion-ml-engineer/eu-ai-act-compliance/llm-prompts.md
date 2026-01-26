# LLM Prompts for EU AI Act Compliance

Prompts for automating compliance analysis and documentation.

## Prompt 1: Risk Classification

```
You are an EU AI Act compliance expert. Classify the following AI system according to the EU AI Act risk categories.

**AI System Description:**
{system_description}

**Questions to Answer:**

1. **Prohibited Practices Check (Article 5)**
   - Does it perform social scoring?
   - Does it exploit vulnerabilities of specific groups?
   - Does it use real-time remote biometric identification?
   - Does it recognize emotions in workplace/education?
   - Does it perform biometric categorization by sensitive attributes?

2. **High-Risk Check (Annex III)**
   - Biometrics (remote identification, categorization)
   - Critical infrastructure (energy, transport, water, digital)
   - Education (admissions, assessment, proctoring)
   - Employment (recruitment, HR decisions, termination)
   - Essential services (credit, insurance, emergency)
   - Law enforcement (risk assessment, lie detection)
   - Migration (visa processing, border control)
   - Justice (legal research, sentencing assistance)

3. **Limited Risk Check (Article 50)**
   - Direct interaction with humans (chatbots)
   - Synthetic content generation (deepfakes, AI images)
   - Emotion recognition systems
   - Biometric categorization

**Output Format:**

## Risk Classification Result

**System:** [Name]
**Classification:** [Unacceptable / High / Limited / Minimal]

### Analysis

**Prohibited Practices:** [None identified / Issue: ...]
**Annex III Match:** [Domain if applicable]
**Article 50 Applicability:** [Yes/No - reason]

### Required Compliance

[List of applicable articles and requirements]

### Recommended Actions

1. [Action 1]
2. [Action 2]
```

---

## Prompt 2: Technical Documentation Generator

```
You are an EU AI Act compliance documentation specialist. Generate technical documentation for the following AI system according to Article 11 requirements.

**System Information:**
- Name: {name}
- Type: {type}
- Purpose: {purpose}
- Users: {users}
- Data inputs: {inputs}
- Outputs: {outputs}
- Model architecture: {architecture}
- Training data: {training_data}

**Generate sections for:**

1. General Description
   - System identification
   - Intended purpose
   - Intended users
   - Prohibited uses

2. System Architecture
   - Components
   - Data flow
   - External dependencies

3. Training Data
   - Sources
   - Quality measures
   - Bias mitigation

4. Performance Metrics
   - Accuracy metrics
   - Fairness metrics
   - Performance boundaries

5. Risk Management
   - Identified risks
   - Mitigation measures
   - Residual risks

6. Human Oversight
   - Oversight mechanisms
   - Intervention procedures

**Output in markdown format with tables where appropriate.**
```

---

## Prompt 3: Bias Assessment

```
You are an AI fairness expert conducting bias assessment for EU AI Act compliance.

**System Details:**
- Purpose: {purpose}
- Protected attributes in data: {attributes}
- Decision type: {decision_type}
- Affected population: {population}

**Evaluation Results:**
{metrics}

**Analyze the following:**

1. **Demographic Parity**
   - Are outcomes distributed equally across groups?
   - What disparities exist?

2. **Equal Opportunity**
   - Do true positive rates differ across groups?
   - What are the implications?

3. **Predictive Equality**
   - Do false positive rates differ across groups?
   - What risks does this create?

4. **Intersectional Analysis**
   - Are there compounded effects for multiple attributes?
   - Which intersections need attention?

**Output Format:**

## Bias Assessment Report

### Summary
[Overall assessment: Pass/Fail/Concerns]

### Findings by Metric

| Metric | Status | Value | Threshold | Notes |
|--------|--------|-------|-----------|-------|

### Risk Analysis
[Describe risks from identified biases]

### Recommendations
1. [Specific recommendation with rationale]
2. [Specific recommendation with rationale]

### Monitoring Plan
[Ongoing monitoring recommendations]
```

---

## Prompt 4: Explainability Generator

```
You are an AI explainability specialist. Generate explanations for AI decisions that comply with EU AI Act transparency requirements (Article 13).

**Decision Context:**
- System: {system_name}
- Decision type: {decision_type}
- Input data: {input_summary}
- Output/Decision: {output}
- Model confidence: {confidence}
- Top contributing features: {features}

**Generate explanations for three audiences:**

1. **End User Explanation**
   - Simple, non-technical language
   - Key factors that influenced the decision
   - How to appeal or request review

2. **Operator Explanation**
   - Technical but accessible
   - Feature contributions
   - Confidence interpretation
   - When to override

3. **Auditor Explanation**
   - Full technical detail
   - Model behavior analysis
   - Compliance evidence
   - Traceability information

**Output Format:**

## Decision Explanation

### For User
[Plain language explanation, max 200 words]

### For Operator
[Technical explanation with feature analysis]

| Feature | Value | Contribution | Direction |
|---------|-------|--------------|-----------|

### For Auditor
[Complete technical record including:]
- Input hash: [hash]
- Model version: [version]
- Decision timestamp: [timestamp]
- Feature weights: [weights]
- Alternative outcomes: [alternatives]
```

---

## Prompt 5: Incident Classification

```
You are an EU AI Act compliance officer. Classify the following AI incident and determine reporting requirements.

**Incident Description:**
{incident_description}

**System Information:**
- System: {system_name}
- Risk level: {risk_level}
- Users affected: {users_affected}
- Decisions impacted: {decisions_impacted}

**Determine:**

1. **Incident Severity**
   - Critical: Fundamental rights violation, serious harm
   - High: Significant malfunction, widespread impact
   - Medium: Limited malfunction, contained impact
   - Low: Minor issue, no significant impact

2. **Serious Incident Criteria (Article 73)**
   - Death or serious damage to health
   - Serious and irreversible disruption of critical infrastructure
   - Breach of fundamental rights obligations
   - Widespread harm to multiple persons

3. **Reporting Requirements**
   - Authority notification required?
   - Notification timeline?
   - Required information?

**Output Format:**

## Incident Classification

**Severity:** [Level]
**Serious Incident:** [Yes/No]
**Authority Notification:** [Required/Not Required]

### Analysis
[Reasoning for classification]

### Required Actions
| Action | Timeline | Responsible |
|--------|----------|-------------|

### Notification Content (if required)
[Draft notification to authorities]
```

---

## Prompt 6: Compliance Gap Analysis

```
You are an EU AI Act compliance auditor. Perform a gap analysis for the following organization.

**Organization Profile:**
- Industry: {industry}
- AI systems in use: {systems}
- Current compliance measures: {current_measures}
- Resources available: {resources}

**For each requirement, assess:**

1. **Current State** - What exists today
2. **Required State** - What the AI Act requires
3. **Gap** - What's missing
4. **Priority** - Critical/High/Medium/Low
5. **Effort** - High/Medium/Low
6. **Recommendation** - Specific action

**Requirements to assess:**
- AI system inventory
- Risk classification
- Technical documentation
- Risk management
- Data governance
- Human oversight
- Transparency measures
- Quality management
- Incident reporting
- Staff training

**Output Format:**

## EU AI Act Compliance Gap Analysis

### Executive Summary
[Overall compliance status and key findings]

### Gap Analysis Matrix

| Requirement | Current | Required | Gap | Priority | Effort |
|-------------|---------|----------|-----|----------|--------|

### Detailed Findings

#### [Requirement 1]
- **Current state:** [Description]
- **Gap:** [What's missing]
- **Recommendation:** [Action]
- **Priority:** [Level]

[Repeat for each requirement]

### Roadmap

| Phase | Focus | Deadline | Key Deliverables |
|-------|-------|----------|------------------|
| 1 | Critical gaps | [Date] | [List] |
| 2 | High priority | [Date] | [List] |
| 3 | Medium priority | [Date] | [List] |
```

---

## Prompt 7: Transparency Disclosure Generator

```
You are a UX writer specializing in AI transparency. Generate compliant disclosure messages for Article 50 requirements.

**System Type:** {system_type}
**Context:** {context}
**User Demographic:** {demographic}
**Interaction Point:** {interaction_point}

**Generate disclosures for:**

1. **Initial Disclosure**
   - Inform user they're interacting with AI
   - Clear, prominent, timely

2. **Capability Disclosure**
   - What the AI can and cannot do
   - Limitations

3. **Data Usage Disclosure**
   - What data is processed
   - How it's used

4. **Human Escalation Option**
   - How to reach a human
   - When available

**Requirements:**
- Clear, simple language
- Culturally appropriate
- Accessible (screen reader friendly)
- Legally compliant

**Output Format:**

## Transparency Disclosures

### Initial Disclosure (Primary)
```
[Message text]
```

### Initial Disclosure (Compact)
```
[Shorter version for space-constrained UI]
```

### Capability Statement
```
[What the AI can/cannot do]
```

### Data Notice
```
[Data usage disclosure]
```

### Human Escalation
```
[How to reach a human]
```

### Implementation Notes
- Placement: [Where to display]
- Timing: [When to show]
- Accessibility: [Requirements]
```

---

## Prompt 8: GPAI Model Documentation

```
You are a technical writer specializing in AI model documentation. Generate GPAI (General Purpose AI) model documentation required by August 2025.

**Model Information:**
- Name: {name}
- Type: {type}
- Parameters: {parameters}
- Training compute: {compute}
- Training data summary: {data_summary}
- Capabilities: {capabilities}
- Known limitations: {limitations}

**Generate documentation sections:**

1. **Technical Documentation**
   - Architecture description
   - Training methodology
   - Evaluation procedures
   - Known capabilities and limitations

2. **Training Data Summary**
   - Data sources (general description)
   - Data types
   - Preprocessing methods
   - Copyright compliance

3. **Transparency Report**
   - Model capabilities
   - Limitations
   - Potential risks
   - Guidance for integrators

4. **Systemic Risk Assessment** (if applicable)
   - Risk evaluation methodology
   - Identified risks
   - Mitigation measures

**Output in structured markdown format.**
```

---

## Usage Notes

### Best Practices

1. **Context is critical** - Provide detailed system information for accurate analysis
2. **Iterate** - Use follow-up prompts to refine outputs
3. **Human review** - Always have compliance experts review generated documentation
4. **Keep current** - EU AI Act guidance evolves; verify against latest requirements

### Integration Examples

```python
# Example: Using prompts with OpenAI API

def classify_ai_system(system_description: str) -> dict:
    prompt = RISK_CLASSIFICATION_PROMPT.format(
        system_description=system_description
    )

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3  # Lower temperature for consistent analysis
    )

    return parse_classification_response(response.choices[0].message.content)
```

### Prompt Customization

Adapt prompts for your jurisdiction:
- Add local regulatory requirements
- Include industry-specific considerations
- Adjust language for your legal review process

---

*ML Engineer Methodology - faion-network*
