---
id: code-review
name: "Code Review"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Code Review

## Overview

Code review is a systematic examination of source code to find bugs, improve quality, ensure consistency, and share knowledge across the team. This methodology is split into focused documents.

## Structure

| File | Content | Focus |
|------|---------|-------|
| [code-review-basics.md](code-review-basics.md) | Principles, checklists, comment types | Core concepts |
| [code-review-process.md](code-review-process.md) | PR templates, automation, scenarios | Process & examples |

## Quick Reference

### When to Use

- All code changes before merging
- Security-sensitive changes (extra review)
- Architectural changes (broader review)
- Junior developer mentoring

### Key Principles

1. Review the code, not the author
2. Keep PRs small and focused
3. Provide timely feedback (< 4 hours)
4. Be constructive and specific
5. Use reviews as learning opportunities

### Review Checklist Categories

- **Correctness**: Does it work? Edge cases handled?
- **Design**: Well-organized? Follows patterns?
- **Maintainability**: Readable? Meaningful names?
- **Testing**: Sufficient coverage? Tests edge cases?
- **Performance**: N+1 queries? Unnecessary allocations?
- **Security**: Input validation? No secrets? SQL injection prevented?

### Comment Types

| Type | When to Use | Blocking? |
|------|-------------|-----------|
| Blocking | Bugs, security issues, standard violations | Yes |
| Suggestion | Improvements that would help | No |
| Nitpick | Style issues, preferences | No |
| Question | Don't understand something | No |
| Praise | Good code deserves recognition | No |

## See Also

- [code-review-basics.md](code-review-basics.md) - Fundamentals and best practices
- [code-review-process.md](code-review-process.md) - Templates and examples
- [refactoring-patterns.md](refactoring-patterns.md) - Code improvement strategies
- [documentation.md](documentation.md) - Documentation practices
