---
id: perf-test-basics
name: "Performance Testing Basics"
domain: DEV
skill: faion-software-developer
category: "development"
parent: "performance-testing"
---

# Performance Testing Basics

## Overview

Performance testing validates that applications meet speed, scalability, and stability requirements under various load conditions. It includes load testing, stress testing, endurance testing, and profiling to identify bottlenecks and ensure acceptable user experience.

## When to Use

- Before major releases or launches
- After significant code changes affecting performance
- When scaling infrastructure
- Setting performance baselines
- Identifying bottlenecks in critical paths

## Key Principles

- **Test realistic scenarios**: Mirror production usage patterns
- **Establish baselines**: Know normal performance before testing
- **Test in production-like environment**: Similar hardware, data, network
- **Monitor everything**: CPU, memory, I/O, network, application metrics
- **Iterative optimization**: Test, identify, fix, repeat

## Performance Testing Types

```
┌─────────────────────────────────────────────────────────────┐
│                 PERFORMANCE TEST TYPES                      │
├─────────────────────────────────────────────────────────────┤
│ LOAD TEST                                                   │
│   Purpose: Verify system under expected load                │
│   Duration: Extended period (hours)                         │
│   Users: Normal to peak expected users                      │
├─────────────────────────────────────────────────────────────┤
│ STRESS TEST                                                 │
│   Purpose: Find breaking point                              │
│   Duration: Until failure                                   │
│   Users: Beyond maximum capacity                            │
├─────────────────────────────────────────────────────────────┤
│ SPIKE TEST                                                  │
│   Purpose: Test sudden load increases                       │
│   Duration: Short bursts                                    │
│   Users: Sudden jump from low to high                       │
├─────────────────────────────────────────────────────────────┤
│ ENDURANCE TEST (Soak)                                       │
│   Purpose: Find memory leaks, resource exhaustion           │
│   Duration: Very long (12-72 hours)                         │
│   Users: Normal load sustained                              │
├─────────────────────────────────────────────────────────────┤
│ SCALABILITY TEST                                            │
│   Purpose: Verify horizontal/vertical scaling               │
│   Duration: Varied                                          │
│   Users: Incrementally increasing                           │
└─────────────────────────────────────────────────────────────┘
```

## Application Profiling

### cProfile for Function-Level Profiling

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func):
    """Decorator to profile a function."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions
        print(stream.getvalue())

        return result
    return wrapper

@profile_function
def expensive_operation():
    # Your code here
    pass
```

### Memory Profiling

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function with memory profiling."""
    large_list = [i ** 2 for i in range(1000000)]
    return sum(large_list)

# Line-by-line profiling with line_profiler
# Add @profile decorator and run: kernprof -l -v script.py

# Async profiling with py-spy
# Run: py-spy top --pid <PID>
# Or: py-spy record -o profile.svg --pid <PID>
```

## pytest-benchmark for Micro-benchmarks

```python
import pytest
from decimal import Decimal

def test_price_calculation_performance(benchmark):
    """Benchmark price calculation function."""
    items = [
        {"price": Decimal("10.00"), "quantity": 2},
        {"price": Decimal("25.50"), "quantity": 1},
        {"price": Decimal("5.00"), "quantity": 10},
    ] * 100  # 300 items

    def calculate():
        return sum(item["price"] * item["quantity"] for item in items)

    result = benchmark(calculate)
    assert result == Decimal("7050.00")

def test_json_serialization_performance(benchmark):
    """Compare JSON serialization methods."""
    import json
    import orjson

    data = {"users": [{"id": i, "name": f"User {i}"} for i in range(1000)]}

    def serialize_stdlib():
        return json.dumps(data)

    def serialize_orjson():
        return orjson.dumps(data)

    # Run benchmark
    result = benchmark.pedantic(
        serialize_orjson,
        iterations=100,
        rounds=10
    )

@pytest.mark.benchmark(group="database")
def test_bulk_insert_performance(benchmark, db_session):
    """Benchmark bulk insert vs individual inserts."""
    users = [User(name=f"User {i}", email=f"user{i}@example.com")
             for i in range(1000)]

    def bulk_insert():
        db_session.bulk_save_objects(users)
        db_session.commit()
        db_session.rollback()

    benchmark(bulk_insert)

# Run with: pytest --benchmark-only
# Compare: pytest --benchmark-compare
```

## Database Query Performance

```python
import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

# Query timing middleware
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 0.1:  # Log slow queries > 100ms
        print(f"SLOW QUERY ({total:.3f}s): {statement[:100]}...")

# Test query performance
def test_query_performance(db_session, benchmark):
    """Ensure critical queries meet performance requirements."""
    # Seed test data
    for i in range(10000):
        db_session.add(User(name=f"User {i}", email=f"user{i}@example.com"))
    db_session.commit()

    def query_users():
        return db_session.query(User).filter(
            User.name.like("User 5%")
        ).limit(100).all()

    result = benchmark(query_users)

    # Assert query time is acceptable
    assert benchmark.stats.stats.mean < 0.1  # < 100ms average

# N+1 query detection
def test_no_n_plus_one_queries(db_session, caplog):
    """Detect N+1 query problems."""
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    orders = db_session.query(Order).limit(10).all()

    query_count = 0
    for record in caplog.records:
        if 'SELECT' in record.message:
            query_count += 1

    # Should be 1-2 queries, not 11+ (N+1)
    assert query_count < 5, f"Potential N+1: {query_count} queries for 10 orders"
```

## Performance Monitoring Script

```python
# scripts/check_performance.py
import json
import sys

def check_results(results_file: str) -> bool:
    with open(results_file) as f:
        results = json.load(f)

    thresholds = {
        'http_req_duration_p95': 500,    # 95th percentile < 500ms
        'http_req_failed_rate': 0.01,    # Error rate < 1%
        'http_reqs_rate': 100,           # At least 100 req/s throughput
    }

    passed = True
    for metric, threshold in thresholds.items():
        actual = results.get('metrics', {}).get(metric, {}).get('value', 0)

        if 'rate' in metric or 'failed' in metric:
            check = actual <= threshold
        else:
            check = actual >= threshold if 'rate' in metric else actual <= threshold

        status = "PASS" if check else "FAIL"
        print(f"{metric}: {actual:.2f} (threshold: {threshold}) - {status}")

        if not check:
            passed = False

    return passed

if __name__ == "__main__":
    if not check_results(sys.argv[1]):
        sys.exit(1)
```

## Anti-patterns

- **Testing in unrealistic environments**: Using weak hardware or empty databases
- **Ignoring warm-up time**: Not accounting for JIT compilation, caching
- **Testing single endpoints**: Missing integration performance issues
- **No baseline**: Can't detect regressions without comparison
- **Premature optimization**: Optimizing before measuring
- **Ignoring client-side**: Only testing backend performance

## References

- [Locust Documentation](https://docs.locust.io/)
- [k6 Documentation](https://k6.io/docs/)
- [pytest-benchmark](https://pytest-benchmark.readthedocs.io/)
- [Google Web Vitals](https://web.dev/vitals/)
- [Performance Testing Guidance](https://www.perfmatrix.com/)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement perf-test-basics pattern | haiku | Straightforward implementation |
| Review perf-test-basics implementation | sonnet | Requires code analysis |
| Optimize perf-test-basics design | opus | Complex trade-offs |

