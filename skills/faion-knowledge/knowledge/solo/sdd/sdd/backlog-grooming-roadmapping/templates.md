# Backlog & Roadmap Templates

Copy-paste templates for backlog items, grooming sessions, and roadmaps.

---

## Backlog Item Template

```markdown
# BACKLOG: [Item Title]

**ID:** BL-XXX
**Status:** Idea | Validated | Specified | Designed | Ready
**Priority:** P0 | P1 | P2 | P3
**MoSCoW:** Must | Should | Could | Won't
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

---

## Summary

[1-2 sentence description of the feature/change]

---

## Problem

[What problem does this solve? Who experiences it? How painful is it?]

---

## Proposed Solution

[High-level approach - not technical design, just the concept]

---

## User Stories

- As a [user type], I want [action], so that [benefit]
- As a [user type], I want [action], so that [benefit]

---

## RICE Score

| Factor | Value | Notes |
|--------|-------|-------|
| Reach | X | [How many users per quarter] |
| Impact | X | [0.25 minimal, 0.5 low, 1 medium, 2 high, 3 massive] |
| Confidence | X% | [50% low, 80% medium, 100% high] |
| Effort | X | [Person-months: 0.5, 1, 2, 3, 6+] |
| **Score** | **X.X** | [(R x I x C) / E] |

---

## Success Criteria

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

---

## Dependencies

- [Dependency 1]: [Status/Notes]
- [Dependency 2]: [Status/Notes]

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [How to mitigate] |
| [Risk 2] | Low/Med/High | Low/Med/High | [How to mitigate] |

---

## Open Questions

- [ ] [Question 1] - Owner: [Name]
- [ ] [Question 2] - Owner: [Name]

---

## Next Steps

- [ ] [Action needed to move forward]
- [ ] [Action needed to move forward]
```

---

## Grooming Session Template

```markdown
# Backlog Grooming: YYYY-MM-DD

**Attendees:** [Names]
**Duration:** [X minutes]
**Facilitator:** [Name]

---

## New Ideas Reviewed

| ID | Title | Decision | Reason |
|----|-------|----------|--------|
| BL-XXX | [Title] | Keep / Drop | [Brief reason] |
| BL-XXY | [Title] | Keep / Drop | [Brief reason] |

---

## Priority Changes

| ID | Title | Old Priority | New Priority | Reason |
|----|-------|--------------|--------------|--------|
| BL-XXX | [Title] | P2 | P1 | [Why changed] |

---

## Items Refined

| ID | Title | Changes Made |
|----|-------|--------------|
| BL-XXX | [Title] | [What was added/clarified] |

---

## Items Archived

| ID | Title | Reason |
|----|-------|--------|
| BL-XXX | [Title] | [Why archived] |

---

## Added to "Won't Do"

| ID | Title | Reason | Revisit? |
|----|-------|--------|----------|
| BL-XXX | [Title] | [Why not doing] | [When to revisit or "Never"] |

---

## Next Sprint Candidates

| Priority | ID | Title | Complexity | Dependencies |
|----------|-----|-------|------------|--------------|
| 1 | BL-XXX | [Title] | Low/Med/High | [Any blockers] |
| 2 | BL-XXY | [Title] | Low/Med/High | [Any blockers] |
| 3 | BL-XXZ | [Title] | Low/Med/High | [Any blockers] |

---

## Action Items

- [ ] [Action] - Owner: [Name] - Due: [Date]
- [ ] [Action] - Owner: [Name] - Due: [Date]

---

## Notes

[Any additional discussion points, decisions, or context]
```

---

## Now/Next/Later Roadmap Template

```markdown
# Product Roadmap: [Product Name]

**Last Updated:** YYYY-MM-DD
**Owner:** [Product Owner]
**Review Cadence:** Monthly

---

## Vision

[One sentence describing where the product is going]

---

## NOW (Current Focus)

*Committed work. These items are in progress or will start this sprint.*

### [Initiative/Feature Name]
**Status:** In Progress | Starting Soon
**Confidence:** High

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

### [Initiative/Feature Name]
**Status:** In Progress | Starting Soon
**Confidence:** High

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

---

## NEXT (Near-Term)

*Planned work. High priority but not yet started.*

### [Initiative/Feature Name]
**Target:** Next quarter
**Confidence:** Medium

Features under consideration:
- [Feature 1]
- [Feature 2]

### [Initiative/Feature Name]
**Target:** Next quarter
**Confidence:** Medium

Features under consideration:
- [Feature 1]
- [Feature 2]

---

## LATER (Future)

*Exploratory. May change based on learnings.*

### [Theme/Initiative Name]

Potential features:
- [Feature 1]
- [Feature 2]
- [Feature 3]

*Note: Later items will be refined as we learn more.*

---

## NOT PLANNED

*Items explicitly not on roadmap. Documented to avoid revisiting.*

| Item | Reason | Revisit? |
|------|--------|----------|
| [Item 1] | [Why not building] | [When/If to revisit] |
| [Item 2] | [Why not building] | Never |

---

## Dependencies

| Initiative | Depends On | Risk Level | Mitigation |
|------------|------------|------------|------------|
| [Initiative] | [External team/resource] | Low/Med/High | [Plan] |

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| YYYY-MM-DD | [What changed] | [Why] |
```

---

## Quarterly Roadmap Template

```markdown
# Q[X] [YEAR] Roadmap: [Product Name]

**Created:** YYYY-MM-DD
**Owner:** [Product Owner]
**Status:** Draft | Approved | In Progress | Complete

---

## Quarter Goals

1. [Goal 1 - Measurable outcome]
2. [Goal 2 - Measurable outcome]
3. [Goal 3 - Measurable outcome]

---

## Month 1: [Theme/Focus]

### Week 1-2: [Milestone Name]

| Feature | Owner | Status |
|---------|-------|--------|
| [Feature 1] | [Name] | Not Started / In Progress / Done |
| [Feature 2] | [Name] | Not Started / In Progress / Done |

### Week 3-4: [Milestone Name]

| Feature | Owner | Status |
|---------|-------|--------|
| [Feature 1] | [Name] | Not Started / In Progress / Done |
| [Feature 2] | [Name] | Not Started / In Progress / Done |

---

## Month 2: [Theme/Focus]

### Week 1-2: [Milestone Name]

| Feature | Owner | Status |
|---------|-------|--------|
| [Feature 1] | [Name] | Not Started / In Progress / Done |

### Week 3-4: [Milestone Name]

| Feature | Owner | Status |
|---------|-------|--------|
| [Feature 1] | [Name] | Not Started / In Progress / Done |

---

## Month 3: [Theme/Focus]

### Week 1-2: [Milestone Name]

| Feature | Owner | Status |
|---------|-------|--------|
| [Feature 1] | [Name] | Not Started / In Progress / Done |

### Week 3-4: [Milestone Name]

| Feature | Owner | Status |
|---------|-------|--------|
| [Feature 1] | [Name] | Not Started / In Progress / Done |

---

## Risks & Dependencies

| Risk/Dependency | Likelihood | Impact | Mitigation | Owner |
|-----------------|------------|--------|------------|-------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Plan] | [Name] |

---

## Success Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| [Metric 1] | [Value] | [Goal] | On Track / At Risk |
| [Metric 2] | [Value] | [Goal] | On Track / At Risk |

---

## Quarter Retrospective

*Fill out at end of quarter*

### What Worked
- [Item]

### What Didn't Work
- [Item]

### Key Learnings
- [Learning]

### Carry-over to Next Quarter
- [Item not completed]
```

---

## Theme-Based Roadmap Template

```markdown
# Roadmap: [Product Name]

**Last Updated:** YYYY-MM-DD
**Time Horizon:** [X months]

---

## Active Themes

### Theme: [Theme Name]
**Priority:** P0 | P1 | P2
**Owner:** [Name]
**Timeline:** Q[X]-Q[Y] [YEAR]

**Objective:** [What this theme achieves]

**Initiatives:**
```
[Theme Name]
├── [Initiative 1]
│   ├── [Feature/Task]
│   ├── [Feature/Task]
│   └── [Feature/Task]
├── [Initiative 2]
│   ├── [Feature/Task]
│   └── [Feature/Task]
└── [Initiative 3]
    ├── [Feature/Task]
    └── [Feature/Task]
```

**Success Metrics:**
- [Metric]: [Target]
- [Metric]: [Target]

---

### Theme: [Theme Name]
**Priority:** P0 | P1 | P2
**Owner:** [Name]
**Timeline:** Q[X]-Q[Y] [YEAR]

**Objective:** [What this theme achieves]

**Initiatives:**
```
[Theme Name]
├── [Initiative 1]
│   └── [Feature/Task]
└── [Initiative 2]
    └── [Feature/Task]
```

---

## Future Themes (Not Active)

| Theme | Description | Earliest Start | Dependency |
|-------|-------------|----------------|------------|
| [Theme] | [Brief description] | Q[X] [YEAR] | [What needs to happen first] |

---

## Retired Themes

| Theme | Timeline | Outcome |
|-------|----------|---------|
| [Theme] | Q[X]-Q[Y] | [Summary of what was achieved] |
```

---

## RICE Scoring Template

```markdown
# RICE Scoring: [Feature Set/Release Name]

**Date:** YYYY-MM-DD
**Scorer:** [Name]

---

## Scoring Guidelines

| Factor | Scale | Description |
|--------|-------|-------------|
| Reach | 1-10 | Users affected per quarter (1=10%, 10=100%) |
| Impact | 0.25, 0.5, 1, 2, 3 | Minimal, Low, Medium, High, Massive |
| Confidence | 50%, 80%, 100% | Low, Medium, High |
| Effort | 0.5, 1, 2, 3, 6 | Person-months |

---

## Feature Scores

| Feature | Reach | Impact | Confidence | Effort | RICE | Rank |
|---------|-------|--------|------------|--------|------|------|
| [Feature 1] | | | | | | |
| [Feature 2] | | | | | | |
| [Feature 3] | | | | | | |
| [Feature 4] | | | | | | |
| [Feature 5] | | | | | | |

---

## Notes

| Feature | Scoring Rationale |
|---------|-------------------|
| [Feature 1] | [Why these scores] |
| [Feature 2] | [Why these scores] |

---

## Recommendation

Based on RICE scores:

**Prioritize:**
1. [Feature] (Score: X.X)
2. [Feature] (Score: X.X)

**Deprioritize:**
- [Feature] (Score: X.X) - [Reason]

**Additional Considerations:**
- [Strategic factors not captured in RICE]
```

---

## MoSCoW Categorization Template

```markdown
# MoSCoW: [Release/Sprint Name]

**Date:** YYYY-MM-DD
**Release Target:** [Date or Sprint]
**Scope Budget:** [Person-days or Story Points]

---

## Must Have (~60% of scope)

*Non-negotiable. Release fails without these.*

| Item | Effort | Owner | Status |
|------|--------|-------|--------|
| [Item 1] | [X] | [Name] | |
| [Item 2] | [X] | [Name] | |

**Must Have Total:** [X] / [Budget]

---

## Should Have (~20% of scope)

*Important but not critical. Can launch without.*

| Item | Effort | Owner | Status |
|------|--------|-------|--------|
| [Item 1] | [X] | [Name] | |
| [Item 2] | [X] | [Name] | |

**Should Have Total:** [X]

---

## Could Have (~20% of scope)

*Nice to have. Only if time permits.*

| Item | Effort | Owner | Status |
|------|--------|-------|--------|
| [Item 1] | [X] | [Name] | |
| [Item 2] | [X] | [Name] | |

**Could Have Total:** [X]

---

## Won't Have (This Release)

*Explicitly out of scope.*

| Item | Reason | Future Release? |
|------|--------|-----------------|
| [Item 1] | [Why not now] | [When] |
| [Item 2] | [Why not now] | Never |

---

## Summary

| Category | Effort | % of Total |
|----------|--------|------------|
| Must Have | [X] | [X]% |
| Should Have | [X] | [X]% |
| Could Have | [X] | [X]% |
| **Total Planned** | **[X]** | **100%** |
| Budget | [X] | |
| Buffer | [X] | [X]% |
```
