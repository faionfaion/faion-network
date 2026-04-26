# LLM Prompts for Python Code Quality

Effective prompts for AI-assisted code review, refactoring, and quality improvement.

---

## General Code Review

### Comprehensive Code Review

```
Review this Python code for:
1. **Correctness**: Does it do what it's supposed to?
2. **Type safety**: Are type hints complete and correct?
3. **Error handling**: Are exceptions handled appropriately?
4. **Clean code**: Does it follow SOLID principles?
5. **Security**: Any potential vulnerabilities?
6. **Performance**: Any obvious inefficiencies?

Code:
```python
[paste code here]
```

Provide specific suggestions with code examples for each issue found.
```

### Quick Review (Style & Bugs)

```
Quickly review this Python code for:
- Style issues (PEP 8, naming)
- Common bugs (mutable defaults, bare except, etc.)
- Missing type hints
- Potential None/null issues

Code:
```python
[paste code here]
```

List issues with line numbers and one-line fixes.
```

### Review Against Standards

```
Review this code against our project standards:
- Line length: 88
- Type hints required for all public functions
- Google-style docstrings
- No bare except clauses
- Constants in UPPER_SNAKE_CASE

Code:
```python
[paste code here]
```
```

---

## SOLID Principles Analysis

### Check Single Responsibility

```
Analyze this class for Single Responsibility Principle violations:

```python
[paste class code here]
```

Questions to answer:
1. What are all the responsibilities of this class?
2. Are any responsibilities that should be separate?
3. Does this class have more than one reason to change?
4. Suggest how to split if violations found.
```

### Check Dependency Inversion

```
Analyze this code for Dependency Inversion Principle:

```python
[paste code here]
```

Identify:
1. What concrete implementations does this code depend on?
2. Are there hardcoded dependencies that should be injected?
3. What abstractions (Protocols/ABCs) should be introduced?
4. Show refactored code with proper dependency injection.
```

### Full SOLID Analysis

```
Perform a SOLID principles analysis on this code:

```python
[paste code here]
```

For each principle (S, O, L, I, D):
1. Does the code follow the principle? (Yes/Partially/No)
2. What specific violations exist?
3. How would you fix them? (Show code)
```

---

## Type Hints & mypy

### Add Type Hints

```
Add complete type hints to this Python code:
- Use modern Python 3.10+ syntax (X | None instead of Optional[X])
- Use built-in generics (list[str] instead of List[str])
- Add return types including -> None
- Use TypedDict for dict structures
- Use Protocol for duck typing interfaces

Code:
```python
[paste code here]
```

Explain any complex type annotations.
```

### Fix mypy Errors

```
Help me fix these mypy errors:

Error messages:
[paste mypy output]

Code:
```python
[paste code here]
```

For each error:
1. Explain why it occurs
2. Show the fix
3. Explain if there's a better design approach
```

### Convert to Strict Mode

```
This code runs with mypy's default settings. Convert it to pass strict mode:

```python
[paste code here]
```

Consider:
- Explicit type annotations everywhere
- Proper handling of Optional types
- No implicit Any
- Proper return types
```

---

## Clean Code Refactoring

### Simplify Complex Function

```
This function is too complex. Refactor it:
- Split into smaller functions (max 20 lines each)
- Use early returns instead of nested if/else
- Extract magic numbers to named constants
- Improve naming to be self-documenting

Current code:
```python
[paste code here]
```

Show the refactored version with explanations.
```

### Reduce Nesting

```
Reduce the nesting depth in this code using guard clauses and early returns:

```python
[paste code here]
```

Target: Maximum 2 levels of indentation in the main logic.
```

### Improve Naming

```
Improve variable and function names in this code:
- Names should reveal intent
- Names should be pronounceable and searchable
- Use domain terminology
- Avoid abbreviations

Code:
```python
[paste code here]
```

Explain your naming choices.
```

### Extract Method

```
This function does too many things. Apply "Extract Method" refactoring:

```python
[paste code here]
```

Split into cohesive, single-purpose functions with clear names.
```

---

## Documentation

### Generate Docstrings

```
Generate Google-style docstrings for these functions/classes:

```python
[paste code here]
```

Include:
- One-line summary (imperative mood)
- Detailed description if complex
- Args with types and descriptions
- Returns with type and description
- Raises with exception types and conditions
- Example usage for complex functions
```

### Improve Existing Docstrings

```
Improve these docstrings:
- Make them more informative
- Add missing sections (Args, Returns, Raises)
- Include usage examples
- Fix any incorrect information based on the code

Code:
```python
[paste code here]
```
```

### Generate Module Docstring

```
Generate a module-level docstring for this Python file:

```python
[paste module code here]
```

Include:
- Module purpose
- Main classes/functions
- Usage example
- Any important notes/caveats
```

---

## Error Handling

### Review Error Handling

```
Review the error handling in this code:

```python
[paste code here]
```

Check for:
1. Bare except clauses
2. Silently swallowed exceptions
3. Missing exception handling
4. Generic exceptions instead of specific
5. Lost exception context (not using "from e")
6. Proper resource cleanup (context managers)

Suggest improvements with code examples.
```

### Add Custom Exceptions

```
This code uses generic exceptions. Create appropriate custom exceptions:

```python
[paste code here]
```

For each custom exception:
1. Name following XxxError convention
2. Inherit from appropriate base (ValueError, RuntimeError, etc.)
3. Include relevant context in the exception
4. Show updated code using the exceptions
```

### Add Error Handling

```
Add proper error handling to this code:

```python
[paste code here]
```

Consider:
- What can fail? (I/O, network, validation, etc.)
- What exceptions should be caught?
- How should errors be communicated?
- Should any be logged? Re-raised?
```

---

## Testing

### Generate Unit Tests

```
Generate pytest unit tests for this code:

```python
[paste code here]
```

Include:
- Happy path tests
- Edge cases
- Error conditions
- Use pytest fixtures where appropriate
- Use parametrize for multiple test cases
- Mock external dependencies
```

### Review Test Quality

```
Review these tests for quality:

```python
[paste test code here]
```

Check:
1. Are all paths tested?
2. Are edge cases covered?
3. Are assertions meaningful (not just "doesn't crash")?
4. Is test isolation maintained?
5. Are mocks used appropriately?
6. Is the test naming clear (test_<function>_<scenario>_<expected>)?
```

### Suggest Missing Tests

```
Here's a function and its tests. What test cases are missing?

Function:
```python
[paste function]
```

Current tests:
```python
[paste tests]
```

List missing test scenarios and provide code.
```

---

## Performance

### Review for Performance

```
Review this code for performance issues:

```python
[paste code here]
```

Check for:
1. N+1 queries (if database involved)
2. Inefficient algorithms (O(n^2) where O(n) possible)
3. Repeated expensive operations in loops
4. Missing caching opportunities
5. Inefficient data structures
6. Unnecessary object creation
```

### Optimize Algorithm

```
Optimize this algorithm for better time/space complexity:

```python
[paste code here]
```

Show:
1. Current complexity analysis
2. Optimized version
3. New complexity analysis
4. Trade-offs made
```

---

## Security

### Security Review

```
Review this Python code for security vulnerabilities:

```python
[paste code here]
```

Check for:
1. SQL injection
2. Command injection
3. Path traversal
4. Hardcoded secrets
5. Unsafe deserialization
6. SSRF vulnerabilities
7. Improper input validation
8. Information disclosure in errors

For each issue, explain the risk and show the fix.
```

### Secure Input Handling

```
Add proper input validation and sanitization to this code:

```python
[paste code here]
```

Consider:
- Type validation
- Length limits
- Format validation
- Sanitization for output context
- Fail securely
```

---

## Refactoring Patterns

### Extract Class

```
This class has grown too large. Apply "Extract Class" to break it up:

```python
[paste code here]
```

Identify cohesive groups of methods and data that should be separate classes.
```

### Replace Conditionals with Polymorphism

```
Replace the conditional logic in this code with polymorphism:

```python
[paste code here]
```

Show:
1. Base class or Protocol
2. Concrete implementations
3. How the client code changes
```

### Introduce Strategy Pattern

```
Refactor this code to use the Strategy pattern:

```python
[paste code here]
```

This will allow adding new [strategies/algorithms/behaviors] without modifying existing code.
```

---

## Context Packing Prompts

### Code Review with Context

```
Review this pull request:

**Context:**
- Project: [project description]
- This code handles: [feature/module description]
- Standards: Ruff, mypy strict, 80% coverage required
- Framework: [Django/FastAPI/etc.]

**Changes:**
```python
[paste code changes]
```

**Related code** (for context):
```python
[paste related code]
```

Review for correctness, style, and consistency with the codebase.
```

### Refactoring with Constraints

```
Refactor this code with these constraints:
- Must maintain backward compatibility
- Must not change public API signatures
- Must keep test coverage above 80%
- Framework: [Django/FastAPI/etc.]
- Python version: 3.11+

Current code:
```python
[paste code]
```

Current tests:
```python
[paste tests]
```

Show refactored code and updated tests.
```

---

## Quick Prompts (One-Liners)

| Task | Prompt |
|------|--------|
| Add type hints | "Add complete Python 3.10+ type hints to this code: [code]" |
| Fix bare except | "Replace bare except clauses with specific exceptions: [code]" |
| Add docstrings | "Add Google-style docstrings to all public functions: [code]" |
| Simplify | "Simplify this code while maintaining functionality: [code]" |
| Name variables | "Suggest better names for variables in this code: [code]" |
| Find bugs | "Find potential bugs in this Python code: [code]" |
| Security check | "Check this code for security vulnerabilities: [code]" |
| Generate tests | "Generate pytest tests for this function: [code]" |
| Explain code | "Explain what this Python code does step by step: [code]" |
| Modernize | "Update this code to use Python 3.11+ features: [code]" |

---

## Batch Processing Prompts

### Review Multiple Files

```
Review these files as a cohesive module:

**File 1: models.py**
```python
[paste]
```

**File 2: services.py**
```python
[paste]
```

**File 3: api.py**
```python
[paste]
```

Check:
1. Consistency across files
2. Proper separation of concerns
3. Correct dependencies between layers
4. Type hint consistency
```

### Audit Entire Module

```
Audit this Python module:

```
[paste entire module or directory listing]
```

Rate (1-5) and comment on:
1. Code organization
2. Naming consistency
3. Type coverage
4. Documentation coverage
5. Test coverage
6. Error handling
7. SOLID compliance

Provide prioritized improvement recommendations.
```

---

## Tips for Effective LLM Code Review

### Provide Sufficient Context

- Include related files/classes
- Mention the framework (Django, FastAPI, etc.)
- Specify Python version
- Include project conventions

### Be Specific About Goals

- "Review for security" vs "Review for performance"
- "Add type hints for strict mypy" vs "Add basic type hints"
- "Refactor for testability" vs "Refactor for readability"

### Request Actionable Output

- Ask for specific code examples, not just descriptions
- Ask for line numbers or function names
- Request prioritization (critical, important, nice-to-have)

### Iterate

- Start with broad review, then drill into specific issues
- Ask follow-up questions about suggestions
- Request alternatives if first suggestion doesn't fit

### Verify AI Suggestions

- Always test suggested code
- Understand why before accepting
- Check that suggestions match project conventions
- Run linters/type checkers on AI-generated code
