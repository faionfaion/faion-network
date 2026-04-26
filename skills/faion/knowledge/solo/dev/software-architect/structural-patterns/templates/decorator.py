"""
Decorator pattern — Python implementation.
Two forms: function decorator (Python-native) and class decorator (GoF structural).
Both add behavior without subclassing; class decorators can be stacked.
"""
from __future__ import annotations
import functools
import time
import logging
from typing import Protocol, Any

logger = logging.getLogger(__name__)


# ===================================================================
# FORM 1: Python function decorator (language-native, simplest)
# ===================================================================

def log_calls(func):
    """Add entry/exit logging to any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Calling %s", func.__name__)
        result = func(*args, **kwargs)
        logger.info("Finished %s", func.__name__)
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry on exception with delay."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_attempts:
                        raise
                    logger.warning("Attempt %d/%d failed: %s", attempt, max_attempts, exc)
                    time.sleep(delay)
        return wrapper
    return decorator


@log_calls
@retry(max_attempts=3)
def fetch_data(url: str) -> dict:
    """Function with stacked decorators: log_calls wraps retry wraps fetch_data."""
    import urllib.request
    with urllib.request.urlopen(url) as resp:
        import json
        return json.loads(resp.read())


# ===================================================================
# FORM 2: Class-based GoF Decorator
# Use when: runtime stacking is needed, decorators maintain state,
#           or the same interface must be upheld for type checking.
# ===================================================================

class DataStore(Protocol):
    """Component interface: both ConcreteComponent and all Decorators implement this."""
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...


class InMemoryStore:
    """ConcreteComponent: the real object being decorated."""
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value


class LoggingDecorator:
    """Decorator 1: logs all reads and writes."""
    def __init__(self, store: DataStore) -> None:
        self._store = store

    def get(self, key: str) -> Any:
        value = self._store.get(key)
        logger.info("GET key=%s hit=%s", key, value is not None)
        return value

    def set(self, key: str, value: Any) -> None:
        logger.info("SET key=%s", key)
        self._store.set(key, value)


class CachingDecorator:
    """Decorator 2: caches get results in a local dict (TTL omitted for brevity)."""
    def __init__(self, store: DataStore) -> None:
        self._store = store
        self._cache: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        if key not in self._cache:
            self._cache[key] = self._store.get(key)
        return self._cache[key]

    def set(self, key: str, value: Any) -> None:
        self._cache.pop(key, None)  # invalidate cache on write
        self._store.set(key, value)


# Stacking: LoggingDecorator wraps CachingDecorator wraps InMemoryStore
if __name__ == "__main__":
    store: DataStore = LoggingDecorator(CachingDecorator(InMemoryStore()))
    store.set("user:1", {"name": "Alice"})
    print(store.get("user:1"))  # logged + cached
    print(store.get("user:1"))  # served from cache (no underlying get)
