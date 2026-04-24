# LLM Prompts for ADR Writing

Effective prompts for using Large Language Models (Claude, GPT, etc.) to assist with Architecture Decision Record creation.

## When to Use LLMs for ADRs

| Task | LLM Helpful? | Notes |
|------|--------------|-------|
| Initial draft structure | Yes | Fast boilerplate generation |
| Brainstorming alternatives | Yes | Identifies options you might miss |
| Pros/cons analysis | Yes | Systematic evaluation |
| Consequence exploration | Yes | Thinks through implications |
| Improving clarity | Yes | Better writing, clearer explanations |
| Context gathering | Partially | Needs your domain input |
| Technical accuracy | Verify | May hallucinate specifics |
| Final decision | No | Requires human judgment |

## Ground Rules

1. **LLM output is a starting point**, not the final answer
2. **Verify technical claims** - LLMs may hallucinate
3. **Add team context** - LLM doesn't know your constraints
4. **Humans own decisions** - accountability matters
5. **Iterate and refine** - first output rarely perfect

---

## Prompts by Task

### 1. Generate Initial ADR Draft

**Basic Draft Prompt:**
```
I need to write an Architecture Decision Record (ADR) for the following decision:

Context:
- [Describe the situation/problem]
- [List key constraints]
- [Mention team/project context]

The decision we're leaning toward: [Your preferred option]
Alternatives we've considered: [List alternatives]

Please generate an ADR in MADR format with:
- Clear context and problem statement
- At least 3 alternatives with pros/cons
- Honest consequences (both positive and negative)
- Keep it to 1-2 pages

Use professional tone, avoid jargon without explanation.
```

**With Specific Template:**
```
Generate an ADR using Michael Nygard's format:
- Title
- Status (set to Proposed)
- Context
- Decision
- Consequences

Decision topic: [Your topic]
Background: [Relevant context]
Constraints: [Key constraints]
Preferred approach: [Your leaning]
```

### 2. Brainstorm Alternatives

**Discovery Prompt:**
```
I'm writing an ADR about [topic].

Current context:
- [Constraint 1]
- [Constraint 2]
- [Team size/expertise]
- [Budget/timeline]

What are 5-7 alternative approaches I should consider? For each, briefly explain:
1. What it is
2. When it's commonly used
3. One key advantage
4. One key disadvantage

Include both obvious choices and less conventional options I might not have considered.
```

**Comparison Matrix:**
```
For an ADR comparing [Option A], [Option B], and [Option C] for [purpose]:

Create a comparison matrix with these criteria:
- Performance
- Cost (initial and ongoing)
- Team learning curve
- Maintenance burden
- Scalability
- Vendor lock-in risk
- Community/ecosystem

Rate each option on a scale of 1-5 for each criterion and explain the ratings.
```

### 3. Analyze Consequences

**Consequence Exploration:**
```
I've decided to [decision] for [context].

Help me think through the consequences:

1. Immediate positive impacts
2. Long-term positive impacts
3. Immediate negative impacts / tradeoffs
4. Long-term risks
5. Neutral changes (neither good nor bad)
6. Impact on different stakeholders:
   - Development team
   - Operations team
   - End users
   - Business stakeholders

Be honest about downsides - I need realistic assessment, not sales pitch.
```

**Risk Analysis:**
```
For this architectural decision: [describe decision]

Identify potential risks:
1. Technical risks
2. Organizational risks
3. Business risks
4. Integration risks
5. Migration risks (if replacing something)

For each risk, suggest:
- Likelihood (High/Medium/Low)
- Impact (High/Medium/Low)
- Mitigation strategy
```

### 4. Improve Existing ADR

**Clarity Review:**
```
Review this ADR draft and suggest improvements:

[Paste your ADR]

Focus on:
1. Is the context clear to someone unfamiliar with the project?
2. Is the decision statement unambiguous?
3. Are consequences balanced (not just positive)?
4. Are alternatives fairly represented (not strawmanned)?
5. Is the language clear and jargon-free?

Provide specific rewrites for unclear sections.
```

**Gap Analysis:**
```
Review this ADR for completeness:

[Paste your ADR]

What's missing?
- Are all constraints mentioned?
- Are there alternatives we should have considered?
- Are there consequences we haven't addressed?
- Are there stakeholders we haven't considered?
- Should we reference any related decisions?

Suggest additions where appropriate.
```

### 5. Write Specific Sections

**Context Section:**
```
Help me write the Context section of an ADR.

Situation:
- [Describe what's happening]
- [Why we need to make a decision]
- [Key constraints and forces]

The context should:
- Be objective (facts, not opinions)
- Explain the forces at play
- Be understandable to someone joining the team
- Not exceed 3-4 paragraphs

Write in professional, clear prose.
```

**Alternatives Section:**
```
For this decision context: [describe context]

Write the Alternatives Considered section for these options:
1. [Option A]
2. [Option B]
3. [Option C]

For each, provide:
- Brief description
- 3 pros
- 3 cons
- Why it might be rejected

Be fair to all options - don't strawman the alternatives.
```

**Y-Statement:**
```
Convert this decision into a Y-statement format:

Context: [describe]
Decision: [what we chose]
Rejected alternatives: [what we didn't choose]
Benefits: [what we gain]
Tradeoffs: [what we accept]

Y-statement format:
"In the context of [X], facing [Y], we decided for [A] and against [B],
to achieve [C], accepting that [D]."

Make it one coherent sentence that captures the essence of the decision.
```

### 6. Technology-Specific ADRs

**Database Selection:**
```
Generate an ADR for database selection with these requirements:
- Use case: [describe application]
- Data model: [relational/document/graph/time-series]
- Scale: [expected data volume and queries]
- Team expertise: [current skills]
- Budget: [constraints]
- Compliance: [any requirements]

Compare at least 3 relevant database options.
Include migration considerations if replacing existing database.
```

**Framework Selection:**
```
Generate an ADR for selecting a [frontend/backend/mobile] framework:
- Project type: [describe]
- Team size: [number]
- Current tech stack: [list]
- Must integrate with: [systems]
- Performance requirements: [specifics]
- Timeline: [constraints]

Compare [Option A], [Option B], [Option C] with honest assessment.
```

**Cloud Architecture:**
```
Generate an ADR for [specific cloud decision]:
- Current infrastructure: [describe]
- Requirements: [list]
- Budget: [monthly/annual]
- Compliance: [requirements]
- Team DevOps expertise: [level]

Consider:
- Multi-cloud vs single cloud
- Managed vs self-hosted
- Vendor lock-in implications
- Cost at different scales
```

### 7. Migration and Deprecation

**Migration ADR:**
```
Generate an ADR for migrating from [Old System] to [New System]:

Current state:
- [What we have now]
- [Why it's problematic]

Target state:
- [What we want]
- [Expected benefits]

Include:
- Migration strategy options (big bang vs incremental)
- Risk assessment
- Rollback plan
- Success criteria
- Timeline considerations (without specific dates)
```

**Superseding ADR:**
```
Help me write an ADR that supersedes ADR-[XXX].

Original decision: [what was decided]
Why it needs to change: [new context/requirements]
New decision: [what we're deciding now]

The new ADR should:
- Reference the original ADR
- Explain what changed
- Not invalidate the original reasoning (it was right at the time)
- Clearly state the new direction
```

---

## Prompt Templates for Common Scenarios

### Microservices vs Monolith

```
Generate an ADR for architecture style decision:

Project: [describe]
Current state: [monolith/greenfield/etc]
Team size: [number]
Expected scale: [users/requests]
Time to market pressure: [high/medium/low]

Compare:
1. Monolith
2. Modular monolith
3. Microservices
4. Serverless

Focus on honest tradeoffs for our specific context.
```

### Authentication Strategy

```
Generate an ADR for authentication approach:

Application type: [web/mobile/API]
Users: [internal/external/both]
Compliance: [SOC2/HIPAA/GDPR/none]
SSO requirement: [yes/no]
MFA requirement: [yes/no]
Budget for auth services: [range]

Compare session-based, JWT, OAuth2/OIDC, and third-party providers.
```

### API Design

```
Generate an ADR for API design approach:

API purpose: [internal/public/partner]
Consumers: [describe]
Data complexity: [simple/nested/graph-like]
Real-time requirements: [yes/no]
Caching needs: [critical/nice-to-have/not needed]

Compare REST, GraphQL, gRPC with honest tradeoffs.
```

---

## Refinement Prompts

**Make It Shorter:**
```
This ADR is too long. Reduce it to 1-2 pages while keeping:
- Essential context
- Clear decision
- Key alternatives (can summarize)
- Critical consequences

Remove implementation details and keep focus on the decision.

[Paste ADR]
```

**Make It More Specific:**
```
This ADR is too vague. Make it more specific:

[Paste ADR]

Add:
- Specific technologies/versions
- Quantified requirements where possible
- Concrete examples
- Clear scope boundaries
```

**Add Missing Perspectives:**
```
Review this ADR from the perspective of:
- Operations team (deployment, monitoring, maintenance)
- Security team (vulnerabilities, compliance)
- Product team (user impact, feature implications)
- Finance (cost implications)

What concerns would each raise? Add to consequences section.

[Paste ADR]
```

---

## Quality Checklist Prompt

```
Review this ADR against this checklist and identify gaps:

[Paste ADR]

Checklist:
- [ ] Title is short and descriptive
- [ ] Status is clearly stated
- [ ] Date is included
- [ ] Deciders are listed
- [ ] Context explains the problem objectively
- [ ] Decision uses active voice ("We will...")
- [ ] At least 2 alternatives documented
- [ ] Pros/cons for each alternative
- [ ] Rejected alternatives explain why rejected
- [ ] Positive consequences listed
- [ ] Negative consequences listed honestly
- [ ] Related ADRs referenced
- [ ] Length is 1-2 pages

Mark each as PASS or FAIL with explanation.
```

---

## Anti-Patterns to Avoid

When prompting LLMs for ADRs, avoid:

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| "Make this sound good" | Hides real tradeoffs | "Be honest about downsides" |
| "Justify [decision]" | Confirms bias | "Fairly compare alternatives" |
| No context provided | Generic output | Provide specific constraints |
| Asking for time estimates | Unreliable | Ask for complexity assessment |
| One-shot generation | Misses nuances | Iterate with follow-ups |
| Skipping review | Errors propagate | Always verify output |

---

## Related Files

- [README.md](README.md) - Overview and when to use ADRs
- [checklist.md](checklist.md) - Step-by-step writing guide
- [examples.md](examples.md) - Real-world ADR examples
- [templates.md](templates.md) - Copy-paste templates
