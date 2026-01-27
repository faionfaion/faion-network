# Python Async Patterns Templates

Copy-paste templates for common async patterns. Replace placeholders with your implementation.

---

## Basic Async Function

```python
import asyncio
from typing import TypeVar

T = TypeVar("T")


async def fetch_resource(resource_id: int) -> dict:
    """
    Fetch a resource by ID.

    Args:
        resource_id: The resource identifier

    Returns:
        Resource data as dictionary

    Raises:
        ResourceNotFoundError: If resource doesn't exist
        NetworkError: If request fails
    """
    # TODO: Replace with actual implementation
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/resources/{resource_id}",
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
```

---

## Concurrent Fetch with gather()

```python
import asyncio
import httpx
from typing import TypeVar

T = TypeVar("T")


async def fetch_many(
    ids: list[int],
    *,
    return_exceptions: bool = True
) -> list[dict | Exception]:
    """
    Fetch multiple resources concurrently.

    Args:
        ids: List of resource IDs to fetch
        return_exceptions: If True, return exceptions instead of raising

    Returns:
        List of results (same order as input IDs)
    """
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:

        async def fetch_one(resource_id: int) -> dict:
            response = await client.get(
                f"/resources/{resource_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

        coroutines = [fetch_one(id_) for id_ in ids]
        return await asyncio.gather(*coroutines, return_exceptions=return_exceptions)


# Usage:
# results = await fetch_many([1, 2, 3, 4, 5])
# successful = [r for r in results if not isinstance(r, Exception)]
```

---

## TaskGroup with Error Handling (Python 3.11+)

```python
import asyncio
from typing import TypeVar

T = TypeVar("T")


async def process_batch_taskgroup(items: list[T]) -> list[dict]:
    """
    Process items concurrently with TaskGroup.
    Cancels all tasks if any fails.

    Args:
        items: Items to process

    Returns:
        List of processed results

    Raises:
        ExceptionGroup: If any task fails
    """
    tasks: list[asyncio.Task] = []

    try:
        async with asyncio.TaskGroup() as tg:
            for item in items:
                task = tg.create_task(
                    process_single(item),
                    name=f"process-{item}"
                )
                tasks.append(task)
    except* ValueError as eg:
        # Handle specific exception types
        for exc in eg.exceptions:
            print(f"ValueError in task: {exc}")
        raise
    except* Exception as eg:
        # Handle other exceptions
        for exc in eg.exceptions:
            print(f"Error in task: {exc}")
        raise

    return [task.result() for task in tasks]


async def process_single(item: T) -> dict:
    """Process a single item."""
    # TODO: Replace with actual implementation
    await asyncio.sleep(0.1)
    return {"item": item, "status": "processed"}
```

---

## Rate-Limited Concurrent Requests

```python
import asyncio
import httpx
from typing import TypeVar

T = TypeVar("T")


class RateLimitedFetcher:
    """Fetch resources with concurrency limit."""

    def __init__(
        self,
        base_url: str,
        max_concurrent: int = 10,
        timeout: float = 30.0
    ):
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = timeout

    async def fetch_one(self, path: str) -> dict | None:
        """Fetch single resource with rate limiting."""
        async with self.semaphore:
            try:
                async with httpx.AsyncClient(base_url=self.base_url) as client:
                    response = await client.get(path, timeout=self.timeout)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching {path}: {e}")
                return None

    async def fetch_many(self, paths: list[str]) -> list[dict | None]:
        """Fetch multiple resources with rate limiting."""
        tasks = [self.fetch_one(path) for path in paths]
        return await asyncio.gather(*tasks)


# Usage:
# fetcher = RateLimitedFetcher("https://api.example.com", max_concurrent=5)
# results = await fetcher.fetch_many(["/users/1", "/users/2", "/users/3"])
```

---

## Timeout Wrapper

```python
import asyncio
from typing import TypeVar, Awaitable, Callable

T = TypeVar("T")


async def with_timeout(
    coro: Awaitable[T],
    timeout: float,
    *,
    default: T | None = None,
    on_timeout: Callable[[], None] | None = None
) -> T | None:
    """
    Execute coroutine with timeout.

    Args:
        coro: Coroutine to execute
        timeout: Timeout in seconds
        default: Value to return on timeout
        on_timeout: Callback to execute on timeout

    Returns:
        Coroutine result or default on timeout
    """
    try:
        async with asyncio.timeout(timeout):
            return await coro
    except asyncio.TimeoutError:
        if on_timeout:
            on_timeout()
        return default


# Usage:
# result = await with_timeout(
#     slow_operation(),
#     timeout=5.0,
#     default={"status": "timeout"},
#     on_timeout=lambda: logger.warning("Operation timed out")
# )
```

---

## Async Context Manager (Class-Based)

```python
import asyncio
from typing import TypeVar, Generic

T = TypeVar("T")


class AsyncResource(Generic[T]):
    """
    Async context manager for resource lifecycle management.

    Usage:
        async with AsyncResource(config) as resource:
            await resource.do_something()
    """

    def __init__(self, config: dict):
        self.config = config
        self._resource: T | None = None

    async def __aenter__(self) -> T:
        """Acquire resource."""
        # TODO: Replace with actual resource acquisition
        self._resource = await self._create_resource()
        return self._resource

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Release resource."""
        if self._resource:
            await self._cleanup_resource()
            self._resource = None
        return False  # Don't suppress exceptions

    async def _create_resource(self) -> T:
        """Create the managed resource."""
        # TODO: Implement resource creation
        raise NotImplementedError

    async def _cleanup_resource(self) -> None:
        """Cleanup the managed resource."""
        # TODO: Implement cleanup
        pass
```

---

## Async Context Manager (Function-Based)

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, TypeVar

T = TypeVar("T")


@asynccontextmanager
async def managed_resource(config: dict) -> AsyncIterator[T]:
    """
    Async context manager using decorator.

    Usage:
        async with managed_resource(config) as resource:
            await resource.do_something()
    """
    # Setup
    resource = await create_resource(config)

    try:
        yield resource
    except Exception as e:
        # Handle errors (optional)
        await handle_error(resource, e)
        raise
    finally:
        # Cleanup (always runs)
        await cleanup_resource(resource)


async def create_resource(config: dict):
    """Create resource."""
    # TODO: Implement
    pass


async def cleanup_resource(resource) -> None:
    """Cleanup resource."""
    # TODO: Implement
    pass


async def handle_error(resource, error: Exception) -> None:
    """Handle error during resource usage."""
    # TODO: Implement (optional)
    pass
```

---

## Async Generator for Pagination

```python
import asyncio
import httpx
from typing import AsyncIterator, TypeVar

T = TypeVar("T")


async def paginate(
    base_url: str,
    path: str,
    *,
    page_size: int = 100,
    max_pages: int | None = None
) -> AsyncIterator[dict]:
    """
    Paginate through API results.

    Args:
        base_url: API base URL
        path: Endpoint path
        page_size: Items per page
        max_pages: Maximum pages to fetch (None = unlimited)

    Yields:
        Individual items from paginated results
    """
    page = 1

    async with httpx.AsyncClient(base_url=base_url) as client:
        while max_pages is None or page <= max_pages:
            response = await client.get(
                path,
                params={"page": page, "per_page": page_size},
                timeout=30.0
            )
            data = response.json()

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                yield item

            # Check if more pages exist
            if len(items) < page_size:
                break

            page += 1


# Usage:
# async for item in paginate("https://api.example.com", "/users"):
#     print(item)
```

---

## Background Task Manager

```python
import asyncio
from typing import Awaitable, Callable
import logging

logger = logging.getLogger(__name__)


class BackgroundTaskManager:
    """
    Manage background tasks with proper lifecycle.

    Usage:
        manager = BackgroundTaskManager()
        manager.add(send_email(user_id), name="email-123")

        # On shutdown:
        await manager.shutdown()
    """

    def __init__(self):
        self._tasks: set[asyncio.Task] = set()

    def add(
        self,
        coro: Awaitable,
        *,
        name: str | None = None,
        on_success: Callable[[any], None] | None = None,
        on_error: Callable[[Exception], None] | None = None
    ) -> asyncio.Task:
        """Add a background task."""
        task = asyncio.create_task(coro, name=name)
        self._tasks.add(task)

        def done_callback(t: asyncio.Task) -> None:
            self._tasks.discard(t)

            if t.cancelled():
                logger.debug(f"Task {t.get_name()} cancelled")
                return

            exc = t.exception()
            if exc:
                logger.error(f"Task {t.get_name()} failed: {exc}")
                if on_error:
                    on_error(exc)
            else:
                if on_success:
                    on_success(t.result())

        task.add_done_callback(done_callback)
        return task

    async def shutdown(self, timeout: float = 5.0) -> None:
        """Cancel all tasks and wait for completion."""
        if not self._tasks:
            return

        logger.info(f"Cancelling {len(self._tasks)} background tasks")

        for task in self._tasks:
            task.cancel()

        done, pending = await asyncio.wait(
            self._tasks,
            timeout=timeout,
            return_when=asyncio.ALL_COMPLETED
        )

        if pending:
            logger.warning(f"{len(pending)} tasks didn't complete")

    @property
    def count(self) -> int:
        """Number of active tasks."""
        return len(self._tasks)


# Global instance
background = BackgroundTaskManager()
```

---

## Retry with Exponential Backoff

```python
import asyncio
import random
from typing import TypeVar, Awaitable, Callable

T = TypeVar("T")


async def retry_async(
    coro_factory: Callable[[], Awaitable[T]],
    *,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retry_on: tuple[type[Exception], ...] = (Exception,)
) -> T:
    """
    Retry async operation with exponential backoff.

    Args:
        coro_factory: Function that creates new coroutine on each call
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries
        max_delay: Maximum delay cap
        exponential_base: Base for exponential calculation
        jitter: Add random jitter to delays
        retry_on: Exception types to retry on

    Returns:
        Result from successful execution

    Raises:
        Last exception if all retries fail
    """
    last_exception: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            return await coro_factory()
        except retry_on as e:
            last_exception = e

            if attempt == max_retries:
                break

            # Calculate delay
            delay = min(base_delay * (exponential_base ** attempt), max_delay)

            if jitter:
                delay = delay * (0.5 + random.random())

            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s")
            await asyncio.sleep(delay)

    raise last_exception


# Usage:
# result = await retry_async(
#     lambda: fetch_data(url),
#     max_retries=3,
#     retry_on=(httpx.HTTPError, asyncio.TimeoutError)
# )
```

---

## Async Queue Consumer

```python
import asyncio
from typing import TypeVar, Callable, Awaitable

T = TypeVar("T")


class AsyncQueueConsumer:
    """
    Consume items from async queue with concurrent workers.

    Usage:
        consumer = AsyncQueueConsumer(process_item, workers=5)
        await consumer.start()

        # Add items
        await consumer.put(item)

        # Shutdown
        await consumer.stop()
    """

    def __init__(
        self,
        handler: Callable[[T], Awaitable[None]],
        *,
        workers: int = 3,
        max_queue_size: int = 100
    ):
        self.handler = handler
        self.workers = workers
        self.queue: asyncio.Queue[T | None] = asyncio.Queue(maxsize=max_queue_size)
        self._tasks: list[asyncio.Task] = []
        self._running = False

    async def start(self) -> None:
        """Start worker tasks."""
        self._running = True
        for i in range(self.workers):
            task = asyncio.create_task(
                self._worker(i),
                name=f"worker-{i}"
            )
            self._tasks.append(task)

    async def stop(self, timeout: float = 5.0) -> None:
        """Stop workers gracefully."""
        self._running = False

        # Send stop signals
        for _ in range(self.workers):
            await self.queue.put(None)

        # Wait for workers
        await asyncio.wait(self._tasks, timeout=timeout)

        # Cancel any remaining
        for task in self._tasks:
            if not task.done():
                task.cancel()

    async def put(self, item: T) -> None:
        """Add item to queue."""
        await self.queue.put(item)

    async def _worker(self, worker_id: int) -> None:
        """Worker coroutine."""
        while self._running:
            item = await self.queue.get()

            if item is None:  # Stop signal
                break

            try:
                await self.handler(item)
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
            finally:
                self.queue.task_done()


# Usage:
# async def process(item):
#     await asyncio.sleep(0.1)
#     print(f"Processed: {item}")
#
# consumer = AsyncQueueConsumer(process, workers=5)
# await consumer.start()
# for i in range(100):
#     await consumer.put(i)
# await consumer.stop()
```

---

## HTTP Client Singleton

```python
import asyncio
import httpx
from typing import ClassVar


class HTTPClientSingleton:
    """
    Singleton HTTP client for reuse across requests.

    Usage:
        client = await HTTPClientSingleton.get_client()
        response = await client.get("/path")

        # On shutdown:
        await HTTPClientSingleton.close()
    """

    _instance: ClassVar[httpx.AsyncClient | None] = None
    _lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        """Get or create the singleton client."""
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = httpx.AsyncClient(
                        base_url="https://api.example.com",
                        timeout=30.0,
                        limits=httpx.Limits(
                            max_connections=100,
                            max_keepalive_connections=20
                        )
                    )
        return cls._instance

    @classmethod
    async def close(cls) -> None:
        """Close the singleton client."""
        if cls._instance:
            await cls._instance.aclose()
            cls._instance = None


# Usage:
# client = await HTTPClientSingleton.get_client()
# response = await client.get("/users/1")
```

---

## FastAPI Lifespan Template

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI


# Resources
db_pool = None
background_tasks = BackgroundTaskManager()
http_client = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage application lifecycle.

    - Startup: Initialize resources
    - Shutdown: Cleanup resources
    """
    global db_pool, http_client

    # Startup
    db_pool = await create_db_pool()
    http_client = httpx.AsyncClient(timeout=30.0)

    yield

    # Shutdown
    await background_tasks.shutdown()
    await http_client.aclose()
    await db_pool.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok"}
```

---

## Test Fixtures Template

```python
import asyncio
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing."""
    mock = AsyncMock()
    mock.get.return_value.json.return_value = {"id": 1, "name": "Test"}
    mock.get.return_value.raise_for_status = AsyncMock()
    return mock


@pytest.fixture
async def db_session():
    """Async database session fixture."""
    session = await create_test_session()
    await session.begin()

    yield session

    await session.rollback()
    await session.close()


@pytest.mark.asyncio
async def test_example(mock_http_client, db_session):
    """Example test using fixtures."""
    # Test implementation
    pass
```
