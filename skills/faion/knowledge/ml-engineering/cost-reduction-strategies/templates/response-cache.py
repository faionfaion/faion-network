"""
ResponseCache + CachedLLMClient: SHA-256 keyed response caching with Redis and memory backends.
Input:  redis_client (optional), ttl_hours, max_memory_items
Output: cached str response or None on miss
"""
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional

try:
    import redis as redis_lib
except ImportError:
    redis_lib = None


class ResponseCache:
    def __init__(self, redis_client=None, ttl_hours: int = 24, max_memory_items: int = 1000):
        self.redis = redis_client
        self.ttl = timedelta(hours=ttl_hours)
        self.memory_cache: dict = {}
        self.max_memory_items = max_memory_items

    def _make_key(self, model: str, messages: list, **kwargs) -> str:
        key_data = {
            "model": model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 1.0),
            "max_tokens": kwargs.get("max_tokens"),
        }
        return hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

    def get(self, model: str, messages: list, **kwargs) -> Optional[str]:
        key = self._make_key(model, messages, **kwargs)
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now() < entry["expires"]:
                return entry["response"]
            del self.memory_cache[key]
        if self.redis:
            cached = self.redis.get(f"llm:{key}")
            if cached:
                return json.loads(cached)
        return None

    def set(self, model: str, messages: list, response: str, **kwargs):
        key = self._make_key(model, messages, **kwargs)
        if len(self.memory_cache) >= self.max_memory_items:
            oldest = sorted(self.memory_cache, key=lambda k: self.memory_cache[k]["created"])[:100]
            for k in oldest:
                del self.memory_cache[k]
        self.memory_cache[key] = {
            "response": response,
            "created": datetime.now(),
            "expires": datetime.now() + self.ttl,
        }
        if self.redis:
            self.redis.setex(f"llm:{key}", int(self.ttl.total_seconds()), json.dumps(response))


class CachedLLMClient:
    def __init__(self, client, cache: Optional[ResponseCache] = None):
        self.client = client
        self.cache = cache or ResponseCache()
        self.hits = 0
        self.misses = 0

    def complete(self, model: str, messages: list, use_cache: bool = True, **kwargs) -> str:
        temperature = kwargs.get("temperature", 1.0)
        cacheable = use_cache and temperature == 0
        if cacheable:
            cached = self.cache.get(model, messages, **kwargs)
            if cached:
                self.hits += 1
                return cached
        self.misses += 1
        resp = self.client.chat.completions.create(model=model, messages=messages, **kwargs)
        result = resp.choices[0].message.content
        if cacheable:
            self.cache.set(model, messages, result, **kwargs)
        return result
