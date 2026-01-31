# Caching Strategy Examples

Real-world caching implementations for various use cases.

## E-Commerce Product Catalog

### Problem
Product catalog with 100k+ products, 10k RPS reads, infrequent updates.

### Solution: Multi-Layer Caching

```python
from dataclasses import dataclass
from typing import Optional
import redis
from functools import lru_cache

@dataclass
class Product:
    id: str
    name: str
    price: float
    category: str
    stock: int

class ProductCache:
    def __init__(self, redis_client: redis.Redis, db):
        self.redis = redis_client
        self.db = db

    # L1: Process-local cache for hot products
    @lru_cache(maxsize=1000)
    def _get_hot_product_local(self, product_id: str) -> Optional[dict]:
        return None  # Cache miss triggers L2 lookup

    # L2: Redis distributed cache
    def _get_product_redis(self, product_id: str) -> Optional[dict]:
        cached = self.redis.get(f"product:{product_id}")
        if cached:
            return json.loads(cached)
        return None

    # L3: Database
    def _get_product_db(self, product_id: str) -> Optional[dict]:
        return self.db.products.find_one({"_id": product_id})

    def get_product(self, product_id: str) -> Optional[Product]:
        # Try L1 (local)
        data = self._get_hot_product_local(product_id)

        # Try L2 (Redis)
        if not data:
            data = self._get_product_redis(product_id)

        # Try L3 (Database)
        if not data:
            data = self._get_product_db(product_id)
            if data:
                # Populate L2
                self.redis.setex(
                    f"product:{product_id}",
                    3600,  # 1 hour TTL
                    json.dumps(data)
                )

        return Product(**data) if data else None

    def update_product(self, product_id: str, updates: dict):
        # Update database
        self.db.products.update_one(
            {"_id": product_id},
            {"$set": updates}
        )

        # Invalidate all cache layers
        self._get_hot_product_local.cache_clear()
        self.redis.delete(f"product:{product_id}")

        # Invalidate category cache
        product = self.db.products.find_one({"_id": product_id})
        if product:
            self.redis.delete(f"category:{product['category']}")

# Usage
cache = ProductCache(redis.Redis(), mongo_client.shop)

# Read (hits L1 → L2 → L3)
product = cache.get_product("prod_123")

# Write (invalidates all layers)
cache.update_product("prod_123", {"price": 29.99})
```

**Metrics:**
- L1 hit rate: 40% (hot products)
- L2 hit rate: 50% (warm products)
- L3 hit rate: 10% (cold products)
- Average latency: 5ms (L1), 15ms (L2), 50ms (L3)

---

## User Session Management

### Problem
10k concurrent users, session data 1-5KB, 15-minute inactivity timeout.

### Solution: Redis Session Store

```python
import hashlib
import secrets
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.session_ttl = 900  # 15 minutes

    def create_session(self, user_id: str, metadata: dict = None) -> str:
        """Create new session and return session token."""
        # Generate secure session token
        session_token = secrets.token_urlsafe(32)

        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }

        # Store in Redis with sliding expiration
        session_key = f"session:{session_token}"
        self.redis.setex(session_key, self.session_ttl, json.dumps(session_data))

        return session_token

    def get_session(self, session_token: str) -> Optional[dict]:
        """Get session and refresh TTL."""
        session_key = f"session:{session_token}"

        # Get session data
        session_data = self.redis.get(session_key)
        if not session_data:
            return None

        # Refresh TTL (sliding expiration)
        self.redis.expire(session_key, self.session_ttl)

        return json.loads(session_data)

    def update_session(self, session_token: str, updates: dict):
        """Update session data."""
        session_key = f"session:{session_token}"

        # Get current data
        session_data = self.get_session(session_token)
        if not session_data:
            raise ValueError("Session not found")

        # Merge updates
        session_data["metadata"].update(updates)

        # Save with refreshed TTL
        self.redis.setex(session_key, self.session_ttl, json.dumps(session_data))

    def destroy_session(self, session_token: str):
        """Delete session (logout)."""
        session_key = f"session:{session_token}"
        self.redis.delete(session_key)

    def get_active_sessions(self, user_id: str) -> list[str]:
        """Get all active sessions for a user."""
        sessions = []
        for key in self.redis.scan_iter(match="session:*", count=100):
            session_data = self.redis.get(key)
            if session_data:
                data = json.loads(session_data)
                if data["user_id"] == user_id:
                    token = key.decode().split(":", 1)[1]
                    sessions.append(token)
        return sessions

# Usage
sessions = SessionManager(redis.Redis())

# Login
token = sessions.create_session(
    user_id="user_123",
    metadata={"ip": "192.168.1.1", "user_agent": "Mozilla/5.0"}
)

# Validate session (auto-extends TTL)
session_data = sessions.get_session(token)

# Update session
sessions.update_session(token, {"last_page": "/dashboard"})

# Logout
sessions.destroy_session(token)
```

---

## Rate Limiting

### Problem
API rate limiting: 1000 requests/hour per API key.

### Solution: Redis Sliding Window

```python
import time

class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def check_rate_limit(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, dict]:
        """
        Check if request is within rate limit.

        Returns:
            (allowed, info) where info contains limit details
        """
        rate_key = f"rate:{key}"
        now = time.time()
        window_start = now - window_seconds

        # Remove old requests outside window
        self.redis.zremrangebyscore(rate_key, 0, window_start)

        # Count requests in current window
        request_count = self.redis.zcard(rate_key)

        if request_count < max_requests:
            # Add current request
            self.redis.zadd(rate_key, {str(now): now})
            self.redis.expire(rate_key, window_seconds)

            return True, {
                "allowed": True,
                "limit": max_requests,
                "remaining": max_requests - request_count - 1,
                "reset": int(now + window_seconds)
            }
        else:
            # Get oldest request in window
            oldest = self.redis.zrange(rate_key, 0, 0, withscores=True)
            reset_time = int(oldest[0][1] + window_seconds) if oldest else int(now + window_seconds)

            return False, {
                "allowed": False,
                "limit": max_requests,
                "remaining": 0,
                "reset": reset_time
            }

# Usage with Flask
from flask import Flask, request, jsonify

app = Flask(__name__)
limiter = RateLimiter(redis.Redis())

@app.before_request
def rate_limit():
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return jsonify({"error": "API key required"}), 401

    # 1000 requests per hour
    allowed, info = limiter.check_rate_limit(
        key=f"api:{api_key}",
        max_requests=1000,
        window_seconds=3600
    )

    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(info["limit"])
    response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
    response.headers["X-RateLimit-Reset"] = str(info["reset"])

    if not allowed:
        return jsonify({
            "error": "Rate limit exceeded",
            "retry_after": info["reset"] - int(time.time())
        }), 429
```

---

## Feed/Timeline Caching

### Problem
Social media feed, personalized per user, 100+ items, updated frequently.

### Solution: Redis Sorted Sets

```python
class FeedCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def add_to_feed(self, user_id: str, post_id: str, timestamp: float):
        """Add post to user's feed."""
        feed_key = f"feed:{user_id}"

        # Add to sorted set (score = timestamp)
        self.redis.zadd(feed_key, {post_id: timestamp})

        # Keep only latest 1000 posts
        self.redis.zremrangebyrank(feed_key, 0, -1001)

        # Set expiration
        self.redis.expire(feed_key, 86400)  # 24 hours

    def get_feed(
        self,
        user_id: str,
        page: int = 1,
        per_page: int = 20
    ) -> list[dict]:
        """Get paginated feed for user."""
        feed_key = f"feed:{user_id}"

        # Calculate range
        start = (page - 1) * per_page
        end = start + per_page - 1

        # Get post IDs (newest first)
        post_ids = self.redis.zrevrange(feed_key, start, end)

        if not post_ids:
            return []

        # Fetch post data (batch)
        posts = []
        for post_id in post_ids:
            post_data = self.redis.get(f"post:{post_id}")
            if post_data:
                posts.append(json.loads(post_data))

        return posts

    def fanout_to_followers(self, post_id: str, timestamp: float, follower_ids: list[str]):
        """Add post to all followers' feeds (write fanout)."""
        pipe = self.redis.pipeline()

        for follower_id in follower_ids:
            feed_key = f"feed:{follower_id}"
            pipe.zadd(feed_key, {post_id: timestamp})
            pipe.zremrangebyrank(feed_key, 0, -1001)
            pipe.expire(feed_key, 86400)

        pipe.execute()

# Usage
feed_cache = FeedCache(redis.Redis())

# User posts (fanout to followers)
followers = get_followers("user_123")
feed_cache.fanout_to_followers(
    post_id="post_456",
    timestamp=time.time(),
    follower_ids=followers
)

# User reads feed
feed = feed_cache.get_feed("user_789", page=1, per_page=20)
```

---

## Geospatial Caching

### Problem
Find nearby restaurants within 5km, 1000 RPS.

### Solution: Redis Geospatial Index

```python
class LocationCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def add_location(self, location_id: str, lon: float, lat: float, metadata: dict):
        """Add location to geo index."""
        # Add to geospatial index
        self.redis.geoadd("locations", (lon, lat, location_id))

        # Store metadata separately
        self.redis.setex(
            f"location:{location_id}",
            86400,  # 24 hours
            json.dumps(metadata)
        )

    def search_nearby(
        self,
        lon: float,
        lat: float,
        radius_km: float,
        limit: int = 20
    ) -> list[dict]:
        """Find locations within radius."""
        # Search by radius
        results = self.redis.georadius(
            "locations",
            lon,
            lat,
            radius_km,
            unit="km",
            withdist=True,
            withcoord=True,
            count=limit,
            sort="ASC"
        )

        # Fetch metadata for each result
        locations = []
        for location_id, distance, coords in results:
            metadata = self.redis.get(f"location:{location_id}")
            if metadata:
                location_data = json.loads(metadata)
                location_data["distance_km"] = float(distance)
                location_data["coordinates"] = coords
                locations.append(location_data)

        return locations

# Usage
location_cache = LocationCache(redis.Redis())

# Add restaurants
location_cache.add_location(
    location_id="restaurant_1",
    lon=-122.4194,
    lat=37.7749,
    metadata={
        "name": "Pizza Palace",
        "cuisine": "Italian",
        "rating": 4.5
    }
)

# Search nearby (user at San Francisco)
nearby = location_cache.search_nearby(
    lon=-122.4194,
    lat=37.7749,
    radius_km=5.0,
    limit=10
)
```

---

## Analytics Dashboard Caching

### Problem
Complex analytics queries, 5-10 second execution, updated every 15 minutes.

### Solution: Materialized View Pattern

```python
import schedule
import threading

class AnalyticsCache:
    def __init__(self, redis_client: redis.Redis, db):
        self.redis = redis_client
        self.db = db

    def compute_dashboard_data(self) -> dict:
        """Expensive aggregation query."""
        pipeline = [
            {"$match": {"created_at": {"$gte": datetime.utcnow() - timedelta(days=30)}}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                "total_revenue": {"$sum": "$amount"},
                "order_count": {"$sum": 1},
                "avg_order_value": {"$avg": "$amount"}
            }},
            {"$sort": {"_id": 1}}
        ]

        results = list(self.db.orders.aggregate(pipeline))
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "data": results
        }

    def refresh_dashboard(self):
        """Background task to refresh dashboard data."""
        try:
            data = self.compute_dashboard_data()
            self.redis.setex(
                "dashboard:revenue",
                1800,  # 30 minutes (2x refresh interval)
                json.dumps(data)
            )
            print(f"Dashboard refreshed at {datetime.utcnow()}")
        except Exception as e:
            print(f"Dashboard refresh failed: {e}")

    def get_dashboard(self) -> dict:
        """Get cached dashboard data."""
        cached = self.redis.get("dashboard:revenue")
        if cached:
            return json.loads(cached)

        # Cache miss - compute now
        data = self.compute_dashboard_data()
        self.redis.setex("dashboard:revenue", 1800, json.dumps(data))
        return data

    def start_background_refresh(self):
        """Start background refresh every 15 minutes."""
        schedule.every(15).minutes.do(self.refresh_dashboard)

        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)

        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()

# Usage
analytics = AnalyticsCache(redis.Redis(), mongo_client.analytics)

# Start background refresh
analytics.start_background_refresh()

# API endpoint
@app.get("/api/dashboard")
def dashboard():
    data = analytics.get_dashboard()
    return jsonify(data)
```

**Results:**
- Query time without cache: 8 seconds
- Query time with cache: 15ms
- Refresh interval: 15 minutes
- Stale data tolerance: Acceptable for business metrics

---

## Comparison Matrix

| Use Case | Pattern | TTL | Invalidation | Hit Rate Target |
|----------|---------|-----|--------------|-----------------|
| Product catalog | Multi-layer | 1 hour | Event-based | 90%+ |
| User sessions | Write-through | 15 min | Sliding window | 95%+ |
| Rate limiting | Sliding window | 1 hour | Automatic | N/A |
| Social feed | Write fanout | 24 hours | Real-time | 85%+ |
| Geospatial | Cache-aside | 24 hours | Event-based | 80%+ |
| Analytics | Materialized view | 15 min | Background refresh | 99%+ |
