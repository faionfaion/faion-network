# LLM Prompts for Go Error Handling Patterns

Effective prompts for AI-assisted development with go error handling patterns.

## Architecture & Design Prompts

### Initial Design

```
I need to implement go error handling patterns for my project.

**Context:**
- Project type: [web app / API / microservice / CLI]
- Language: [Python / Go / Rust / Node.js]
- Scale: [X requests/sec, Y concurrent users]
- Infrastructure: [AWS / GCP / on-premise / Kubernetes]

**Requirements:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Constraints:**
- [Constraint 1]
- [Constraint 2]

**Please provide:**
1. Recommended architecture
2. Technology choices from: pkg/errors, Sentry, Logging
3. Implementation approach
4. Key trade-offs
5. Risk mitigations
```

### Technology Selection

```
Help me choose the best tool for go error handling patterns.

**Context:**
- Use case: [description]
- Scale: [metrics]
- Team expertise: [languages/tools]
- Budget: [constraints]

**Compare:**
- pkg/errors
- Sentry
- Logging

Provide comparison matrix with:
- Performance
- Complexity
- Ecosystem
- Cost
- Recommendation
```

---

## Implementation Prompts

### Generate Implementation

```
Generate go error handling patterns implementation for [language].

**Requirements:**
- Focus: Error patterns, recovery, logging
- Features:
  - [ ] [Feature 1]
  - [ ] [Feature 2]
  - [ ] [Feature 3]
- Error handling: [strategy]
- Testing: [unit/integration]

**Include:**
1. Core implementation
2. Error handling
3. Logging
4. Tests
5. Documentation
6. Usage examples
```

### Add Feature

```
Add [feature] to my existing go error handling patterns code.

**Current Code:**
[paste code]

**New Feature:**
- Description: [what to add]
- Requirements: [specs]
- Integration: [how it fits]

**Please:**
1. Suggest implementation approach
2. Provide code changes
3. Update tests
4. Document new behavior
```

---

## Optimization Prompts

### Performance Analysis

```
Analyze my go error handling patterns implementation for performance issues.

**Current Metrics:**
- [Metric 1]: [value]
- [Metric 2]: [value]
- Target: [goals]

**Code:**
[paste implementation]

**Please analyze:**
1. Bottlenecks
2. Inefficiencies
3. Optimization opportunities
4. Provide improved code
5. Expected improvements
```

### Refactoring

```
Refactor this go error handling patterns code for better maintainability.

**Current Issues:**
- [Issue 1]
- [Issue 2]
- [Issue 3]

**Code:**
[paste code]

**Goals:**
- Improve readability
- Reduce complexity
- Better error handling
- Enhanced testability

Provide refactored code with explanations.
```

---

## Troubleshooting Prompts

### Debug Issue

```
I'm experiencing [issue] with go error handling patterns.

**Error:**
[paste error message]

**Context:**
- Tool: pkg/errors
- Environment: [dev/staging/prod]
- Recent changes: [description]

**Logs:**
[paste relevant logs]

**Please help:**
1. Diagnose root cause
2. Suggest fixes
3. Provide prevention strategies
4. Update code if needed
```

### Best Practices Review

```
Review my go error handling patterns implementation for best practices.

**Code:**
[paste implementation]

**Review for:**
1. Code quality
2. Error handling
3. Security issues
4. Performance concerns
5. Testing gaps
6. Documentation completeness

Provide specific recommendations with improved code.
```

---

## Testing Prompts

### Generate Tests

```
Generate comprehensive tests for go error handling patterns.

**Code to test:**
[paste implementation]

**Test Requirements:**
- Unit tests (>80% coverage)
- Integration tests
- Edge cases
- Error scenarios
- Performance tests

**Framework:** [pytest / go test / cargo test / jest]

Include:
1. Test structure
2. Fixtures/mocks
3. Assertions
4. Coverage analysis
```

### Test Scenarios

```
What test scenarios should I cover for go error handling patterns?

**Implementation:**
[brief description]

**Context:**
- [Context 1]
- [Context 2]

**Please provide:**
1. Happy path scenarios
2. Edge cases
3. Error scenarios
4. Performance test cases
5. Test data examples
```

---

## Documentation Prompts

### Generate Documentation

```
Generate documentation for this go error handling patterns implementation.

**Code:**
[paste implementation]

**Documentation needs:**
- [ ] README with usage examples
- [ ] API documentation
- [ ] Architecture overview
- [ ] Troubleshooting guide
- [ ] Configuration reference

Format: Markdown with code examples
```

### Create Tutorial

```
Create step-by-step tutorial for implementing go error handling patterns.

**Target audience:** [junior/mid/senior developers]
**Prerequisites:** [required knowledge]
**Goal:** [learning objective]

**Please include:**
1. Introduction and motivation
2. Setup instructions
3. Step-by-step implementation
4. Code explanations
5. Common pitfalls
6. Next steps
```

---

## Migration Prompts

### Migrate Implementation

```
Migrate go error handling patterns from [old tool] to [new tool].

**Current Stack:**
- Tool: [current]
- Code: [paste snippet]

**Target Stack:**
- Tool: pkg/errors
- Requirements: [compatibility, features]

**Please provide:**
1. Migration strategy
2. Code transformation
3. Testing approach
4. Rollback plan
5. Timeline estimate
```

---

## Best Practices for LLM Prompts

### Do's

1. **Provide context** - System type, scale, constraints
2. **Specify tools** - Mention specific technologies
3. **Include code** - Show existing implementation
4. **Set goals** - Define success criteria
5. **Ask for trade-offs** - Compare approaches

### Don'ts

1. **Don't be vague** - Avoid "make it better"
2. **Don't omit scale** - Always mention traffic/data size
3. **Don't forget tests** - Request test coverage
4. **Don't skip errors** - Always include error handling

### Iterative Refinement

```
1. "Design go error handling patterns for [project]"
   -> Get architecture

2. "Generate implementation in [language]"
   -> Get code

3. "Add [feature] to the code"
   -> Enhance

4. "Generate tests"
   -> Add coverage

5. "Review for production readiness"
   -> Final check
```

---

## Quick Prompt Templates

### Implementation Template

```
Generate go error handling patterns in [language]:
- Feature: [description]
- Tool: pkg/errors
- Include: error handling, logging, tests

Output: production-ready code with docs
```

### Review Template

```
Review this go error handling patterns code:
[paste code]

Check:
1. Best practices
2. Performance
3. Security
4. Testability

Provide fixes with explanations.
```

### Debug Template

```
Debug go error handling patterns issue:
Error: [message]
Code: [paste]
Context: [details]

Diagnose and provide fix.
```
