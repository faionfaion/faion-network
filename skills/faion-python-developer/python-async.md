# Python Async (asyncio)

**Efficient concurrent execution for I/O-bound operations**

---

## Problem

Python applications need efficient concurrent execution for I/O-bound operations like API calls, database queries, and file operations.

## Framework

### Basic Async/Await

```python
import asyncio


async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main():
    result = await fetch_data("https://api.example.com/data")
    print(result)


# Run the async function
asyncio.run(main())
```

### Concurrent Execution

```python
import asyncio


async def fetch_user(user_id: int) -> dict:
    """Simulate fetching user data."""
    await asyncio.sleep(0.5)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}


async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)


async def main():
    # Sequential: 5 seconds
    # Concurrent: ~0.5 seconds
    users = await fetch_all_users([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Fetched {len(users)} users")
```

### TaskGroup (Python 3.11+)

```python
import asyncio


async def process_item(item: str) -> str:
    await asyncio.sleep(0.1)
    return f"Processed: {item}"


async def main():
    results = []

    async with asyncio.TaskGroup() as tg:
        for item in ["a", "b", "c"]:
            task = tg.create_task(process_item(item))
            # Tasks run concurrently

    # All tasks completed when exiting context
```

### Async Context Managers

```python
import asyncio
from contextlib import asynccontextmanager


class AsyncDatabaseConnection:
    async def connect(self) -> None:
        print("Connecting to database...")
        await asyncio.sleep(0.1)

    async def disconnect(self) -> None:
        print("Disconnecting from database...")
        await asyncio.sleep(0.1)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


# Using async context manager
async def main():
    async with AsyncDatabaseConnection() as db:
        # Use db connection
        pass


# Function-based context manager
@asynccontextmanager
async def get_connection():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()
```

### Async Generators

```python
import asyncio


async def async_range(start: int, stop: int):
    """Async generator example."""
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i


async def main():
    async for num in async_range(0, 5):
        print(num)
```

### Semaphores for Rate Limiting

```python
import asyncio


async def fetch_with_limit(
    urls: list[str],
    max_concurrent: int = 5,
) -> list[dict]:
    """Fetch URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Timeouts

```python
import asyncio


async def slow_operation() -> str:
    await asyncio.sleep(10)
    return "Done"


async def main():
    try:
        # Timeout after 2 seconds
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out")


# Context manager timeout (Python 3.11+)
async def main_with_scope():
    async with asyncio.timeout(2.0):
        result = await slow_operation()
```

### Async in Django

```python
# views.py
from django.http import JsonResponse
import asyncio


async def async_view(request):
    """Async Django view."""
    data = await fetch_external_data()
    return JsonResponse(data)


# Call sync code from async
from asgiref.sync import sync_to_async

@sync_to_async
def get_user_sync(user_id: int):
    return User.objects.get(id=user_id)


async def async_view_with_db(request):
    user = await get_user_sync(request.user.id)
    return JsonResponse({"name": user.name})
```

### Async in FastAPI

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()


@app.get("/items")
async def get_items():
    """Async endpoint."""
    items = await fetch_items_from_db()
    return {"items": items}


@app.get("/aggregate")
async def get_aggregate():
    """Concurrent data fetching."""
    users, products, orders = await asyncio.gather(
        fetch_users(),
        fetch_products(),
        fetch_orders(),
    )
    return {
        "users": users,
        "products": products,
        "orders": orders,
    }
```

## Templates

**Async main pattern:**
```python
async def main():
    # Your async code
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

## Sources

- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html) - Official asyncio reference
- [Real Python - Async IO](https://realpython.com/async-io-python/) - Comprehensive async guide
- [Python 3.11 TaskGroup](https://docs.python.org/3/library/asyncio-task.html#task-groups) - Structured concurrency
- [aiohttp Documentation](https://docs.aiohttp.org/) - Async HTTP client/server
- [Async Best Practices](https://superfastpython.com/asyncio-best-practices/) - Production patterns

## Agent

Executed by: faion-code-agent
