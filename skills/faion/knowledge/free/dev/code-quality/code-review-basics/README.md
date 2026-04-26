---
id: code-review-basics
name: "Code Review Basics"
domain: DEV
skill: faion-software-developer
category: "development"
parent: code-review
---

# Code Review Basics

## Overview

Code review is a systematic examination of source code to find bugs, improve quality, ensure consistency, and share knowledge across the team. Effective code reviews balance thoroughness with velocity.

## When to Use

- All code changes before merging
- During pair programming sessions
- Security-sensitive changes (extra review)
- Architectural changes (broader review)
- Junior developer mentoring

## Key Principles

- **Review the code, not the author**: Focus on improvement, not criticism
- **Small, focused reviews**: Large PRs are hard to review well
- **Timely feedback**: Review within hours, not days
- **Constructive comments**: Suggest improvements, explain why
- **Share knowledge**: Reviews are learning opportunities

## What to Review

```markdown
## Code Review Checklist

### Correctness
- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled?
- [ ] Is error handling appropriate?
- [ ] Are there any obvious bugs?

### Design
- [ ] Is the code well-organized?
- [ ] Does it follow project patterns?
- [ ] Is there unnecessary complexity?
- [ ] Are responsibilities properly separated?

### Maintainability
- [ ] Is the code readable?
- [ ] Are names meaningful?
- [ ] Is it properly documented?
- [ ] Would a new team member understand it?

### Testing
- [ ] Are there sufficient tests?
- [ ] Do tests cover edge cases?
- [ ] Are tests readable and maintainable?
- [ ] Do tests actually verify behavior?

### Performance
- [ ] Any obvious performance issues?
- [ ] N+1 queries?
- [ ] Unnecessary allocations?
- [ ] Missing indexes for new queries?

### Security
- [ ] Input validation present?
- [ ] No hardcoded secrets?
- [ ] SQL injection prevented?
- [ ] Proper authentication/authorization?
```

## Writing Good Review Comments

```markdown
## Comment Types

### Blocking (Must Fix)
Use when the code has bugs, security issues, or violates standards.

**Bad:**
"This is wrong."

**Good:**
"This will cause a null pointer exception when `user` is None.
Consider adding a guard clause:
```python
if not user:
    return None
```"

### Suggestion (Should Consider)
Use for improvements that would make code better.

**Bad:**
"Use a different approach."

**Good:**
"Suggestion: Consider using `dict.get()` with a default value
to avoid the KeyError. This is more Pythonic and handles missing
keys gracefully:
```python
# Instead of
value = data['key'] if 'key' in data else 'default'

# Consider
value = data.get('key', 'default')
```"

### Nitpick (Minor)
Use for style issues or personal preferences. Mark as optional.

**Good:**
"Nit: Consider renaming `x` to `user_count` for clarity.
(Not blocking)"

### Question
Use when you don't understand something.

**Good:**
"Question: Why do we need to fetch the user twice here?
Is there a caching issue I'm missing?"

### Praise
Acknowledge good code!

**Good:**
"Nice! This is a clean solution to the caching problem.
The decorator pattern makes it very reusable."
```

## Review Response Guidelines

```markdown
## As a Reviewer

1. **Be timely**: Review within 24 hours (ideally 4 hours)
2. **Be thorough**: Don't just skim
3. **Be respectful**: Critique code, not people
4. **Be specific**: Point to exact lines, suggest fixes
5. **Be proportionate**: Don't block on nitpicks

## As an Author

1. **Keep PRs small**: < 400 lines ideally
2. **Provide context**: Good description, linked issues
3. **Self-review first**: Catch obvious issues
4. **Respond to all comments**: Even if just "Done"
5. **Don't take it personally**: Reviews improve code
```

## Anti-patterns

- **Rubber stamping**: Approving without reading
- **Nitpick blocking**: Holding PRs for trivial issues
- **Inconsistent standards**: Different rules for different people
- **No praise**: Only pointing out problems
- **Delayed reviews**: Taking days to respond
- **Review avoidance**: Finding excuses not to review

## Best Practices Summary

```markdown
## For Reviewers

DO:
- Review promptly (within 4 hours)
- Explain the "why" behind suggestions
- Acknowledge good code
- Ask questions when unclear
- Approve when good enough (not perfect)

DON'T:
- Block on style preferences
- Rewrite author's code
- Be condescending
- Rubber stamp without reading
- Leave vague comments

## For Authors

DO:
- Keep PRs small and focused
- Write good descriptions
- Self-review before requesting
- Respond to all comments
- Test before submitting

DON'T:
- Take feedback personally
- Ignore comments
- Submit untested code
- Create massive PRs
- Rush reviewers
```

## References

- [Google Engineering Code Review](https://google.github.io/eng-practices/review/)
- [Microsoft Code Review Best Practices](https://docs.microsoft.com/en-us/azure/devops/repos/git/about-pull-requests)
- [Thoughtbot Code Review Guide](https://github.com/thoughtbot/guides/tree/main/code-review)
- [Conventional Comments](https://conventionalcomments.org/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Review code for architectural violations | sonnet | Code review with pattern matching |
| Refactor legacy code to clean architecture | opus | Complex refactoring with trade-offs |
| Calculate code coverage for module | haiku | Metric collection and reporting |
| Design domain-driven architecture | opus | Strategic design decision |
| Write test cases for edge cases | sonnet | Testing with reasoning about coverage |
| Apply decomposition pattern to class | sonnet | Refactoring with patterns |

