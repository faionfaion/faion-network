# LLM Prompts for Design Docs

Effective prompts for using LLMs (Claude, GPT-4, Gemini) to assist with design document writing. These prompts help generate structure, analyze alternatives, identify gaps, and improve technical writing.

## Table of Contents

1. [Generating Design Doc Structure](#generating-design-doc-structure)
2. [Problem Analysis](#problem-analysis)
3. [Alternative Analysis](#alternative-analysis)
4. [Cross-Cutting Concerns](#cross-cutting-concerns)
5. [Risk Identification](#risk-identification)
6. [Technical Writing Improvement](#technical-writing-improvement)
7. [Review and Critique](#review-and-critique)
8. [Specific Formats](#specific-formats)
9. [Implementation Planning](#implementation-planning)
10. [Best Practices](#best-practices)

---

## Generating Design Doc Structure

### Initial Outline Generation

```
I need to write a design document for [feature/system]. Here's the context:

**Problem:** [Brief description of the problem]
**Constraints:** [Technical, business, or timeline constraints]
**Stakeholders:** [Who cares about this decision]

Generate a detailed outline for a Google-style design document including:
1. All major sections with subsection headers
2. Key questions to answer in each section
3. Suggested diagrams or artifacts to include
4. Potential reviewers to involve based on the scope

Format the outline as a markdown template I can fill in.
```

### Expand Bullet Points to Prose

```
I have these bullet points for the [section name] of my design doc:

[Your bullet points]

Expand these into well-structured prose paragraphs suitable for a technical design document. Maintain technical precision while improving readability. Use active voice and be concise.
```

### Generate Goals and Non-Goals

```
For a project that [brief description], generate:

**Goals (5-7):**
- Each should be specific and measurable
- Include success criteria where applicable

**Non-Goals (3-5):**
- Explicitly state what this project will NOT address
- Include common misconceptions to clarify

Format each as a clear, actionable statement.
```

---

## Problem Analysis

### Problem Statement Refinement

```
I'm trying to solve this problem: [Your initial problem description]

Help me refine this into a crisp problem statement by:
1. Identifying the core issue vs symptoms
2. Quantifying the impact where possible
3. Clarifying who is affected and how
4. Distinguishing facts from assumptions

Then provide a 2-3 sentence problem statement I can use in my design doc.
```

### Current State Analysis

```
I'm documenting the current state before proposing changes. Here's what I know:

[Current system/process description]

Help me analyze this by:
1. Identifying pain points and inefficiencies
2. Noting technical debt or limitations
3. Highlighting what's working well (to preserve)
4. Quantifying issues where possible with placeholder metrics

Structure this as a "Current State" section for my design doc.
```

### Stakeholder Impact Analysis

```
For this proposed change: [Brief description]

These stakeholders are involved:
- [Stakeholder 1]: [Their role/interest]
- [Stakeholder 2]: [Their role/interest]

For each stakeholder, analyze:
1. How they'll be affected (positive/negative)
2. What concerns they might raise
3. What they need to approve/support the change
4. Communication approach for each

Format as a stakeholder analysis table.
```

---

## Alternative Analysis

### Generate Alternatives

```
I'm considering this approach for [problem]: [Your proposed solution]

Generate 3-4 alternative approaches including:
1. A simpler/minimal approach
2. A more comprehensive approach
3. A completely different paradigm
4. "Do nothing" or status quo

For each alternative, briefly describe the approach, its key characteristics, and when it might be preferred.
```

### Pros/Cons Analysis

```
Compare these approaches for [problem]:

**Option A:** [Description]
**Option B:** [Description]
**Option C:** [Description]

For each option, provide:
- 3-5 Pros (benefits, advantages)
- 3-5 Cons (drawbacks, risks, costs)
- Best suited for (scenarios)
- Deal-breakers (conditions where this fails)

Then recommend which to choose given [your specific constraints].
```

### Decision Matrix

```
Help me create a decision matrix for these options: [List options]

Using these criteria (with weights):
- [Criterion 1] (weight: [1-5])
- [Criterion 2] (weight: [1-5])
- [Criterion 3] (weight: [1-5])

Score each option 1-5 on each criterion and calculate weighted totals. Format as a markdown table with analysis.
```

### Why Not Chosen Rationale

```
I chose [Option A] over [Option B] for [project].

Help me write a clear "Why not chosen" explanation for Option B that:
1. Acknowledges its merits
2. Explains specific reasons for rejection
3. References our constraints/context
4. Avoids being dismissive

Keep it to 2-3 sentences, professional tone.
```

---

## Cross-Cutting Concerns

### Security Analysis

```
For this design: [Brief description of system/feature]

Analyze security considerations:
1. **Authentication:** How users/services are verified
2. **Authorization:** How permissions are controlled
3. **Data protection:** Encryption, PII handling
4. **Input validation:** Attack surface areas
5. **Audit:** What should be logged
6. **Compliance:** Relevant regulations (GDPR, SOC2, etc.)

For each area, identify risks and propose mitigations. Flag any items needing security team review.
```

### Scalability Analysis

```
This system needs to handle:
- Current load: [X] requests/day
- Expected growth: [Y]% per [timeframe]
- Peak multiplier: [Z]x normal

For this design: [Brief description]

Analyze:
1. Potential bottlenecks at scale
2. Scaling strategy (horizontal vs vertical)
3. Data growth implications
4. Cost implications of scaling
5. When we'd need to re-architect

Provide specific recommendations.
```

### Reliability Analysis

```
For this system: [Description]

With target SLA: [X]% availability

Analyze:
1. **Failure modes:** What can go wrong?
2. **Blast radius:** What's affected by each failure?
3. **Detection:** How will we know something failed?
4. **Recovery:** How do we restore service?
5. **Prevention:** How do we prevent each failure?

Create a failure modes table with severity ratings.
```

### Comprehensive Cross-Cutting Review

```
Review this design for cross-cutting concerns:

[Paste your design section]

Check for gaps in:
- [ ] Security (auth, encryption, input validation)
- [ ] Privacy (PII, retention, consent)
- [ ] Scalability (load, growth, bottlenecks)
- [ ] Reliability (failures, recovery, redundancy)
- [ ] Observability (logging, metrics, tracing)
- [ ] Performance (latency, throughput, efficiency)
- [ ] Accessibility (if applicable)
- [ ] Internationalization (if applicable)

For each gap found, suggest what to add to the design.
```

---

## Risk Identification

### Risk Brainstorming

```
For this project: [Description]

Brainstorm risks across these categories:
1. **Technical:** Implementation challenges, dependencies
2. **Schedule:** Timeline threats, blockers
3. **Resource:** Team, budget, tooling
4. **External:** Third parties, market, regulations
5. **Adoption:** User acceptance, migration

For each risk, estimate:
- Likelihood: High/Medium/Low
- Impact: High/Medium/Low
- Detection difficulty: Easy/Moderate/Hard

Prioritize by risk score (likelihood x impact).
```

### Risk Mitigation Strategies

```
For this risk: [Risk description]

Generate mitigation strategies:
1. **Prevention:** How to stop it from happening
2. **Detection:** How to know early if it's happening
3. **Response:** What to do if it happens
4. **Recovery:** How to get back to normal

Recommend the most practical approach given [constraints].
```

### Pre-mortem Analysis

```
Imagine this project has failed 6 months from now.

Project: [Description]
Timeline: [Duration]
Team: [Size/composition]

Write a post-mortem from the future explaining:
1. What went wrong
2. Warning signs we missed
3. What we should have done differently

Use this to identify preventive actions for the design doc.
```

---

## Technical Writing Improvement

### Clarity Improvement

```
Rewrite this section for clarity:

[Your text]

Guidelines:
- Use active voice
- Shorter sentences (max 25 words)
- One idea per paragraph
- Define jargon on first use
- Remove hedge words (might, possibly, somewhat)
```

### Technical Precision

```
Review this technical description for precision:

[Your text]

Check for:
- Vague quantities (make specific)
- Ambiguous pronouns (clarify references)
- Missing units (add where needed)
- Undefined terms (flag or define)
- Unsupported claims (note what needs evidence)

Suggest specific improvements.
```

### Executive Summary

```
Write an executive summary of this design doc:

[Paste full design doc or key sections]

The summary should:
- Be 3-5 sentences
- State the problem and solution
- Highlight key benefits
- Note major risks or tradeoffs
- Be understandable by non-technical stakeholders
```

### Diagram Description

```
I have this diagram: [Describe your diagram or paste ASCII version]

Write alt-text and a prose description that:
1. Explains what the diagram shows
2. Walks through the key flows/relationships
3. Highlights important details
4. Could substitute for the diagram if it didn't load
```

---

## Review and Critique

### Design Review

```
Act as a senior engineer reviewing this design doc:

[Paste design doc]

Provide feedback on:
1. **Completeness:** What's missing?
2. **Clarity:** What's confusing?
3. **Correctness:** Any technical errors?
4. **Feasibility:** What might not work in practice?
5. **Alternatives:** What options weren't considered?

Be constructive but thorough. Prioritize feedback by importance.
```

### Gap Analysis

```
Review this design doc for gaps:

[Paste design doc]

Check for missing:
- [ ] Non-goals section
- [ ] Alternatives analysis
- [ ] Security considerations
- [ ] Rollback plan
- [ ] Success metrics
- [ ] Timeline/milestones
- [ ] Open questions
- [ ] Dependencies

For each gap, explain why it matters and suggest what to add.
```

### Devil's Advocate

```
Take a devil's advocate position on this design:

[Paste design doc or key sections]

Challenge:
1. The stated assumptions
2. The chosen approach
3. The claimed benefits
4. The risk mitigations
5. The timeline estimates

Raise objections that a skeptical reviewer might have. Be specific.
```

### Question Generation

```
Generate questions that reviewers might ask about this design:

[Paste design doc]

Include questions from perspectives of:
- Security team
- SRE/Operations
- Product manager
- Other engineers
- Finance/business stakeholders

Categorize by difficulty to answer (easy, medium, hard).
```

---

## Specific Formats

### Amazon 6-Pager Narrative

```
Convert these bullet points into Amazon 6-pager narrative prose:

[Your bullet points]

Requirements:
- No bullet points, only paragraphs
- Professional but engaging tone
- Data-driven where possible
- Clear logical flow
- Approximately [X] words
```

### DIBB Framework

```
Help me structure this initiative using Spotify's DIBB framework:

**Initiative:** [Description]
**Context:** [Background]

Generate:
1. **Data:** 3-5 objective facts/metrics
2. **Insight:** Key learnings from the data
3. **Belief:** Hypothesis based on insights
4. **Bet:** Proposed initiative to test the belief

Include placeholder metrics I should fill in.
```

### ADR Format

```
Convert this design decision into an ADR:

**Decision:** [What we decided]
**Context:** [Why we had to decide]
**Options considered:** [What we evaluated]

Format as an Architecture Decision Record with:
- Title, Date, Status
- Context (problem/forces)
- Decision (what and why)
- Consequences (positive, negative, neutral)
- Alternatives considered
```

### RFC Metadata

```
Generate RFC metadata and sections for:

**Title:** [RFC title]
**Author:** [Your name]
**Problem:** [Brief problem description]

Include:
- Standard RFC header fields
- Summary section
- Motivation section
- Outline for detailed design
- Standard sections for alternatives, security, timeline
```

---

## Implementation Planning

### Milestone Breakdown

```
Break this project into milestones:

**Project:** [Description]
**Scope:** [Key deliverables]
**Constraints:** [Timeline, resources, dependencies]

For each milestone:
- Name and description
- Deliverables
- Success criteria
- Dependencies on other milestones
- Key risks

Suggest 3-5 milestones with logical progression.
```

### Rollout Strategy

```
Design a rollout strategy for:

**Feature:** [Description]
**Risk level:** [Low/Medium/High]
**User base:** [Size and segments]

Include:
1. Feature flag strategy
2. Percentage rollout stages
3. Success metrics per stage
4. Rollback criteria and procedure
5. Communication plan
```

### Migration Plan

```
Create a migration plan from:
**Current state:** [Old system/approach]
**Target state:** [New system/approach]
**Data/users affected:** [Scope]

Include:
1. Pre-migration steps
2. Migration phases
3. Rollback plan at each phase
4. Data validation approach
5. Backward compatibility period
6. Deprecation timeline
```

---

## Best Practices

### Effective Prompt Patterns

1. **Context first:** Always provide background before asking
2. **Specific constraints:** State your limitations explicitly
3. **Format requests:** Ask for specific output formats (table, prose, bullets)
4. **Iterative refinement:** Start broad, then narrow down
5. **Examples help:** Provide examples of what you want

### When LLMs Work Well

| Task | Why It Works |
|------|--------------|
| Structure generation | Pattern matching from training |
| Alternative brainstorming | Broad knowledge base |
| Prose improvement | Strong language model |
| Checklist generation | Aggregates best practices |
| Question generation | Simulates perspectives |

### When LLMs Struggle

| Task | Why It's Hard | Mitigation |
|------|---------------|------------|
| Context-specific decisions | Lacks your knowledge | Provide detailed context |
| Accurate technical details | May hallucinate | Verify all claims |
| Trade-off evaluation | Can't weigh your values | Make decisions yourself |
| Political navigation | No org awareness | Add constraints explicitly |
| Novel architectures | Limited to training data | Use as brainstorming only |

### Workflow Integration

1. **Start with human thinking:** Define the problem yourself
2. **Use LLM for structure:** Generate outline and sections
3. **Fill in with expertise:** Add your specific knowledge
4. **LLM for refinement:** Improve prose and clarity
5. **Human final review:** Verify accuracy and completeness

### Quality Checks

After using LLM assistance, always:
- [ ] Verify technical claims
- [ ] Check links and references
- [ ] Confirm numbers and metrics
- [ ] Ensure alignment with company standards
- [ ] Have human review for accuracy
- [ ] Test any generated code or configs

---

## Quick Reference Prompts

### For Starting a New Design Doc

```
I need to write a design doc for [feature]. Help me:
1. Generate an outline
2. Identify key questions to answer
3. List stakeholders to involve
4. Suggest diagrams to create
```

### For Getting Unstuck

```
I'm stuck on the [section] of my design doc for [feature].
Current draft: [paste what you have]
Help me: [expand/clarify/restructure/find gaps]
```

### For Final Review

```
Review this design doc for completeness and quality:
[Paste doc]
Provide: gaps, unclear sections, missing considerations, improvement suggestions.
```

---

*For design doc templates, see [templates.md](templates.md). For real examples, see [examples.md](examples.md).*
