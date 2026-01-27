# LLM Prompts for Code Review

Prompts for AI-assisted code review workflows.

## Pre-Review Prompts

### Self-Review Assistance

Use before creating a PR to catch obvious issues.

```markdown
Review this code change for a pull request. Focus on:

1. **Correctness**: Logic errors, edge cases, potential bugs
2. **Security**: Input validation, injection risks, auth issues
3. **Performance**: N+1 queries, unnecessary allocations, inefficient algorithms
4. **Readability**: Naming, organization, comments
5. **Testing**: Missing test cases, inadequate coverage

For each issue found:
- State the category
- Quote the problematic code
- Explain why it's a problem
- Suggest a fix

If you find no issues in a category, say "No issues found."

Do NOT comment on:
- Formatting (handled by linter)
- Import order
- Subjective style preferences

Code to review:
```
[paste diff or code]
```

Context:
- Language/framework: [e.g., TypeScript/React]
- This code does: [brief description]
```

### Security-Focused Review

```markdown
Perform a security review of this code. Check for:

## OWASP Top 10
- [ ] Injection (SQL, NoSQL, Command, LDAP)
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XML External Entities (XXE)
- [ ] Broken Access Control
- [ ] Security Misconfiguration
- [ ] Cross-Site Scripting (XSS)
- [ ] Insecure Deserialization
- [ ] Using Components with Known Vulnerabilities
- [ ] Insufficient Logging & Monitoring

## Additional Checks
- [ ] Hardcoded secrets or credentials
- [ ] Improper error handling (information leakage)
- [ ] Missing rate limiting
- [ ] CORS misconfiguration
- [ ] Missing CSRF protection

For each finding:
- Severity: Critical / High / Medium / Low
- Location: file:line
- Issue: Description
- Risk: What could happen
- Fix: Recommended remediation
- Reference: CWE or OWASP link

Code to review:
```
[paste code]
```
```

### Test Coverage Analysis

```markdown
Analyze this code and its tests. Identify:

1. **Untested code paths**: Functions or branches without tests
2. **Missing edge cases**: Boundary conditions not tested
3. **Inadequate assertions**: Tests that pass but don't verify much
4. **Missing error scenarios**: Error handling not tested

For each gap, suggest a specific test case:
- Test name: `test_[scenario]_[expected_result]`
- Setup: What to prepare
- Action: What to call
- Assert: What to verify

Code:
```
[paste implementation]
```

Tests:
```
[paste tests]
```
```

---

## During-Review Prompts

### Understand Complex Code

```markdown
Explain this code in detail:

1. What does it do? (high-level purpose)
2. How does it work? (step-by-step logic)
3. Why might it be written this way? (design decisions)
4. What are the edge cases?
5. What could go wrong?

Code:
```
[paste code]
```

Context: This is part of [system/feature description]
```

### Compare Approaches

```markdown
Compare these two implementations:

**Approach A:**
```
[code A]
```

**Approach B:**
```
[code B]
```

Compare on:
1. Correctness: Do both handle all cases?
2. Performance: Time and space complexity
3. Readability: Which is clearer?
4. Maintainability: Which is easier to modify?
5. Testability: Which is easier to test?

Recommendation: Which approach is better for [context], and why?
```

### Generate Review Comments

```markdown
Generate code review comments for this diff. Use these prefixes:

- [Required]: Must fix before merge
- [Suggestion]: Consider this improvement
- [Question]: Need clarification
- [Nitpick]: Minor preference
- [Nice]: Positive feedback

Format each comment as:
```
[Prefix] Line X: Comment text

[Code snippet if relevant]

[Suggested fix if applicable]
```

Focus on substance over style. Prioritize:
1. Bugs and correctness issues
2. Security vulnerabilities
3. Performance problems
4. Design and architecture
5. Readability (only if significantly impacted)

Diff to review:
```
[paste diff]
```

Project context: [language, framework, coding standards]
```

### Validate Against Design Doc

```markdown
Compare this implementation against the design document.

**Design Document:**
```
[paste relevant design sections]
```

**Implementation:**
```
[paste code]
```

Check:
1. Does the implementation match the design?
2. Are there deviations? If so, are they improvements or problems?
3. Are all design requirements addressed?
4. Are there implementation details not covered by design?

For each deviation, assess:
- Severity: Breaking / Minor / Improvement
- Should design be updated, or code be fixed?
```

---

## Post-Review Prompts

### Summarize Review Findings

```markdown
Summarize these code review comments into a structured report:

**Comments:**
[paste all review comments]

Generate:

## Summary
[1-2 sentence overview]

## Critical Issues (must fix)
- Issue 1: [description]
- Issue 2: [description]

## Suggestions (should consider)
- Suggestion 1: [description]

## Minor Items (optional)
- Item 1: [description]

## Positive Highlights
- [Good patterns observed]

## Metrics
- Total comments: X
- Required changes: Y
- Suggestions: Z
- Questions: W
```

### Generate Commit Message for Fixes

```markdown
Generate a commit message for these review feedback fixes:

**Original PR description:**
[paste PR description]

**Review comments addressed:**
[paste addressed comments]

**Changes made:**
[paste diff of fixes]

Generate a commit message following this format:
- First line: type: short description (50 chars max)
- Body: What was fixed and why (if needed)

Types: fix, refactor, perf, security, docs, test
```

### Create Follow-Up Tasks

```markdown
Based on this code review, create follow-up tasks for items
that were out of scope but should be addressed later.

**Review comments deferred:**
[paste deferred items]

For each item, create a task:

## Task: [Title]
**Priority:** High / Medium / Low
**Type:** Bug / Enhancement / Tech Debt / Security
**Description:**
[What needs to be done and why]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Context:**
[Link to PR and relevant discussion]
```

---

## Specialized Review Prompts

### API Review

```markdown
Review this API endpoint implementation:

```
[paste endpoint code]
```

Check:
## Request Handling
- [ ] Input validation complete
- [ ] Required fields enforced
- [ ] Types validated
- [ ] Size limits enforced

## Response Format
- [ ] Consistent with API standards
- [ ] Error responses informative but safe
- [ ] Status codes appropriate
- [ ] Content-type correct

## Security
- [ ] Authentication required/checked
- [ ] Authorization verified
- [ ] Rate limiting in place
- [ ] No sensitive data leaked

## Performance
- [ ] Database queries optimized
- [ ] Response pagination if needed
- [ ] Caching considered
- [ ] Async operations where appropriate

## Documentation
- [ ] OpenAPI/Swagger updated
- [ ] Examples provided
- [ ] Error cases documented

Generate specific feedback for any issues found.
```

### Database Query Review

```markdown
Review these database queries for issues:

```
[paste queries]
```

Check:
1. **SQL Injection**: Are parameters properly escaped?
2. **N+1 Queries**: Are there loops with queries inside?
3. **Missing Indexes**: Will queries need full table scans?
4. **Over-fetching**: Are we selecting more than needed?
5. **Transactions**: Are related operations atomic?
6. **Locking**: Could this cause deadlocks?

For each issue:
- Quote the problematic query
- Explain the problem
- Show the optimized version
- Estimate performance impact
```

### React Component Review

```markdown
Review this React component:

```
[paste component code]
```

Check:
## Correctness
- [ ] Props typed correctly
- [ ] State managed appropriately
- [ ] Effects have correct dependencies
- [ ] Cleanup functions where needed

## Performance
- [ ] Unnecessary re-renders avoided
- [ ] useMemo/useCallback used appropriately
- [ ] Large lists virtualized
- [ ] Images optimized

## Accessibility
- [ ] Semantic HTML used
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus management correct

## Best Practices
- [ ] Component is focused (single responsibility)
- [ ] Props are reasonable (not too many)
- [ ] Custom hooks extracted where useful
- [ ] Error boundaries in place

Generate specific feedback with code suggestions.
```

---

## AI Review Tool Commands

### CodeRabbit Chat Commands

```markdown
@coderabbitai summary
# Generates high-level summary of changes

@coderabbitai review
# Triggers full review

@coderabbitai explain [file or function]
# Explains specific code

@coderabbitai suggest improvements for [file]
# Focused improvement suggestions

@coderabbitai check security
# Security-focused review

@coderabbitai ignore [comment]
# Dismiss specific suggestion
```

### GitHub Copilot Commands

```markdown
@copilot review
# Basic review

@copilot explain this code
# Code explanation

@copilot suggest tests
# Test suggestions

@copilot find bugs
# Bug-focused review
```

### Claude Code Commands

```markdown
/review [file or PR]
# General review

/review --security [file]
# Security focus

/review --performance [file]
# Performance focus

/explain [function or code block]
# Detailed explanation
```

---

## Multi-Model Review Workflow

```markdown
## Step 1: Initial AI Review (Fast Model)

Prompt: "Quick review for obvious issues: bugs, security, performance"
Model: GPT-4-turbo or Claude Haiku
Goal: Fast feedback on clear issues

## Step 2: Deep Analysis (Capable Model)

Prompt: "Detailed review: design patterns, edge cases, architecture fit"
Model: GPT-4 or Claude Sonnet/Opus
Goal: Thorough analysis of subtle issues

## Step 3: Security Scan (Specialized)

Tool: Semgrep, CodeQL, or specialized security model
Goal: Catch security-specific patterns

## Step 4: Human Review

Focus: Business logic, architecture decisions, team conventions
Goal: Final approval with full context

## Combining Results

Merge findings from all steps:
1. De-duplicate (AI models often find same issues)
2. Prioritize (security > correctness > design > style)
3. Validate (human confirms AI findings)
4. Document (capture rationale for decisions)
```
