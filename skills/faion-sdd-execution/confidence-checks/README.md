---
id: confidence-checks
name: "Confidence Checks"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Confidence Checks

## Problem

AI-assisted development introduces challenges:
- AI-generated code may contain hallucinations or errors
- Confidence in outputs varies significantly
- No systematic way to assess reliability
- Uncertainty areas often ignored

**Root cause:** No confidence assessment framework for AI outputs.

## Confidence Levels

| Level | Score | Meaning | Action |
|-------|-------|---------|--------|
| **High** | 90-100% | Very confident, verified | Proceed |
| **Medium** | 70-89% | Likely correct, needs review | Review before use |
| **Low** | 50-69% | Uncertain, may have issues | Deep review required |
| **Very Low** | <50% | Probably wrong | Regenerate or manual fix |

## Confidence Check Process

```
GENERATE → ASSESS → VERIFY → DECIDE
            ↓         ↓
        UNCERTAIN → REVIEW → RE-ASSESS
```

1. **Generate:** AI creates output (code, design, etc.)
2. **Assess:** Evaluate confidence across multiple aspects
3. **Verify:** Gather evidence through testing, review
4. **Decide:** Use as-is, review first, or regenerate
5. **Review:** Address areas of uncertainty
6. **Re-assess:** Update confidence after review

## Template

```markdown
## Confidence Check: [Task/Output]

**Date:** YYYY-MM-DD
**Author/Source:** [Human/AI Agent]

### Confidence Assessment

| Aspect | Confidence | Notes |
|--------|------------|-------|
| Correctness | High/Med/Low | [Notes] |
| Completeness | High/Med/Low | [Notes] |
| Best Practices | High/Med/Low | [Notes] |
| Security | High/Med/Low | [Notes] |
| Performance | High/Med/Low | [Notes] |

### Overall Confidence: [X]%

### Evidence

- [ ] Tested manually
- [ ] Unit tests pass
- [ ] Reviewed by human
- [ ] Compared to reference implementation
- [ ] Verified against documentation

### Verification Steps Taken

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Areas of Uncertainty

- [Area 1]: [Why uncertain]
- [Area 2]: [Why uncertain]

### Recommendation

- [ ] Use as-is (high confidence)
- [ ] Use after review (medium confidence)
- [ ] Regenerate/rework (low confidence)
```

## Example: Auth Middleware

```markdown
## Confidence Check: Auth Middleware

**Source:** faion-code-agent
**Task:** TASK-010 - Implement auth middleware

### Confidence Assessment

| Aspect | Confidence | Notes |
|--------|------------|-------|
| Correctness | Medium (75%) | Logic looks right, needs testing |
| Completeness | High (90%) | All requirements covered |
| Best Practices | Medium (70%) | JWT handling standard |
| Security | Medium (65%) | Need to verify token validation |
| Performance | High (85%) | Simple middleware, no concerns |

### Overall Confidence: 77%

### Evidence

- [x] Code compiles without errors
- [x] Unit tests written and pass
- [ ] Reviewed by human ← NEEDED
- [x] Compared to Express middleware patterns
- [x] Verified JWT library usage

### Areas of Uncertainty

1. **Token expiration handling:** Not sure if edge cases covered
2. **Error messages:** May leak information
3. **Rate limiting:** Not implemented, spec was unclear

### Verification Steps Needed

1. Human review of security aspects
2. Test with expired tokens
3. Test with malformed tokens
4. Confirm rate limiting requirements

### Recommendation

- [ ] Use as-is
- [x] Use after review - human should verify security
- [ ] Regenerate/rework
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 100% confidence claims | Even experts have uncertainty - be honest |
| Ignoring low-confidence areas | Address them before production |
| No evidence gathering | Always verify with tests or review |
| Skipping uncertainty documentation | Document what you're unsure about |

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Executing design patterns | haiku | Pattern application, code generation |
| Reviewing implementation against spec | sonnet | Quality assurance, consistency check |
| Resolving design-execution conflicts | opus | Trade-off analysis, adaptive decisions |

## Sources

- [AI Confidence Calibration](https://arxiv.org/abs/2207.08799)
- [Hallucination Detection in LLMs](https://arxiv.org/abs/2305.14975)
- [Software Quality Assurance](https://www.atlassian.com/software-quality)
- [Code Review Best Practices](https://google.github.io/eng-practices/review/)
- [AI-Assisted Development Risks](https://github.blog/2023-06-29-responsible-use-of-ai-in-coding/)
