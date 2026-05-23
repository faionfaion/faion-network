# purpose: Django CACHES configuration with Redis.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a caching-architecture artefact validating against scripts/validate-caching-architecture.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
"""
django-cache-settings.py — Django CACHES settings for default + session caches
using django-redis backend.

Requires: django-redis >= 5.0, Django >= 4.0
Install:  pip install django-redis

Place this in settings.py (or settings/production.py).
"""

import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
CACHE_KEY_PREFIX = os.environ.get("CACHE_KEY_PREFIX", "prod")

CACHES = {
    # ---- Default application cache -----------------------------------------
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 300,  # seconds; None = no expiry (use with caution)
        "KEY_PREFIX": CACHE_KEY_PREFIX,  # namespaces keys by env
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            # Connection pool: shared across threads in the same process
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "socket_connect_timeout": 1,   # seconds
                "socket_timeout": 1,            # seconds
            },
            # Ignore cache backend exceptions (return None on Redis error)
            # Set False in development to surface Redis issues early.
            "IGNORE_EXCEPTIONS": True,
            # Compress values > 1KB (requires python-lz4 or similar)
            # "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
        },
    },
    # ---- Session cache (separate DB index to allow selective flush) ---------
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_SESSION_URL", "redis://127.0.0.1:6379/1"),
        "TIMEOUT": 86400,  # 24h session TTL
        "KEY_PREFIX": f"{CACHE_KEY_PREFIX}:session",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,  # Session failures should surface
        },
    },
}

# Use Redis for Django sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# ---------------------------------------------------------------------------
# Usage examples in views / services
# ---------------------------------------------------------------------------
#
# from django.core.cache import cache
#
# # Simple get/set
# user = cache.get(f"user:{user_id}")
# if user is None:
#     user = User.objects.get(pk=user_id)
#     cache.set(f"user:{user_id}", user, timeout=300)
#
# # get_or_set (atomic in Django >= 4.0)
# user = cache.get_or_set(f"user:{user_id}", lambda: User.objects.get(pk=user_id), 300)
#
# # Decorator: cache entire view for 5 minutes
# from django.views.decorators.cache import cache_page
#
# @cache_page(60 * 5)
# def product_list(request):
#     ...
#
# # Invalidate a key
# cache.delete(f"user:{user_id}")
#
# # Invalidate by pattern (django-redis specific, use sparingly)
# from django_redis import get_redis_connection
# con = get_redis_connection("default")
# keys = con.keys(f"{CACHE_KEY_PREFIX}:user:*")
# if keys:
#     con.delete(*keys)
