# Python Basics LLM Prompts

Effective prompts for LLM-assisted Python learning and development.

---

## Learning Prompts

### Explain Concepts

```
Explain Python [CONCEPT] with:
1. Simple definition
2. Why it's useful
3. Basic example
4. Common mistakes to avoid
5. When to use vs alternatives

CONCEPT examples: list comprehensions, decorators, generators, context managers
```

```
Compare Python [A] vs [B]:
- Key differences
- Performance characteristics
- Use cases for each
- Code examples
- Best practices

Examples:
- list vs tuple
- @staticmethod vs @classmethod
- async/await vs threading
- dict vs defaultdict
```

### Debug Help

```
Debug this Python code:

```python
[YOUR CODE HERE]
```

Error message:
[ERROR MESSAGE]

Please:
1. Explain what's wrong
2. Show the fixed code
3. Explain why the fix works
4. Suggest how to prevent this in the future
```

### Code Review

```
Review this Python code for:
- Correctness
- Pythonic style (PEP 8)
- Type safety
- Error handling
- Performance
- Security issues

```python
[YOUR CODE HERE]
```

Provide specific improvements with examples.
```

---

## Code Generation Prompts

### Function Generation

```
Generate a Python 3.12+ function that [DESCRIPTION]:

Requirements:
- Full type hints (modern syntax: list[T], X | None)
- Docstring with Args, Returns, Raises, Examples
- Error handling for [EDGE CASES]
- Unit tests with pytest

Example input/output:
Input: [EXAMPLE INPUT]
Output: [EXAMPLE OUTPUT]
```

### Class Generation

```
Generate a Python 3.12+ class for [DESCRIPTION]:

Requirements:
- Use @dataclass with slots=True
- Full type hints
- Properties for computed attributes
- Methods: [LIST METHODS]
- Implement __str__ and __repr__
- Include validation in __post_init__

The class should handle:
[LIST OF USE CASES]
```

### Refactoring Prompts

```
Refactor this Python code to be more Pythonic:

```python
[YOUR CODE HERE]
```

Apply these improvements:
- List/dict/set comprehensions where appropriate
- Context managers for resources
- Modern type hints (Python 3.12+ syntax)
- Remove redundant code
- Follow PEP 8
- Add type hints

Show before/after comparison with explanations.
```

```
Convert this code to use modern Python 3.12+ features:

```python
[YOUR CODE HERE]
```

Modernize:
- TypeVar → generic syntax (class Foo[T]:)
- Union[X, Y] → X | Y
- Optional[X] → X | None
- from typing import List → list
- Add pattern matching where appropriate
```

---

## Data Structures Prompts

### List Operations

```
Generate Python code to [OPERATION] on a list:

Input: [DESCRIBE INPUT]
Expected output: [DESCRIBE OUTPUT]

Requirements:
- Use list comprehension if appropriate
- Consider memory efficiency for large lists
- Add type hints
- Include edge case handling (empty list, etc.)
```

### Dictionary Operations

```
Generate Python code to [OPERATION] on dictionaries:

Input structure:
[DESCRIBE DICT STRUCTURE]

Expected output:
[DESCRIBE OUTPUT]

Requirements:
- Use dict comprehension if appropriate
- Consider using collections (Counter, defaultdict) if helpful
- Handle missing keys gracefully
- Add type hints
```

### Data Transformation

```
Transform this data structure:

From:
```python
[INPUT STRUCTURE]
```

To:
```python
[OUTPUT STRUCTURE]
```

Requirements:
- Use comprehensions where readable
- Maintain O(n) complexity if possible
- Add type hints
- Handle edge cases
```

---

## Error Handling Prompts

### Exception Design

```
Design a custom exception hierarchy for [DOMAIN]:

Use cases:
1. [USE CASE 1]
2. [USE CASE 2]
3. [USE CASE 3]

Requirements:
- Base exception class
- Specific exceptions for each use case
- Include useful attributes (error codes, context)
- Add type hints
- Follow Python best practices
```

### Error Handling Pattern

```
Add proper error handling to this code:

```python
[YOUR CODE HERE]
```

Requirements:
- Catch specific exceptions (not bare except)
- Use EAFP pattern where appropriate
- Add logging
- Re-raise with context when needed
- Handle cleanup with finally or context managers
```

---

## File I/O Prompts

### File Operations

```
Generate Python code to [FILE OPERATION]:

File type: [txt/json/csv/yaml]
Input: [DESCRIBE INPUT]
Output: [DESCRIBE OUTPUT]

Requirements:
- Use pathlib.Path
- Specify encoding (utf-8)
- Use context managers
- Handle file not found gracefully
- Consider memory for large files (streaming if needed)
- Add type hints
```

### Data Processing

```
Generate a Python data processing pipeline:

1. Read from: [SOURCE - file/API/database]
2. Transform: [DESCRIBE TRANSFORMATIONS]
3. Write to: [DESTINATION]

Requirements:
- Stream processing for large data (generators)
- Error handling with logging
- Progress indication for long operations
- Type hints
- Unit tests
```

---

## Testing Prompts

### Generate Tests

```
Generate pytest tests for this function:

```python
[YOUR FUNCTION HERE]
```

Include:
- Happy path tests
- Edge cases (empty input, None, etc.)
- Error cases (invalid input)
- Parametrized tests for multiple inputs
- Fixtures if needed
- Type hints on test functions
```

### Test-First Development

```
I need to implement [FEATURE DESCRIPTION].

Generate pytest tests first, then the implementation.

Expected behavior:
- Input: [DESCRIBE INPUTS]
- Output: [DESCRIBE OUTPUTS]
- Edge cases: [LIST EDGE CASES]
- Errors: [WHEN SHOULD IT RAISE ERRORS]

Include:
- Test file with fixtures
- Implementation file
- Type hints throughout
```

---

## Project Setup Prompts

### New Project

```
Generate a modern Python 3.12+ project structure for [PROJECT TYPE]:

Project type: [CLI tool / web API / library / data pipeline]
Name: [PROJECT NAME]
Description: [DESCRIPTION]

Include:
- pyproject.toml with ruff, mypy, pytest config
- .gitignore
- README.md skeleton
- src/ layout
- tests/ with conftest.py
- GitHub Actions workflow for CI
```

### Dependency Management

```
Create a pyproject.toml for a Python project with:

Runtime dependencies:
[LIST DEPENDENCIES]

Dev dependencies:
[LIST DEV DEPS]

Include configuration for:
- ruff (linting + formatting)
- mypy (strict mode)
- pytest (coverage)
- Python version: 3.12+
```

---

## Performance Prompts

### Optimization

```
Optimize this Python code for performance:

```python
[YOUR CODE HERE]
```

Current performance: [DESCRIBE ISSUE]
Target: [DESCRIBE GOAL]

Consider:
- Algorithm complexity
- Data structure choice
- Built-in functions vs loops
- Generator expressions vs lists
- functools.lru_cache for memoization
- Profiling to identify bottlenecks
```

### Memory Efficiency

```
Optimize this code for memory efficiency:

```python
[YOUR CODE HERE]
```

Current memory usage: [DESCRIBE]
Processing: [DESCRIBE DATA SIZE]

Consider:
- Generators instead of lists
- itertools for efficient iteration
- __slots__ for classes
- Array types for numerical data
- Streaming for large files
```

---

## Prompt Templates Summary

### Quick Templates

| Need | Prompt Start |
|------|--------------|
| Learn concept | "Explain Python [X] with examples and common mistakes" |
| Debug code | "Debug this Python code: [code] Error: [error]" |
| Generate function | "Generate a Python 3.12+ function that [X] with type hints" |
| Generate class | "Generate a Python 3.12+ @dataclass for [X]" |
| Refactor | "Refactor this code to be more Pythonic: [code]" |
| Add tests | "Generate pytest tests for this function: [code]" |
| Optimize | "Optimize this Python code for [performance/memory]: [code]" |

### Context to Always Include

1. **Python version**: "Using Python 3.12+..."
2. **Type hints**: "...with full type hints"
3. **Error handling**: "...with proper error handling"
4. **Testing**: "...include pytest tests"
5. **Framework** (if relevant): "...for Django/FastAPI/etc."

### Effective Prompt Structure

```
[ACTION VERB] [WHAT] for [CONTEXT]:

[CODE OR DESCRIPTION]

Requirements:
- [REQUIREMENT 1]
- [REQUIREMENT 2]
- [REQUIREMENT 3]

Expected:
- Input: [DESCRIBE]
- Output: [DESCRIBE]
```

---

## Best Practices for LLM Interaction

### Do

- Specify Python version explicitly
- Request type hints
- Ask for docstrings with examples
- Request error handling
- Ask for tests alongside code
- Provide example inputs/outputs
- Specify constraints (memory, performance)

### Avoid

- Vague requests ("make it better")
- Missing context (Python version, framework)
- Not specifying edge cases
- Accepting code without type hints
- Ignoring error handling
- Not asking for tests

### Iterative Refinement

```
1. Generate initial code
2. "Add type hints to this code"
3. "Add error handling for [edge cases]"
4. "Generate tests for this code"
5. "Optimize for [performance/readability]"
```

---

*Python Basics LLM Prompts v2.0*
*Last updated: 2026-01-25*
