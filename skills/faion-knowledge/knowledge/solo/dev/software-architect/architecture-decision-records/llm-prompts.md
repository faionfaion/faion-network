# LLM Prompts for ADR Writing

Effective prompts for LLM-assisted Architecture Decision Record creation.

## Prompt Categories

| Category | Use Case |
|----------|----------|
| [Initial Draft](#1-initial-adr-draft) | Create first draft from notes |
| [Research](#2-research-alternatives) | Explore options and alternatives |
| [Analysis](#3-trade-off-analysis) | Evaluate pros/cons |
| [Improvement](#4-improve-existing-adr) | Enhance existing ADR |
| [Review](#5-adr-review) | Check completeness |
| [Conversion](#6-format-conversion) | Convert between formats |

---

## 1. Initial ADR Draft

### 1.1 From Problem Statement

```
You are a software architect helping write an Architecture Decision Record.

Context:
- Project: [Project name and brief description]
- Team: [Team size and expertise]
- Current stack: [Existing technologies]
- Problem: [Brief description of the decision needed]

Task: Create an ADR draft in MADR format covering:
1. Clear problem statement
2. At least 3 viable alternatives
3. Decision drivers (what matters most)
4. Pros/cons for each option
5. Recommended decision with justification
6. Consequences (positive and negative)

Format the output as a complete markdown ADR document.
```

### 1.2 From Meeting Notes

```
Convert the following meeting notes into a formal ADR using the Nygard format:

Meeting Notes:
"""
[Paste meeting notes here]
"""

Include:
- Clear context section explaining the problem
- The decision that was made
- All consequences discussed
- Any alternatives that were mentioned

If information is missing, note it as [TO BE FILLED] in the appropriate section.
```

### 1.3 Technology Selection ADR

```
Help me write an ADR for selecting [technology category] for [use case].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Constraints:
- [Constraint 1, e.g., budget, team skills, timeline]
- [Constraint 2]

Compare at least 3 options including:
- [Specific option to consider]
- [Another option]

Use MADR format with detailed pros/cons analysis.
```

---

## 2. Research Alternatives

### 2.1 Option Discovery

```
I need to make an architecture decision about [topic].

Context:
- Use case: [What we're trying to achieve]
- Scale: [Expected load, data volume, users]
- Team: [Size, expertise, preferences]
- Timeline: [When this needs to be decided/implemented]

List 5-7 viable alternatives with:
1. Brief description (1-2 sentences)
2. Key strengths
3. Key weaknesses
4. Best suited for (use cases)
5. Not recommended when (anti-patterns)

Rank them by fit for my context.
```

### 2.2 Deep Dive on Options

```
Compare [Option A] vs [Option B] vs [Option C] for [use case].

For each option, analyze:

1. Technical Capabilities
   - Core features
   - Limitations
   - Scalability characteristics

2. Operational Aspects
   - Deployment complexity
   - Monitoring/observability
   - Maintenance burden

3. Team Considerations
   - Learning curve
   - Community/documentation quality
   - Hiring market

4. Cost Analysis
   - Licensing
   - Infrastructure
   - Development time

5. Risk Assessment
   - Vendor lock-in
   - Technology maturity
   - Security track record

Conclude with a recommendation matrix.
```

### 2.3 Industry Research

```
What are the current (2025) best practices for [topic]?

Include:
- Industry-standard approaches
- Common patterns used by companies at [our scale]
- Emerging trends and their maturity
- Patterns to avoid and why

Reference specific companies or projects if possible.
```

---

## 3. Trade-off Analysis

### 3.1 Quality Attributes Impact

```
Analyze how [proposed decision] impacts these quality attributes:

- Scalability
- Performance
- Security
- Maintainability
- Reliability
- Cost

For each attribute:
1. Current state (before decision)
2. Expected state (after decision)
3. Trade-offs accepted
4. Mitigation strategies for negative impacts
```

### 3.2 Build vs Buy Analysis

```
Help me analyze build vs buy for [capability].

Build option:
- Tech stack we'd use: [technologies]
- Team availability: [X developers for Y weeks]
- Maintenance commitment: [ongoing effort]

Buy options:
- [Product/Service 1]
- [Product/Service 2]

Analyze:
1. Total cost of ownership (3-year horizon)
2. Time to value
3. Customization needs
4. Integration complexity
5. Vendor risk
6. Strategic value of building in-house

Recommend build or buy with clear rationale.
```

### 3.3 Risk Analysis

```
Identify risks for this architecture decision:

Decision: [The proposed decision]
Context: [Brief context]

For each risk:
1. Description
2. Likelihood (Low/Medium/High)
3. Impact (Low/Medium/High)
4. Mitigation strategy
5. Contingency if risk materializes

Format as a risk register table.
```

---

## 4. Improve Existing ADR

### 4.1 Completeness Check

```
Review this ADR for completeness and suggest improvements:

"""
[Paste ADR content here]
"""

Check for:
- [ ] Clear problem statement
- [ ] Sufficient context
- [ ] At least 3 alternatives considered
- [ ] Objective evaluation criteria
- [ ] Clear decision with rationale
- [ ] Both positive and negative consequences
- [ ] Missing information that should be added

Provide specific suggestions for each gap found.
```

### 4.2 Strengthen Rationale

```
The following ADR has weak justification. Strengthen the rationale:

Current ADR:
"""
[Paste ADR with weak rationale]
"""

Improve by:
1. Adding specific, measurable criteria
2. Providing evidence for claims
3. Addressing obvious counterarguments
4. Making trade-offs explicit
5. Adding relevant industry references
```

### 4.3 Add Missing Consequences

```
This ADR is missing detailed consequences. Expand them:

Decision: [Brief description of decision]
Current consequences listed:
- [Current consequence 1]
- [Current consequence 2]

Generate comprehensive consequences including:

Positive:
- Immediate benefits
- Long-term benefits
- Quality attribute improvements

Negative:
- Immediate drawbacks
- Technical debt introduced
- Operational overhead
- Skills/training needed

Follow-up decisions required:
- What other decisions does this trigger?
```

---

## 5. ADR Review

### 5.1 Devil's Advocate

```
Play devil's advocate for this ADR:

"""
[Paste ADR content]
"""

Challenge:
1. The problem framing - Is this the right problem?
2. The alternatives - What's missing?
3. The evaluation - Is it biased?
4. The decision - What could go wrong?
5. The consequences - What's underestimated?

Be constructive but thorough. Identify blind spots.
```

### 5.2 Stakeholder Perspective Review

```
Review this ADR from different stakeholder perspectives:

"""
[Paste ADR content]
"""

Perspectives to consider:
- Security team: What security implications?
- Operations team: What operational burden?
- Product team: What feature/timeline impact?
- Finance: What cost implications?
- Future developers: What maintenance burden?

Identify concerns each stakeholder might raise.
```

### 5.3 Technical Accuracy Check

```
Verify the technical claims in this ADR:

"""
[Paste ADR content]
"""

For each technical claim:
1. Is it accurate?
2. Is it current (2025)?
3. Are there caveats missing?
4. Should benchmarks/references be added?

Flag any outdated or incorrect information.
```

---

## 6. Format Conversion

### 6.1 Nygard to MADR

```
Convert this Nygard-format ADR to MADR format:

"""
[Paste Nygard ADR]
"""

Add these MADR sections:
- Decision Drivers
- Considered Options (expanded)
- Pros and Cons of Options
- Links section

Maintain all original content while restructuring.
```

### 6.2 Y-Statement to Full ADR

```
Expand this Y-statement into a full MADR document:

Y-Statement:
"""
[Paste Y-statement]
"""

Create complete ADR with:
- Full context section
- Expanded decision drivers
- Detailed alternatives analysis
- Comprehensive consequences
```

### 6.3 Meeting Discussion to ADR

```
Transform this architecture discussion into a formal ADR:

Discussion transcript:
"""
[Paste discussion notes/transcript]
"""

Extract:
- The core problem being discussed
- All options mentioned
- Arguments for/against each option
- The decision reached
- Concerns raised (as consequences)

Format as MADR with proper structure.
```

---

## 7. Specialized Scenarios

### 7.1 Migration Decision

```
Help write an ADR for migrating from [Current] to [Proposed].

Current state:
- Technology: [Current technology]
- Scale: [Current usage metrics]
- Pain points: [Why considering migration]

Proposed state:
- Technology: [Proposed technology]
- Expected benefits: [What we hope to gain]

Address:
1. Migration strategy options
2. Risk assessment
3. Rollback plan
4. Success criteria
5. Timeline considerations

Include a migration plan outline in the ADR.
```

### 7.2 Deprecation Decision

```
Write an ADR for deprecating [technology/pattern/service].

Current state:
- What: [What's being deprecated]
- Usage: [Current usage/dependencies]
- Why: [Reasons for deprecation]

Replacement:
- What: [Replacement technology/pattern]
- Migration: [High-level migration approach]

Cover:
1. Impact assessment
2. Deprecation timeline
3. Communication plan
4. Support during transition
5. Removal criteria
```

### 7.3 Vendor Selection

```
Create an ADR for selecting a vendor for [service category].

Requirements:
- Functional: [What we need]
- Non-functional: [SLAs, compliance, etc.]
- Budget: [Budget constraints]

Vendors to evaluate:
- [Vendor 1]
- [Vendor 2]
- [Vendor 3]

Evaluation criteria:
1. Feature completeness
2. Pricing model
3. Support quality
4. Integration capabilities
5. Vendor stability
6. Exit strategy

Recommend with detailed comparison matrix.
```

---

## 8. Iteration Prompts

### 8.1 Refine Context

```
The context section of this ADR is unclear. Rewrite it to:

Current:
"""
[Paste current context]
"""

Make it:
- More specific about the problem
- Clear about what triggered this decision
- Explicit about constraints
- Understandable to someone new to the project
```

### 8.2 Better Alternatives

```
The alternatives in this ADR seem limited. Suggest more options:

Current problem: [Problem statement]
Current alternatives: [List current alternatives]

Identify 2-3 additional alternatives that:
- Address the same problem differently
- May have been overlooked
- Come from different technical paradigms

Brief each new alternative with pros/cons.
```

### 8.3 Clearer Decision

```
The decision in this ADR is vague. Make it more actionable:

Current decision:
"""
[Paste current decision]
"""

Rewrite to include:
- Specific technology/version
- Scope of application
- Timeline for implementation
- Success criteria
- Ownership
```

---

## Best Practices for LLM-Assisted ADRs

### Do

- Provide comprehensive context about your project
- Specify constraints and requirements upfront
- Ask for multiple alternatives
- Request both pros and cons
- Validate technical claims independently
- Iterate on drafts

### Don't

- Accept first draft without review
- Skip human validation of technical accuracy
- Let LLM make the final decision
- Use without team review
- Copy industry examples without adaptation

### Iteration Pattern

```
1. Initial prompt → Get draft
2. "Expand the consequences section"
3. "Add more detail to Option B analysis"
4. "Challenge assumption X"
5. "Format for our template"
6. Human review and finalization
```

---

## Quick Reference

| Task | Key Elements to Include |
|------|------------------------|
| Draft creation | Context, requirements, constraints, scale |
| Alternative research | Use case, scale, team skills, timeline |
| Trade-off analysis | Quality attributes, current state, priorities |
| Review | Specific concerns, stakeholder perspectives |
| Conversion | Source format, target format, additions needed |
