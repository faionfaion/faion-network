# LLM Prompts for Type Hints

Effective prompts for LLM-assisted Python type annotation.

## Table of Contents

1. [Adding Type Hints to Existing Code](#adding-type-hints-to-existing-code)
2. [Generating Typed Code](#generating-typed-code)
3. [Type Checking and Fixing](#type-checking-and-fixing)
4. [Framework-Specific Prompts](#framework-specific-prompts)
5. [Advanced Typing Prompts](#advanced-typing-prompts)
6. [Review and Improvement Prompts](#review-and-improvement-prompts)

---

## Adding Type Hints to Existing Code

### Basic Type Annotation

```
Add comprehensive type hints to this Python code:

Requirements:
- Use Python 3.12+ syntax (list[int] not List[int])
- Use | for unions (str | None not Optional[str])
- Add return types to all functions
- Type all function parameters
- Use Sequence/Mapping for read-only parameters
- Add type hints for class attributes

Code:
```python
{paste code here}
```
```

### Gradual Type Annotation

```
Add type hints to this code gradually, prioritizing:

1. Public function signatures (parameters and return types)
2. Class attributes and __init__ parameters
3. Complex data structures (dicts, nested collections)
4. Callbacks and closures

Start with the most important interfaces first:

```python
{paste code here}
```
```

### Infer Types from Usage

```
Analyze this code and add type hints by inferring types from:
- Variable assignments
- Function calls and their arguments
- Return statements
- Method chains
- Conditional checks

If a type cannot be confidently inferred, use a TODO comment:
# TODO: Verify type for {variable}

```python
{paste code here}
```
```

---

## Generating Typed Code

### Generate Function with Types

```
Write a Python function with full type hints:

Function: {function_name}
Purpose: {description}
Parameters:
- {param1}: {description} (type: {type_hint})
- {param2}: {description} (type: {type_hint})
Returns: {return_description}

Requirements:
- Python 3.12+ type syntax
- Handle edge cases with proper None checks
- Include docstring with type information
```

### Generate Class with Types

```
Create a Python class with comprehensive type hints:

Class: {ClassName}
Purpose: {description}

Attributes:
- {attr1}: {type} - {description}
- {attr2}: {type} - {description}

Methods:
- {method1}({params}) -> {return_type}: {description}
- {method2}({params}) -> {return_type}: {description}

Requirements:
- Use @dataclass if appropriate
- Type all attributes at class level
- Use ClassVar for class variables
- Use Self for methods returning instance
- Add __init__ type hints
```

### Generate Generic Class

```
Create a generic class with proper type parameters:

Class: {ClassName}[T]
Purpose: {description}
Type parameter constraints: {constraints, e.g., "T: Comparable" or "T: (int, float)"}

Methods:
- {method1}(item: T) -> T
- {method2}() -> list[T]

Use Python 3.12+ generic syntax: class Name[T]:
```

### Generate Protocol

```
Create a Protocol for duck typing:

Protocol: {ProtocolName}
Purpose: {description}

Required methods:
- {method1}({params}) -> {return_type}
- {method2}({params}) -> {return_type}

Required properties:
- {property1}: {type}

Should it be @runtime_checkable? {yes/no}
```

---

## Type Checking and Fixing

### Fix Type Errors

```
Fix the type errors in this code. The mypy/pyright errors are:

{paste error messages}

Code:
```python
{paste code here}
```

Requirements:
- Fix the actual type issues, don't just add # type: ignore
- Preserve the original functionality
- Add type guards if needed for narrowing
- Use cast() only as last resort
```

### Eliminate Any Usage

```
Replace all Any types in this code with specific types:

```python
{paste code here}
```

For each Any:
1. Analyze how the variable is used
2. Determine the most specific valid type
3. If truly dynamic, use Union of expected types
4. If from external library, check for available stubs
5. Document if Any is truly necessary
```

### Add Type Guards

```
Add TypeIs/TypeGuard functions to narrow types in this code:

```python
{paste code here}
```

Requirements:
- Use TypeIs (Python 3.13+) for bidirectional narrowing
- Use TypeGuard only when TypeIs won't work
- Name guards clearly: is_{type_name}()
- Add to conditions where isinstance() is used repeatedly
```

### Fix Optional Handling

```
Improve None handling in this code:

```python
{paste code here}
```

Requirements:
- Make optional types explicit (T | None)
- Add proper None checks before usage
- Consider using early returns for None cases
- Add assert_not_none helper if needed
- Use Optional only for compatibility
```

---

## Framework-Specific Prompts

### Django Type Hints

```
Add type hints to this Django code:

```python
{paste code here}
```

Requirements:
- Use django-stubs conventions
- Type QuerySet returns: QuerySet[Model]
- Type view parameters: HttpRequest, int/str for path params
- Type model fields appropriately
- Use Manager[Model] for custom managers
- Handle related_name with forward references
```

### FastAPI Type Hints

```
Add type hints to this FastAPI code:

```python
{paste code here}
```

Requirements:
- Use Pydantic BaseModel for request/response
- Use Annotated for dependencies
- Type path parameters: Annotated[int, Path()]
- Type query parameters: Annotated[str, Query()]
- Use response_model for automatic serialization
- Type async functions properly
```

### Pydantic Models

```
Create a Pydantic model with proper type hints:

Model: {ModelName}
Purpose: {description}

Fields:
- {field1}: {type} - {description} - {constraints}
- {field2}: {type} - {description} - {constraints}

Requirements:
- Use Annotated with Field() for validation
- Use EmailStr, HttpUrl for validated strings
- Use Literal for enums/fixed values
- Add model_validator for cross-field validation
- Use ConfigDict for model configuration
```

### SQLAlchemy Type Hints

```
Add type hints to this SQLAlchemy code:

```python
{paste code here}
```

Requirements:
- Use Mapped[T] for column types
- Use mapped_column() with proper types
- Type relationships with Mapped[list[Model]]
- Use ForeignKey with proper back_populates
- Type session operations
```

---

## Advanced Typing Prompts

### Create Decorator with Types

```
Create a typed decorator:

Decorator: {decorator_name}
Purpose: {description}
Modifies signature: {yes/no, how}

Requirements:
- Preserve function signature with ParamSpec
- Preserve return type with TypeVar
- Use Concatenate if adding parameters
- Use @overload if multiple signatures
- Support both sync and async functions (if needed)
```

### TypedDict from JSON

```
Create TypedDict definitions from this JSON structure:

```json
{paste JSON here}
```

Requirements:
- Create separate TypedDict for nested objects
- Use NotRequired for optional fields
- Use Literal for enum-like strings
- Add type aliases for repeated structures
- Handle arrays with proper item types
```

### Union Type Handling

```
Create a type-safe function that handles multiple types:

Input types: {list input types}
Output type: {output type}
Behavior per type:
- {type1}: {behavior}
- {type2}: {behavior}

Requirements:
- Use @overload for different signatures
- Add runtime type checks with isinstance
- Use TypeIs for type narrowing
- Ensure exhaustive handling with assert_never
```

### Callback Types

```
Create typed callback definitions for this API:

Callbacks needed:
- {callback1}: {signature} - {description}
- {callback2}: {signature} - {description}

Requirements:
- Use Callable with proper signature
- Create Protocol if callbacks have multiple methods
- Support both sync and async callbacks
- Use ParamSpec if wrapping callbacks
```

---

## Review and Improvement Prompts

### Review Type Hints

```
Review and improve the type hints in this code:

```python
{paste code here}
```

Check for:
1. Overly broad types (Any, object when more specific is possible)
2. Missing | None for nullable values
3. Inconsistent use of generic types
4. Missing return types
5. Type: ignore comments that could be fixed
6. Outdated syntax (List instead of list)

Suggest improvements with explanations.
```

### Upgrade Type Hints Syntax

```
Upgrade type hints to Python 3.12+ syntax:

```python
{paste code here}
```

Changes to make:
- List[T] -> list[T]
- Dict[K, V] -> dict[K, V]
- Optional[T] -> T | None
- Union[A, B] -> A | B
- TypeVar("T") -> [T] syntax for generics
- Remove unnecessary typing imports
```

### Add Strict Mode Compliance

```
Make this code pass mypy --strict:

```python
{paste code here}
```

Requirements:
- Add missing type hints
- Fix implicit Any issues
- Add explicit return types
- Handle None properly
- Type all class attributes
- No implicit Optional
```

### Generate Type Stubs

```
Generate type stubs (.pyi file) for this module:

```python
{paste code here}
```

Requirements:
- Include all public functions and classes
- Omit implementation details
- Use ... for function bodies
- Include docstrings as comments
- Handle overloads properly
```

---

## Quick Reference Prompts

### One-liner Prompts

| Task | Prompt |
|------|--------|
| Add types | "Add Python 3.12+ type hints to: {code}" |
| Fix error | "Fix this mypy error: {error} in: {code}" |
| TypedDict | "Create TypedDict from this JSON: {json}" |
| Protocol | "Create Protocol for objects with {method} method" |
| Generic | "Make this class generic over type T: {code}" |
| Narrow | "Add TypeIs to narrow {Union} in: {code}" |

### Context-Setting Prefix

Use this prefix for consistent results:

```
Context: Python 3.12+, using modern type syntax.
- list[T] not List[T]
- str | None not Optional[str]
- class Name[T]: not Generic[T]
- TypeIs for type narrowing

Task: {your specific task}
```

### Output Format Request

```
{your prompt}

Format your response as:
1. Explanation of type choices
2. Complete typed code
3. Any assumptions made
4. Potential edge cases to consider
```
