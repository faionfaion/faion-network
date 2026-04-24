# Caching Strategy Templates

Production-ready code templates for caching patterns.

## Cache-Aside Pattern (Python)

### Decorator-Based Cache-Aside

```python
import redis
import json
import hashlib
from functools import wraps
from typing import Callable, Any, Optional

class CacheManager:
    def __init__(self, redis_url: str = 'redis://localhost:6379/0'):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

    def cache_aside(
        self,
        key_prefix: str,
        ttl: int = 3600,
        key_builder: Optional[Callable] = None
    ):
        """
        Cache-aside decorator with automatic key generation.

        Args:
            key_prefix: Namespace prefix for cache keys
            ttl: Time to live in seconds
            key_builder: Custom function to build cache key from args
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                # Build cache key
                if key_builder:
                    cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
                else:
                    key_data = f"{args}:{sorted(kwargs.items())}"
                    key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
                    cache_key = f"{key_prefix}:{key_hash}"

                # Try cache first
                cached = self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)

                # Cache miss - call function
                result = func(*args, **kwargs)

                # Store in cache
                self.redis_client.setex(cache_key, ttl, json.dumps(result))
                return result

            # Add invalidation method
            def invalidate(*args, **kwargs):
                if key_builder:
                    cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
                    self.redis_client.delete(cache_key)
                else:
                    # Delete all keys matching prefix
                    pattern = f"{key_prefix}:*"
                    for key in self.redis_client.scan_iter(match=pattern, count=100):
                        self.redis_client.delete(key)

            wrapper.invalidate = invalidate
            return wrapper
        return decorator

# Usage Example
cache = CacheManager()

@cache.cache_aside("user", ttl=1800, key_builder=lambda user_id: user_id)
def get_user(user_id: str):
    # Expensive database query
    return db.users.find_one({"_id": user_id})

@cache.cache_aside("product_search", ttl=300)
def search_products(query: str, page: int = 1):
    # Expensive search operation
    return elasticsearch.search(query=query, page=page)

# Invalidate specific user
get_user.invalidate("user123")

# Invalidate all search results
search_products.invalidate()
```

### Class-Based Cache-Aside

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Optional
import pickle

T = TypeVar('T')

@dataclass
class CacheConfig:
    ttl: int = 3600
    prefix: str = "cache"
    serializer: str = "json"  # json | pickle | msgpack

class CacheAside(Generic[T]):
    def __init__(self, redis_client: redis.Redis, config: CacheConfig):
        self.redis = redis_client
        self.config = config

    def _serialize(self, data: T) -> bytes:
        if self.config.serializer == "json":
            return json.dumps(data).encode()
        elif self.config.serializer == "pickle":
            return pickle.dumps(data)
        elif self.config.serializer == "msgpack":
            import msgpack
            return msgpack.packb(data)
        raise ValueError(f"Unknown serializer: {self.config.serializer}")

    def _deserialize(self, data: bytes) -> T:
        if self.config.serializer == "json":
            return json.loads(data.decode())
        elif self.config.serializer == "pickle":
            return pickle.loads(data)
        elif self.config.serializer == "msgpack":
            import msgpack
            return msgpack.unpackb(data)
        raise ValueError(f"Unknown serializer: {self.config.serializer}")

    def get(
        self,
        key: str,
        loader: Callable[[], T],
        ttl: Optional[int] = None
    ) -> T:
        """
        Get value from cache or load from source.

        Args:
            key: Cache key
            loader: Function to load data on cache miss
            ttl: Override default TTL
        """
        cache_key = f"{self.config.prefix}:{key}"

        # Try cache
        cached = self.redis.get(cache_key)
        if cached:
            return self._deserialize(cached)

        # Load from source
        data = loader()

        # Store in cache
        ttl = ttl or self.config.ttl
        self.redis.setex(cache_key, ttl, self._serialize(data))

        return data

    def set(self, key: str, value: T, ttl: Optional[int] = None):
        """Set value in cache."""
        cache_key = f"{self.config.prefix}:{key}"
        ttl = ttl or self.config.ttl
        self.redis.setex(cache_key, ttl, self._serialize(value))

    def delete(self, key: str):
        """Delete key from cache."""
        cache_key = f"{self.config.prefix}:{key}"
        self.redis.delete(cache_key)

    def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern."""
        full_pattern = f"{self.config.prefix}:{pattern}"
        for key in self.redis.scan_iter(match=full_pattern, count=100):
            self.redis.delete(key)

# Usage
cache = CacheAside[dict](
    redis_client=redis.Redis(),
    config=CacheConfig(ttl=1800, prefix="user")
)

user = cache.get(
    key="123",
    loader=lambda: db.users.find_one({"_id": "123"})
)
```

## Write-Through Pattern

```python
class WriteThroughCache:
    def __init__(self, redis_client: redis.Redis, db, collection_name: str, ttl: int = 3600):
        self.redis = redis_client
        self.collection = db[collection_name]
        self.ttl = ttl
        self.key_prefix = collection_name

    def _cache_key(self, doc_id: str) -> str:
        return f"{self.key_prefix}:{doc_id}"

    def get(self, doc_id: str) -> Optional[dict]:
        """Get document from cache or database."""
        cache_key = self._cache_key(doc_id)

        # Try cache
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Load from DB
        doc = self.collection.find_one({"_id": doc_id})
        if doc:
            # Populate cache
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
            self.redis.setex(cache_key, self.ttl, json.dumps(doc))
        return doc

    def set(self, doc_id: str, data: dict) -> dict:
        """
        Write to DB and cache atomically.

        Returns updated document.
        """
        # Write to DB first
        self.collection.update_one(
            {"_id": doc_id},
            {"$set": data},
            upsert=True
        )

        # Read updated document
        doc = self.collection.find_one({"_id": doc_id})
        doc['_id'] = str(doc['_id'])

        # Update cache
        cache_key = self._cache_key(doc_id)
        self.redis.setex(cache_key, self.ttl, json.dumps(doc))

        return doc

    def delete(self, doc_id: str):
        """Delete from DB and cache."""
        # Delete from DB
        self.collection.delete_one({"_id": doc_id})

        # Delete from cache
        cache_key = self._cache_key(doc_id)
        self.redis.delete(cache_key)

# Usage
user_cache = WriteThroughCache(
    redis_client=redis.Redis(),
    db=mongo_client.mydb,
    collection_name="users",
    ttl=1800
)

# Reads from cache or DB
user = user_cache.get("user123")

# Writes to both DB and cache
updated_user = user_cache.set("user123", {"name": "John Doe"})

# Deletes from both
user_cache.delete("user123")
```

## Write-Behind Pattern

```python
import asyncio
from collections import defaultdict
from datetime import datetime
from pymongo import UpdateOne

class WriteBehindCache:
    def __init__(
        self,
        redis_client: redis.Redis,
        db,
        flush_interval: int = 5,
        batch_size: int = 100
    ):
        self.redis = redis_client
        self.db = db
        self.flush_interval = flush_interval
        self.batch_size = batch_size
        self.pending_writes = defaultdict(dict)
        self.running = False

    async def set(self, collection: str, doc_id: str, data: dict):
        """Write to cache immediately, queue for DB write."""
        # Write to cache immediately
        cache_key = f"{collection}:{doc_id}"
        self.redis.setex(cache_key, 3600, json.dumps(data))

        # Queue for async DB write
        self.pending_writes[collection][doc_id] = {
            "data": data,
            "timestamp": datetime.utcnow()
        }

    async def start(self):
        """Start background flush loop."""
        self.running = True
        while self.running:
            await asyncio.sleep(self.flush_interval)
            await self._flush_all()

    async def stop(self):
        """Stop background loop and flush remaining writes."""
        self.running = False
        await self._flush_all()

    async def _flush_all(self):
        """Flush all pending writes to database."""
        for collection, docs in list(self.pending_writes.items()):
            if not docs:
                continue

            # Prepare bulk write operations
            operations = []
            for doc_id, doc_info in list(docs.items()):
                operations.append(
                    UpdateOne(
                        {"_id": doc_id},
                        {"$set": doc_info["data"]},
                        upsert=True
                    )
                )

                # Process in batches
                if len(operations) >= self.batch_size:
                    try:
                        self.db[collection].bulk_write(operations)
                        operations = []
                    except Exception as e:
                        print(f"Bulk write error: {e}")

            # Write remaining operations
            if operations:
                try:
                    self.db[collection].bulk_write(operations)
                except Exception as e:
                    print(f"Bulk write error: {e}")

            # Clear processed writes
            self.pending_writes[collection].clear()

# Usage
cache = WriteBehindCache(
    redis_client=redis.Redis(),
    db=mongo_client.mydb,
    flush_interval=5
)

# Start background flush loop
asyncio.create_task(cache.start())

# Write to cache (DB write happens asynchronously)
await cache.set("users", "user123", {"name": "John Doe"})

# Graceful shutdown
await cache.stop()
```

## Tag-Based Invalidation

```python
class TaggedCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def set_with_tags(self, key: str, value: str, ttl: int, tags: list[str]):
        """
        Store value with associated tags.

        Args:
            key: Cache key
            value: Value to store
            ttl: Time to live
            tags: List of tags for grouped invalidation
        """
        pipe = self.redis.pipeline()

        # Set main key
        pipe.setex(key, ttl, value)

        # Associate key with tags
        for tag in tags:
            tag_key = f"cache:tag:{tag}"
            pipe.sadd(tag_key, key)
            pipe.expire(tag_key, ttl)

        pipe.execute()

    def invalidate_tags(self, *tags: str):
        """Invalidate all keys associated with tags."""
        keys_to_delete = set()

        for tag in tags:
            tag_key = f"cache:tag:{tag}"
            keys = self.redis.smembers(tag_key)
            keys_to_delete.update(keys)
            keys_to_delete.add(tag_key)

        if keys_to_delete:
            self.redis.delete(*keys_to_delete)

    def get_tags(self, key: str) -> set[str]:
        """Get all tags associated with a key."""
        tags = set()
        for tag_key in self.redis.scan_iter(match="cache:tag:*", count=100):
            if self.redis.sismember(tag_key, key):
                tag = tag_key.split(":", 2)[2]
                tags.add(tag)
        return tags

# Usage
cache = TaggedCache(redis.Redis())

# Store product with tags
cache.set_with_tags(
    key="product:123",
    value=json.dumps(product),
    ttl=3600,
    tags=["products", "category:electronics", "brand:apple"]
)

# Invalidate all products in category
cache.invalidate_tags("category:electronics")

# Invalidate specific brand
cache.invalidate_tags("brand:apple")

# Invalidate multiple tags
cache.invalidate_tags("products", "category:electronics")
```

## Version-Based Invalidation

```python
class VersionedCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def get_version(self, entity: str) -> int:
        """Get current version for entity type."""
        version_key = f"cache:version:{entity}"
        version = self.redis.get(version_key)
        return int(version) if version else 0

    def increment_version(self, entity: str) -> int:
        """Increment version (invalidates all old cached data)."""
        version_key = f"cache:version:{entity}"
        return self.redis.incr(version_key)

    def cache_key(self, entity: str, id: str) -> str:
        """Generate versioned cache key."""
        version = self.get_version(entity)
        return f"{entity}:v{version}:{id}"

    def get(self, entity: str, id: str) -> Optional[str]:
        """Get value with automatic version handling."""
        key = self.cache_key(entity, id)
        return self.redis.get(key)

    def set(self, entity: str, id: str, value: str, ttl: int = 3600):
        """Set value with current version."""
        key = self.cache_key(entity, id)
        self.redis.setex(key, ttl, value)

# Usage
cache = VersionedCache(redis.Redis())

# Store user data
cache.set("user", "123", json.dumps(user_data))

# Read with automatic versioning
user = cache.get("user", "123")

# Deploy new code with schema change
cache.increment_version("user")  # All old user:v0:* keys are now orphaned

# New reads use new version
user = cache.get("user", "123")  # Returns None (cache miss), will fetch fresh data
```

## Stampede Prevention

### Distributed Lock

```python
import time
import uuid
from contextlib import contextmanager

class StampedePrevention:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    @contextmanager
    def distributed_lock(self, key: str, timeout: int = 10):
        """
        Distributed lock to prevent cache stampede.

        Args:
            key: Lock key
            timeout: Lock expiration in seconds
        """
        lock_key = f"lock:{key}"
        lock_value = str(uuid.uuid4())
        acquired = False

        try:
            # Try to acquire lock
            acquired = self.redis.set(lock_key, lock_value, ex=timeout, nx=True)
            yield acquired
        finally:
            # Release lock only if we acquired it
            if acquired:
                # Use Lua script for atomic check-and-delete
                lua_script = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
                """
                self.redis.eval(lua_script, 1, lock_key, lock_value)

    def cache_with_lock(
        self,
        cache_key: str,
        loader: Callable[[], Any],
        ttl: int = 3600
    ) -> Any:
        """
        Load data with stampede prevention.

        Only one process loads data, others wait.
        """
        # Try cache first
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Attempt to acquire lock
        with self.distributed_lock(cache_key) as acquired:
            if acquired:
                # We got the lock - load data
                data = loader()
                self.redis.setex(cache_key, ttl, json.dumps(data))
                return data
            else:
                # Someone else is loading - wait and retry
                time.sleep(0.1)
                cached = self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)
                else:
                    # Fallback - load anyway
                    return loader()

# Usage
stampede = StampedePrevention(redis.Redis())

def expensive_query():
    time.sleep(2)  # Simulate slow query
    return {"result": "data"}

result = stampede.cache_with_lock(
    cache_key="report:daily",
    loader=expensive_query,
    ttl=3600
)
```

### Probabilistic Early Refresh

```python
import random

class EarlyRefreshCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def get_with_refresh(
        self,
        key: str,
        loader: Callable[[], Any],
        ttl: int = 3600,
        beta: float = 1.0
    ) -> Any:
        """
        Get value with probabilistic early refresh.

        Args:
            key: Cache key
            loader: Function to load data
            ttl: Time to live
            beta: Refresh probability factor (higher = more aggressive)
        """
        cached_data = self.redis.get(key)

        if cached_data:
            # Check if we should refresh early
            remaining_ttl = self.redis.ttl(key)

            if remaining_ttl > 0:
                # Calculate refresh probability
                # As TTL approaches 0, probability approaches 1
                delta = ttl - remaining_ttl
                probability = beta * delta / ttl

                if random.random() < probability:
                    # Refresh proactively
                    try:
                        data = loader()
                        self.redis.setex(key, ttl, json.dumps(data))
                        return data
                    except Exception:
                        # On error, return stale data
                        return json.loads(cached_data)

            return json.loads(cached_data)

        # Cache miss - load data
        data = loader()
        self.redis.setex(key, ttl, json.dumps(data))
        return data

# Usage
cache = EarlyRefreshCache(redis.Redis())

product = cache.get_with_refresh(
    key="product:123",
    loader=lambda: db.products.find_one({"_id": "123"}),
    ttl=3600,
    beta=1.5  # Refresh aggressively
)
```

## Node.js/TypeScript Templates

### Cache-Aside with node-redis

```typescript
import { createClient, RedisClientType } from 'redis';

interface CacheOptions {
  ttl?: number;
  prefix?: string;
}

class CacheManager {
  private client: RedisClientType;

  constructor(redisUrl: string = 'redis://localhost:6379') {
    this.client = createClient({ url: redisUrl });
    this.client.connect();
  }

  async cacheAside<T>(
    key: string,
    loader: () => Promise<T>,
    options: CacheOptions = {}
  ): Promise<T> {
    const { ttl = 3600, prefix = 'cache' } = options;
    const fullKey = `${prefix}:${key}`;

    // Try cache
    const cached = await this.client.get(fullKey);
    if (cached) {
      return JSON.parse(cached) as T;
    }

    // Load from source
    const data = await loader();

    // Store in cache
    await this.client.setEx(fullKey, ttl, JSON.stringify(data));

    return data;
  }

  async invalidate(pattern: string, prefix: string = 'cache'): Promise<void> {
    const fullPattern = `${prefix}:${pattern}`;
    const keys = [];

    for await (const key of this.client.scanIterator({ MATCH: fullPattern, COUNT: 100 })) {
      keys.push(key);
    }

    if (keys.length > 0) {
      await this.client.del(keys);
    }
  }

  async disconnect(): Promise<void> {
    await this.client.disconnect();
  }
}

// Usage
const cache = new CacheManager();

const user = await cache.cacheAside(
  'user:123',
  async () => await db.users.findOne({ id: '123' }),
  { ttl: 1800, prefix: 'user' }
);

await cache.invalidate('user:*', 'user');
```

## HTTP Cache Headers (Express.js)

```javascript
const express = require('express');
const app = express();

// Static assets - long cache
app.use('/static', express.static('public', {
  maxAge: '1y',
  immutable: true
}));

// API with cache control
app.get('/api/products/:id', async (req, res) => {
  const product = await getProduct(req.params.id);

  // Generate ETag
  const etag = hashObject(product);

  // Check If-None-Match
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }

  // Set cache headers
  res.set({
    'Cache-Control': 'public, max-age=300, stale-while-revalidate=60',
    'ETag': etag,
    'Vary': 'Accept-Encoding'
  });

  res.json(product);
});

// Private user data - no cache
app.get('/api/user/profile', async (req, res) => {
  const profile = await getUserProfile(req.user.id);

  res.set({
    'Cache-Control': 'private, no-cache, must-revalidate'
  });

  res.json(profile);
});

// CDN-cacheable endpoint
app.get('/api/catalog', async (req, res) => {
  const catalog = await getProductCatalog();

  res.set({
    'Cache-Control': 'public, s-maxage=600, max-age=300',
    'Surrogate-Key': 'catalog products'
  });

  res.json(catalog);
});
```

## Go Cache Templates

```go
package cache

import (
    "context"
    "encoding/json"
    "time"
    "github.com/go-redis/redis/v8"
)

type CacheManager struct {
    client *redis.Client
}

func NewCacheManager(addr string) *CacheManager {
    return &CacheManager{
        client: redis.NewClient(&redis.Options{
            Addr: addr,
        }),
    }
}

func (c *CacheManager) CacheAside(
    ctx context.Context,
    key string,
    ttl time.Duration,
    loader func() (interface{}, error),
) (interface{}, error) {
    // Try cache
    cached, err := c.client.Get(ctx, key).Result()
    if err == nil {
        var result interface{}
        json.Unmarshal([]byte(cached), &result)
        return result, nil
    }

    // Load from source
    data, err := loader()
    if err != nil {
        return nil, err
    }

    // Store in cache
    encoded, _ := json.Marshal(data)
    c.client.Set(ctx, key, encoded, ttl)

    return data, nil
}
```
