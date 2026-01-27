# LLM Prompts for Python Typing

Effective prompts for generating well-typed Python code with LLMs.

---

## Context Setting Prompts

### Setting Python Version

```
Use Python 3.12+ features including:
- New generic syntax: class Container[T]: instead of Generic[T]
- Type aliases: type Name = ... instead of TypeAlias
- Union syntax: X | Y instead of Union[X, Y]
- Built-in generics: list[int] instead of List[int]
```

### Setting Strictness Level

```
Generate strict mypy-compatible code:
- All functions must have full type annotations
- No implicit Optional (use explicit X | None)
- No Any unless absolutely necessary
- Use Protocol for duck typing
- Use TypedDict for structured dicts
```

### Setting Framework Context

```
Generate Django 5.x code with django-stubs compatible types:
- Use QuerySet[Model] for query results
- Use HttpRequest and HttpResponse types
- Type all model methods
- Use AuthenticatedHttpRequest for authenticated views
```

```
Generate FastAPI code with Pydantic v2:
- Use BaseModel for request/response schemas
- Use Annotated for parameter metadata
- Use Field() for validation
- Use proper response_model typing
```

---

## Type Generation Prompts

### Adding Types to Existing Code

```
Add comprehensive type hints to this Python function:
- Parameter types
- Return type
- Handle None cases explicitly
- Use modern Python 3.12+ syntax
- Make types as specific as possible (avoid Any)

[paste code here]
```

### Converting Legacy Code

```
Convert this Python 2/3.5-era typing to modern Python 3.12+ syntax:
- Replace typing.List with list
- Replace typing.Dict with dict
- Replace Union[X, Y] with X | Y
- Replace Optional[X] with X | None
- Replace TypeVar + Generic with new generic syntax
- Replace TypeAlias with type keyword

[paste code here]
```

### Generating Typed Functions

```
Create a Python function with the following:
- Name: [function_name]
- Purpose: [description]
- Parameters: [list parameters with their purposes]
- Returns: [describe return value]
- Constraints: [any validation or error conditions]

Include:
- Full type annotations (Python 3.12+)
- Docstring with Args and Returns
- Input validation if appropriate
- Proper None handling
```

---

## Protocol and Interface Prompts

### Creating Protocols

```
Create a Python Protocol for [interface description]:
- Methods needed: [list methods]
- Properties needed: [list properties]
- Use @runtime_checkable if isinstance() checks are needed
- Keep the protocol minimal and focused
```

### Duck Typing with Protocols

```
I have multiple classes that share these behaviors:
[list methods/properties]

Create a Protocol that captures this interface, then type a function
that can work with any class implementing this protocol.
```

---

## Generic Type Prompts

### Creating Generic Classes

```
Create a generic class [ClassName] that:
- Works with type parameter T [with bounds if needed]
- Methods: [list methods]
- Use Python 3.12+ syntax (class Name[T]:)
- Include proper type hints for all methods
```

### Repository Pattern

```
Create a typed generic Repository pattern:
- Base class/protocol Repository[T] with CRUD operations
- Concrete implementation for [EntityName]
- Use Python 3.12+ generic syntax
- Type all methods including QuerySet returns
```

---

## TypedDict Prompts

### API Response Types

```
Create TypedDict definitions for this API response:
[paste JSON example]

Include:
- Proper nesting for nested objects
- NotRequired for optional fields
- Correct types for all fields
- Documentation comment
```

### Configuration Types

```
Create a TypedDict for configuration with:
- Required fields: [list]
- Optional fields: [list]
- Use total=False if most are optional with Required[] for mandatory ones
```

---

## Callable and Decorator Prompts

### Decorator Typing

```
Create a typed decorator that:
- Purpose: [what it does]
- Preserves the original function signature using ParamSpec
- [Add/modify arguments if needed using Concatenate]
- Works with both sync and async functions if needed
- Use Python 3.12+ syntax
```

### Callback Types

```
Define typed callback signatures for:
- [describe callback purpose and parameters]
- Include async version if needed
- Use Protocol if signature is complex (keyword args, defaults)
```

---

## Django-Specific Prompts

### Model Typing

```
Add type hints to this Django model:
- Type all field access
- Type model methods with return values
- Add QuerySet[Model] return types for class methods
- Make compatible with django-stubs

[paste model code]
```

### View Typing

```
Type this Django view:
- Use HttpRequest for input
- Use appropriate response type (HttpResponse, JsonResponse)
- Handle authenticated requests with AuthenticatedHttpRequest
- Type any serialization/deserialization

[paste view code]
```

### Service Layer Typing

```
Create a typed service class for [purpose]:
- Constructor dependencies with types
- Methods with full signatures
- QuerySet return types
- Transaction handling (@transaction.atomic)
```

---

## FastAPI-Specific Prompts

### Pydantic Models

```
Create Pydantic models for:
- Request: [describe fields and validation]
- Response: [describe fields]
- Include: Field() with validation, EmailStr, etc.
- Use model_config for ORM mode if needed
```

### Endpoint Typing

```
Create a FastAPI endpoint:
- Method: [GET/POST/PUT/DELETE]
- Path: [path with parameters]
- Query params: [list with types and defaults]
- Request body: [describe or None]
- Response: [describe]
- Include Annotated[] for parameter metadata
```

### Dependency Typing

```
Create a typed FastAPI dependency for:
- Purpose: [what it provides]
- Input: [headers, query params, etc.]
- Output: [what it returns]
- Error handling: [401, 403, etc.]
```

---

## Refactoring Prompts

### Improving Weak Types

```
Improve the typing in this code:
- Replace Any with specific types where possible
- Replace dict with TypedDict where structure is known
- Replace broad types with narrower ones
- Add Literal types for known string values
- Use Protocol instead of ABC where appropriate

[paste code here]
```

### Adding Overloads

```
Add @overload decorators to this function that has different
return types based on input:

[paste function]

The function returns:
- [type A] when [condition]
- [type B] when [condition]
```

---

## Validation Prompts

### Type Checking Existing Code

```
Review this code for typing issues:
- Missing type annotations
- Incorrect types
- Overly broad types (Any, object)
- Missing None handling
- TypedDict vs dict usage
- Protocol vs ABC decision

[paste code here]
```

### Fixing Type Errors

```
This code has a mypy/pyright error:
[paste error message]

Here's the code:
[paste code]

Fix the typing issue while maintaining the intended behavior.
Explain what was wrong and why the fix works.
```

---

## Complex Pattern Prompts

### Result/Either Pattern

```
Implement a typed Result[T, E] pattern:
- Ok(value: T) for success
- Err(error: E) for failure
- map() method for transforming success
- map_err() method for transforming error
- unwrap() with proper error
- Use Python 3.12+ generics
```

### Builder Pattern

```
Create a typed Builder pattern for [class]:
- Each method returns Self for chaining
- Validate required fields in build()
- Type all builder methods
- Use @dataclass for the target class
```

### Factory Pattern

```
Create a typed Factory for [base class/protocol]:
- Register implementations by key
- Generic return type based on registration
- Type-safe creation method
- Use Protocol for the product type
```

---

## Quick Reference Prompts

### "Type This For Me"

```
Add type hints to this code (Python 3.12+, strict mypy):
[paste code]
```

### "Create Typed Version"

```
Create a fully typed version of this function/class:
- Python 3.12+
- Strict mypy compatible
- Generic where appropriate
- Protocol for interfaces
[paste code or description]
```

### "Fix The Types"

```
Fix mypy errors in this code. Error: [error message]
Code:
[paste code]
```

---

## Prompt Modifiers

Add these to any prompt for specific behavior:

| Modifier | Effect |
|----------|--------|
| "Python 3.12+" | Uses new generic syntax, type keyword |
| "Python 3.10-3.11" | Uses `X \| Y` but old generics |
| "Python 3.9" | Uses old Union, but new built-in generics |
| "strict mypy" | No implicit Optional, full annotations |
| "with docstrings" | Adds Google/NumPy style docstrings |
| "Django compatible" | Uses django-stubs patterns |
| "FastAPI/Pydantic" | Uses Pydantic v2 patterns |
| "minimal" | Only essential types, fewer imports |
| "comprehensive" | Full coverage including edge cases |

---

## Anti-Patterns to Avoid

Tell the LLM to avoid these:

```
Do NOT:
- Use Any unless absolutely necessary
- Use object as a catch-all
- Forget None in return types when applicable
- Use mutable default arguments
- Ignore TypeVar bounds/constraints
- Mix old and new typing syntax
- Use # type: ignore without comment
```

---

## Example Conversation Flow

### 1. Set Context

```
I'm working on a Python 3.12 Django 5.x project with:
- mypy strict mode
- django-stubs installed
- Pydantic v2 for serialization

I need help with typing patterns.
```

### 2. Request Specific Help

```
Create a typed service class for user management:
- create_user(email, password, name) -> User
- get_user(user_id) -> User | None
- list_users(active_only=True, limit=100) -> QuerySet[User]
- update_user(user_id, **fields) -> User
- delete_user(user_id) -> bool

Include proper typing for Django ORM operations.
```

### 3. Iterate

```
The typing looks good. Now:
1. Add error handling with typed exceptions
2. Add a TypedDict for the **fields parameter
3. Add logging with proper type hints
```

---

*Use these prompts as starting points and customize for your specific needs.*
