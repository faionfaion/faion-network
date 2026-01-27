# Python Web Frameworks

**Comprehensive guide to Django, FastAPI, and Flask for modern web development (2025-2026).**

---

## Overview

Django, FastAPI, and Flask are Python's dominant web frameworks, each serving distinct needs:

| Framework | Philosophy | Best For | GitHub Stars (2025) |
|-----------|------------|----------|---------------------|
| **Django** | Batteries-included | Full-stack apps, admin panels, rapid development | 80K+ |
| **FastAPI** | Modern, async-first | High-performance APIs, microservices, ML serving | 78K+ |
| **Flask** | Minimalist micro-framework | Flexibility, small apps, prototypes | 68K+ |

---

## Framework Comparison Matrix

### Core Characteristics

| Feature | Django | FastAPI | Flask |
|---------|--------|---------|-------|
| **Type** | Full-stack | API framework | Micro-framework |
| **Architecture** | MTV (Model-Template-View) | Dependency Injection | Minimal core + extensions |
| **Async Support** | Partial (ASGI) | Native (built-in) | Limited (WSGI) |
| **ORM** | Built-in (Django ORM) | None (use SQLAlchemy) | None (use SQLAlchemy) |
| **Admin Panel** | Built-in | External (SQLAdmin) | External (Flask-Admin) |
| **API Docs** | Manual / DRF | Auto-generated (OpenAPI) | Manual / Flasgger |
| **Learning Curve** | Moderate | Moderate-Steep | Easy |
| **Maturity** | 20 years (2005) | 6 years (2018) | 15 years (2010) |

### Performance Benchmarks (2025)

| Metric | Django | FastAPI | Flask |
|--------|--------|---------|-------|
| **Requests/sec** | ~1,500 RPS | ~3,000+ RPS | ~1,800 RPS |
| **Response Time** | ~50-100ms | <50ms | ~40-80ms |
| **Concurrent Connections** | Limited by threads | High (async) | Limited by threads |
| **Memory Usage** | Higher | Lower | Lowest |

> **Note:** FastAPI consistently outperforms Django and Flask in high-concurrency scenarios due to native async support.

### Feature Comparison

| Feature | Django | FastAPI | Flask |
|---------|--------|---------|-------|
| Authentication | Built-in | External (e.g., Authlib) | Flask-Login |
| Database Migrations | Built-in | Alembic | Flask-Migrate |
| Form Handling | Built-in | Pydantic | Flask-WTF |
| Caching | Built-in | External | Flask-Caching |
| Testing | Built-in | pytest | pytest |
| WebSockets | Django Channels | Native | Flask-SocketIO |
| Background Tasks | Celery | Built-in + Celery | Celery |
| Template Engine | Django Templates | Jinja2 | Jinja2 |
| Security (CSRF, XSS) | Built-in | Manual | Manual / Extensions |

---

## When to Use Each Framework

### Django

**Choose Django when:**

- Building full-stack web applications with user interfaces
- Need built-in admin panel for content management
- Rapid development with "batteries-included" approach
- Enterprise applications requiring stability and security
- Teams with varying experience levels
- Projects requiring ORM with migrations
- CMS, e-commerce, social platforms

**Real-world users:** Instagram, Spotify, Dropbox, Pinterest, Mozilla

**Strengths:**
- Comprehensive built-in features
- Excellent documentation
- Large ecosystem and community
- Battle-tested security
- Django Admin saves weeks of development

**Limitations:**
- Monolithic architecture can be challenging to scale
- Not optimized for async workloads
- Heavier memory footprint
- Can be overkill for simple APIs

---

### FastAPI

**Choose FastAPI when:**

- Building high-performance REST APIs
- Async/await is critical for your use case
- Serving ML models or AI applications
- Microservices architecture
- Real-time applications with WebSockets
- API-first development with auto-documentation
- Type safety and validation are priorities

**Real-world users:** Netflix, Uber, Microsoft, Expedia

**Strengths:**
- Exceptional performance (async-native)
- Automatic OpenAPI documentation
- Type hints with Pydantic validation
- Modern Python features (3.8+)
- Easy dependency injection
- Excellent for AI/ML model serving

**Limitations:**
- Smaller ecosystem than Django/Flask
- No built-in admin panel
- Requires separate ORM setup
- Steeper learning curve for async patterns

---

### Flask

**Choose Flask when:**

- Building small to medium applications
- Maximum flexibility and control needed
- Learning web development
- Rapid prototyping
- Simple APIs without complex requirements
- Custom architecture requirements
- Internal tools and utilities

**Real-world users:** Netflix, Airbnb, Reddit, Lyft

**Strengths:**
- Minimal and lightweight
- Easy to learn and use
- Maximum flexibility
- Large extension ecosystem
- Perfect for prototypes
- Stable API (minimal breaking changes)

**Limitations:**
- No built-in features (DIY everything)
- Security must be implemented manually
- Can become messy without structure
- Limited async support

---

## Modern Trend: Hybrid Architecture (2025-2026)

Many teams adopt a **FastAPI + Django** combination:

```
                    +------------------+
                    |   Load Balancer  |
                    +--------+---------+
                             |
            +----------------+----------------+
            |                                 |
    +-------v-------+               +---------v---------+
    |    FastAPI    |               |      Django       |
    | (Public APIs) |               |   (Admin/CMS)     |
    +-------+-------+               +---------+---------+
            |                                 |
            +----------------+----------------+
                             |
                    +--------v--------+
                    |    Database     |
                    +-----------------+
```

**Why this works:**
- FastAPI handles high-throughput public APIs
- Django provides admin panel and content management
- Shared database with clear boundaries
- Best of both worlds

---

## Async Support Deep Dive

### Django Async (2025)

Django 5.2 provides mature async support:

```python
# Async view
async def my_view(request):
    data = await sync_to_async(MyModel.objects.get)(pk=1)
    return JsonResponse({"data": data.name})

# Async ORM methods (Django 4.1+)
async def get_users():
    users = await User.objects.filter(active=True).aall()
    return users

# For WebSockets: use Django Channels
```

**Considerations:**
- ORM calls need `sync_to_async` wrapper or `a`-prefixed methods
- Requires ASGI server (Daphne, Uvicorn)
- Mixed sync/async has ~1ms performance penalty
- WebSockets require Django Channels

### FastAPI Async (Native)

```python
# Native async - no wrappers needed
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# WebSockets - built-in
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

### Flask Async

Flask 2.0+ supports async views but remains WSGI-focused:

```python
@app.route("/data")
async def get_data():
    data = await some_async_operation()
    return jsonify(data)
```

**Limitations:**
- WSGI by default (not truly async)
- Requires ASGI adapter for full async
- No native WebSocket support

---

## WebSocket Support Comparison

| Framework | WebSocket Support | Library | Complexity |
|-----------|-------------------|---------|------------|
| **Django** | External | Django Channels | High |
| **FastAPI** | Native | Built-in | Low |
| **Flask** | External | Flask-SocketIO | Medium |

### Production WebSocket Considerations

1. **Connection Management:** Use Redis Pub/Sub for multi-instance deployments
2. **Scaling:** Shard connections by logical groups (rooms, channels)
3. **Health Checks:** Implement ping/pong for stale connection cleanup
4. **Backpressure:** Queue or drop messages for slow clients

---

## Testing Approaches

### Django Testing

```bash
# Built-in test runner
python manage.py test

# With pytest-django
pytest apps/users/tests/
```

**Features:**
- Test client for views
- Database fixtures
- Transaction rollback per test
- Factory Boy integration

### FastAPI Testing

```python
# test_main.py
from fastapi.testclient import TestClient
from httpx import AsyncClient  # For async tests

def test_read_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

# Async tests
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users")
        assert response.status_code == 200
```

### Flask Testing

```python
# test_app.py
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
```

---

## Database Integration

| Framework | Default ORM | Async ORM Options |
|-----------|-------------|-------------------|
| **Django** | Django ORM | `sync_to_async`, async methods |
| **FastAPI** | SQLAlchemy | SQLAlchemy 2.0 async, Tortoise ORM |
| **Flask** | SQLAlchemy | SQLAlchemy 2.0 async |

### Recommended Patterns

**Django:** Use built-in ORM with service layer
**FastAPI:** SQLAlchemy 2.0 with async session
**Flask:** SQLAlchemy with repository pattern

---

## Deployment Recommendations

### Django

```bash
# Production with Gunicorn + Uvicorn workers
gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w 4
```

### FastAPI

```bash
# Production with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Flask

```bash
# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## Quick Decision Matrix

| Requirement | Recommendation |
|-------------|----------------|
| Full-stack web app | Django |
| High-performance API | FastAPI |
| Quick prototype | Flask |
| Admin panel needed | Django |
| ML model serving | FastAPI |
| Maximum flexibility | Flask |
| WebSocket-heavy | FastAPI |
| Enterprise/stability | Django |
| Learning Python web | Flask |
| Microservices | FastAPI |
| Content management | Django |
| Internal tool | Flask |

---

## LLM Usage Tips

When asking LLMs to help with Python web frameworks:

1. **Specify framework and version:** "Django 5.1" not just "Django"
2. **Mention async requirements:** Async patterns differ significantly
3. **Include context:** API vs full-stack, scale requirements
4. **Request modern patterns:** Ask for 2025 best practices explicitly
5. **Specify testing needs:** Unit, integration, or E2E tests

See [llm-prompts.md](llm-prompts.md) for ready-to-use prompts.

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Framework selection checklist |
| [examples.md](examples.md) | Real-world usage examples |
| [templates.md](templates.md) | Project structure templates |
| [llm-prompts.md](llm-prompts.md) | Effective LLM prompts |

---

## External Resources

### Official Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Framework-Specific

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)

### Comparisons & Analysis

- [JetBrains: Django vs Flask vs FastAPI](https://blog.jetbrains.com/pycharm/2025/02/django-flask-fastapi/)
- [Better Stack: Django vs FastAPI](https://betterstack.com/community/guides/scaling-python/django-vs-fastapi/)
- [PropelAuth: Framework Comparison 2025](https://www.propelauth.com/post/fastapi-vs-flask-vs-django-in-2025)

### Performance & Scaling

- [FastAPI WebSocket Scaling](https://hexshift.medium.com/top-ten-advanced-techniques-for-scaling-websocket-applications-with-fastapi-a5af1e5e901f)
- [Django Async Architecture Guide](https://medium.com/@yogeshkrishnanseeniraj/the-ultimate-async-django-architecture-guide-2025-2026-edition-4333ab4c8a90)

---

*Python Web Frameworks v2.0*
*Django | FastAPI | Flask*
*Last updated: 2025-01*
