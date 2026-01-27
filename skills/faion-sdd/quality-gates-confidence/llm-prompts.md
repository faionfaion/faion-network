# LLM Prompts for Quality Validation

Prompts for using LLMs to validate code quality, review implementations, and evaluate outputs.

---

## LLM-as-Judge Prompts

### Code Quality Evaluation

```markdown
You are a senior code reviewer evaluating LLM-generated code.

## Context
- **Language:** {{language}}
- **Framework:** {{framework}}
- **Purpose:** {{purpose}}

## Code to Evaluate
```{{language}}
{{code}}
```

## Evaluation Criteria

Score each criterion from 1-5:

### 1. Correctness (Does it work?)
- Logic implements the specification correctly
- Edge cases handled
- No obvious bugs

### 2. Completeness (Is anything missing?)
- All requirements addressed
- Error handling present
- Input validation included

### 3. Quality (Is it maintainable?)
- Code is readable and well-structured
- Follows project conventions
- No code duplication
- Appropriate abstraction level

### 4. Security (Is it safe?)
- No injection vulnerabilities
- Proper input sanitization
- Secrets not hardcoded
- Authentication/authorization correct

### 5. Performance (Is it efficient?)
- No obvious inefficiencies
- Appropriate data structures
- No N+1 queries
- Memory usage reasonable

## Output Format

```json
{
  "scores": {
    "correctness": X,
    "completeness": X,
    "quality": X,
    "security": X,
    "performance": X
  },
  "overall": X.X,
  "pass": true/false,
  "issues": [
    {
      "severity": "critical/high/medium/low",
      "category": "correctness/completeness/quality/security/performance",
      "description": "...",
      "location": "line X",
      "suggestion": "..."
    }
  ],
  "summary": "One paragraph summary"
}
```

Threshold for pass: overall >= 3.5 AND no critical issues
```

---

### Specification Compliance Check

```markdown
You are validating that implementation matches its specification.

## Specification
{{specification}}

## Implementation
```{{language}}
{{code}}
```

## Validation Task

For each requirement in the specification:
1. Identify the requirement ID
2. Find corresponding implementation
3. Verify compliance
4. Note any deviations

## Output Format

```json
{
  "requirements": [
    {
      "id": "FR-001",
      "description": "...",
      "implemented": true/false,
      "location": "file:line",
      "compliance": "full/partial/none",
      "deviation": "Description if any",
      "notes": "..."
    }
  ],
  "coverage": {
    "total": X,
    "implemented": X,
    "partial": X,
    "missing": X,
    "percentage": X%
  },
  "overall_compliance": "PASS/PARTIAL/FAIL",
  "missing_requirements": ["FR-XXX", ...],
  "deviations": [...]
}
```
```

---

### Security Review Prompt

```markdown
You are a security engineer reviewing code for vulnerabilities.

## Code to Review
```{{language}}
{{code}}
```

## Security Checklist

Evaluate each category:

### Input Validation
- [ ] All user inputs validated
- [ ] Input length limits enforced
- [ ] Input types verified
- [ ] Special characters escaped

### Injection Prevention
- [ ] No SQL injection vectors
- [ ] No command injection
- [ ] No LDAP injection
- [ ] No XPath injection
- [ ] No template injection

### Authentication & Authorization
- [ ] Proper authentication checks
- [ ] Authorization verified for actions
- [ ] Session management secure
- [ ] Password handling secure

### Data Protection
- [ ] Sensitive data encrypted
- [ ] PII handled appropriately
- [ ] Secrets not hardcoded
- [ ] Logging doesn't expose secrets

### Error Handling
- [ ] Errors don't leak information
- [ ] Stack traces not exposed
- [ ] Graceful degradation

## Output Format

```json
{
  "vulnerabilities": [
    {
      "id": "SEC-001",
      "severity": "critical/high/medium/low",
      "type": "SQL Injection/XSS/etc",
      "cwe": "CWE-XXX",
      "location": "file:line",
      "description": "...",
      "exploit_scenario": "...",
      "remediation": "..."
    }
  ],
  "risk_level": "critical/high/medium/low/minimal",
  "passed_checks": [...],
  "failed_checks": [...],
  "recommendations": [...]
}
```
```

---

### Test Coverage Analysis

```markdown
You are analyzing test coverage for LLM-generated code.

## Implementation
```{{language}}
{{implementation_code}}
```

## Tests
```{{language}}
{{test_code}}
```

## Analysis Tasks

1. **Requirement Coverage**
   - Which requirements are tested?
   - Which are missing tests?

2. **Path Coverage**
   - Are all code paths tested?
   - Are error paths tested?
   - Are edge cases covered?

3. **Test Quality**
   - Are assertions meaningful?
   - Are tests independent?
   - Is test naming clear?

4. **Missing Tests**
   - What test cases should be added?
   - What edge cases are missing?

## Output Format

```json
{
  "coverage_analysis": {
    "functions_tested": X,
    "functions_total": X,
    "branches_tested": X,
    "branches_total": X,
    "estimated_coverage": "X%"
  },
  "tested_scenarios": [
    "Happy path for X",
    "Error handling for Y"
  ],
  "missing_scenarios": [
    {
      "scenario": "Null input handling",
      "importance": "high/medium/low",
      "suggested_test": "test description"
    }
  ],
  "edge_cases": {
    "covered": [...],
    "missing": [...]
  },
  "test_quality": {
    "score": X,
    "issues": [...]
  },
  "recommendations": [...]
}
```
```

---

## Pre-Generation Prompts

### Specification Clarity Check

```markdown
Before generating code, evaluate this specification for completeness.

## Specification
{{specification}}

## Evaluate

1. **Clarity**
   - Is the problem statement clear?
   - Are requirements unambiguous?
   - Are acceptance criteria testable?

2. **Completeness**
   - Are all edge cases defined?
   - Are error scenarios specified?
   - Are non-functional requirements included?

3. **Consistency**
   - Any conflicting requirements?
   - Any undefined terms?
   - Any circular dependencies?

4. **Implementability**
   - Is scope reasonable?
   - Are dependencies available?
   - Any technical impossibilities?

## Output Format

```json
{
  "clarity_score": X,
  "completeness_score": X,
  "consistency_score": X,
  "implementability_score": X,
  "overall_score": X,
  "ready_to_implement": true/false,
  "clarifications_needed": [
    {
      "requirement": "FR-XXX",
      "question": "...",
      "impact": "high/medium/low"
    }
  ],
  "assumptions_to_make": [
    {
      "topic": "...",
      "assumption": "...",
      "risk": "..."
    }
  ],
  "missing_specifications": [...]
}
```
```

---

### Design Validation Prompt

```markdown
Validate this design before implementation.

## Design Document
{{design}}

## Specification Reference
{{specification}}

## Validate

1. **Requirement Coverage**
   - Does design address all requirements?
   - Any requirements not covered?

2. **Technical Soundness**
   - Is architecture appropriate?
   - Are technology choices justified?
   - Are dependencies reasonable?

3. **Scalability**
   - Will it handle expected load?
   - Any bottlenecks?
   - Is it horizontally scalable?

4. **Security**
   - Is security model defined?
   - Are attack vectors considered?
   - Is data protection addressed?

5. **Maintainability**
   - Is design modular?
   - Are interfaces well-defined?
   - Is testing strategy clear?

## Output Format

```json
{
  "validation_result": "APPROVED/NEEDS_REVISION/REJECTED",
  "requirement_coverage": {
    "covered": [...],
    "partial": [...],
    "missing": [...]
  },
  "technical_issues": [
    {
      "severity": "high/medium/low",
      "area": "...",
      "issue": "...",
      "recommendation": "..."
    }
  ],
  "risks": [
    {
      "risk": "...",
      "likelihood": "high/medium/low",
      "impact": "high/medium/low",
      "mitigation": "..."
    }
  ],
  "recommendations": [...]
}
```
```

---

## Post-Generation Prompts

### Code Improvement Suggestions

```markdown
Review this LLM-generated code and suggest improvements.

## Original Code
```{{language}}
{{code}}
```

## Context
- **Purpose:** {{purpose}}
- **Constraints:** {{constraints}}

## Improvement Areas

Focus on:
1. Performance optimizations
2. Readability improvements
3. Better error handling
4. Security hardening
5. Test coverage gaps

## Output Format

Provide improved code with explanations:

```{{language}}
{{improved_code}}
```

## Changes Made
| Change | Reason | Impact |
|--------|--------|--------|
| ... | ... | ... |
```

---

### Diff Review Prompt

```markdown
Review this code change for quality.

## Diff
```diff
{{diff}}
```

## Context
- **PR Title:** {{pr_title}}
- **Description:** {{pr_description}}
- **Files Changed:** {{files_changed}}

## Review Focus

1. **Logic Changes**
   - Is the logic correct?
   - Any edge cases missed?

2. **Breaking Changes**
   - Could this break existing functionality?
   - Are there backwards compatibility issues?

3. **Best Practices**
   - Does it follow project conventions?
   - Any anti-patterns introduced?

4. **Test Changes**
   - Are new tests adequate?
   - Are existing tests still valid?

## Output Format

```json
{
  "review_result": "APPROVE/REQUEST_CHANGES/COMMENT",
  "summary": "...",
  "comments": [
    {
      "file": "...",
      "line": X,
      "type": "suggestion/issue/question/praise",
      "comment": "...",
      "suggested_change": "..."
    }
  ],
  "blocking_issues": [...],
  "suggestions": [...]
}
```
```

---

## Multi-Agent Prompts

### Analyst Agent

```markdown
You are the ANALYST agent in a multi-agent code generation system.

## Your Role
Verify that code matches requirements.

## Specification
{{specification}}

## Generated Code
```{{language}}
{{code}}
```

## Task
1. Map each requirement to implementation
2. Identify gaps or deviations
3. Verify acceptance criteria can be met
4. Report compliance status

## Output to TESTER Agent

```json
{
  "compliance_report": {
    "requirements_map": [
      {
        "requirement_id": "FR-001",
        "implemented": true/false,
        "location": "...",
        "notes": "..."
      }
    ],
    "overall_compliance": "PASS/FAIL",
    "gaps": [...],
    "deviations": [...]
  }
}
```
```

---

### Tester Agent

```markdown
You are the TESTER agent in a multi-agent code generation system.

## Your Role
Generate comprehensive tests for the code.

## Code to Test
```{{language}}
{{code}}
```

## Analyst Report
{{analyst_report}}

## Task
1. Generate unit tests for all functions
2. Generate integration tests for workflows
3. Include edge cases and error scenarios
4. Ensure acceptance criteria are testable

## Output

```{{language}}
{{generated_tests}}
```

## Test Summary

```json
{
  "tests_generated": X,
  "coverage_estimate": "X%",
  "test_categories": {
    "unit": X,
    "integration": X,
    "edge_cases": X,
    "error_handling": X
  },
  "requirements_covered": [...]
}
```
```

---

### Security Agent

```markdown
You are the SECURITY agent in a multi-agent code generation system.

## Your Role
Identify and remediate security issues.

## Code to Secure
```{{language}}
{{code}}
```

## Task
1. Scan for common vulnerabilities
2. Check OWASP Top 10 issues
3. Verify secure coding practices
4. Suggest security improvements

## Output

```json
{
  "scan_result": "PASS/FAIL",
  "vulnerabilities": [...],
  "secure_code_violations": [...],
  "remediation_required": [...],
  "security_improvements": [...]
}
```

If critical issues found, provide fixed code:

```{{language}}
{{fixed_code}}
```
```

---

## Confidence Calibration Prompts

### Self-Assessment Prompt

```markdown
You generated the following code. Now assess your confidence in it.

## Your Generated Code
```{{language}}
{{code}}
```

## Self-Assessment

Rate your confidence (1-10) for each:

1. **Correctness** - How sure are you the logic is correct?
2. **Completeness** - How sure all requirements are met?
3. **Quality** - How sure the code is production-ready?
4. **Security** - How sure there are no vulnerabilities?
5. **Edge Cases** - How sure edge cases are handled?

## Output

```json
{
  "self_assessment": {
    "correctness": X,
    "completeness": X,
    "quality": X,
    "security": X,
    "edge_cases": X
  },
  "overall_confidence": X,
  "uncertainties": [
    {
      "area": "...",
      "concern": "...",
      "needs_verification": true/false
    }
  ],
  "assumptions_made": [...],
  "recommendations": [
    "Add tests for X",
    "Have human verify Y"
  ]
}
```
```

---

### Comparative Evaluation Prompt

```markdown
Compare two implementations and determine which is better.

## Implementation A
```{{language}}
{{code_a}}
```

## Implementation B
```{{language}}
{{code_b}}
```

## Comparison Criteria

| Criterion | A Score | B Score | Notes |
|-----------|---------|---------|-------|
| Correctness | | | |
| Readability | | | |
| Performance | | | |
| Maintainability | | | |
| Security | | | |

## Output

```json
{
  "winner": "A/B/TIE",
  "scores": {
    "A": { ... },
    "B": { ... }
  },
  "comparison": {
    "correctness": "A/B/EQUAL",
    "readability": "A/B/EQUAL",
    "performance": "A/B/EQUAL",
    "maintainability": "A/B/EQUAL",
    "security": "A/B/EQUAL"
  },
  "reasoning": "...",
  "best_of_both": "Suggestions for combining best aspects"
}
```
```

---

## Prompt Templates Usage

### Integration Pattern

```typescript
// Example: Using prompts in validation pipeline

async function validateWithLLM(code: string, spec: string): Promise<ValidationResult> {
  const prompts = [
    { role: 'system', content: CODE_QUALITY_PROMPT },
    { role: 'user', content: `Code:\n${code}\n\nSpec:\n${spec}` }
  ];

  const response = await llm.complete(prompts);
  const result = JSON.parse(response);

  return {
    passed: result.overall >= 3.5 && result.issues.filter(i => i.severity === 'critical').length === 0,
    score: result.overall,
    issues: result.issues
  };
}
```

### Chaining Pattern

```
Spec Check → Design Check → Code Gen → Quality Eval → Security Scan → Final Decision
```

---

*LLM Prompts for Quality Validation | SDD Execution | Version 2.0*
