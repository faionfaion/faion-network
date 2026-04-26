"""cache-aside.py — Cache-aside decorator backed by Redis with TTL, key builder, and invalidation.

Usage:
    @cache_aside("user", ttl=1800, key_builder=lambda user_id: user_id)
    def get_user(user_id: str) -> dict:
        return db.users.find_one({"_id": user_id})

    # Explicit invalidation after write:
    get_user.invalidate(user_id)
"""
import hashlib
import json
from functools import wraps

import redis

_redis: redis.Redis = redis.Redis(host="localhost", port=6379, decode_responses=True)


def cache_aside(key_prefix: str, ttl: int = 3600, key_builder=None):
    """Decorator: check Redis first; on miss load from function, cache result."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
            else:
                key_data = f"{args}:{sorted(kwargs.items())}"
                key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
                cache_key = f"{key_prefix}:{key_hash}"

            cached = _redis.get(cache_key)
            if cached is not None:
                return json.loads(cached)

            result = func(*args, **kwargs)
            if result is not None:
                _redis.setex(cache_key, ttl, json.dumps(result))
            else:
                # Negative cache with shorter TTL to prevent DB hammering
                _redis.setex(cache_key, min(ttl, 60), json.dumps(None))
            return result

        def invalidate(*args, **kwargs):
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
                _redis.delete(cache_key)
            else:
                # Cannot compute key without args — caller must supply them
                raise ValueError("Provide key_builder to use .invalidate()")

        wrapper.invalidate = invalidate
        return wrapper
    return decorator
