# ADR Writing Checklist

A step-by-step guide for creating effective Architecture Decision Records.

## Pre-Writing Checklist

### 1. Determine If You Need an ADR

- [ ] Is this decision architecturally significant?
- [ ] Will this decision be hard to reverse later?
- [ ] Does it affect multiple components or teams?
- [ ] Will future developers need to understand why this choice was made?
- [ ] Is the cost of change high if we get it wrong?

**If most answers are "No"**: Consider documenting in code comments, commit messages, or a simpler format.

### 2. Gather Context

- [ ] Identify the problem or requirement driving this decision
- [ ] List all constraints (technical, business, time, budget, team)
- [ ] Identify stakeholders who should be involved
- [ ] Review any existing ADRs that might be related
- [ ] Check if similar decisions exist in other projects/teams

### 3. Research Alternatives

- [ ] Brainstorm at least 2-3 alternative solutions
- [ ] Research each alternative (documentation, case studies, benchmarks)
- [ ] Create a comparison matrix of alternatives
- [ ] Identify pros and cons for each option
- [ ] Consider "do nothing" as an alternative

## Writing Checklist

### 4. Draft the ADR

#### Title Section
- [ ] Use sequential numbering (0001, 0002...)
- [ ] Write a short, descriptive title (noun phrase)
- [ ] Include date of creation
- [ ] List deciders/authors

#### Context Section
- [ ] Describe the current situation objectively
- [ ] State the problem clearly
- [ ] List all forces at play (technical, business, political)
- [ ] Use value-neutral language (facts, not opinions)
- [ ] Include relevant constraints

#### Decision Section
- [ ] State the decision clearly using active voice ("We will...")
- [ ] Be specific about what is being done
- [ ] Keep it to one decision per ADR
- [ ] Include scope (what systems/components affected)

#### Alternatives Section
- [ ] Document all alternatives considered
- [ ] Include pros and cons for each
- [ ] Explain why each was rejected
- [ ] Be fair to rejected alternatives (don't strawman)

#### Consequences Section
- [ ] List positive consequences
- [ ] List negative consequences (be honest!)
- [ ] List neutral implications
- [ ] Identify risks and mitigation strategies
- [ ] Consider short-term vs. long-term impacts

### 5. Quality Checks

- [ ] ADR is 1-2 pages maximum
- [ ] Language is clear and jargon-free (or jargon is explained)
- [ ] A new team member could understand it
- [ ] All claims are supported (links to benchmarks, docs, etc.)
- [ ] No implementation details (unless necessary for decision)
- [ ] References to related ADRs included

## Review Checklist

### 6. Prepare for Review

- [ ] Set ADR status to "Proposed"
- [ ] Identify reviewers (affected teams, architects, stakeholders)
- [ ] Create pull request or share document
- [ ] Set review deadline

### 7. Conduct Review

- [ ] Allow time for silent reading (10 minutes minimum)
- [ ] Collect feedback from all reviewers
- [ ] Address questions and concerns
- [ ] Update ADR based on feedback
- [ ] Document any dissenting opinions

### 8. Finalize

- [ ] All reviewers have approved or acknowledged
- [ ] Major concerns have been addressed
- [ ] Update status to "Accepted" (or "Rejected" if not approved)
- [ ] Merge to main branch
- [ ] Communicate decision to affected parties

## Post-Decision Checklist

### 9. After Acceptance

- [ ] Implement the decision
- [ ] Update related documentation
- [ ] Link ADR from relevant code/docs
- [ ] Schedule follow-up review if appropriate

### 10. Maintenance

- [ ] Review ADR when context changes
- [ ] Create new ADR if decision needs to change
- [ ] Update status to "Superseded" and link to new ADR
- [ ] Keep rejected alternatives for historical reference

## Quick Reference Card

### ADR Structure

```markdown
# ADR-NNNN: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Deciders:** [Names]

## Context
[What is the situation? What forces are at play?]

## Decision
[What did we decide? "We will..."]

## Alternatives Considered
[What options did we consider and why were they rejected?]

## Consequences
[What are the results of this decision?]
```

### Status Flow

```
Proposed → Accepted → Deprecated
                   → Superseded by ADR-XXXX
         → Rejected
```

### Decision Criteria Matrix

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Performance | High | Good | Better | Best |
| Complexity | Medium | Low | Medium | High |
| Cost | Medium | Low | Medium | High |
| Team familiarity | Low | High | Medium | Low |
| **Score** | | X | Y | Z |

## Common Pitfalls to Avoid

| Pitfall | Prevention |
|---------|------------|
| Writing after implementation | Create ADR when decision is being made |
| Skipping alternatives | Always document at least 2 alternatives |
| Ignoring consequences | List both positive AND negative impacts |
| Too much detail | Focus on "why", not "how" |
| Not updating status | Mark old ADRs as deprecated/superseded |
| Single-author ADRs | Involve affected stakeholders in review |
| Storing in wikis | Keep ADRs in version control with code |

## Time Budget Guidelines

| Activity | Suggested Time |
|----------|----------------|
| Context gathering | 30 min - 2 hours |
| Research alternatives | 1 - 4 hours |
| Writing first draft | 30 min - 1 hour |
| Review process | 1 - 3 days |
| Revisions | 30 min - 1 hour |

**Total**: A well-researched ADR typically takes 4-8 hours of effort spread over several days.

## Templates

See [templates.md](templates.md) for ready-to-use templates:
- Nygard format (minimal)
- MADR format (comprehensive)
- Y-statements (one-liner)
- Extended format (enterprise)
