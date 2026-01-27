# LLM Prompts for Performance Architecture

Effective prompts for using LLMs to assist with performance analysis, optimization, and architecture decisions.

---

## Performance Analysis Prompts

### Analyze Slow Query

```
I have a slow PostgreSQL query that takes [X seconds]. Help me optimize it.

**Query:**
```sql
[paste query here]
```

**Table schemas:**
```sql
[paste relevant CREATE TABLE statements]
```

**Current indexes:**
```sql
[paste current indexes]
```

**EXPLAIN ANALYZE output:**
```
[paste explain analyze output]
```

**Context:**
- Database: PostgreSQL [version]
- Table sizes: [table name: row count]
- Expected query frequency: [per second/minute/hour]

Please analyze:
1. What is causing the slow performance?
2. What indexes should I add?
3. Can the query be rewritten more efficiently?
4. Are there any schema changes that would help?
```

### Review Caching Strategy

```
Review my caching strategy and suggest improvements.

**Current architecture:**
- Application: [framework/language]
- Cache: [Redis/Memcached/other]
- Database: [type]

**Current caching implementation:**
```[language]
[paste caching code]
```

**Traffic patterns:**
- Read/write ratio: [e.g., 90/10]
- Peak requests per second: [number]
- Data freshness requirements: [seconds/minutes]

**Known issues:**
- [list any cache-related problems]

Please analyze:
1. Is the caching pattern appropriate for my use case?
2. Are TTLs set correctly?
3. How can I prevent cache stampedes?
4. What cache invalidation strategy would work best?
5. Should I add additional caching layers?
```

### Diagnose Latency Issue

```
Help me diagnose a latency issue in my [service/API].

**Symptoms:**
- p50 latency: [value]
- p95 latency: [value]
- p99 latency: [value]
- Target SLO: [value]

**Architecture:**
```
[describe or diagram the architecture]
```

**Recent changes:**
- [list recent deployments or changes]

**Observations:**
- CPU utilization: [%]
- Memory utilization: [%]
- Database connection pool usage: [%]
- Cache hit rate: [%]

**Distributed trace sample:**
```
[paste trace or timing breakdown]
```

What are the likely causes and how should I investigate further?
```

---

## Architecture Design Prompts

### Design Scalable System

```
Help me design a performance-optimized architecture for:

**System requirements:**
- Type: [e-commerce/SaaS/API/etc.]
- Expected users: [number] DAU
- Peak concurrent users: [number]
- Data volume: [size] per [time period]

**Performance requirements:**
- Response time p95: < [X]ms
- Throughput: [X] RPS
- Availability: [X]%

**Constraints:**
- Budget: [cloud spend/month]
- Team size: [number]
- Existing stack: [technologies]

Please provide:
1. High-level architecture diagram (describe in text)
2. Technology recommendations for each component
3. Caching strategy
4. Database selection and scaling approach
5. Load balancing strategy
6. Potential bottlenecks and mitigation strategies
```

### Design Caching Layer

```
Design a multi-layer caching architecture for my application.

**Application type:** [description]

**Data characteristics:**
- Hot data size: [approximate size]
- Read/write ratio: [e.g., 95/5]
- Data freshness requirement: [seconds/minutes]
- Geographic distribution: [regions]

**Current stack:**
- Backend: [language/framework]
- Database: [type]
- Existing cache: [if any]

**Specific requirements:**
- [list any specific requirements]

Please design:
1. Cache hierarchy (what to cache at each layer)
2. Cache eviction policies
3. Cache invalidation strategy
4. Handling cache stampedes
5. Cache warming approach
6. Monitoring metrics to track
```

### Design Auto-scaling Strategy

```
Help me design an auto-scaling strategy for my Kubernetes deployment.

**Workload characteristics:**
- Traffic pattern: [steady/bursty/scheduled peaks]
- Peak-to-average ratio: [e.g., 5:1]
- Response time sensitivity: [critical/moderate/low]

**Current setup:**
- Pod resources: [CPU/memory requests and limits]
- Current replica count: [number]
- Average CPU utilization: [%]

**Constraints:**
- Maximum pods: [number]
- Budget constraints: [if any]
- Cold start time: [seconds]

Please recommend:
1. HPA configuration (thresholds, behaviors)
2. Whether to use VPA additionally
3. Custom metrics to consider
4. Cluster autoscaler settings
5. Pod disruption budget
6. Scale-down stabilization settings
```

---

## Load Testing Prompts

### Design Load Test

```
Help me design a comprehensive load testing strategy for my [application type].

**System under test:**
- Endpoints: [list main endpoints]
- Expected load: [RPS]
- SLOs: [latency and error rate targets]

**User journeys:**
1. [describe journey 1]
2. [describe journey 2]
3. [describe journey 3]

**Environment:**
- Test environment specs: [describe]
- Production specs: [describe]

Please provide:
1. Test scenarios (smoke, load, stress, spike, soak)
2. k6 or Locust test script structure
3. Realistic think times and user behavior
4. What metrics to capture
5. Pass/fail criteria
6. How to interpret results
```

### Analyze Load Test Results

```
Analyze these load test results and recommend optimizations.

**Test configuration:**
- Tool: [k6/Locust/JMeter]
- Virtual users: [number]
- Duration: [time]
- Ramp-up: [pattern]

**Results:**
```
[paste summary results]
```

**Latency distribution:**
- p50: [value]
- p95: [value]
- p99: [value]
- max: [value]

**Error breakdown:**
- [error type 1]: [count]
- [error type 2]: [count]

**Resource utilization during test:**
- CPU: [peak %]
- Memory: [peak %]
- DB connections: [peak]
- Network: [throughput]

What are the bottlenecks and how should I address them?
```

---

## Database Optimization Prompts

### Index Recommendation

```
Recommend indexes for my PostgreSQL database based on these queries.

**Table schema:**
```sql
[CREATE TABLE statements]
```

**Most frequent queries:**
1. Query 1 (frequency: X/sec):
```sql
[query]
```

2. Query 2 (frequency: X/sec):
```sql
[query]
```

3. Query 3 (frequency: X/sec):
```sql
[query]
```

**Current indexes:**
```sql
[list current indexes]
```

**Constraints:**
- Write frequency: [inserts/updates per second]
- Storage budget: [if limited]

Please recommend:
1. Indexes to add (with CREATE INDEX statements)
2. Indexes that may be redundant
3. Partial indexes where applicable
4. Index maintenance considerations
```

### Connection Pool Sizing

```
Help me size my database connection pool.

**Application:**
- Type: [web app/API/worker]
- Framework: [language/framework]
- Deployment: [number of instances]

**Database:**
- Type: [PostgreSQL/MySQL]
- Server specs: [CPU cores, memory]
- max_connections setting: [value]

**Traffic:**
- Peak concurrent requests: [number]
- Average query duration: [ms]
- Peak query duration (p99): [ms]

**Current issues:**
- [describe any connection-related problems]

What pool settings do you recommend for:
1. Application-level pool size per instance
2. PgBouncer/ProxySQL configuration
3. Connection timeouts
4. Idle connection handling
```

---

## Code Review Prompts

### Review for Performance

```
Review this code for performance issues.

**Language:** [language]
**Context:** [where this code runs, frequency]
**Current performance:** [if known]

```[language]
[paste code]
```

Please identify:
1. Performance anti-patterns
2. N+1 query issues
3. Memory inefficiencies
4. Blocking operations that should be async
5. Missing caching opportunities
6. Specific refactoring suggestions with code examples
```

### Optimize Hot Path

```
Optimize this hot path code for maximum performance.

**Language:** [language]
**Call frequency:** [per second]
**Current latency:** [p50, p95, p99]
**Target latency:** [desired values]

**Code:**
```[language]
[paste code]
```

**Profiler output (if available):**
```
[paste profiler results]
```

**Constraints:**
- Must maintain [specific behavior/compatibility]
- Cannot use [specific restrictions]

Please provide optimized code with explanations for each change.
```

---

## SLO and Monitoring Prompts

### Define SLOs

```
Help me define appropriate SLOs for my service.

**Service type:** [API/web app/batch processor/etc.]
**User expectations:** [describe what users expect]
**Business impact of downtime:** [describe]

**Current metrics (if available):**
- Availability: [%]
- p50 latency: [ms]
- p95 latency: [ms]
- Error rate: [%]

**Dependencies:**
- [list external dependencies and their SLAs]

Please recommend:
1. Appropriate SLOs (availability, latency, throughput)
2. SLI definitions (how to measure)
3. Error budget policies
4. Alert thresholds (burn rate based)
5. Dashboard metrics to track
```

### Design Alerting Strategy

```
Design an alerting strategy based on these SLOs.

**SLOs:**
- Availability: [target %]
- Latency p95: < [ms]
- Error rate: < [%]

**Current alerting issues:**
- [describe false positives/negatives]
- [describe alert fatigue if present]

**On-call structure:**
- [describe team and escalation]

Please design:
1. Multi-window burn rate alerts
2. Alert severity levels
3. Runbook outlines for each alert
4. Dashboard requirements
5. Alert routing and escalation
```

---

## Prompt Templates for Common Scenarios

### Quick Performance Review

```
Quick performance review for [component/endpoint].

Current state:
- Latency: p50=[X]ms, p95=[X]ms, p99=[X]ms
- Throughput: [X] RPS
- Error rate: [X]%
- Resource usage: CPU [X]%, Memory [X]%

Target:
- Latency p95 < [X]ms
- Error rate < [X]%

Top 3 optimization recommendations?
```

### Database Query Optimization

```
Optimize this query:

```sql
[query]
```

Table has [X] rows. Query runs [X] times per [second/minute].

Current execution time: [X]ms
Target: < [X]ms

Provide:
1. Optimized query
2. Required indexes
3. Explanation of changes
```

### Cache Key Design

```
Design cache keys for [use case].

Data model:
- [describe entities and relationships]

Access patterns:
- [list how data is accessed]

Requirements:
- Invalidation granularity: [entity/list/all]
- Multi-tenancy: [yes/no]

Provide cache key schema and invalidation strategy.
```

---

## Best Practices for LLM Prompts

### Effective Prompt Structure

1. **Context first**: Describe your system and constraints
2. **Specific data**: Include actual metrics, not estimates
3. **Clear question**: State exactly what you need
4. **Output format**: Specify how you want the answer

### What to Include

| Category | Include | Example |
|----------|---------|---------|
| Metrics | Actual numbers | "p95: 450ms, target: 200ms" |
| Code | Relevant snippets | Actual queries, not pseudocode |
| Context | Tech stack | "Python 3.11, FastAPI, PostgreSQL 15" |
| Constraints | Real limitations | "Cannot add more than 2 new indexes" |

### What to Avoid

- Vague descriptions ("it's slow")
- Assumed knowledge ("you know how our system works")
- Missing constraints ("optimize this" without targets)
- Incomplete code snippets

### Iterative Refinement

```
[After receiving initial response]

Thank you. Let me add more context:

**Additional information:**
- [new detail 1]
- [new detail 2]

**Clarification on constraint:**
- [clarify any misunderstanding]

Given this, how would you modify your recommendation?
```

---

## Integration with Development Workflow

### PR Review Prompt

```
Review this PR for performance implications:

**Changed files:**
- [list files]

**Diff summary:**
```diff
[relevant diff sections]
```

**Questions:**
1. Are there any performance regressions?
2. Should any of these changes have performance tests?
3. Are there caching or indexing implications?
```

### Incident Post-mortem Analysis

```
Help analyze this performance incident.

**Timeline:**
- [time]: [event]
- [time]: [event]
- [time]: [event]

**Metrics during incident:**
- [metric graphs or data]

**Root cause (suspected):**
- [description]

**Questions:**
1. What early warning signs did we miss?
2. How can we prevent recurrence?
3. What monitoring should we add?
4. What runbook steps should exist?
```
