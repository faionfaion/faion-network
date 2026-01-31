# Code Review Cycle LLM Prompts

## Prompt 1: Self-Review Before PR

```
You are conducting a self-review of code before submitting a pull request.

CODE:
{code_diff}

SDD REFERENCES:
- Spec: {spec_link}
- Design: {design_link}
- Task: {task_link}

CHECKLIST:
1. Code Quality
   - Follows project style guide
   - No commented code or debug statements
   - Proper error handling
   - No hardcoded values

2. Functionality
   - All acceptance criteria met
   - Edge cases handled
   - Works locally
   - No regressions

3. Testing
   - Unit tests cover new code
   - Tests are meaningful
   - All tests pass
   - Integration tests updated

4. Documentation
   - Self-documenting code
   - Complex logic commented
   - API docs updated
   - README updated if needed

5. SDD Compliance
   - Matches design document
   - Deviations documented
   - Traceability correct

OUTPUT FORMAT:
{
  "ready_for_review": boolean,
  "issues_found": [
    {
      "category": "code_quality|functionality|testing|documentation|sdd",
      "severity": "critical|high|medium|low",
      "description": "Issue description",
      "location": "file:line",
      "fix": "Suggested fix"
    }
  ],
  "checklist_status": {
    "code_quality": "✅|❌",
    "functionality": "✅|❌",
    "testing": "✅|❌",
    "documentation": "✅|❌",
    "sdd_compliance": "✅|❌"
  }
}
```

## Prompt 2: Peer Code Review

```
You are reviewing a pull request as a senior developer.

PR INFORMATION:
Title: {pr_title}
Description: {pr_description}
Author: {author}

CODE CHANGES:
{code_diff}

SDD REFERENCES:
- Spec: {spec_content}
- Design: {design_content}
- Task: {task_content}

REVIEW FOCUS AREAS:
1. Correctness - Does it solve the problem? Edge cases handled?
2. Design - Follows patterns? Appropriate abstraction? No complexity?
3. Readability - Clear names? Well-organized? Helpful comments?
4. Performance - No N+1 queries? Caching used? Efficient at scale?
5. Security - Input validated? No injection risks? Auth correct?
6. Testing - Tests meaningful? Cover edge cases? Catch regressions?

COMMENT PREFIXES:
- [Required] - Must fix before merge
- [Suggestion] - Consider this improvement
- [Question] - Need clarification
- [Nitpick] - Minor style preference
- [Nice] - Good pattern worth highlighting
- [FYI] - Educational, no action needed

OUTPUT FORMAT:
{
  "verdict": "approved|approved_with_suggestions|request_changes",
  "summary": "Overall assessment",
  "comments": [
    {
      "type": "required|suggestion|question|nitpick|nice|fyi",
      "file": "path/to/file",
      "line": 42,
      "message": "Review comment with context and suggestions"
    }
  ],
  "checklist": {
    "correctness": "✅|❌",
    "design": "✅|❌",
    "code_quality": "✅|❌",
    "testing": "✅|❌",
    "security": "✅|❌",
    "documentation": "✅|❌",
    "sdd_compliance": "✅|❌"
  },
  "metrics": {
    "required_changes": number,
    "suggestions": number,
    "questions": number
  }
}
```

## Prompt 3: Generate PR Description

```
You are helping generate a comprehensive PR description.

TASK INFORMATION:
- Task ID: {task_id}
- Acceptance Criteria: {acceptance_criteria}
- Spec: {spec_link}
- Design: {design_link}

CODE CHANGES:
{git_diff}

TESTS ADDED:
{test_files}

Generate a PR description following this template:

## Summary
[Brief description of changes]

## SDD References
| Document | Section |
|----------|---------|
| Spec | [SPEC-XXX](link) |
| Design | [DESIGN-XXX](link) |
| Task | [TASK-XXX](link) |

## Changes
- [x] Change 1
- [x] Change 2

## Acceptance Criteria Verification
| AC | Status | Notes |
|----|--------|-------|
| AC-1: ... | Verified | ... |

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases tested

## Checklist
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No lint/type errors
- [ ] Documentation updated
- [ ] No secrets committed

OUTPUT: Return the formatted PR description in markdown.
```

## Prompt 4: Detect Anti-Patterns

```
You are a code quality analyzer looking for anti-patterns and code smells.

CODE:
{code}

LANGUAGE: {language}

KNOWN ANTI-PATTERNS TO CHECK:
1. Security
   - SQL injection (string concatenation in queries)
   - Hardcoded secrets
   - Missing input validation
   - Weak password hashing

2. Performance
   - N+1 queries
   - Missing indexes
   - Inefficient loops
   - Memory leaks

3. Design
   - God classes (too many responsibilities)
   - Tight coupling
   - Missing abstractions
   - Magic numbers

4. Testing
   - Missing error cases
   - Fragile tests (depends on order)
   - Insufficient coverage
   - Testing implementation not behavior

OUTPUT FORMAT:
{
  "anti_patterns_found": [
    {
      "category": "security|performance|design|testing",
      "pattern": "Pattern name",
      "location": "file:line",
      "description": "What's wrong and why",
      "fix": "How to fix it",
      "severity": "critical|high|medium|low",
      "source": "Related mistake ID if applicable"
    }
  ],
  "recommendations": [
    "General improvement suggestions"
  ]
}
```

## Prompt 5: Post-Merge Reflexion

```
You are facilitating a post-merge reflexion session for completed feature.

FEATURE INFORMATION:
Feature: {feature_name}
Tasks completed: {task_count}
PRs merged: {pr_count}
Duration: {duration}

PR HISTORY:
{pr_list_with_metrics}

REVIEW METRICS:
{review_metrics}

ISSUES ENCOUNTERED:
{issues_list}

ANALYZE:
1. What worked well?
   - Patterns that should be repeated
   - Process improvements that helped
   - Good decisions made

2. What could be better?
   - Improvements for next time
   - Lessons learned
   - Tech debt created

3. Memory updates needed?
   - New patterns to remember
   - Mistakes to document
   - Process changes to make

OUTPUT FORMAT:
{
  "what_worked_well": {
    "patterns": ["Pattern 1", "Pattern 2"],
    "process": ["Process 1", "Process 2"]
  },
  "what_could_be_better": {
    "improvements": ["Improvement 1", "Improvement 2"],
    "lessons": ["Lesson 1", "Lesson 2"]
  },
  "memory_updates": {
    "patterns_learned": [
      {
        "pattern": "Pattern description",
        "context": "When to apply",
        "file": "patterns_learned.jsonl"
      }
    ],
    "mistakes_avoided": [
      {
        "mistake": "Mistake description",
        "prevention": "How it was prevented",
        "source": "MIS_ID if applicable"
      }
    ]
  },
  "next_feature_improvements": [
    "Action item 1",
    "Action item 2"
  ]
}
```

## Prompt 6: Review Metrics Analysis

```
You are analyzing code review metrics to identify trends and improvements.

METRICS DATA:
{metrics_json}

ANALYZE:
1. Efficiency
   - Time to first review
   - Time to merge
   - Review iterations
   - Trends over time

2. Quality
   - Bugs found in review
   - Bugs escaped to production
   - Prevention rate
   - Issue types

3. Engagement
   - Reviewer participation
   - Feedback distribution
   - Knowledge sharing

4. Recommendations
   - What's working well
   - What needs improvement
   - Action items

OUTPUT FORMAT:
{
  "efficiency_analysis": {
    "time_to_first_review": {
      "average": "X hours",
      "target": "< Y hours",
      "status": "on_track|needs_improvement",
      "trend": "improving|stable|declining"
    },
    ...
  },
  "quality_analysis": {
    "prevention_rate": "X%",
    "top_issue_types": ["type1", "type2"],
    "trend": "improving|stable|declining"
  },
  "engagement_analysis": {
    "participation_rate": "X%",
    "feedback_quality": "high|medium|low",
    "knowledge_sharing": "active|moderate|low"
  },
  "recommendations": [
    {
      "area": "efficiency|quality|engagement",
      "issue": "Problem identified",
      "action": "Recommended action",
      "priority": "high|medium|low"
    }
  ],
  "trends": [
    "Trend observation 1",
    "Trend observation 2"
  ]
}
```
