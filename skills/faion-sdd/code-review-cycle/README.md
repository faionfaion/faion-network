# Code Review Cycle

## Overview

The Code Review Cycle in SDD ensures quality, knowledge sharing, and continuous improvement through structured review processes. This methodology integrates human expertise with LLM assistance to create efficient, thorough reviews.

**Key Principle:** LLMs assist but never replace human judgment. Think of AI as a tireless first-pass reviewer that catches obvious issues, freeing humans to focus on architecture, business logic, and security.

## Why LLM-Assisted Code Review?

### The 2026 Reality

- Over 30% of senior developers ship mostly AI-generated code
- PRs are 18% larger on average with AI adoption
- Change failure rates up 30% when AI output exceeds verification capacity
- AI excels at drafting but falters on logic, security, and edge cases

### The Solution: Human-AI Collaboration

| Task | AI Does | Human Does |
|------|---------|------------|
| Style/formatting | Catches all issues | Defines standards |
| Common patterns | Identifies deviations | Decides exceptions |
| Security scanning | Flags vulnerabilities | Assesses real risk |
| Test coverage | Reports metrics | Judges test quality |
| Documentation | Checks completeness | Reviews accuracy |
| Business logic | Highlights complexity | Validates correctness |
| Architecture | Notes inconsistencies | Makes decisions |

## Review Types

### By Reviewer

| Type | Reviewer | Focus | When |
|------|----------|-------|------|
| Self-Review | Author | Completeness, obvious issues | Before PR |
| AI Pre-Review | LLM | Style, patterns, common issues | On PR creation |
| Automated | CI/CD | Tests, lint, security scans | On PR creation |
| Peer Review | Team member | Logic, design, patterns | After automated |
| Architectural | Senior/Lead | System design, consistency | Complex changes |
| Security | Security team | Vulnerabilities, auth/authz | Sensitive code |

### By Focus Area

| Focus | Description | AI Assistance Level |
|-------|-------------|---------------------|
| **Correctness** | Does it work? Edge cases? | Medium - flags, human decides |
| **Design** | Follows patterns? Extensible? | Low - human domain |
| **Readability** | Clear naming? Well-organized? | High - AI excels here |
| **Performance** | N+1 queries? Memory leaks? | Medium - detects patterns |
| **Security** | Input validation? Injection? | High - pattern matching |
| **Testing** | Coverage? Meaningful tests? | Medium - metrics vs quality |

## The Review Workflow

```
Task Completion
      |
      v
Self-Review (Author + AI assist)
      |
      v
PR Creation (with AI pre-review)
      |
      v
Automated Checks (CI/CD)
      |
      v
AI Review Pass (CodeRabbit, Copilot, etc.)
      |
      v
Human Review (peer/senior)
      |
      v
Iterations (address feedback)
      |
      v
Approval + Merge
      |
      v
Reflexion Learning
```

## LLM-Assisted Review Levels

### Level 1: AI Pre-Screening

AI reviews before human sees the PR:
- Style guide compliance
- Common anti-patterns
- Missing tests
- Documentation gaps
- Security red flags

**Result:** Cleaner PRs for human review, faster iterations.

### Level 2: AI as Co-Reviewer

AI provides inline comments during human review:
- Explains complex code sections
- Suggests alternatives
- Highlights similar patterns in codebase
- Flags potential issues for human judgment

**Result:** Humans catch more issues, learn faster.

### Level 3: AI Validation

AI validates after human approval:
- Runs additional security scans
- Checks integration compatibility
- Validates against design docs
- Verifies acceptance criteria

**Result:** Final safety net before merge.

## Multi-Model Review Strategy

Different LLMs have different strengths:

| Model | Best For |
|-------|----------|
| Claude | Code explanation, architecture review |
| GPT-4 | General review, documentation |
| Specialized (Semgrep, CodeQL) | Security scanning |
| CodeRabbit | Structured PR review |
| Copilot | Real-time suggestions |

**Recommended:** Use generation model + separate review model (checks and balances).

## AI Code Review Tools (2026)

| Tool | Type | Integration | Strengths |
|------|------|-------------|-----------|
| **CodeRabbit** | Dedicated reviewer | GitHub, GitLab, Azure | Structured feedback, 40+ linters |
| **GitHub Copilot Review** | Native | GitHub | Zero setup, inline comments |
| **Qodo (Codium)** | IDE + PR | VS Code, GitHub | Test generation, context-aware |
| **Sourcery** | PR review | GitHub | Python-focused, refactoring |
| **SonarCloud** | Quality gate | CI/CD | Code quality metrics |

## Best Practices

### For PR Authors

1. **Self-review with AI first** - Run AI review locally before creating PR
2. **Small PRs** - Easier for both AI and humans to review
3. **Clear descriptions** - AI uses context to provide better feedback
4. **Respond to AI feedback** - Don't ignore automated suggestions
5. **Mark AI-generated code** - Help reviewers know what to scrutinize

### For Reviewers

1. **Review AI suggestions first** - Triage before deep dive
2. **Focus on what AI misses** - Business logic, architecture, security implications
3. **Don't rubber-stamp AI approvals** - AI misses context
4. **Use AI to explain** - Ask AI about unfamiliar code
5. **Timely reviews** - Within 24 hours, keep momentum

### For Teams

1. **Configure AI to your standards** - Custom rules, team conventions
2. **Multi-model reviews** - Different perspectives
3. **Track AI effectiveness** - Measure false positives/negatives
4. **Gradual trust building** - Start with suggestions, evolve to gates
5. **Knowledge sharing** - Use [FYI] comments for education

## When NOT to Trust AI

AI review limitations:

- **Business logic** - AI doesn't understand your domain
- **Security implications** - AI flags patterns, misses context
- **Architecture decisions** - Requires system-wide understanding
- **Edge cases** - AI misses what it hasn't seen
- **Performance at scale** - AI doesn't know your load patterns
- **Data integrity** - AI doesn't understand your data model

**Rule:** Treat AI feedback as suggestions for humans to consider, not hard gates.

## SDD Integration

### Task Completion Review

Every SDD task includes review checkpoints:

```yaml
task_completion:
  self_review:
    - "All acceptance criteria met"
    - "AI review passed (no critical issues)"
    - "Tests added and passing"

  pr_review:
    - "Design doc alignment verified"
    - "Traceability links correct"
    - "No SDD deviations (or documented)"
```

### Reflexion Learning

Post-review insights feed back into SDD memory:

```yaml
reflexion:
  patterns_learned:
    - "What review patterns caught issues?"
    - "What did AI miss that humans caught?"

  improvements:
    - "Update AI rules for missed issues?"
    - "Add to self-review checklist?"
```

## File Structure

```
code-review-cycle/
├── README.md           # This file
├── checklist.md        # Review checklists (self, peer, security)
├── examples.md         # Good/bad review examples
├── templates.md        # PR templates, comment formats
└── llm-prompts.md      # AI-assisted review prompts
```

## References

### External

- [Google Engineering Practices - Code Review](https://google.github.io/eng-practices/review/)
- [Conventional Comments](https://conventionalcomments.org/)
- [CodeRabbit Documentation](https://docs.coderabbit.ai/)
- [GitHub Copilot Code Review](https://docs.github.com/en/copilot/using-github-copilot/code-review)

### Internal

- [Quality Gates Confidence](../quality-gates-confidence.md)
- [Reflexion Learning](../reflexion-learning.md)
- [faion-sdd-execution](../faion-sdd-execution/CLAUDE.md)

### Research

- [Evaluating LLMs for Code Review (2025)](https://arxiv.org/html/2505.20206v1)
- [AI-powered Code Review Early Results](https://arxiv.org/abs/2404.18496)
- [Addy Osmani - Code Review in the Age of AI](https://addyo.substack.com/p/code-review-in-the-age-of-ai)
