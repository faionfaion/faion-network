# LLM Prompts for Quality Attributes Analysis

Effective prompts for LLM-assisted quality attribute analysis, scenario generation, trade-off evaluation, and ATAM facilitation.

---

## Scenario Generation Prompts

### Generate Quality Attribute Scenarios

```
You are a software architect analyzing quality attributes for a system.

System Context:
- [Brief system description]
- [Domain: e-commerce, healthcare, fintech, etc.]
- [Scale: users, transactions, data volume]
- [Key business drivers]

Generate 5 quality attribute scenarios for [ATTRIBUTE] using this format:

| Part | Value |
|------|-------|
| Source | [Who/what triggers] |
| Stimulus | [Event or condition] |
| Environment | [Context] |
| Artifact | [Component affected] |
| Response | [Expected behavior] |
| Measure | [Quantifiable criteria] |

Include:
1. Normal operation scenario
2. Peak load scenario
3. Failure/recovery scenario
4. [Attribute-specific scenario]
5. Edge case scenario

For each scenario, provide:
- Priority: (Importance H/M/L, Difficulty H/M/E)
- Rationale for the response measure
- Test strategy suggestion
```

### Performance Scenarios Deep Dive

```
For a [SYSTEM TYPE] with the following characteristics:
- Expected users: [NUMBER]
- Peak load: [Nx normal]
- Critical operations: [LIST]
- Current SLAs: [IF ANY]

Generate detailed performance scenarios covering:

1. **Latency scenarios** for critical user journeys:
   - Define p50, p95, p99 targets
   - Consider geographical distribution
   - Include database query patterns

2. **Throughput scenarios**:
   - Peak request rates
   - Batch processing windows
   - API rate limits

3. **Resource utilization scenarios**:
   - CPU, memory, disk I/O bounds
   - Connection pool limits
   - Cache hit ratios

For each scenario, explain:
- Why this measure matters for this system type
- How to test/validate
- Common architectural tactics to achieve the target
```

### Security Scenarios with Threat Context

```
For a [SYSTEM TYPE] handling [DATA SENSITIVITY LEVEL] data:

Domain context:
- [Industry: healthcare, finance, retail]
- [Compliance requirements: HIPAA, PCI-DSS, GDPR]
- [Deployment: cloud, on-prem, hybrid]

Generate security quality attribute scenarios for:

1. **Authentication attacks**
   - Credential stuffing
   - Session hijacking
   - MFA bypass attempts

2. **Authorization failures**
   - Privilege escalation
   - Horizontal access
   - API abuse

3. **Data protection**
   - Data exfiltration attempts
   - Injection attacks
   - Man-in-the-middle

4. **Availability attacks**
   - DDoS
   - Resource exhaustion
   - Cryptographic attacks

For each scenario, specify:
- Attack vector and source
- Detection time requirements
- Response and recovery expectations
- Compliance implications
```

---

## Utility Tree Prompts

### Build Complete Utility Tree

```
Create a utility tree for a [SYSTEM TYPE] system.

Business context:
- [Primary business goals]
- [Key stakeholders and their priorities]
- [Constraints: budget, time, regulatory]

Structure the utility tree with:

1. **Root**: UTILITY (overall system value)

2. **Level 1**: Primary quality attributes
   - Select 5-7 most relevant for this domain
   - Consider ISO 25010 characteristics

3. **Level 2**: Quality attribute refinements
   - Break each attribute into specific concerns
   - Use domain-specific terminology

4. **Level 3**: Concrete scenarios (leaves)
   - Each leaf should be testable
   - Include priority notation (Importance, Difficulty)
   - Focus on architectural drivers

Output format:
```
UTILITY
├── [Attribute 1]
│   ├── [Refinement 1.1]
│   │   ├── [Scenario] (H,H) - [Brief measure]
│   │   └── [Scenario] (M,M) - [Brief measure]
│   └── [Refinement 1.2]
│       └── ...
└── ...
```

Highlight the (H,H) scenarios as architectural drivers.
```

### Prioritize Utility Tree Scenarios

```
Given this utility tree for [SYSTEM]:

[PASTE UTILITY TREE]

And these stakeholder priorities:
- [Stakeholder 1]: [Top 3 attributes]
- [Stakeholder 2]: [Top 3 attributes]
- [Stakeholder 3]: [Top 3 attributes]

Perform prioritization analysis:

1. **Rate each leaf scenario** on:
   - Business importance (H/M/L): Impact on business goals
   - Technical difficulty (H/M/E): Complexity to achieve

2. **Identify architectural drivers**:
   - List all (H,H) and (H,M) scenarios
   - Explain why each is a driver

3. **Stakeholder conflict analysis**:
   - Where do stakeholder priorities conflict?
   - Which scenarios require trade-off decisions?

4. **Recommendation**:
   - Top 5 scenarios to focus architecture on
   - Scenarios that can be deferred
```

---

## Trade-off Analysis Prompts

### Analyze Quality Attribute Trade-offs

```
Analyze trade-offs for [SYSTEM] between these quality attributes:

Attribute A: [ATTRIBUTE]
- Current requirement: [REQUIREMENT]
- Business driver: [WHY IMPORTANT]

Attribute B: [ATTRIBUTE]
- Current requirement: [REQUIREMENT]
- Business driver: [WHY IMPORTANT]

Provide:

1. **Inherent tension explanation**
   - Why these attributes conflict
   - Typical trade-off patterns in similar systems

2. **Options analysis**

| Option | Impact on A | Impact on B | Other Effects | Cost/Complexity |
|--------|-------------|-------------|---------------|-----------------|
| Option 1 | ... | ... | ... | ... |
| Option 2 | ... | ... | ... | ... |
| Option 3 | ... | ... | ... | ... |

3. **Recommendation based on context**
   - Which option fits this system best
   - Conditions that would change the recommendation

4. **Mitigation strategies**
   - How to minimize the negative impact
   - Monitoring needed to detect degradation
```

### Evaluate Architectural Decision Trade-offs

```
Evaluate this architectural decision for trade-offs:

Decision: [DESCRIBE DECISION]
Context: [SYSTEM CONTEXT]
Current architecture: [BRIEF DESCRIPTION]

Analyze:

1. **Quality attributes affected**
   - List all attributes impacted
   - Rate impact: Positive (+), Negative (-), Neutral (=)

2. **Sensitivity analysis**
   - Which parameters are sensitive to this decision?
   - What happens if requirements change?

3. **Risk assessment**
   - What could go wrong?
   - How likely and how severe?

4. **Reversibility**
   - How hard to change this decision later?
   - What conditions would trigger reconsideration?

5. **ADR recommendation**
   - Draft decision rationale
   - Document alternatives considered
```

### CAP Theorem Trade-off Analysis

```
For a distributed system with these requirements:
- [Data type and operations]
- [Consistency needs: strong, eventual, causal]
- [Availability requirements: uptime %, RTO]
- [Geographic distribution: regions]
- [Network reliability assumptions]

Analyze CAP trade-offs:

1. **Categorize system needs**
   - Is this a CP, AP, or CA-preferring system?
   - What happens during partition?

2. **Scenario analysis**

| Scenario | Without Partition | During Partition | After Partition |
|----------|-------------------|------------------|-----------------|
| Read ops | ... | ... | ... |
| Write ops | ... | ... | ... |
| Consistency | ... | ... | ... |

3. **Technology recommendations**
   - Databases that fit this profile
   - Consistency patterns to implement

4. **Monitoring and recovery**
   - How to detect inconsistency
   - Reconciliation strategies
```

---

## ATAM Facilitation Prompts

### Prepare ATAM Evaluation

```
Prepare for an ATAM evaluation of [SYSTEM].

System documentation provided:
- [Architecture diagrams]
- [Business requirements]
- [Current quality concerns]

Generate:

1. **Business driver questions**
   - 10 questions to ask project sponsors
   - Focus on priorities and constraints

2. **Architecture presentation outline**
   - Key views to request from architect
   - Technical deep-dive areas

3. **Initial utility tree draft**
   - Based on available documentation
   - Hypothesis of key quality attributes

4. **Scenario brainstorming seeds**
   - 3-5 scenarios per attribute to propose
   - Designed to uncover risks

5. **Risk hunting focus areas**
   - Where to look for sensitivity points
   - Common risks in this architecture style
```

### Analyze ATAM Findings

```
Analyze these ATAM findings and synthesize risk themes:

Risks identified:
[LIST OF RISKS]

Sensitivity points:
[LIST OF SENSITIVITY POINTS]

Trade-off points:
[LIST OF TRADE-OFF POINTS]

Provide:

1. **Risk theme identification**
   - Group related risks into themes
   - Name each theme descriptively

2. **Theme severity assessment**

| Theme | Related Risks | Business Impact | Likelihood | Priority |
|-------|---------------|-----------------|------------|----------|
| ... | ... | ... | ... | ... |

3. **Root cause analysis**
   - Underlying architectural issues
   - Process or organizational factors

4. **Mitigation roadmap**
   - Immediate actions (0-30 days)
   - Short-term (1-3 months)
   - Long-term (3-12 months)

5. **Success metrics**
   - How to measure improvement
   - Leading and lagging indicators
```

---

## Stakeholder Analysis Prompts

### Identify Stakeholder Quality Priorities

```
For a [SYSTEM TYPE] in [DOMAIN], identify stakeholder quality priorities.

Known stakeholder groups:
[LIST STAKEHOLDER GROUPS]

For each stakeholder group, determine:

1. **Primary quality concerns**
   - Top 3 quality attributes
   - Rationale for each

2. **Success criteria**
   - How they measure "good enough"
   - Acceptable trade-offs

3. **Conflict potential**
   - Where their needs conflict with others
   - Negotiation leverage

4. **Stakeholder-attribute matrix**

| Stakeholder | Perf | Avail | Sec | Scale | Maint | Cost |
|-------------|------|-------|-----|-------|-------|------|
| [Group 1] | H/M/L | ... | ... | ... | ... | ... |
| [Group 2] | ... | ... | ... | ... | ... | ... |

5. **Communication strategy**
   - How to present trade-offs
   - Decision-making process
```

### Resolve Stakeholder Conflicts

```
Stakeholder quality attribute conflict:

Stakeholder A: [ROLE]
- Wants: [QUALITY ATTRIBUTE + REQUIREMENT]
- Rationale: [WHY]

Stakeholder B: [ROLE]
- Wants: [CONFLICTING REQUIREMENT]
- Rationale: [WHY]

System constraints:
- [TECHNICAL CONSTRAINTS]
- [BUDGET CONSTRAINTS]
- [TIMELINE]

Provide conflict resolution options:

1. **Find common ground**
   - Shared objectives
   - Non-negotiables for each

2. **Creative solutions**
   - Tiered approach (different SLAs)
   - Context-dependent behavior
   - Future evolution path

3. **Trade-off options**

| Option | A's Satisfaction | B's Satisfaction | Feasibility |
|--------|------------------|------------------|-------------|
| ... | ... | ... | ... |

4. **Facilitation script**
   - How to present options
   - Questions to guide discussion
   - Decision criteria to propose
```

---

## Architecture Tactics Prompts

### Recommend Quality Attribute Tactics

```
For [QUALITY ATTRIBUTE] with these requirements:
- Target: [SPECIFIC REQUIREMENT]
- Constraints: [LIMITATIONS]
- Current state: [BASELINE]

Recommend architectural tactics:

1. **Primary tactics** (direct impact)

| Tactic | Description | Impact | Complexity | Trade-offs |
|--------|-------------|--------|------------|------------|
| ... | ... | ... | ... | ... |

2. **Supporting tactics** (indirect/enabling)
   - Tactics that enable primary tactics
   - Monitoring and observability needs

3. **Anti-patterns to avoid**
   - Common mistakes
   - Why they don't work

4. **Implementation sequence**
   - Which tactics to implement first
   - Dependencies between tactics

5. **Validation approach**
   - How to verify tactic effectiveness
   - Metrics to track
```

### Design for Multiple Quality Attributes

```
Design an architecture that balances:
- [ATTRIBUTE 1]: [REQUIREMENT]
- [ATTRIBUTE 2]: [REQUIREMENT]
- [ATTRIBUTE 3]: [REQUIREMENT]

Constraints:
- Technology: [ALLOWED/PREFERRED TECH]
- Scale: [EXPECTED SCALE]
- Team: [TEAM SIZE/SKILLS]

Provide:

1. **Architecture pattern recommendation**
   - Pattern that best fits requirements
   - Rationale

2. **Tactic combination**

| Component | Primary Tactic | Supporting Tactics | Attributes Served |
|-----------|----------------|-------------------|-------------------|
| ... | ... | ... | ... |

3. **Trade-off matrix**
   - Where tactics conflict
   - Resolution for each conflict

4. **Component diagram**
   - Key components
   - Interaction patterns
   - Quality attribute responsibility

5. **Evolution path**
   - How architecture can adapt
   - Future optimization opportunities
```

---

## Review and Validation Prompts

### Validate Quality Attribute Specification

```
Review this quality attribute specification for completeness and quality:

[PASTE SPECIFICATION]

Evaluate:

1. **Completeness check**
   - [ ] All relevant attributes covered
   - [ ] Scenarios have all 6 parts
   - [ ] Measures are quantifiable
   - [ ] Normal, peak, and failure cases included

2. **Quality issues**
   - Vague or unmeasurable requirements
   - Missing stakeholder perspectives
   - Unrealistic targets
   - Conflicting requirements

3. **Gap analysis**
   - Missing scenarios
   - Underspecified areas
   - Implicit assumptions

4. **Recommendations**
   - Priority improvements
   - Additional scenarios needed
   - Clarification questions
```

### Review ATAM Report

```
Review this ATAM evaluation report:

[PASTE REPORT SUMMARY]

Evaluate:

1. **Completeness**
   - All ATAM outputs present
   - Risks adequately documented
   - Trade-offs clearly explained

2. **Quality of analysis**
   - Risk severity appropriate
   - Sensitivity points identified
   - Themes well-synthesized

3. **Actionability**
   - Clear recommendations
   - Realistic mitigation strategies
   - Appropriate ownership assignment

4. **Missing elements**
   - Unidentified risks
   - Unexplored trade-offs
   - Stakeholder gaps

5. **Improvement suggestions**
   - Report clarity
   - Analysis depth
   - Recommendation prioritization
```

---

## Quick Prompts

### One-liner Scenario Generation
```
Generate a [ATTRIBUTE] scenario for [SYSTEM] with [CONTEXT]. Format: Source | Stimulus | Environment | Artifact | Response | Measure.
```

### Quick Trade-off Check
```
What are the trade-offs of choosing [OPTION A] vs [OPTION B] for [QUALITY ATTRIBUTE] in a [SYSTEM TYPE]?
```

### Tactic Suggestion
```
Suggest 3 architectural tactics to improve [QUALITY ATTRIBUTE] for a [SYSTEM] currently experiencing [PROBLEM].
```

### Risk Identification
```
What are the top 5 quality attribute risks for a [SYSTEM TYPE] using [ARCHITECTURE PATTERN] with [KEY CONSTRAINT]?
```

### Stakeholder Priority Check
```
For [STAKEHOLDER ROLE] in [DOMAIN], rank these quality attributes by typical priority: Performance, Availability, Security, Scalability, Maintainability, Cost.
```

---

## Prompt Engineering Tips

### Context Matters

**Poor prompt:**
```
Generate availability scenarios.
```

**Good prompt:**
```
Generate availability scenarios for a B2B SaaS platform serving
financial institutions. The system processes 100K transactions/day
with 99.99% uptime SLA. Focus on scenarios relevant to quarterly
compliance audits.
```

### Be Specific About Output Format

**Poor prompt:**
```
What are the trade-offs of microservices?
```

**Good prompt:**
```
Analyze microservices trade-offs for a 15-person team migrating
from a monolith. Present as a table with columns: Trade-off,
Microservices Impact, Monolith Impact, Mitigation Strategy.
```

### Request Rationale

**Poor prompt:**
```
What latency target should I use?
```

**Good prompt:**
```
For an e-commerce checkout flow, recommend latency targets for
p50/p95/p99. Explain the rationale based on user experience
research and competitive benchmarks. Include how the target
changes for mobile vs desktop.
```

### Iterate on Responses

```
Your previous response suggested [X].
- How would this change if [CONSTRAINT]?
- What are the risks of [ALTERNATIVE]?
- Compare this to [INDUSTRY STANDARD].
```
