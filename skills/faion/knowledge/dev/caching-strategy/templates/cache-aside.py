# purpose: Stdlib cache-aside helper with jittered TTL + single-flight
# consumes: key + loader fn
# produces: cached value or fresh load
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~300 tokens when loaded
"""cache-aside.py — Cache-aside decorator backed by Redis: jittered TTL, single-flight miss, invalidation.

Usage:
    @cache_aside("user", ttl=1800, key_builder=lambda user_id: user_id)
    def get_user(user_id: str) -> dict:
        return db.users.find_one({"_id": user_id})

    get_user.invalidate(user_id)   # explicit invalidation after a write

The header promises two things the first version of this file did not do:

* JITTERED TTL — every key written at the same moment with the same `ttl`
  expires at the same moment, and the next second of traffic hits the origin
  together. `setex(key, ttl)` is exactly that. A +/-10% jitter spreads the
  expiries so a warm-up never turns into a synchronised stampede.
* SINGLE-FLIGHT on miss — with a hot key at 500 rps and a 1.8 s loader, an
  unguarded miss path sends ~900 concurrent identical queries the moment the
  TTL lapses. One caller loads; the rest wait on the lock and read the value
  it writes. The lock carries an owner token so a slow winner cannot release a
  lock a faster retry now holds (see cache-singleflight.py for the same rule
  in async form).
"""
import hashlib
import json
import random
import time
import uuid
from functools import wraps

import redis

_redis: redis.Redis = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Release only if we still own the lock. GET-then-DEL is a race; this is not.
_RELEASE = _redis.register_script(
    "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) end return 0"
)


def _jittered(ttl: int, spread: float = 0.10) -> int:
    return max(1, int(ttl * random.uniform(1.0 - spread, 1.0 + spread)))


def cache_aside(key_prefix: str, ttl: int = 3600, key_builder=None,
                lock_ttl: int = 30, wait_s: float = 5.0):
    """Decorator: Redis first; on miss exactly one caller loads, the rest wait for its write."""

    def build_key(*args, **kwargs) -> str:
        if key_builder:
            return f"{key_prefix}:{key_builder(*args, **kwargs)}"
        raw = f"{args}:{sorted(kwargs.items())}"
        return f"{key_prefix}:{hashlib.md5(raw.encode()).hexdigest()[:12]}"

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = build_key(*args, **kwargs)
            cached = _redis.get(cache_key)
            if cached is not None:
                return json.loads(cached)

            lock_key = f"lock:{cache_key}"
            token = uuid.uuid4().hex
            if _redis.set(lock_key, token, nx=True, ex=lock_ttl):
                try:
                    result = func(*args, **kwargs)
                    # Negative results are cached too, briefly, so a missing row
                    # cannot hammer the origin; the shorter TTL is also jittered.
                    life = _jittered(ttl if result is not None else min(ttl, 60))
                    _redis.set(cache_key, json.dumps(result), ex=life)
                    return result
                finally:
                    _RELEASE(keys=[lock_key], args=[token])

            # Lost the race: wait for the winner's write, bounded.
            deadline = time.monotonic() + wait_s
            while time.monotonic() < deadline:
                time.sleep(0.05)
                cached = _redis.get(cache_key)
                if cached is not None:
                    return json.loads(cached)
            # Winner died or is slower than wait_s: load independently rather
            # than fail the request. This is the one path that can double-load.
            return func(*args, **kwargs)

        def invalidate(*args, **kwargs):
            if not key_builder:
                raise ValueError("Provide key_builder to use .invalidate()")
            _redis.delete(build_key(*args, **kwargs))

        wrapper.invalidate = invalidate
        return wrapper

    return decorator
