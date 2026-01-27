# LLM Prompts for Design Documents

Effective prompts for using LLMs (Claude, GPT-4, Gemini) to assist with writing design documents, RFCs, and architecture decision records.

---

## Prompt Categories

| Category | Best Use Cases | LLM Effectiveness |
|----------|----------------|-------------------|
| [Structure Generation](#structure-generation) | Creating outlines, organizing sections | High |
| [Alternative Analysis](#alternative-analysis) | Brainstorming options, trade-offs | High |
| [Risk Identification](#risk-identification) | Finding edge cases, failure modes | Medium-High |
| [Writing Refinement](#writing-refinement) | Improving clarity, fixing prose | High |
| [Technical Review](#technical-review) | Checking consistency, completeness | Medium |
| [Question Generation](#question-generation) | Identifying gaps, review prep | High |

---

## Best Practices for LLM-Assisted Writing

### Do

1. **Provide context first** - Share system overview, constraints, existing architecture
2. **Work in sections** - Generate one section at a time, not entire documents
3. **Validate technically** - Every technical claim needs human verification
4. **Iterate** - Use LLM output as first draft, then refine
5. **Be specific** - Detailed prompts produce better outputs

### Don't

1. **Don't trust organizational context** - LLMs don't know your team dynamics
2. **Don't skip review** - LLM-generated content needs human review
3. **Don't use raw output** - Always edit for your team's voice and style
4. **Don't rely on technical accuracy** - Verify all technical details
5. **Don't generate entire documents at once** - Quality drops with length

---

## Structure Generation

### Generate Design Doc Outline

```
You are helping me write a design document for [PROJECT/FEATURE NAME].

Context:
- Current system: [brief description of existing architecture]
- Problem: [what we're trying to solve]
- Constraints: [technical, business, or time constraints]

Generate a detailed outline for a Google-style design document. Include:
1. All major sections with subsection headers
2. 2-3 bullet points per section indicating what content belongs there
3. Suggestions for diagrams or tables that would be helpful

Focus on sections most relevant to this specific problem. Don't include generic sections that don't apply.
```

### Generate RFC Structure

```
I need to write an RFC for [PROPOSED CHANGE].

Background:
- Current state: [how things work today]
- Proposed change: [high-level description]
- Scope: [team-only / cross-team / company-wide]
- Affected systems: [list of systems]

Create an RFC outline using the Uber/Stripe style. Include:
1. All required sections for this scope level
2. Placeholder questions I should answer in each section
3. Suggested approvers based on affected systems

Indicate which sections need the most detail for this type of change.
```

### Generate ADR Structure

```
I need to record an architectural decision.

Decision: [what was decided]
Context: [why this decision was needed]
Options considered: [list 2-3 options]

Generate an ADR outline following the Spotify format. Include:
1. All standard ADR sections
2. Prompting questions for each section
3. Suggestions for related decisions to reference
```

---

## Alternative Analysis

### Brainstorm Alternatives

```
I'm designing [FEATURE/SYSTEM] and need to explore alternatives.

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Constraints:
- [Constraint 1]
- [Constraint 2]

Currently considering: [brief description of current approach]

Generate 4-5 alternative approaches I should consider. For each:
1. Brief description (2-3 sentences)
2. Key advantages
3. Key disadvantages
4. When this approach works best

Include at least one "do nothing" or "minimal viable" option.
```

### Analyze Trade-offs

```
I'm comparing these approaches for [PROBLEM]:

Option A: [description]
Option B: [description]
Option C: [description]

Evaluation criteria:
- [Criterion 1, e.g., performance]
- [Criterion 2, e.g., maintainability]
- [Criterion 3, e.g., cost]
- [Criterion 4, e.g., time to implement]

Create a comparison matrix with:
1. Rating for each option on each criterion (high/medium/low)
2. Key trade-offs between top options
3. Scenarios where each option is the best choice
4. Questions I should answer to make this decision
```

### Strengthen "Why Not Chosen"

```
In my design doc, I'm recommending [CHOSEN APPROACH] over [REJECTED ALTERNATIVE].

Chosen approach advantages:
- [Advantage 1]
- [Advantage 2]

Help me strengthen my "why not chosen" explanation for the rejected alternative. I need to:
1. Acknowledge its genuine strengths
2. Explain specific reasons it doesn't fit our context
3. Avoid strawman arguments
4. Sound fair to a reviewer who might prefer the alternative

The goal is to show I seriously considered it but have good reasons for my choice.
```

---

## Risk Identification

### Find Edge Cases

```
I'm designing [FEATURE/SYSTEM] with this approach:

[Brief description of design]

Help me identify edge cases and failure modes I might have missed. Consider:
1. Input validation edge cases
2. Concurrency and race conditions
3. Failure modes of dependencies
4. Scale-related issues
5. Data consistency problems
6. Security edge cases

For each issue found, suggest a brief mitigation approach.
```

### Security Review Prep

```
Review this design from a security perspective:

[Paste relevant design section]

Identify potential security concerns in these categories:
1. Authentication and authorization gaps
2. Data exposure risks
3. Input validation issues
4. Injection vulnerabilities
5. Cryptographic weaknesses
6. Audit and logging gaps

For each concern, rate severity (high/medium/low) and suggest mitigation.
```

### Scalability Analysis

```
This system is designed for [CURRENT SCALE]:

[Paste design description]

Expected growth: [growth projections]

Identify potential scalability bottlenecks:
1. Database bottlenecks
2. Network bottlenecks
3. Compute bottlenecks
4. Storage bottlenecks
5. Third-party service limits

For each, suggest:
- At what scale it becomes a problem
- Warning signs to monitor
- Mitigation approaches
```

---

## Writing Refinement

### Improve Clarity

```
Rewrite this design doc section to be clearer and more concise:

[Paste section]

Goals:
1. Remove jargon or define it
2. Use active voice
3. Make each sentence do one thing
4. Ensure a new team member could understand it
5. Keep technical accuracy

Return the improved version with brief notes on what was changed and why.
```

### Fix Passive Voice

```
Rewrite these sentences using active voice. Be clear about who or what performs each action:

[Paste sentences]

For design docs, it's critical that readers know exactly what component/service/team is responsible for each action.
```

### Write Executive Summary

```
Based on this design document content, write a 2-paragraph executive summary:

[Paste key sections or full doc]

The summary should:
1. Explain the problem and solution in non-technical terms
2. Highlight key benefits and any significant risks
3. State what decision or action is needed
4. Be understandable by a non-engineer stakeholder
```

### Convert to Amazon Narrative Style

```
Convert these bullet points into narrative prose for an Amazon 6-pager:

[Paste bullet points]

Requirements:
1. No bullet points - full sentences and paragraphs only
2. Each paragraph should flow logically to the next
3. Data should be woven into the narrative, not presented as lists
4. Write as if explaining to someone unfamiliar with the topic
5. Every word should add value - no fluff
```

---

## Technical Review

### Check Consistency

```
Review this design document for internal consistency:

[Paste document]

Check for:
1. Terminology used consistently
2. Numbers/metrics that match between sections
3. Promises in goals that are addressed in design
4. Dependencies mentioned but not detailed
5. Contradictions between sections

List any inconsistencies found with specific locations.
```

### Completeness Check

```
Review this [DOCUMENT TYPE: design doc/RFC/ADR] for completeness:

[Paste document]

Standard sections for this document type:
[List expected sections]

Check:
1. Are all standard sections present?
2. Are any sections too thin for the document's scope?
3. Are there obvious gaps in the design?
4. Are all goals addressed in the design?
5. Are all open questions captured?

List missing or incomplete elements.
```

### API Review

```
Review this API design for issues:

[Paste API specification]

Check for:
1. Consistency in naming conventions
2. Appropriate HTTP methods for operations
3. Error response handling
4. Pagination for list endpoints
5. Versioning strategy
6. Authentication requirements
7. Rate limiting considerations

Suggest improvements for any issues found.
```

---

## Question Generation

### Prepare for Review Meeting

```
I'm about to submit this design doc for review:

[Paste document or summary]

Generate 10-15 questions reviewers are likely to ask. Categorize them:
1. Clarification questions (things that might be unclear)
2. Challenge questions (things reviewers might disagree with)
3. Scope questions (what about X?)
4. Risk questions (what if Y fails?)
5. Alternative questions (why not Z?)

For each question, draft a brief answer I can prepare.
```

### Generate Open Questions Section

```
Based on this design, what questions should be listed as "open questions"?

[Paste design summary]

Generate 5-7 open questions that:
1. Are genuinely unresolved (not rhetorical)
2. Could reasonably be answered during review
3. Might impact the implementation approach
4. Show appropriate uncertainty rather than false confidence

For each, suggest who might be the right person to answer it.
```

### Identify Stakeholder Concerns

```
This design affects these teams/systems:
- [Team/System 1]: [how affected]
- [Team/System 2]: [how affected]
- [Team/System 3]: [how affected]

For each stakeholder, generate:
1. Their likely primary concern
2. Questions they'll probably ask
3. How to address their concerns in the design doc

Help me anticipate and proactively address objections.
```

---

## Document-Specific Prompts

### Generate Amazon PR-FAQ

```
I'm using Amazon's Working Backwards process for [PRODUCT/FEATURE].

Target customer: [description]
Problem: [customer pain point]
Solution: [high-level solution]
Key benefit: [main value proposition]

Generate a PR-FAQ including:
1. Press release (1 page, narrative format)
   - Opening paragraph with announcement
   - Customer quote about the problem
   - Solution description
   - Executive quote about strategy
   - Availability and pricing

2. Customer FAQ (5-7 questions)
   - What is it?
   - Who is it for?
   - How much does it cost?
   - How is it different from [competitor]?

3. Internal FAQ (5-7 questions)
   - Why are we building this?
   - What are the risks?
   - What does success look like?
```

### Generate Rollout Plan

```
I need a rollout plan for this change:

[Paste design summary]

Risk level: [low/medium/high]
Affected users: [scope]
Rollback complexity: [easy/medium/hard]

Generate a phased rollout plan including:
1. Phases with scope and success criteria
2. Metrics to monitor at each phase
3. Rollback triggers and process
4. Communication plan for each phase
5. Timeline (relative, not absolute dates)
```

### Generate SLA Section

```
I'm designing a new service with these characteristics:

- Type: [API/data pipeline/real-time/batch]
- Criticality: [critical path/important/nice-to-have]
- Upstream dependencies: [list]
- Downstream dependents: [list]
- Expected traffic: [RPS/daily volume]

Generate appropriate SLA targets for:
1. Availability
2. Latency (p50, p95, p99)
3. Throughput
4. Error rate
5. Data freshness (if applicable)

Include how each should be measured and why these targets are appropriate.
```

---

## Iteration Prompts

### Improve Based on Feedback

```
I received this feedback on my design doc:

[Paste feedback]

Help me:
1. Understand the core concern behind each piece of feedback
2. Draft updated sections that address the feedback
3. Identify if any feedback contradicts other feedback
4. Suggest follow-up questions if feedback is unclear
```

### Strengthen Weak Sections

```
A reviewer said this section of my design doc is weak:

[Paste section]

Their specific concern: [what they said]

Help me strengthen this section by:
1. Adding more detail where appropriate
2. Addressing the specific concern
3. Anticipating follow-up questions
4. Maintaining the section's appropriate length (don't over-engineer)
```

### Simplify Complex Section

```
This section of my design doc is too complex:

[Paste section]

Help me simplify it:
1. Break down into smaller, digestible pieces
2. Add a summary at the start
3. Use a diagram or table where helpful
4. Remove unnecessary technical detail
5. Define or link to jargon

Keep the technical accuracy while improving accessibility.
```

---

## Prompt Engineering Tips

### For Better Outputs

1. **Include examples** - Show the format you want
2. **Specify length** - "2-3 paragraphs" or "5-7 bullet points"
3. **Define audience** - "for engineers unfamiliar with this system"
4. **State constraints** - "must fit in 1 page" or "no jargon"
5. **Request structure** - "use headers" or "create a table"

### For Technical Accuracy

1. **Provide context** - Include relevant system details
2. **Ask for caveats** - "note any assumptions you're making"
3. **Request verification points** - "what should I verify?"
4. **Iterate** - Fix errors and regenerate

### For Consistency

1. **Use the same prompt structure** across sections
2. **Reference previous outputs** - "consistent with the overview I generated earlier"
3. **Define terminology** - "use 'service' not 'microservice'"
4. **Specify style** - "match the tone of this example"

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| "Write my entire design doc" | Low quality, misses context | Generate section by section |
| "Make it sound professional" | Vague, often worse output | Specify: "use active voice, define jargon" |
| No context provided | Generic, unhelpful output | Always include system/problem context |
| Trusting technical claims | LLMs make errors | Verify every technical statement |
| Copy-paste without editing | Wrong voice, may have errors | Always edit and adapt |
| Using for sensitive decisions | LLM lacks context | Use for brainstorming, decide yourself |

---

## Example: Full Design Doc Workflow

### Step 1: Generate Outline

```
Create an outline for a design doc about adding rate limiting to our API gateway.

Context:
- Current state: No rate limiting, occasional traffic spikes cause issues
- Proposed: Token bucket rate limiting at gateway level
- Constraints: Must not add >5ms latency, needs per-tenant limits

Use Google-style design doc format.
```

### Step 2: Generate Each Section

```
Now write the "Alternatives Considered" section for the rate limiting design doc.

Options to analyze:
1. Token bucket at gateway (proposed)
2. Leaky bucket algorithm
3. Fixed window counter
4. Application-level rate limiting
5. Do nothing (accept current state)

For each, provide pros, cons, and clear "why not chosen" for rejected options.
```

### Step 3: Refine Specific Sections

```
Improve the clarity of this "Design" section:

[Paste generated section]

Make it understandable to an engineer who doesn't know our system.
```

### Step 4: Generate Questions for Review

```
What questions should I expect in review for this rate limiting design doc?

[Paste summary of design]

Focus on questions about:
- The algorithm choice
- Performance impact
- Tenant fairness
- Failure modes
```

### Step 5: Final Polish

```
Review this complete design doc for:
1. Consistency between sections
2. Any gaps or missing information
3. Clarity and readability
4. Technical accuracy concerns to verify

[Paste full document]
```

---

*LLM Prompts | Design Docs at Big Tech | v2.0*
