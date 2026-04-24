# ADR Writing Checklist

Step-by-step checklist for creating effective Architecture Decision Records.

## Phase 1: Pre-Decision Assessment

### 1.1 Determine ADR Necessity

- [ ] Is this decision architecturally significant?
- [ ] Does it affect system structure, NFRs, or cross-team boundaries?
- [ ] Will it be difficult or costly to reverse?
- [ ] Is there existing documentation covering this decision?
- [ ] Is this a temporary solution (PoC, experiment)?

**Decision Rule:** If 2+ of the first 3 are YES and last 2 are NO, write an ADR.

### 1.2 Identify Stakeholders

- [ ] Who will be affected by this decision?
- [ ] Who has relevant expertise to contribute?
- [ ] Who needs to approve this decision?
- [ ] Who should review the ADR?

### 1.3 Gather Context

- [ ] What problem are we solving?
- [ ] What are the business drivers?
- [ ] What are the technical constraints?
- [ ] What is the current state of the system?
- [ ] What is the timeline for this decision?

## Phase 2: Research and Analysis

### 2.1 Identify Alternatives

- [ ] Brainstorm at least 3 options
- [ ] Include "do nothing" as an option if applicable
- [ ] Consider build vs. buy options
- [ ] Research industry best practices
- [ ] Review similar decisions in other projects

### 2.2 Evaluate Each Alternative

For each option, assess:

- [ ] Technical feasibility
- [ ] Team skills and experience
- [ ] Cost (implementation, operation, maintenance)
- [ ] Risk (security, performance, reliability)
- [ ] Timeline impact
- [ ] Vendor lock-in potential
- [ ] Community support and maturity

### 2.3 Document Trade-offs

- [ ] Create comparison matrix
- [ ] Identify deal-breakers for each option
- [ ] Note quality attribute impacts (scalability, security, etc.)
- [ ] Consider long-term maintainability
- [ ] Assess integration with existing systems

## Phase 3: Writing the ADR

### 3.1 Title and Metadata

- [ ] Write clear, descriptive title
- [ ] Use format: `NNNN-title-with-dashes.md`
- [ ] Set initial status: `Proposed`
- [ ] Add date: `YYYY-MM-DD`
- [ ] List deciders/authors
- [ ] Link to related tickets/stories (optional)

### 3.2 Context Section

- [ ] Describe the problem clearly
- [ ] Explain why a decision is needed now
- [ ] Include relevant business context
- [ ] Note technical constraints
- [ ] Reference related ADRs if applicable
- [ ] Keep it concise (1-2 paragraphs)

### 3.3 Decision Drivers (MADR format)

- [ ] List key factors influencing the decision
- [ ] Prioritize drivers (must-have vs. nice-to-have)
- [ ] Include both functional and non-functional requirements
- [ ] Note team/organizational constraints

### 3.4 Considered Options Section

- [ ] List all evaluated options
- [ ] Provide brief description of each
- [ ] Use neutral language (no bias yet)
- [ ] Include rejected options for completeness

### 3.5 Decision Section

- [ ] State the chosen option clearly
- [ ] Explain the primary reason for the choice
- [ ] Use present tense: "We will use..." or "We decide..."
- [ ] Be specific about scope and boundaries

### 3.6 Consequences Section

Positive consequences:
- [ ] What becomes easier?
- [ ] What quality attributes improve?
- [ ] What problems are solved?

Negative consequences:
- [ ] What becomes harder?
- [ ] What trade-offs are we accepting?
- [ ] What risks are introduced?

Neutral consequences:
- [ ] What changes without clear positive/negative impact?
- [ ] What follow-up decisions are needed?

### 3.7 Alternatives Analysis (Detailed)

For each rejected option:
- [ ] Why was it not chosen?
- [ ] What were the deal-breakers?
- [ ] In what circumstances might it be reconsidered?

### 3.8 Links and References

- [ ] Link to related ADRs
- [ ] Reference external documentation
- [ ] Include relevant tickets/stories
- [ ] Add links to research materials

## Phase 4: Review and Approval

### 4.1 Self-Review

- [ ] Check spelling and grammar
- [ ] Verify technical accuracy
- [ ] Ensure all sections are complete
- [ ] Confirm decision is clearly stated
- [ ] Check links work correctly

### 4.2 Peer Review

- [ ] Share with identified reviewers
- [ ] Allow sufficient review time (2-5 days)
- [ ] Address all comments
- [ ] Document significant discussions
- [ ] Reach consensus or escalate

### 4.3 Formal Approval

- [ ] Get required approvals
- [ ] Update status: `Proposed` → `Accepted`
- [ ] Update date to approval date
- [ ] Merge PR (if using Git workflow)
- [ ] Announce decision to affected teams

## Phase 5: Post-Decision

### 5.1 Communication

- [ ] Announce decision in relevant channels
- [ ] Update architecture documentation
- [ ] Brief affected team members
- [ ] Add to onboarding materials

### 5.2 Implementation Tracking

- [ ] Create implementation tasks/tickets
- [ ] Link ADR to implementation work
- [ ] Monitor implementation progress
- [ ] Note deviations from plan

### 5.3 After-Action Review (1 month later)

- [ ] Did the decision achieve expected outcomes?
- [ ] Were there unexpected consequences?
- [ ] Are any updates needed to the ADR?
- [ ] Should the decision be revisited?

## Quick Checklists by Format

### Nygard Format (Minimal)

- [ ] Title with number
- [ ] Status
- [ ] Context (1-2 paragraphs)
- [ ] Decision (1-2 paragraphs)
- [ ] Consequences (positive and negative)

### MADR Format (Standard)

- [ ] Title with number
- [ ] Status
- [ ] Date
- [ ] Deciders
- [ ] Context and Problem Statement
- [ ] Decision Drivers
- [ ] Considered Options
- [ ] Decision Outcome
- [ ] Positive Consequences
- [ ] Negative Consequences
- [ ] Pros and Cons of Options

### Y-Statement Format (Ultra-Minimal)

- [ ] Context identified
- [ ] Requirement/concern specified
- [ ] Decision stated
- [ ] Alternatives noted
- [ ] Benefits explained
- [ ] Drawbacks accepted

## Red Flags Checklist

Things that indicate a poor ADR:

- [ ] No clear problem statement
- [ ] Only one option considered
- [ ] No consequences documented
- [ ] Decision rationale missing
- [ ] Too long (>2 pages)
- [ ] Too vague ("improve performance")
- [ ] No stakeholder input
- [ ] Written long after decision made
- [ ] Copied from another project without adaptation

## ADR Quality Scoring

Score your ADR (1-5 for each):

| Criterion | Score |
|-----------|-------|
| Problem clarity | /5 |
| Context completeness | /5 |
| Alternatives considered | /5 |
| Trade-offs documented | /5 |
| Decision clarity | /5 |
| Consequences identified | /5 |
| Actionable | /5 |

**Target:** 28/35 or higher for acceptance.
