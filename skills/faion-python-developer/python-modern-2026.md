# Python Modern 2026

**Modern Python 3.12/3.13 features and best practices for 2026.**

---

## Quick Reference

| Technology | Version | Status |
|------------|---------|--------|
| Python | 3.12/3.13 with type hints | Stable |
| Async | asyncio with TaskGroup | Stable |
| Type System | mypy/pyright strict mode | Stable |

---

## Python 3.13 Features

**Problem:** Leveraging latest Python features for better performance and code quality.

**Framework:**

1. **Free-threaded CPython (experimental):**
   ```python
   # PEP 703 - No GIL mode
   # Enable with: python3.13 -X nogil

   import threading
   from concurrent.futures import ThreadPoolExecutor

   def cpu_bound_task(data):
       # Actually runs in parallel without GIL
       return process(data)

   with ThreadPoolExecutor(max_workers=4) as executor:
       results = list(executor.map(cpu_bound_task, large_dataset))
   ```

2. **JIT Compiler (experimental):**
   ```bash
   # Enable experimental JIT
   python3.13 -X jit script.py
   ```

3. **Improved REPL:**
   - Syntax highlighting
   - Multi-line editing
   - Better auto-completion
   - Command history with context

4. **New typing features:**
   ```python
   from typing import TypeIs, ReadOnly

   # TypeIs for narrowing (PEP 742)
   def is_string_list(val: list[object]) -> TypeIs[list[str]]:
       return all(isinstance(x, str) for x in val)

   # ReadOnly for TypedDict (PEP 705)
   from typing import TypedDict

   class User(TypedDict):
       id: ReadOnly[int]  # Cannot be modified after creation
       name: str
   ```

**Performance (Python 3.12 vs 3.11):**
- 15% runtime improvement
- 10% memory reduction
- Dictionary lookup: 2.3M ops/sec

**Sources:**
- [Python 3.13 What's New - python.org](https://docs.python.org/3/whatsnew/3.13.html)
- [Modern Python 3.12+ Features - dasroot.net](https://dasroot.net/posts/2026/01/modern-python-312-features-type-hints-generics-performance/)
- [Python 3.13 New Features - Real Python](https://realpython.com/python313-new-features/)

---

## Python Async Best Practices

**Problem:** Efficient async/await patterns for I/O-bound applications.

**Framework:**

1. **TaskGroup (Python 3.11+):**
   ```python
   import asyncio

   async def fetch_all_data():
       async with asyncio.TaskGroup() as tg:
           users_task = tg.create_task(fetch_users())
           products_task = tg.create_task(fetch_products())
           orders_task = tg.create_task(fetch_orders())

       # All tasks completed, exceptions automatically propagated
       return users_task.result(), products_task.result(), orders_task.result()
   ```

2. **Timeout context manager:**
   ```python
   import asyncio

   async def fetch_with_timeout():
       async with asyncio.timeout(5.0):
           return await slow_operation()
   ```

3. **Semaphore for rate limiting:**
   ```python
   import asyncio
   import aiohttp

   async def fetch_many_urls(urls: list[str], max_concurrent: int = 10):
       semaphore = asyncio.Semaphore(max_concurrent)

       async def fetch_one(url: str) -> dict:
           async with semaphore:
               async with aiohttp.ClientSession() as session:
                   async with session.get(url) as response:
                       return await response.json()

       return await asyncio.gather(*[fetch_one(url) for url in urls])
   ```

4. **Async context managers:**
   ```python
   from contextlib import asynccontextmanager

   @asynccontextmanager
   async def database_connection():
       conn = await create_connection()
       try:
           yield conn
       finally:
           await conn.close()

   async def main():
       async with database_connection() as conn:
           await conn.execute("SELECT * FROM users")
   ```

**Performance:** Async patterns reduce latency by up to 65% for I/O-bound applications.

---

## Python Type Hints (2026)

**Problem:** Comprehensive type safety with modern Python typing.

**Framework:**

1. **Modern union syntax:**
   ```python
   # Python 3.10+
   def process(value: int | str | None) -> str:
       if value is None:
           return "None"
       return str(value)
   ```

2. **Generic types:**
   ```python
   from typing import TypeVar, Generic
   from dataclasses import dataclass

   T = TypeVar('T')

   @dataclass
   class Result(Generic[T]):
       value: T
       error: str | None = None

       @property
       def is_ok(self) -> bool:
           return self.error is None

   def get_user(id: int) -> Result[User]:
       try:
           user = db.find(id)
           return Result(value=user)
       except NotFoundError as e:
           return Result(value=None, error=str(e))
   ```

3. **Protocol for structural typing:**
   ```python
   from typing import Protocol

   class Serializable(Protocol):
       def to_dict(self) -> dict: ...
       def to_json(self) -> str: ...

   def save(item: Serializable) -> None:
       data = item.to_dict()
       # Works with any class implementing these methods
   ```

4. **ParamSpec for decorators:**
   ```python
   from typing import ParamSpec, TypeVar, Callable

   P = ParamSpec('P')
   R = TypeVar('R')

   def retry(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
       def decorator(func: Callable[P, R]) -> Callable[P, R]:
           def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
               for attempt in range(times):
                   try:
                       return func(*args, **kwargs)
                   except Exception:
                       if attempt == times - 1:
                           raise
               raise RuntimeError("Unreachable")
           return wrapper
       return decorator
   ```

**Checklist:**
- [ ] Enable strict mode in mypy/pyright
- [ ] Use `|` union syntax over `Optional`
- [ ] Define Protocols for duck typing
- [ ] Type all function signatures
- [ ] Use TypedDict for complex dicts

---

## Methodologies Index

| Name | Section |
|------|---------|
| Python 3.13 Features | Python 3.13 |
| Python Async Best Practices | Async |
| Python Type Hints (2026) | Type Hints |

---

## References

**Python:**
- [Python 3.13 What's New](https://docs.python.org/3/whatsnew/3.13.html)
- [Python 3.12 What's New](https://docs.python.org/3/whatsnow/3.12.html)
- [Modern Python 3.12+ Features](https://dasroot.net/posts/2026/01/modern-python-312-features-type-hints-generics-performance/)
- [Python Best Practices 2025](https://johal.in/python-programming-best-practices-in-2025/)

---

*Python Modern 2026 v1.0*
*Last updated: 2026-01-23*
