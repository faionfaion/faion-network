"""
Proxy pattern — Python implementation.
Demonstrates Virtual Proxy (lazy initialization) and Cache Proxy (memoization).
All proxy types implement the same interface as the real subject.
"""
from __future__ import annotations
from typing import Protocol


# --- Subject interface ---
class ImageLoader(Protocol):
    def render(self) -> str: ...
    def dimensions(self) -> tuple[int, int]: ...


# --- Real Subject: expensive to create ---
class HighResImage:
    """Loading this image is expensive (disk I/O, network, decompression)."""

    def __init__(self, file_path: str) -> None:
        print(f"[HighResImage] Loading {file_path} from disk...")  # expensive
        self._file_path = file_path
        self._data = f"<pixels from {file_path}>"  # simulate loaded image

    def render(self) -> str:
        return f"Rendering {self._file_path}"

    def dimensions(self) -> tuple[int, int]:
        return (3840, 2160)


# ===================================================================
# VIRTUAL PROXY: lazy initialization
# Delays creation of the real object until it is first needed.
# ===================================================================

class LazyImageProxy:
    """
    Virtual Proxy for HighResImage.
    The real image is not loaded until render() is first called.
    """

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._real_image: HighResImage | None = None

    def _load(self) -> HighResImage:
        if self._real_image is None:
            self._real_image = HighResImage(self._file_path)
        return self._real_image

    def render(self) -> str:
        return self._load().render()

    def dimensions(self) -> tuple[int, int]:
        return self._load().dimensions()


# ===================================================================
# CACHE PROXY: memoization
# Caches expensive results; avoids re-computation on repeated calls.
# ===================================================================

class DatabaseQueryProxy:
    """
    Cache Proxy for database queries.
    Returns cached result on repeated calls with the same key.
    In production: add TTL and eviction logic.
    """

    def __init__(self, db_executor) -> None:
        self._executor = db_executor
        self._cache: dict[str, object] = {}

    def execute(self, query: str, params: tuple = ()) -> object:
        cache_key = f"{query}:{params}"
        if cache_key not in self._cache:
            print(f"[CacheProxy] Cache miss — executing query")
            self._cache[cache_key] = self._executor.execute(query, params)
        else:
            print(f"[CacheProxy] Cache hit")
        return self._cache[cache_key]

    def invalidate(self, pattern: str) -> None:
        """Invalidate cache entries matching a pattern prefix."""
        keys_to_remove = [k for k in self._cache if k.startswith(pattern)]
        for k in keys_to_remove:
            del self._cache[k]


# ===================================================================
# PROTECTION PROXY: access control
# ===================================================================

class ProtectedService:
    """Wraps a real service and enforces permission checks before delegation."""

    def __init__(self, real_service, user_roles: list[str]) -> None:
        self._service = real_service
        self._roles = user_roles

    def admin_action(self) -> str:
        if "admin" not in self._roles:
            raise PermissionError("admin role required")
        return self._service.admin_action()

    def read_data(self) -> str:
        return self._service.read_data()  # no restriction


# --- Usage ---
if __name__ == "__main__":
    # Virtual proxy: image not loaded until render() is called
    image: ImageLoader = LazyImageProxy("photo.jpg")
    print("Proxy created — image not loaded yet")
    print(image.render())   # triggers load
    print(image.render())   # uses already-loaded image
