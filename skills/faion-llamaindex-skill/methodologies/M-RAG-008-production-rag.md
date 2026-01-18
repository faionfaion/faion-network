# M-RAG-008: Production RAG

## Overview

Production RAG requires more than good retrieval - it needs caching, monitoring, error handling, and graceful degradation. This methodology covers scaling RAG systems, optimizing latency and cost, and maintaining reliability under load.

**When to use:** Deploying RAG to production, handling high traffic, or when reliability and performance matter.

## Core Concepts

### 1. Production Requirements

| Requirement | Development | Production |
|-------------|-------------|------------|
| **Latency** | Seconds OK | < 2s P99 |
| **Availability** | Best effort | 99.9%+ |
| **Error Handling** | Crash OK | Graceful degradation |
| **Monitoring** | Logs | Metrics, alerts, traces |
| **Caching** | None | Multi-layer |
| **Cost** | Ignored | Optimized |

### 2. Production Architecture

```
                    ┌─────────────────────────────────────┐
                    │           Load Balancer             │
                    └─────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
              ┌─────────┐      ┌─────────┐      ┌─────────┐
              │ RAG API │      │ RAG API │      │ RAG API │
              └─────────┘      └─────────┘      └─────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
     ┌────▼────┐              ┌──────▼──────┐            ┌──────▼──────┐
     │  Cache  │              │ Vector DB   │            │  LLM API    │
     │ (Redis) │              │ (Primary)   │            │ (Gateway)   │
     └─────────┘              └─────────────┘            └─────────────┘
                                     │
                              ┌──────▼──────┐
                              │ Vector DB   │
                              │ (Replica)   │
                              └─────────────┘
```

### 3. Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| P50 latency | < 500ms | > 750ms |
| P99 latency | < 2000ms | > 3000ms |
| Error rate | < 0.1% | > 0.5% |
| Cache hit rate | > 70% | < 50% |
| Retrieval quality | > 0.8 MRR | < 0.7 MRR |
| Answer quality | > 4/5 | < 3.5/5 |

## Best Practices

### 1. Implement Multi-Layer Caching

```python
from functools import lru_cache
import redis
import hashlib

class RAGCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.local_cache = {}
        self.local_cache_size = 1000

    def _cache_key(self, query: str, filters: dict = None) -> str:
        """Generate cache key from query and filters."""
        content = query + json.dumps(filters or {}, sort_keys=True)
        return f"rag:{hashlib.sha256(content.encode()).hexdigest()[:16]}"

    def get(self, query: str, filters: dict = None) -> dict | None:
        """Multi-layer cache lookup."""
        key = self._cache_key(query, filters)

        # L1: Local in-memory cache
        if key in self.local_cache:
            return self.local_cache[key]

        # L2: Redis cache
        cached = self.redis.get(key)
        if cached:
            result = json.loads(cached)
            # Promote to L1
            self._add_to_local(key, result)
            return result

        return None

    def set(self, query: str, result: dict, filters: dict = None, ttl: int = 3600):
        """Cache result at all layers."""
        key = self._cache_key(query, filters)

        # L1: Local cache
        self._add_to_local(key, result)

        # L2: Redis cache
        self.redis.setex(key, ttl, json.dumps(result))

    def _add_to_local(self, key: str, value: dict):
        """Add to local cache with LRU eviction."""
        if len(self.local_cache) >= self.local_cache_size:
            # Simple LRU: remove oldest
            oldest = next(iter(self.local_cache))
            del self.local_cache[oldest]
        self.local_cache[key] = value
```

### 2. Add Comprehensive Monitoring

```python
from prometheus_client import Counter, Histogram, Gauge
import structlog

# Metrics
rag_requests = Counter('rag_requests_total', 'Total RAG requests', ['status'])
rag_latency = Histogram('rag_latency_seconds', 'RAG latency', ['stage'])
cache_hits = Counter('rag_cache_hits_total', 'Cache hits', ['layer'])
retrieval_quality = Gauge('rag_retrieval_quality', 'Retrieval quality score')

logger = structlog.get_logger()

class MonitoredRAG:
    def __init__(self, rag_system):
        self.rag = rag_system

    async def query(self, query: str, user_id: str = None) -> dict:
        """Query with full monitoring."""
        request_id = generate_request_id()

        try:
            with rag_latency.labels(stage='total').time():
                # Check cache
                with rag_latency.labels(stage='cache').time():
                    cached = self.cache.get(query)
                    if cached:
                        cache_hits.labels(layer='redis').inc()
                        return self._wrap_response(cached, request_id, cached=True)

                # Retrieve
                with rag_latency.labels(stage='retrieval').time():
                    docs = await self.rag.retrieve(query)

                # Generate
                with rag_latency.labels(stage='generation').time():
                    answer = await self.rag.generate(query, docs)

                result = {"answer": answer, "sources": docs}
                self.cache.set(query, result)

                rag_requests.labels(status='success').inc()
                return self._wrap_response(result, request_id)

        except Exception as e:
            rag_requests.labels(status='error').inc()
            logger.error("rag_error", request_id=request_id, error=str(e))
            raise

    def _wrap_response(self, result: dict, request_id: str, cached: bool = False) -> dict:
        return {
            **result,
            "request_id": request_id,
            "cached": cached,
            "timestamp": datetime.utcnow().isoformat()
        }
```

### 3. Implement Graceful Degradation

```python
class ResilientRAG:
    def __init__(self, primary_rag, fallback_rag=None):
        self.primary = primary_rag
        self.fallback = fallback_rag
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60
        )

    async def query(self, query: str) -> dict:
        """Query with fallback and circuit breaker."""

        # Try primary
        if self.circuit_breaker.is_closed:
            try:
                result = await asyncio.wait_for(
                    self.primary.query(query),
                    timeout=10.0
                )
                self.circuit_breaker.record_success()
                return result
            except Exception as e:
                self.circuit_breaker.record_failure()
                logger.warning("primary_failed", error=str(e))

        # Primary failed or circuit open - use fallback
        if self.fallback:
            try:
                result = await self.fallback.query(query)
                result["fallback"] = True
                return result
            except Exception as e:
                logger.error("fallback_failed", error=str(e))

        # All failed - return graceful error
        return {
            "answer": "I'm unable to answer right now. Please try again shortly.",
            "error": True,
            "retry_after": 30
        }

class CircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: int):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"

    @property
    def is_closed(self) -> bool:
        if self.state == "closed":
            return True

        # Check if recovery timeout has passed
        if time.time() - self.last_failure_time > self.recovery_timeout:
            self.state = "half-open"
            return True

        return False

    def record_success(self):
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"
```

## Common Patterns

### Pattern 1: Streaming Responses

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/query/stream")
async def stream_query(request: QueryRequest):
    """Stream RAG response for better UX."""

    async def generate():
        # First, stream retrieved sources quickly
        docs = await rag.retrieve(request.query)

        yield json.dumps({"type": "sources", "data": [d.metadata for d in docs]}) + "\n"

        # Then stream the answer
        async for chunk in rag.generate_stream(request.query, docs):
            yield json.dumps({"type": "answer_chunk", "data": chunk}) + "\n"

        # Finally, metadata
        yield json.dumps({"type": "done", "data": {"latency_ms": get_latency()}}) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )
```

### Pattern 2: Request Coalescing

```python
import asyncio
from collections import defaultdict

class RequestCoalescer:
    """Combine identical concurrent requests."""

    def __init__(self, rag_system):
        self.rag = rag_system
        self.pending: dict[str, asyncio.Future] = {}
        self.lock = asyncio.Lock()

    async def query(self, query: str) -> dict:
        """Query with request coalescing."""
        query_key = hashlib.sha256(query.encode()).hexdigest()[:16]

        async with self.lock:
            if query_key in self.pending:
                # Wait for existing request
                return await self.pending[query_key]

            # Create new request
            future = asyncio.Future()
            self.pending[query_key] = future

        try:
            # Execute query
            result = await self.rag.query(query)
            future.set_result(result)
            return result
        except Exception as e:
            future.set_exception(e)
            raise
        finally:
            async with self.lock:
                del self.pending[query_key]
```

### Pattern 3: LLM Gateway with Fallback

```python
class LLMGateway:
    """Route to multiple LLM providers with fallback."""

    def __init__(self):
        self.providers = {
            "openai": OpenAIClient(),
            "anthropic": AnthropicClient(),
            "azure": AzureOpenAIClient()
        }
        self.primary = "openai"
        self.fallback_order = ["anthropic", "azure"]

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate with automatic fallback."""

        # Try primary
        try:
            return await self._call_provider(self.primary, prompt, **kwargs)
        except Exception as e:
            logger.warning(f"primary_llm_failed", provider=self.primary, error=str(e))

        # Try fallbacks
        for provider in self.fallback_order:
            try:
                result = await self._call_provider(provider, prompt, **kwargs)
                logger.info("fallback_succeeded", provider=provider)
                return result
            except Exception as e:
                logger.warning(f"fallback_failed", provider=provider, error=str(e))

        raise Exception("All LLM providers failed")

    async def _call_provider(self, provider: str, prompt: str, **kwargs) -> str:
        return await asyncio.wait_for(
            self.providers[provider].generate(prompt, **kwargs),
            timeout=30.0
        )
```

### Pattern 4: Index Update Pipeline

```python
class IndexUpdatePipeline:
    """Handle document updates without downtime."""

    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.update_queue = asyncio.Queue()
        self.batch_size = 100
        self.batch_timeout = 10  # seconds

    async def start(self):
        """Start background update processor."""
        asyncio.create_task(self._process_updates())

    async def schedule_update(self, doc: dict):
        """Schedule document for indexing."""
        await self.update_queue.put(doc)

    async def _process_updates(self):
        """Process updates in batches."""
        while True:
            batch = []
            deadline = time.time() + self.batch_timeout

            while len(batch) < self.batch_size and time.time() < deadline:
                try:
                    doc = await asyncio.wait_for(
                        self.update_queue.get(),
                        timeout=max(0, deadline - time.time())
                    )
                    batch.append(doc)
                except asyncio.TimeoutError:
                    break

            if batch:
                await self._index_batch(batch)

    async def _index_batch(self, docs: list):
        """Index batch of documents."""
        try:
            # Generate embeddings in parallel
            texts = [d["content"] for d in docs]
            embeddings = await batch_embed_async(texts)

            # Upsert to vector store
            points = [
                {"id": d["id"], "vector": e, "payload": d["metadata"]}
                for d, e in zip(docs, embeddings)
            ]

            await self.vector_store.upsert_batch(points)
            logger.info("batch_indexed", count=len(docs))

        except Exception as e:
            logger.error("batch_index_failed", error=str(e))
            # Re-queue failed docs
            for doc in docs:
                await self.update_queue.put(doc)
```

### Pattern 5: Quality Feedback Loop

```python
class FeedbackCollector:
    """Collect and act on user feedback."""

    def __init__(self, db, alerter):
        self.db = db
        self.alerter = alerter

    async def record_feedback(self, request_id: str, rating: int, comment: str = None):
        """Record user feedback."""
        await self.db.insert("feedback", {
            "request_id": request_id,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.utcnow()
        })

        # Check for quality degradation
        await self._check_quality_alerts()

    async def _check_quality_alerts(self):
        """Alert if quality drops."""
        # Get last hour's ratings
        recent = await self.db.query("""
            SELECT AVG(rating) as avg_rating, COUNT(*) as count
            FROM feedback
            WHERE timestamp > NOW() - INTERVAL '1 hour'
        """)

        if recent.count > 10 and recent.avg_rating < 3.5:
            await self.alerter.send(
                "RAG quality degradation",
                f"Average rating: {recent.avg_rating:.2f} (n={recent.count})"
            )

    async def get_improvement_candidates(self, limit: int = 20) -> list:
        """Find queries that need improvement."""
        return await self.db.query("""
            SELECT query, answer, rating, comment
            FROM feedback
            JOIN requests ON feedback.request_id = requests.id
            WHERE rating <= 2
            ORDER BY timestamp DESC
            LIMIT $1
        """, limit)
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No caching | High latency, cost | Multi-layer caching |
| Single LLM provider | SPOF | Provider fallback |
| Sync updates | Blocks requests | Async update pipeline |
| No circuit breaker | Cascading failures | Implement circuit breaker |
| Ignoring feedback | Quality degrades | Feedback collection |
| No rate limiting | Abuse, cost overrun | Rate limits per user |

## Deployment Checklist

### Before Launch
- [ ] Load tested at 2x expected traffic
- [ ] Fallback providers configured
- [ ] Caching implemented and tested
- [ ] Monitoring dashboards ready
- [ ] Alerts configured
- [ ] Circuit breakers tuned
- [ ] Rate limits set
- [ ] Error handling tested
- [ ] Rollback plan documented

### Post-Launch
- [ ] Monitor latency P50/P99
- [ ] Track error rates
- [ ] Collect user feedback
- [ ] Review cache hit rates
- [ ] Check cost per query
- [ ] Weekly quality reviews
- [ ] Regular index updates
- [ ] Capacity planning

## Tools & References

### Related Skills
- faion-vector-db-skill
- faion-langchain-skill

### Related Agents
- faion-rag-agent
- faion-devops-agent

### External Resources
- [LangSmith](https://www.langchain.com/langsmith) - LLM observability
- [Prometheus](https://prometheus.io/) - Metrics
- [Redis](https://redis.io/) - Caching
- [Litellm](https://github.com/BerriAI/litellm) - LLM gateway

## Checklist

- [ ] Implemented multi-layer caching
- [ ] Added comprehensive monitoring
- [ ] Set up graceful degradation
- [ ] Configured LLM fallback
- [ ] Implemented streaming responses
- [ ] Added request coalescing
- [ ] Set up async index updates
- [ ] Created feedback collection
- [ ] Configured alerts
- [ ] Load tested system

---

*Methodology: M-RAG-008 | Category: RAG/Vector DB*
*Related: faion-rag-agent, faion-devops-agent*
