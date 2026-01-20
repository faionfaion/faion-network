---
id: M-SDD-007
name: "Reflexion & Learning"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# M-SDD-007: Reflexion & Learning

## Metadata

| Field | Value |
|-------|-------|
| **ID** | M-SDD-007 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #reflexion, #learning |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-executor-agent |

---

## Problem

Teams and AI agents repeat the same mistakes because:
- No structured reflection after tasks/projects
- Lessons learned not captured
- Patterns not identified across projects
- Knowledge not shared or accessible

**The root cause:** No systematic learning loop.

---

## Framework

### What is Reflexion?

Reflexion is a process of:
1. **Reflecting** on what happened
2. **Analyzing** what went well and what didn't
3. **Learning** explicit lessons
4. **Applying** lessons to future work

### The Reflexion Loop

```
DO → REFLECT → LEARN → APPLY → DO (improved)
```

### When to Reflect

| Trigger | Scope | Duration |
|---------|-------|----------|
| Task completed | Single task | 5 minutes |
| Feature completed | Feature (5-20 tasks) | 30 minutes |
| Sprint ended | Sprint (2 weeks) | 1 hour |
| Project completed | Entire project | 2-4 hours |
| Failure occurred | Incident | As needed |

### Reflection Questions

#### For Tasks
- Did I achieve the acceptance criteria?
- What took longer than expected? Why?
- What was easier than expected? Why?
- What would I do differently next time?
- What tools/techniques worked well?

#### For Features
- Did we deliver what the spec required?
- How accurate were our estimates?
- What technical debt did we accumulate?
- What went wrong and how did we fix it?
- What patterns emerged?

#### For Projects
- Did we meet the business goals?
- What was our biggest success?
- What was our biggest failure?
- What would we change in our process?
- What should we replicate in future projects?

### Learning Types

| Type | Example | Storage |
|------|---------|---------|
| **Pattern** | "Always add rate limiting to auth endpoints" | patterns_learned.jsonl |
| **Mistake** | "Forgot to add indexes, caused slow queries" | mistakes_learned.jsonl |
| **Shortcut** | "Use this snippet for JWT validation" | code snippets |
| **Process** | "Spec review before design saves 30% rework" | documentation |

---

## Templates

### Task Reflexion Template

```markdown
## Task Reflexion: TASK-XXX

**Date:** YYYY-MM-DD
**Duration:** Estimated: Xh | Actual: Yh

### Outcome

- [x] Acceptance criteria met
- [ ] Acceptance criteria partially met
- [ ] Acceptance criteria not met

### What Went Well

- [Item 1]
- [Item 2]

### What Went Wrong

- [Issue 1]: [How resolved]
- [Issue 2]: [How resolved]

### Lessons Learned

1. **Pattern:** [Pattern to replicate]
2. **Mistake:** [Mistake to avoid]
3. **Insight:** [General insight]

### Time Analysis

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Coding | 2h | 3h | [Why] |
| Testing | 1h | 1h | On target |
| Debugging | 0h | 1h | Unexpected issue |

### Next Time I Will

- [Action 1]
- [Action 2]
```

### Feature Retrospective Template

```markdown
## Feature Retrospective: [Feature Name]

**Date:** YYYY-MM-DD
**Duration:** Planned: X days | Actual: Y days
**Tasks:** X completed / Y planned

---

### Summary

[2-3 sentences summarizing the feature delivery]

---

### Metrics

| Metric | Planned | Actual | Delta |
|--------|---------|--------|-------|
| Duration | X days | Y days | +Z% |
| Tasks | X | Y | +Z |
| Bugs found | - | N | - |
| Technical debt items | - | N | - |

---

### What Went Well

1. **[Category]:** [Description]
   - Evidence: [Specific example]

2. **[Category]:** [Description]
   - Evidence: [Specific example]

---

### What Went Wrong

1. **[Issue]:** [Description]
   - Root cause: [Analysis]
   - Resolution: [How fixed]
   - Prevention: [How to avoid next time]

2. **[Issue]:** [Description]
   - Root cause: [Analysis]
   - Resolution: [How fixed]
   - Prevention: [How to avoid next time]

---

### Patterns Identified

| ID | Pattern | Context | Recommendation |
|----|---------|---------|----------------|
| P-001 | [Pattern] | [When applies] | [What to do] |
| P-002 | [Pattern] | [When applies] | [What to do] |

---

### Mistakes to Avoid

| ID | Mistake | Impact | Prevention |
|----|---------|--------|------------|
| M-001 | [Mistake] | [Impact] | [How to prevent] |
| M-002 | [Mistake] | [Impact] | [How to prevent] |

---

### Action Items

| Item | Owner | Due |
|------|-------|-----|
| [Action] | [Name] | [Date] |

---

### Team Feedback

> "[Quote from team member]" - [Name]

> "[Quote from team member]" - [Name]
```

### Learning Entry Template (JSONL)

```json
{
  "id": "P-2026-001",
  "type": "pattern",
  "date": "2026-01-17",
  "project": "faion-net",
  "feature": "auth-system",
  "title": "Rate limit authentication endpoints",
  "description": "Always add rate limiting to login/register endpoints to prevent brute force attacks",
  "context": "Discovered during security review that unlimited login attempts were possible",
  "recommendation": "Use express-rate-limit with 5 attempts per minute per IP",
  "tags": ["security", "authentication", "api"],
  "confidence": "high"
}
```

```json
{
  "id": "M-2026-001",
  "type": "mistake",
  "date": "2026-01-17",
  "project": "faion-net",
  "feature": "auth-system",
  "title": "Forgot database indexes on frequently queried columns",
  "description": "Users table had no index on email column, causing slow lookups",
  "impact": "Login took 500ms instead of 50ms with 10K users",
  "root_cause": "Assumed ORM would create indexes automatically",
  "prevention": "Always verify indexes exist for columns used in WHERE clauses",
  "tags": ["database", "performance"],
  "confidence": "high"
}
```

### Session Context Template

```markdown
# Session Context: YYYY-MM-DD

## Active Project

- **Name:** [Project]
- **Feature:** [Current feature]
- **Phase:** [Spec/Design/Implementation]

## Recent Decisions

1. [Decision 1] - [Rationale]
2. [Decision 2] - [Rationale]

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

## Lessons Applied

- Applied P-2026-001 (rate limiting)
- Avoided M-2026-001 (added indexes)

## Tomorrow's Focus

- [Priority 1]
- [Priority 2]
```

---

## Examples

### Example: Task Reflexion

```markdown
## Task Reflexion: TASK-007

**Task:** Implement register handler
**Date:** 2026-01-17
**Duration:** Estimated: 2h | Actual: 3.5h

### Outcome

- [x] Acceptance criteria met

### What Went Well

- Password hashing implementation was straightforward
- Test cases from spec were comprehensive
- Reused patterns from TASK-006 (login handler)

### What Went Wrong

- Email validation edge cases took extra hour
  - Resolved: Found email-validator library
- Database constraint errors not handled properly
  - Resolved: Added try-catch with specific error handling

### Lessons Learned

1. **Pattern:** Use email-validator library instead of regex
2. **Mistake:** Test with duplicate emails early
3. **Insight:** Handler error responses should be consistent

### Time Analysis

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Coding | 1.5h | 2h | Email validation |
| Testing | 0.5h | 1h | Edge cases |
| Debugging | 0h | 0.5h | DB constraints |

### Next Time I Will

- Start with edge case tests
- Check for existing validation libraries first
- Define error response format upfront
```

### Example: Pattern Learned

**Context:** Building multiple APIs, noticed same issues recurring.

```json
{
  "id": "P-2026-015",
  "type": "pattern",
  "date": "2026-01-17",
  "project": "faion-net",
  "title": "Standardize API error responses",
  "description": "All API errors should return consistent JSON structure",
  "context": "Different endpoints returned errors in different formats, confusing frontend",
  "recommendation": "Use RFC 7807 format: {type, title, status, detail, instance}",
  "example": {
    "type": "https://faion.net/errors/validation",
    "title": "Validation Error",
    "status": 400,
    "detail": "Email format is invalid",
    "instance": "/api/auth/register"
  },
  "tags": ["api", "errors", "standards"],
  "confidence": "high"
}
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping reflection when busy | Schedule it - even 5 minutes helps |
| Vague lessons ("do better") | Be specific - what exactly will you do differently? |
| Not storing learnings | Use structured format (JSONL, markdown) |
| Not applying past lessons | Review learnings before starting similar work |
| Blaming instead of learning | Focus on process, not people |

---

## Storage Structure

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Patterns to replicate
├── mistakes_learned.jsonl    # Mistakes to avoid
└── session_context.md        # Current session state

aidocs/sdd/{project}/
└── reflexions/
    ├── tasks/               # Per-task reflexions
    ├── features/            # Feature retrospectives
    └── projects/            # Project post-mortems
```

---

## Related Methodologies

- **M-SDD-006:** Quality Gates & Confidence Checks
- **M-SDD-008:** Backlog Grooming & Roadmapping
- **M-PM-020:** Lessons Learned

---

## Agent

**faion-task-executor-agent** performs reflexion after tasks. The agent:
- Automatically reflects after task completion
- Stores patterns and mistakes
- Applies learnings to similar tasks
- Updates session context

---

*Methodology M-SDD-007 | SDD Foundation | Version 1.0*
