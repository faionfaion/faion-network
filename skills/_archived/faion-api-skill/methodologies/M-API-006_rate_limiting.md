# M-API-006: Rate Limiting

## Metadata
- **ID:** M-API-006
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, rate-limiting, throttling, security]
- **Agent:** faion-api-agent

---

## Problem

Without rate limiting:
- Single client can overwhelm your API
- DoS attacks are easy to execute
- Costs spiral from excessive usage
- Fair usage is impossible to enforce
- No protection against scraping or abuse

---

## Framework

### Step 1: Choose Rate Limiting Strategy

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Fixed Window | Count requests per fixed time window | Simple, high burst tolerance |
| Sliding Window | Rolling window, smoother | More accurate, less bursty |
| Token Bucket | Tokens replenish over time | Allows controlled bursts |
| Leaky Bucket | Constant rate, queue excess | Smooth, predictable |

### Step 2: Define Rate Limits

**Common patterns:**

| Tier | Requests | Window | Use Case |
|------|----------|--------|----------|
| Anonymous | 20/min | 1 minute | Public endpoints |
| Free | 100/min | 1 minute | Basic users |
| Pro | 1000/min | 1 minute | Paid users |
| Enterprise | 10000/min | 1 minute | Large customers |

**Per-endpoint limits:**

| Endpoint | Limit | Reason |
|----------|-------|--------|
| POST /auth/login | 5/min | Prevent brute force |
| GET /users | 100/min | Standard read |
| POST /upload | 10/min | Resource intensive |
| GET /search | 30/min | Expensive query |

### Step 3: Implement Fixed Window

```python
# Django with django-ratelimit
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/m', block=True)
def my_view(request):
    return JsonResponse({'data': 'success'})

# Custom implementation with Redis
import redis
from django.http import JsonResponse

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        key = f"ratelimit:{client_ip}"

        current = redis_client.get(key)

        if current is None:
            redis_client.setex(key, 60, 1)  # 60 second window
        elif int(current) >= 100:
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429
            )
        else:
            redis_client.incr(key)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
```

```javascript
// Express.js with express-rate-limit
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per window
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  message: {
    error: 'Too many requests',
    retryAfter: 60
  }
});

app.use('/api/', limiter);

// Different limits for different endpoints
const loginLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 5,
  message: { error: 'Too many login attempts' }
});

app.post('/auth/login', loginLimiter, loginHandler);
```

### Step 4: Implement Sliding Window

```javascript
// Redis-based sliding window
const Redis = require('ioredis');
const redis = new Redis();

async function slidingWindowRateLimit(key, limit, windowMs) {
  const now = Date.now();
  const windowStart = now - windowMs;

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count current entries
  const count = await redis.zcard(key);

  if (count >= limit) {
    const oldestTimestamp = await redis.zrange(key, 0, 0, 'WITHSCORES');
    const retryAfter = Math.ceil((parseInt(oldestTimestamp[1]) + windowMs - now) / 1000);
    return { allowed: false, retryAfter };
  }

  // Add new entry
  await redis.zadd(key, now, `${now}-${Math.random()}`);
  await redis.expire(key, Math.ceil(windowMs / 1000));

  return { allowed: true, remaining: limit - count - 1 };
}

// Middleware
const slidingWindowMiddleware = async (req, res, next) => {
  const key = `ratelimit:${req.ip}`;
  const result = await slidingWindowRateLimit(key, 100, 60000);

  res.set('X-RateLimit-Limit', 100);
  res.set('X-RateLimit-Remaining', result.remaining || 0);

  if (!result.allowed) {
    res.set('Retry-After', result.retryAfter);
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }

  next();
};
```

### Step 5: Implement Token Bucket

```python
import time
import redis

class TokenBucket:
    def __init__(self, redis_client, capacity, refill_rate):
        self.redis = redis_client
        self.capacity = capacity  # Max tokens
        self.refill_rate = refill_rate  # Tokens per second

    def consume(self, key, tokens=1):
        now = time.time()
        bucket_key = f"tokenbucket:{key}"

        # Get current state
        data = self.redis.hmget(bucket_key, 'tokens', 'last_update')
        current_tokens = float(data[0] or self.capacity)
        last_update = float(data[1] or now)

        # Refill tokens
        elapsed = now - last_update
        current_tokens = min(
            self.capacity,
            current_tokens + elapsed * self.refill_rate
        )

        # Check if we can consume
        if current_tokens >= tokens:
            current_tokens -= tokens
            self.redis.hmset(bucket_key, {
                'tokens': current_tokens,
                'last_update': now
            })
            self.redis.expire(bucket_key, 3600)
            return True, current_tokens

        return False, current_tokens

# Usage
bucket = TokenBucket(redis_client, capacity=100, refill_rate=10)

def rate_limit_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        client_ip = get_client_ip(request)
        allowed, remaining = bucket.consume(client_ip)

        if not allowed:
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429,
                headers={'X-RateLimit-Remaining': int(remaining)}
            )

        return view_func(request, *args, **kwargs)
    return wrapper
```

### Step 6: Add Rate Limit Headers

**Standard headers:**

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 75
X-RateLimit-Reset: 1735689600
```

**When limit exceeded:**

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1735689600
Retry-After: 45

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please retry after 45 seconds.",
    "retryAfter": 45
  }
}
```

**Implementation:**

```javascript
// Express middleware with headers
const rateLimitWithHeaders = (limit, windowMs) => {
  return async (req, res, next) => {
    const key = `ratelimit:${req.ip}`;
    const result = await checkRateLimit(key, limit, windowMs);

    const resetTime = Math.floor((Date.now() + windowMs) / 1000);

    res.set({
      'X-RateLimit-Limit': limit,
      'X-RateLimit-Remaining': Math.max(0, result.remaining),
      'X-RateLimit-Reset': resetTime
    });

    if (!result.allowed) {
      const retryAfter = Math.ceil(windowMs / 1000);
      res.set('Retry-After', retryAfter);

      return res.status(429).json({
        error: {
          code: 'RATE_LIMIT_EXCEEDED',
          message: `Rate limit exceeded. Retry after ${retryAfter} seconds.`,
          retryAfter
        }
      });
    }

    next();
  };
};
```

### Step 7: Implement Per-User Limits

```python
# Django with user-based limits
from functools import wraps

def rate_limit(limit_anonymous=20, limit_authenticated=100, window=60):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                key = f"ratelimit:user:{request.user.id}"
                limit = get_user_rate_limit(request.user)  # Based on subscription
            else:
                key = f"ratelimit:ip:{get_client_ip(request)}"
                limit = limit_anonymous

            allowed, remaining = check_rate_limit(key, limit, window)

            if not allowed:
                return JsonResponse(
                    {'error': 'Rate limit exceeded'},
                    status=429
                )

            response = view_func(request, *args, **kwargs)
            response['X-RateLimit-Remaining'] = remaining
            return response

        return wrapper
    return decorator

def get_user_rate_limit(user):
    """Get rate limit based on user's subscription tier"""
    tier_limits = {
        'free': 100,
        'pro': 1000,
        'enterprise': 10000
    }
    return tier_limits.get(user.subscription_tier, 100)
```

```javascript
// Express with tiered limits
const getUserRateLimit = async (user) => {
  const tierLimits = {
    free: { limit: 100, window: 60000 },
    pro: { limit: 1000, window: 60000 },
    enterprise: { limit: 10000, window: 60000 }
  };

  if (!user) {
    return { limit: 20, window: 60000 }; // Anonymous
  }

  return tierLimits[user.tier] || tierLimits.free;
};

const tieredRateLimiter = async (req, res, next) => {
  const { limit, window } = await getUserRateLimit(req.user);
  const key = req.user ? `user:${req.user.id}` : `ip:${req.ip}`;

  const result = await checkRateLimit(key, limit, window);

  res.set('X-RateLimit-Limit', limit);
  res.set('X-RateLimit-Remaining', result.remaining);

  if (!result.allowed) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }

  next();
};
```

---

## Templates

### Rate Limit Configuration

```yaml
# rate_limits.yaml
default:
  anonymous:
    limit: 20
    window: 60  # seconds

  authenticated:
    free:
      limit: 100
      window: 60
    pro:
      limit: 1000
      window: 60
    enterprise:
      limit: 10000
      window: 60

endpoints:
  /auth/login:
    limit: 5
    window: 60
    key: ip

  /auth/register:
    limit: 3
    window: 3600  # 1 hour
    key: ip

  /api/search:
    limit: 30
    window: 60
    key: user_or_ip

  /api/upload:
    limit: 10
    window: 60
    key: user
```

### Rate Limit Response Schema

```yaml
# OpenAPI schema
components:
  responses:
    TooManyRequests:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
          description: Request limit per window
        X-RateLimit-Remaining:
          schema:
            type: integer
          description: Remaining requests in window
        X-RateLimit-Reset:
          schema:
            type: integer
          description: Unix timestamp when limit resets
        Retry-After:
          schema:
            type: integer
          description: Seconds until retry allowed
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: object
                properties:
                  code:
                    type: string
                    example: RATE_LIMIT_EXCEEDED
                  message:
                    type: string
                  retryAfter:
                    type: integer
```

---

## Examples

### Complete Rate Limiting Setup (Express + Redis)

```javascript
// rateLimit.js
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

class RateLimiter {
  constructor(options = {}) {
    this.defaultLimit = options.defaultLimit || 100;
    this.defaultWindow = options.defaultWindow || 60000;
  }

  async check(key, limit, windowMs) {
    const now = Date.now();
    const windowKey = `ratelimit:${key}:${Math.floor(now / windowMs)}`;

    const multi = redis.multi();
    multi.incr(windowKey);
    multi.pexpire(windowKey, windowMs);

    const results = await multi.exec();
    const count = results[0][1];

    return {
      allowed: count <= limit,
      remaining: Math.max(0, limit - count),
      reset: Math.ceil(now / windowMs) * windowMs
    };
  }

  middleware(options = {}) {
    return async (req, res, next) => {
      const limit = options.limit || this.getLimit(req);
      const windowMs = options.window || this.defaultWindow;
      const key = options.keyGenerator
        ? options.keyGenerator(req)
        : this.getKey(req);

      const result = await this.check(key, limit, windowMs);

      // Set headers
      res.set({
        'X-RateLimit-Limit': limit,
        'X-RateLimit-Remaining': result.remaining,
        'X-RateLimit-Reset': Math.floor(result.reset / 1000)
      });

      if (!result.allowed) {
        const retryAfter = Math.ceil((result.reset - Date.now()) / 1000);
        res.set('Retry-After', retryAfter);

        return res.status(429).json({
          error: {
            code: 'RATE_LIMIT_EXCEEDED',
            message: 'Too many requests',
            retryAfter
          }
        });
      }

      next();
    };
  }

  getKey(req) {
    if (req.user) {
      return `user:${req.user.id}`;
    }
    return `ip:${req.ip}`;
  }

  getLimit(req) {
    if (!req.user) return 20;

    const tierLimits = {
      free: 100,
      pro: 1000,
      enterprise: 10000
    };

    return tierLimits[req.user.tier] || this.defaultLimit;
  }
}

module.exports = new RateLimiter();

// app.js
const rateLimiter = require('./rateLimit');

// Global rate limit
app.use('/api', rateLimiter.middleware());

// Endpoint-specific limits
app.post('/auth/login', rateLimiter.middleware({
  limit: 5,
  window: 60000,
  keyGenerator: (req) => `login:${req.ip}`
}), loginHandler);

app.post('/api/upload', rateLimiter.middleware({
  limit: 10,
  window: 60000
}), uploadHandler);
```

### Django with Tiered Limits

```python
# rate_limit.py
import time
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse

class RateLimiter:
    TIER_LIMITS = {
        'anonymous': 20,
        'free': 100,
        'pro': 1000,
        'enterprise': 10000
    }

    def __init__(self, limit=None, window=60, key_func=None):
        self.limit = limit
        self.window = window
        self.key_func = key_func or self.default_key_func

    def default_key_func(self, request):
        if request.user.is_authenticated:
            return f"user:{request.user.id}"
        return f"ip:{self.get_client_ip(request)}"

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def get_limit(self, request):
        if self.limit:
            return self.limit

        if not request.user.is_authenticated:
            return self.TIER_LIMITS['anonymous']

        tier = getattr(request.user, 'subscription_tier', 'free')
        return self.TIER_LIMITS.get(tier, self.TIER_LIMITS['free'])

    def check(self, key, limit):
        cache_key = f"ratelimit:{key}"
        current = cache.get(cache_key, 0)

        if current >= limit:
            return False, 0

        cache.set(cache_key, current + 1, self.window)
        return True, limit - current - 1

    def __call__(self, view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            key = self.key_func(request)
            limit = self.get_limit(request)
            allowed, remaining = self.check(key, limit)

            if not allowed:
                response = JsonResponse({
                    'error': {
                        'code': 'RATE_LIMIT_EXCEEDED',
                        'message': 'Too many requests',
                        'retryAfter': self.window
                    }
                }, status=429)
                response['Retry-After'] = self.window
            else:
                response = view_func(request, *args, **kwargs)

            response['X-RateLimit-Limit'] = limit
            response['X-RateLimit-Remaining'] = remaining
            return response

        return wrapper

# Usage
rate_limit = RateLimiter

@rate_limit(limit=5, window=60)
def login_view(request):
    # Login logic
    pass

@rate_limit()  # Uses tier-based limits
def api_view(request):
    # API logic
    pass
```

---

## Common Mistakes

1. **Not using distributed storage**
   - In-memory limits don't work with multiple servers
   - Use Redis or similar

2. **Limiting by IP only**
   - Shared IPs (offices, VPNs) affect many users
   - Use user ID when authenticated

3. **No headers or response info**
   - Clients don't know their limits
   - Always include X-RateLimit headers

4. **Same limits for all endpoints**
   - Login needs stricter limits
   - Expensive operations need lower limits

5. **Not handling bursts**
   - Fixed windows allow burst at window boundary
   - Use sliding window or token bucket

---

## Next Steps

1. **Start simple** - Fixed window with Redis
2. **Add headers** - Help clients manage requests
3. **Tier by user** - Different limits for different plans
4. **Monitor abuse** - Alert on repeated 429s
5. **Document limits** - Include in API docs

---

## Related Methodologies

- [M-API-005: API Authentication](./M-API-005_api_authentication.md)
- [M-API-007: Error Handling](./M-API-007_error_handling.md)
- [M-API-010: API Monitoring](./M-API-010_api_monitoring.md)

---

*Methodology: Rate Limiting*
*Version: 1.0*
*Agent: faion-api-agent*
