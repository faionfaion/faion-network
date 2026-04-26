"""Minimal Python FeatureFlagService for CD.

WARNING: Uses a short-TTL in-process cache only. For production use a proper
flag SDK (LaunchDarkly, Unleash) with SSE/WebSocket streaming to avoid hiding
flag changes for hours. This sketch shows the evaluation contract only.
"""
from typing import Optional
import httpx


class FeatureFlagService:
    """Evaluate feature flags via HTTP API with a short in-process cache.

    Separates deployment (code ships) from release (flag toggled).
    """

    def __init__(self, api_url: str, api_key: str, cache_ttl_seconds: int = 30):
        self.api_url = api_url
        self.api_key = api_key
        self.cache_ttl = cache_ttl_seconds
        self._cache: dict[str, tuple[bool, float]] = {}

    def is_enabled(
        self,
        flag: str,
        user_id: Optional[str] = None,
        default: bool = False,
    ) -> bool:
        """Return True if flag is enabled for user_id (or globally)."""
        import time
        cache_key = f"{flag}:{user_id or 'global'}"
        cached = self._cache.get(cache_key)
        if cached and time.time() - cached[1] < self.cache_ttl:
            return cached[0]
        try:
            response = httpx.post(
                f"{self.api_url}/flags/{flag}/evaluate",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"user_id": user_id},
                timeout=0.5,
            )
            result = response.json().get("enabled", default)
        except Exception:
            result = default
        self._cache[cache_key] = (result, time.time())
        return result
