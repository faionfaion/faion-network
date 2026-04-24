# LLM Prompts for Backlog & Roadmap Work

Prompts for using LLMs (Claude, GPT, Gemini) to assist with backlog grooming and roadmap planning.

---

## Important Guidelines

### What LLMs Excel At

- Thought clarification and structuring
- Gap analysis ("What'd I miss?")
- Risk and edge case identification
- Template filling and formatting
- Generating acceptance criteria
- Comparing prioritization options

### What LLMs Cannot Do

- Make final prioritization decisions (lacks business context)
- Understand true user pain (no customer relationships)
- Replace stakeholder negotiation
- Provide certainty where none exists

### Critical Warning

> LLMs produce polished text that can mask uncertainty. Mark AI-generated content as hypothesis, not fact. Always validate with real users and data.

---

## User Story Generation

### Convert Feature Idea to User Story

```
<task>
Convert this feature idea into a well-structured user story with acceptance criteria.
</task>

<context>
Product: [Product name]
Target user: [User segment]
</context>

<feature_idea>
[Paste the rough feature idea here]
</feature_idea>

<output_format>
## User Story
As a [user type], I want [action], so that [benefit].

## Acceptance Criteria
Given [precondition]
When [action]
Then [expected result]

## Additional Considerations
- [Edge cases]
- [Non-functional requirements]
</output_format>
```

### Refine Existing User Story

```
<task>
Review this user story and suggest improvements. Identify missing acceptance criteria, edge cases, and potential issues.
</task>

<user_story>
[Paste the existing user story]
</user_story>

<questions>
1. Are the acceptance criteria complete and testable?
2. What edge cases might be missing?
3. What assumptions need validation?
4. Are there dependency risks?
</questions>
```

---

## Gap Analysis Prompts

### Feature Completeness Check

```
<task>
Review this feature breakdown and identify what might be missing.
</task>

<feature>
Name: [Feature name]
Description: [Brief description]
</feature>

<current_breakdown>
[List current sub-features/tasks]
</current_breakdown>

<analysis_areas>
1. User flows - Are all paths covered?
2. Edge cases - What could go wrong?
3. Dependencies - What else is needed?
4. Non-functional - Performance, security, accessibility?
5. Rollback - What if we need to undo?
</analysis_areas>
```

### Identify Hidden Assumptions

```
<task>
Analyze this backlog item and surface hidden assumptions that should be validated.
</task>

<backlog_item>
[Paste backlog item details]
</backlog_item>

<output_format>
## Assumptions Found

| Assumption | Risk if Wrong | Validation Method |
|------------|---------------|-------------------|
| [Assumption] | [What happens] | [How to validate] |

## Recommended Actions
- [ ] [Action to validate assumption]
</output_format>
```

---

## Prioritization Assistance

### RICE Scoring Helper

```
<task>
Help me score this feature using the RICE framework. Ask clarifying questions if needed.
</task>

<feature>
[Feature description]
</feature>

<context>
Total active users: [Number]
Target segment: [Who benefits]
Competitive landscape: [Brief context]
</context>

<rice_guidance>
- Reach: How many users will this affect per quarter? (1-10 scale)
- Impact: How much will it improve their experience? (0.25-3 scale)
- Confidence: How certain are we about these estimates? (50-100%)
- Effort: How many person-months to complete? (0.5-6+)
</rice_guidance>

Ask me questions to determine accurate scores, then calculate the RICE score.
```

### Compare Prioritization Options

```
<task>
Compare these features and recommend prioritization order.
</task>

<features>
1. [Feature A]: [Brief description]
2. [Feature B]: [Brief description]
3. [Feature C]: [Brief description]
</features>

<criteria>
- Strategic alignment: [Current company priorities]
- User impact: [What matters most to users]
- Resource constraints: [Available capacity]
</criteria>

<output_format>
## Comparison Matrix

| Criterion | Feature A | Feature B | Feature C |
|-----------|-----------|-----------|-----------|
| [Criterion] | [Score] | [Score] | [Score] |

## Recommended Priority Order
1. [Feature] - Reason: [Why first]
2. [Feature] - Reason: [Why second]
3. [Feature] - Reason: [Why third]

## Trade-offs to Consider
- [Trade-off 1]
- [Trade-off 2]
</output_format>
```

---

## Roadmap Drafting

### Generate Now/Next/Later Roadmap

```
<task>
Organize these initiatives into a Now/Next/Later roadmap structure.
</task>

<initiatives>
[List all initiatives/features being considered]
</initiatives>

<constraints>
- Team size: [Number]
- Current quarter focus: [Theme/Goal]
- Blockers: [Known dependencies]
</constraints>

<output_format>
## NOW (This Month/Quarter)
Committed, in progress or starting immediately.
- [Initiative]: [Rationale]

## NEXT (Next Quarter)
High priority, planned but not started.
- [Initiative]: [Rationale]

## LATER (6-12 Months)
Important but timing uncertain.
- [Initiative]: [Rationale]

## NOT PLANNED
Explicitly deprioritized.
- [Initiative]: [Why not / When to revisit]
</output_format>
```

### Theme-Based Roadmap Structure

```
<task>
Organize these features into strategic themes for roadmap communication.
</task>

<features>
[List all features with brief descriptions]
</features>

<business_goals>
[Current quarter/year goals]
</business_goals>

<output_format>
## Theme: [Theme Name]
**Goal:** [What this theme achieves]
**Timeline:** [Quarter range]

Features:
- [Feature 1]: [How it supports theme]
- [Feature 2]: [How it supports theme]

[Repeat for each theme]

## Unthemed Features
- [Feature]: [Suggested theme or reason it doesn't fit]
</output_format>
```

---

## Grooming Session Prep

### Pre-Grooming Analysis

```
<task>
Prepare analysis for our upcoming backlog grooming session.
</task>

<new_items>
[List new backlog items added since last grooming]
</new_items>

<current_top_10>
[Current top 10 prioritized items]
</current_top_10>

<questions>
1. Which new items warrant discussion vs. quick drop?
2. Should any top 10 items be reprioritized?
3. What questions should we discuss as a team?
4. Are there any duplicate or overlapping items?
</questions>
```

### Post-Grooming Documentation

```
<task>
Format these grooming session notes into a structured summary.
</task>

<raw_notes>
[Paste messy meeting notes]
</raw_notes>

<output_format>
# Backlog Grooming: [Date]

## Decisions Made
| Item | Decision | Rationale |
|------|----------|-----------|

## Priority Changes
| Item | Old Priority | New Priority | Reason |

## Action Items
- [ ] [Action] - Owner: [Name]

## Items for Next Sprint
1. [Item with complexity]

## Parked/Dropped Items
- [Item]: [Reason]
</output_format>
```

---

## Risk Identification

### Backlog Item Risk Analysis

```
<task>
Identify risks for this backlog item and suggest mitigations.
</task>

<item>
[Backlog item details]
</item>

<output_format>
## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Technical: [Risk] | Low/Med/High | Low/Med/High | [Action] |
| User: [Risk] | Low/Med/High | Low/Med/High | [Action] |
| Business: [Risk] | Low/Med/High | Low/Med/High | [Action] |
| Dependency: [Risk] | Low/Med/High | Low/Med/High | [Action] |

## Highest Priority Risks
1. [Risk]: [Why critical and what to do]
</output_format>
```

### Roadmap Dependency Mapping

```
<task>
Analyze this roadmap for dependencies and potential blockers.
</task>

<roadmap>
[Paste roadmap with initiatives and timeline]
</roadmap>

<output_format>
## Dependency Map

| Initiative | Depends On | Dependency Type | Risk |
|------------|------------|-----------------|------|
| [Initiative] | [Dependency] | Technical/Resource/External | Low/Med/High |

## Critical Path
Items that block other work:
1. [Item]: Blocks [X items]

## Recommendations
- [Suggestion to reduce dependency risk]
</output_format>
```

---

## Stakeholder Communication

### Roadmap Change Announcement

```
<task>
Draft a stakeholder communication about this roadmap change.
</task>

<change>
What changed: [Description]
Why: [Reason for change]
Impact: [Who is affected]
</change>

<audience>
[Engineering / Sales / Marketing / Executives / Customers]
</audience>

<tone>
[Direct / Empathetic / Positive / Neutral]
</tone>

<output_format>
Subject: [Email subject line]

[Communication body - appropriate length for audience]

Key points:
- What changed
- Why it changed
- What it means for them
- Next steps/timeline
</output_format>
```

### Priority Decision Justification

```
<task>
Help me explain why we're prioritizing Feature A over Feature B to stakeholders.
</task>

<feature_a>
[Description of prioritized feature]
[RICE score or prioritization rationale]
</feature_a>

<feature_b>
[Description of deprioritized feature]
[Why it's valuable but not now]
</feature_b>

<audience>
[Who is asking for Feature B]
</audience>

<output_format>
## Decision: [Feature A] Before [Feature B]

### Why [Feature A] First
- [Reason with data]
- [Business justification]

### [Feature B] Status
- Not cancelled, deferred to [timeframe]
- What needs to happen for it to move up

### What We Considered
- [Show you understood their perspective]
</output_format>
```

---

## Acceptance Criteria Generation

### Generate AC from Requirements

```
<task>
Generate comprehensive acceptance criteria for this requirement.
</task>

<requirement>
[User story or feature requirement]
</requirement>

<output_format>
## Acceptance Criteria

### Happy Path
```gherkin
Given [precondition]
When [action]
Then [expected result]
```

### Edge Cases
```gherkin
Given [edge case condition]
When [action]
Then [expected handling]
```

### Error Handling
```gherkin
Given [error condition]
When [action]
Then [error is handled gracefully]
```

### Non-Functional
- Performance: [Criterion]
- Accessibility: [Criterion]
- Security: [Criterion]
</output_format>
```

---

## Refine and Thought (RaT) Prompting

Advanced technique for better LLM outputs on complex backlog work.

```
<task>
Use the Refine and Thought approach to analyze this feature request.
</task>

<step_1_refine>
First, extract and organize the key information from this input:
[Raw feature request or messy notes]
</step_1_refine>

<step_2_think>
Now analyze systematically:
1. Core user need
2. Proposed solution
3. Assumptions made
4. Gaps in information
5. Risks identified
</step_2_think>

<step_3_output>
Provide structured output:
- User story
- Acceptance criteria
- Open questions
- Recommended next steps
</step_3_output>
```

---

## Prompt Best Practices

### Use XML Tags for Structure

Claude and other LLMs handle structured prompts better:

```
<context>Project background</context>
<task>What you want</task>
<constraints>Limitations</constraints>
<output_format>Expected format</output_format>
```

### Be Explicit About Uncertainty

Ask the LLM to surface its own uncertainty:

```
After providing your analysis, rate your confidence:
- High: Well-supported by the information provided
- Medium: Reasonable inference but could be wrong
- Low: Speculation, needs validation
```

### Request Multiple Options

```
Provide 3 different approaches with trade-offs:
1. Conservative option
2. Balanced option
3. Aggressive option
```

### Chain of Thought for Complex Analysis

```
Think through this step by step:
1. First, identify [X]
2. Then, consider [Y]
3. Finally, recommend [Z]

Show your reasoning at each step.
```
