# Reflexion Cycle Checklist

Step-by-step checklist for applying Reflexion methodology in SDD tasks.

## Pre-Task Checklist (PLAN)

### Memory Loading

- [ ] Check if `.aidocs/memory/` exists
- [ ] Load `patterns.md` - identify relevant patterns for task type
- [ ] Load `mistakes.md` - identify domain-specific warnings
- [ ] Load `session.md` - restore context if continuing previous work
- [ ] Load `decisions.md` - review relevant architectural decisions

### Pattern Selection

- [ ] Filter patterns by task domain (coding, testing, deployment, etc.)
- [ ] Sort by confidence score (prioritize high-confidence patterns)
- [ ] Select top 3-5 most relevant patterns
- [ ] Note pattern IDs for tracking usage

### Mistake Review

- [ ] Filter mistakes by task domain
- [ ] Sort by severity (high severity first)
- [ ] Identify prevention strategies applicable to current task
- [ ] Create mental checklist of "don't do" items

### Context Preparation

- [ ] Add loaded patterns to task context
- [ ] Add mistake warnings to task context
- [ ] Note any assumptions being made
- [ ] Document starting state of relevant files

## Task Execution Checklist (DO)

### Pattern Application

- [ ] Apply selected patterns consciously
- [ ] Note each pattern used (for usage tracking)
- [ ] Deviate from patterns only with documented reason
- [ ] Watch for situations where loaded mistakes could occur

### Progress Tracking

- [ ] Track decisions made during execution
- [ ] Note any unexpected challenges
- [ ] Document workarounds applied
- [ ] Flag potential issues for reflection

### Quality Signals

- [ ] Monitor test results
- [ ] Watch for linter/type errors
- [ ] Check for runtime warnings
- [ ] Note performance observations

## Post-Task Checklist (CHECK)

### Outcome Evaluation

- [ ] Compare result against acceptance criteria
- [ ] Classify outcome: success / partial / failure
- [ ] Measure actual complexity vs estimated
- [ ] Note token usage if relevant

### Reflection Generation

For success:
- [ ] What specific actions led to success?
- [ ] Which patterns were most useful?
- [ ] Can this approach be generalized?
- [ ] Any new patterns to extract?

For partial/failure:
- [ ] What went wrong?
- [ ] What was the root cause? (use 5 Whys)
- [ ] What would have prevented this?
- [ ] What was the first sign of trouble?

### Pattern Analysis

- [ ] Which loaded patterns were used?
- [ ] Were they effective? (update confidence)
- [ ] Any patterns that should have been used but weren't?
- [ ] Any new patterns discovered?

### Mistake Analysis

- [ ] Did any loaded mistakes almost happen?
- [ ] Any new mistakes made?
- [ ] What would have caught this earlier?
- [ ] How to prevent recurrence?

## Memory Update Checklist (ACT)

### Pattern Updates

For used patterns:
- [ ] Increment usage count
- [ ] Update confidence based on outcome
- [ ] Add context notes if applicable
- [ ] Update last-used timestamp

For new patterns:
- [ ] Create pattern entry with ID
- [ ] Document context and solution
- [ ] Set initial confidence (0.5 for new)
- [ ] Link to source task

### Mistake Updates

For avoided mistakes:
- [ ] Note successful avoidance
- [ ] Validate prevention strategy works

For new mistakes:
- [ ] Create mistake entry with ID
- [ ] Document severity and impact
- [ ] Identify root cause
- [ ] Define prevention strategy
- [ ] Set occurrence count to 1

### Session Cleanup

- [ ] Clear completed task from session.md
- [ ] Update active decisions if changed
- [ ] Note any carry-over to next session
- [ ] Document any blocking questions

### Propagation

- [ ] Is this pattern/mistake broadly applicable?
- [ ] Should it be shared with team?
- [ ] Does any checklist need updating?
- [ ] Should any documentation change?

## Quick Reflexion (5 Minutes)

Minimal checklist for small tasks:

```markdown
## Quick Reflexion: TASK-XXX

**Outcome:** Success / Partial / Failure

**One thing that worked:**
[Brief description]

**One thing to improve:**
[Brief description]

**Pattern to remember:**
[One sentence or "None new"]

**Mistake to avoid:**
[One sentence or "None new"]
```

## Sprint Reflexion

End-of-sprint comprehensive review:

### Metrics Review

- [ ] Calculate estimation accuracy
- [ ] Count tasks completed vs planned
- [ ] Identify velocity trends
- [ ] Note escaped bugs

### Pattern Synthesis

- [ ] Review all patterns used this sprint
- [ ] Calculate usage and success rates
- [ ] Promote high-performing patterns
- [ ] Deprecate unused patterns (90+ days)

### Mistake Synthesis

- [ ] Review all mistakes encountered
- [ ] Identify recurring patterns
- [ ] Calculate prevention effectiveness
- [ ] Update severe mistake priorities

### Memory Maintenance

- [ ] Archive old low-confidence patterns
- [ ] Merge similar patterns
- [ ] Standardize pattern format
- [ ] Clean up session artifacts

### Action Items

- [ ] Document team-wide learnings
- [ ] Update process documentation
- [ ] Schedule improvement implementations
- [ ] Share insights in retrospective

## Validation Criteria

### Pattern Quality

A good pattern entry has:
- [ ] Clear, specific context
- [ ] Defined problem statement
- [ ] Concrete solution steps
- [ ] Measurable benefits
- [ ] Known trade-offs
- [ ] Tracked confidence

### Mistake Quality

A good mistake entry has:
- [ ] Severity classification
- [ ] Specific failure description
- [ ] Root cause (not symptoms)
- [ ] Concrete prevention strategy
- [ ] Detection improvement
- [ ] Tracked occurrences

### Reflection Quality

A good reflection has:
- [ ] Specific, not vague observations
- [ ] Root cause, not surface symptoms
- [ ] Actionable improvements
- [ ] Quantified impact where possible
- [ ] Clear next steps
