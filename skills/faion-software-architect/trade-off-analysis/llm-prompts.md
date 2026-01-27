# LLM Prompts for Trade-off Analysis

Effective prompts for LLM-assisted trade-off analysis, decision-making, and documentation.

## Prompt Engineering Guidelines

### Context is Critical

Always provide:
1. **Business context**: Industry, company size, growth stage
2. **Technical context**: Current stack, team expertise, existing systems
3. **Constraints**: Budget, timeline, regulatory requirements
4. **Priorities**: Which quality attributes matter most

### Ask for Trade-offs Explicitly

LLMs tend to provide balanced recommendations. To get useful trade-off analysis:
- Ask "What do we LOSE by choosing X?"
- Request "Devil's advocate" perspective
- Ask for worst-case scenarios

### Validate with Domain Experts

LLM suggestions need human verification, especially for:
- Domain-specific risks
- Organization-specific constraints
- Team capability assessments

---

## Option Generation Prompts

### Brainstorm Architecture Options

```
I need to design [system/feature description].

Context:
- Industry: [industry]
- Scale: [users/transactions/data volume]
- Team size: [number] engineers
- Current stack: [technologies]
- Timeline: [deadline]

Generate 5 distinct architectural approaches, ranging from simple to complex.
For each option:
1. Brief description (2-3 sentences)
2. Best suited for (when to choose)
3. Main trade-off

Focus on practical options, not theoretical ideals.
```

### Technology Selection Options

```
We need to select a [technology type, e.g., database, message queue, cache] for:

Use case: [description]
Scale requirements: [specific numbers]
Consistency requirements: [strong/eventual/doesn't matter]
Team expertise: [relevant skills]
Budget: [constraints]
Cloud environment: [AWS/GCP/Azure/on-prem]

List top 4 options with:
1. Technology name and category
2. Why it fits our use case
3. Main concern/trade-off
4. When NOT to use it

Include both well-known and emerging options appropriate for [year].
```

---

## Trade-off Analysis Prompts

### General Trade-off Analysis

```
Analyze trade-offs between [Option A] and [Option B] for [context/use case].

Consider these quality attributes:
- Performance
- Scalability
- Maintainability
- Security
- Cost (initial and operational)
- Team expertise required

Format as:

## Option A: [Name]
**What you gain:**
- [Benefit 1]
- [Benefit 2]

**What you sacrifice:**
- [Sacrifice 1]
- [Sacrifice 2]

**Best when:**
[Scenarios where A is clearly better]

## Option B: [Name]
[Same format]

## Trade-off Matrix
| Attribute | Option A | Option B | Winner |
|-----------|----------|----------|--------|

## Recommendation
Based on [context], recommend [option] because [reasons].
```

### Decision Matrix Generation

```
Create a weighted decision matrix for choosing between:
- Option A: [description]
- Option B: [description]
- Option C: [description]

Context: [business and technical context]

Constraints:
- [Constraint 1]
- [Constraint 2]

Business priorities (rank 1-5, 5 being highest):
- Time to market: [priority]
- Cost: [priority]
- Scalability: [priority]
- Maintainability: [priority]
- [Custom priority]: [priority]

Generate:
1. Evaluation criteria with recommended weights (justify weights)
2. Score each option (1-5) with brief rationale
3. Calculate weighted totals
4. Sensitivity analysis: what changes would flip the decision?
5. Final recommendation with confidence level
```

### Quality Attribute Trade-off Analysis

```
Analyze quality attribute trade-offs for [architectural decision].

Current system:
[Brief description of current state]

Proposed change:
[Description of proposed change]

For each quality attribute pair that may conflict:
1. Identify the trade-off (what improves, what degrades)
2. Quantify impact if possible (percentages, response times, etc.)
3. Assess if trade-off is acceptable for [context]
4. Suggest mitigations for negative impacts

Focus especially on:
- Performance vs Maintainability
- Security vs Usability
- Consistency vs Availability
- Flexibility vs Simplicity

Conclude with: Is this trade-off profile acceptable for a [type of system]?
```

---

## Build vs Buy Analysis Prompts

### Initial Assessment

```
Help me evaluate build vs buy for: [capability description]

Our context:
- Company: [size, stage, industry]
- Team: [size, expertise]
- Budget: [constraints]
- Timeline: [deadline]
- Strategic importance: [core/context/commodity]

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Questions to answer:
1. Is this capability core to competitive advantage? Why/why not?
2. What's the realistic build effort (include unknowns)?
3. What buy options exist? Name specific vendors/products.
4. What's the 3-year TCO comparison framework?
5. What's the key trade-off between build and buy here?

Be realistic about build complexity - include typical underestimation factors.
```

### Vendor Evaluation

```
Evaluate [Vendor A] vs [Vendor B] for [capability].

Our requirements:
[List requirements with priority]

For each vendor, assess:
1. Feature fit (% of requirements met)
2. Integration complexity with [our stack]
3. Pricing model and 3-year projection
4. Vendor stability and market position
5. Lock-in risk and exit strategy
6. Hidden costs (training, customization, support)

Create a comparison table and recommendation.
Include: What questions should we ask each vendor?
```

---

## Technical Debt Prompts

### Debt Assessment

```
Assess this technical debt and advise on the trade-off:

Code/System affected: [description]
Current state: [what's wrong]
How it happened: [deliberate/accidental, reason]

Impact:
- Developer time wasted: [estimate]
- Bug frequency: [history]
- Customer impact: [description]

Our situation:
- Upcoming deadline: [date] for [feature]
- Team capacity: [availability]
- Current debt load: [high/medium/low]

Analyze:
1. Classify using Fowler's Technical Debt Quadrant
2. Should we pay this debt now or accept it?
3. If accept: what's the trigger to revisit?
4. If pay: what's the incremental approach?
5. What's the cost of NOT addressing this in 6 months?
```

### Speed vs Quality Trade-off

```
Help me make a speed vs quality trade-off decision:

Feature needed: [description]
Deadline: [date and why it matters]

Options:
A) Ship fast with shortcuts: [specific shortcuts being considered]
B) Build properly: [what "properly" means here]
C) Reduce scope: [what could be cut]

Questions:
1. How real is this deadline? What if we miss it?
2. What's the true cost of each shortcut?
3. Will we actually fix this later? (Be honest about typical behavior)
4. Is there a creative Option D?

Include: A framework for when to accept vs reject speed trade-offs.
```

---

## ATAM-Style Prompts

### Scenario Generation

```
Generate quality attribute scenarios for [system description].

Business context:
- [Business driver 1]
- [Business driver 2]

System characteristics:
- [Characteristic 1]
- [Characteristic 2]

Generate 10 scenarios across these quality attributes:
- Performance
- Availability
- Security
- Modifiability
- Scalability

For each scenario, use this format:
**Scenario [N]: [Name]**
- Source: [Who/what triggers this]
- Stimulus: [The event]
- Artifact: [What is affected]
- Environment: [System state]
- Response: [What should happen]
- Response Measure: [How to verify]
- Priority: (Importance H/M/L, Difficulty H/M/L)

Focus on scenarios that reveal architectural trade-offs.
```

### Sensitivity Point Analysis

```
Analyze this architecture for sensitivity points:

[Architecture description or diagram]

Key quality attributes:
- [QA1]: Target [metric]
- [QA2]: Target [metric]
- [QA3]: Target [metric]

For each architectural element/decision:
1. Which quality attributes does it affect?
2. How sensitive is [QA] to changes in this element?
3. What would break if this element fails/degrades?

Identify:
- Single points of failure
- Bottleneck candidates
- High-sensitivity components

Present as a sensitivity matrix and highlight top 5 concerns.
```

### Risk Identification

```
Identify architectural risks for [system/decision]:

Context:
[Architecture description]

Constraints:
[List constraints]

Team:
[Team size and expertise]

Analyze risks in these categories:
1. Technical risks (can we build it?)
2. Operational risks (can we run it?)
3. Integration risks (will it work with X?)
4. Scale risks (will it handle growth?)
5. Security risks (what could go wrong?)
6. Organizational risks (team, skills, politics)

For each risk:
- Description
- Probability (H/M/L)
- Impact (H/M/L)
- Early warning signs
- Mitigation options

Group risks into themes and prioritize top 5 for immediate attention.
```

---

## Documentation Prompts

### ADR Generation

```
Generate an Architecture Decision Record for:

Decision: [What we're deciding]
Context: [Why we're making this decision now]

Options considered:
1. [Option A]: [Brief description]
2. [Option B]: [Brief description]
3. [Option C]: [Brief description]

Our choice: [Option X]

Generate a complete ADR with:
- Context (expanded)
- Decision drivers
- Options with pros/cons
- Decision outcome
- Trade-offs accepted (what we gain AND lose)
- Consequences (positive, negative, neutral)
- Risks and mitigations

Use a professional but concise tone. Focus on capturing the "why" not just the "what".
```

### Trade-off Communication for Stakeholders

```
Translate this technical trade-off decision for [audience: executives/product/operations]:

Technical decision:
[Description with technical terms]

Trade-offs:
[Technical trade-offs]

Rewrite for [audience] focusing on:
- Business impact (cost, timeline, risk)
- What changes for them
- What they need to approve/support
- Simple analogy if helpful

Format as a 1-page executive summary with:
- The Question (1 sentence)
- Options (simple comparison)
- Recommendation (with business rationale)
- Trade-offs (in business terms)
- Ask (what you need from them)
```

---

## Review and Validation Prompts

### Decision Review

```
Review this trade-off decision for blind spots:

Decision: [What was decided]
Context: [When and why]
Options considered: [List]
Chosen option: [Selection]
Stated trade-offs: [What we documented]

Act as a critical reviewer and identify:
1. Trade-offs we may have missed
2. Risks not adequately addressed
3. Assumptions that might not hold
4. Alternative options not considered
5. Questions we should have asked but didn't

Be constructively critical - help us make a better decision.
```

### Post-Implementation Review

```
Help me conduct a post-implementation review of this trade-off decision:

Original decision (date): [What we decided]
Predicted trade-offs: [What we expected]
Predicted risks: [What we anticipated]

Actual outcomes:
- [Outcome 1]
- [Outcome 2]

Analyze:
1. Did our predicted trade-offs materialize as expected?
2. Were there unexpected trade-offs?
3. Did our risk mitigations work?
4. What would we do differently?
5. What lessons should we document?

Format as a retrospective with actionable learnings.
```

---

## Chain of Thought Prompts

### Complex Decision Decomposition

```
I need to make a complex architecture decision. Walk me through it step by step.

Decision: [Description]
Context: [Background]
Constraints: [Limitations]

Use this thinking process:
1. First, clarify: What exactly are we deciding? What are we NOT deciding?
2. Stakeholder analysis: Who cares about this decision and why?
3. Option generation: What are ALL the options (including do nothing)?
4. Criteria identification: What matters for this decision?
5. Trade-off identification: Where do options conflict?
6. Risk assessment: What could go wrong with each option?
7. Recommendation: Given everything, what do you suggest and why?

Think out loud at each step. Identify where you're uncertain.
```

### Devil's Advocate

```
I'm leaning toward [Option X] for [decision].

Arguments for X:
[My reasons]

Now argue AGAINST this decision. Be a rigorous devil's advocate:
1. What are the strongest arguments for alternatives?
2. What am I not seeing or underweighting?
3. What could make this decision catastrophically wrong?
4. What assumptions am I making that might not hold?
5. Who would disagree with this and why might they be right?

Don't hold back - help me stress-test this decision.
```

---

## Prompt Chaining Examples

### Full Trade-off Analysis Session

```
Session structure (use in sequence):

PROMPT 1: "What decision do I need to make? Clarify the decision scope for [problem]."

PROMPT 2: "Generate options for [clarified decision]. Include at least one unconventional option."

PROMPT 3: "Create evaluation criteria for choosing between [options] in context of [constraints]."

PROMPT 4: "Analyze trade-offs between [shortlisted options] using [criteria]."

PROMPT 5: "Identify risks for [top option] and suggest mitigations."

PROMPT 6: "Generate an ADR documenting this decision including trade-offs."

PROMPT 7: "Review the ADR for blind spots and missing considerations."
```

---

## Common Mistakes to Avoid

### In Prompts

| Mistake | Better Approach |
|---------|-----------------|
| "What's the best database?" | Provide context, requirements, constraints |
| "Analyze trade-offs" | Specify which qualities matter for your context |
| Generic context | Include specific numbers, team details |
| Not asking for trade-offs | Explicitly request what you lose |
| Accepting first answer | Follow up with devil's advocate |

### In Using Responses

| Mistake | Better Approach |
|---------|-----------------|
| Taking LLM output as final | Validate with domain experts |
| Ignoring uncertainty | Ask LLM where it's uncertain |
| Not providing feedback | Iterate with corrections |
| Using for final decisions | Use for analysis, humans decide |

---

## Integration with Workflow

### When to Use LLM in Trade-off Analysis

| Phase | LLM Value | Caution |
|-------|-----------|---------|
| Option generation | High | May miss domain-specific options |
| Criteria identification | High | Validate weights with stakeholders |
| Trade-off identification | High | Verify with actual system data |
| Risk identification | Medium | Needs domain expert validation |
| Documentation | High | Review for accuracy |
| Decision making | Low | Humans should decide |

### Output Validation Checklist

Before using LLM trade-off analysis output:
- [ ] Verified technical accuracy with domain expert
- [ ] Confirmed numbers/estimates are realistic
- [ ] Checked for missing options specific to our context
- [ ] Validated risks against actual system knowledge
- [ ] Adjusted for team capabilities and organizational factors
