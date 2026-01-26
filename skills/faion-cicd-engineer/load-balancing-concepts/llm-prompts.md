# Load Balancing LLM Prompts

## Architecture Design

### Prompt: Design Load Balancing Architecture

```
Design a load balancing architecture for the following requirements:

Application Details:
- Type: [web app / API / microservices / streaming]
- Expected traffic: [RPS / concurrent users]
- Protocol: [HTTP/HTTPS / TCP / UDP / WebSocket / gRPC]
- Session requirements: [stateless / stateful / sticky sessions needed]

Infrastructure:
- Cloud provider: [AWS / GCP / Azure / on-premise / hybrid]
- Current setup: [single server / multiple servers / Kubernetes]
- Geographic distribution: [single region / multi-region / global]

Requirements:
- Availability SLA: [99.9% / 99.99% / 99.999%]
- Latency requirements: [p99 latency target]
- Budget constraints: [if any]

Please provide:
1. Recommended load balancer type (L4 vs L7)
2. Load balancing algorithm
3. Health check strategy
4. Session persistence approach (if needed)
5. High availability design
6. Architecture diagram
7. Estimated costs (if cloud-based)
```

### Prompt: L4 vs L7 Decision

```
Help me decide between Layer 4 and Layer 7 load balancing:

My application:
- Protocol: [describe protocols used]
- Need content-based routing: [yes/no]
- Need SSL termination at LB: [yes/no]
- Need HTTP header manipulation: [yes/no]
- Need URL path routing: [yes/no]
- Performance requirements: [describe latency/throughput needs]
- WebSocket support needed: [yes/no]

Current challenges:
[Describe any current issues]

Please analyze and recommend:
1. Which layer is more appropriate and why
2. Trade-offs of each option
3. Specific implementation recommendations
4. Migration path if changing layers
```

## Algorithm Selection

### Prompt: Choose Load Balancing Algorithm

```
Help me select the optimal load balancing algorithm:

Backend servers:
- Number of servers: [count]
- Server capacity: [same / different capacities - describe]
- Current utilization: [describe]

Traffic characteristics:
- Connection duration: [short-lived / long-lived / mixed]
- Request processing time: [uniform / variable]
- Traffic pattern: [steady / bursty / time-based peaks]

Application requirements:
- Session persistence: [required / not required]
- Latency sensitivity: [high / medium / low]
- Stateless: [yes / no]

Current algorithm (if any): [current algorithm]
Current issues: [describe problems]

Please recommend:
1. Best algorithm and why
2. Configuration parameters
3. Fallback strategies
4. Monitoring metrics to track
```

## Health Check Configuration

### Prompt: Design Health Check Strategy

```
Design a comprehensive health check strategy:

Application:
- Type: [web / API / microservices / database proxy]
- Framework: [specify]
- Critical dependencies: [database, cache, external APIs, etc.]

Current health endpoint: [describe or none]

Requirements:
- Detection time for failures: [target seconds]
- False positive tolerance: [low / medium / high]
- Graceful degradation: [required / not required]

Load balancer: [HAProxy / Nginx / AWS ALB / etc.]

Please provide:
1. Health check endpoint design
2. What to check (and what NOT to check)
3. Threshold configuration (intervals, timeouts, thresholds)
4. Response format
5. Sample implementation code
6. Monitoring and alerting recommendations
```

### Prompt: Troubleshoot Health Check Issues

```
Help troubleshoot health check problems:

Symptoms:
- [Describe what's happening - flapping, false positives, etc.]

Current configuration:
- Health check type: [TCP / HTTP / HTTPS]
- Endpoint: [path]
- Interval: [seconds]
- Timeout: [seconds]
- Healthy threshold: [count]
- Unhealthy threshold: [count]

Load balancer: [type]
Backend health check code: [if available]

Recent changes: [any recent changes]

Please analyze:
1. Likely root causes
2. Diagnostic steps
3. Configuration adjustments
4. Best practices violations
5. Recommended fixes
```

## Session Persistence

### Prompt: Design Session Persistence Strategy

```
Design a session persistence strategy:

Application requirements:
- Why persistence needed: [shopping cart / login session / WebSocket / other]
- Session data location: [in-memory / local file / database / cache]
- Session duration: [short / long / indefinite]

User behavior:
- Average session duration: [estimate]
- Multiple tabs/windows: [common / rare]
- Mobile + desktop: [same user on different devices?]

Infrastructure:
- Load balancer: [type]
- Can modify application: [yes / no]
- Can add shared session store: [yes / no]

Constraints:
- Auto-scaling: [yes / no]
- Even distribution importance: [high / medium / low]

Please recommend:
1. Persistence method (IP / cookie / application cookie)
2. Configuration details
3. Trade-offs and limitations
4. Alternative approaches (externalized sessions)
5. Migration path if changing approach
```

## Configuration Review

### Prompt: Review Load Balancer Configuration

```
Review my load balancer configuration for issues and improvements:

Configuration:
```
[Paste your HAProxy/Nginx/etc configuration here]
```

Context:
- Traffic volume: [RPS]
- Backend count: [number]
- Environment: [production / staging / development]
- Known issues: [any current problems]

Please review for:
1. Security issues
2. Performance optimizations
3. High availability concerns
4. Best practices violations
5. Missing configurations
6. Timeout tuning
7. Logging adequacy
```

### Prompt: Optimize Load Balancer Performance

```
Help optimize load balancer performance:

Current setup:
- Load balancer: [type and version]
- Configuration: [paste or describe]
- Hardware/instance type: [specs]

Traffic:
- Current RPS: [number]
- Peak RPS: [number]
- Connection type: [short/long-lived]
- Average request size: [KB]
- Average response size: [KB]

Current metrics:
- CPU utilization: [%]
- Memory utilization: [%]
- Connection count: [number]
- Latency (p50/p95/p99): [ms]

Issues:
- [Describe performance problems]

Please provide:
1. Bottleneck analysis
2. Configuration optimizations
3. Scaling recommendations
4. Connection tuning
5. Caching opportunities
6. Expected improvements
```

## Migration & Upgrades

### Prompt: Plan Load Balancer Migration

```
Help plan a load balancer migration:

Current setup:
- Load balancer: [current type/version]
- Configuration complexity: [simple / moderate / complex]
- Traffic volume: [RPS]
- Downtime tolerance: [zero / minimal / maintenance window OK]

Target:
- New load balancer: [target type]
- Reason for migration: [describe]

Constraints:
- Timeline: [target date]
- Team expertise: [familiar / learning new tech]
- Budget: [if relevant]

Please provide:
1. Migration strategy (big bang / gradual / blue-green)
2. Risk assessment
3. Rollback plan
4. Testing checklist
5. Cutover procedure
6. Post-migration validation
```

## Troubleshooting

### Prompt: Diagnose Load Balancer Issues

```
Help diagnose load balancer issues:

Symptoms:
- [Describe the problem in detail]
- When started: [time/date]
- Frequency: [constant / intermittent / pattern-based]
- Affected users: [all / some / specific regions]

Error messages:
- [Any error messages or codes]

Recent changes:
- [List any recent changes to LB, backends, or network]

Current metrics:
- Error rate: [%]
- Latency: [ms]
- Backend health: [healthy/unhealthy counts]

Configuration:
- [Paste relevant configuration]

Please help:
1. Identify likely root causes
2. Provide diagnostic commands
3. Suggest immediate mitigations
4. Recommend permanent fixes
5. Prevention strategies
```

### Prompt: Debug Connection Issues

```
Debug load balancer connection issues:

Problem:
- [Connection timeouts / refused / reset / etc.]
- Client-side or server-side: [if known]
- Error rate: [%]

Network path:
Client -> [describe path] -> Load Balancer -> Backend

Configuration:
- Timeout settings: [list timeouts]
- Max connections: [limits]
- Keepalive: [enabled/disabled, settings]

What I've checked:
- [List what you've already verified]

Please help:
1. Additional diagnostic steps
2. Common causes for this pattern
3. Configuration adjustments
4. Network-level checks
5. Application-level checks
```

## Capacity Planning

### Prompt: Plan Load Balancer Capacity

```
Help with load balancer capacity planning:

Current state:
- Load balancer: [type]
- Instance/hardware: [specs]
- Current traffic: [RPS, connections, bandwidth]
- Current utilization: [CPU, memory, connections]

Growth projections:
- Expected traffic growth: [% per month/year]
- Peak events: [describe any known peaks]
- New features impact: [any features that will increase traffic]

Requirements:
- Headroom desired: [% buffer]
- Scaling approach: [vertical / horizontal / both]
- Budget constraints: [if any]

Please provide:
1. Capacity analysis
2. Scaling recommendations
3. Timeline for upgrades
4. Cost estimates
5. Monitoring thresholds
6. Auto-scaling strategy (if applicable)
```

## Cost Optimization

### Prompt: Optimize Load Balancing Costs

```
Help optimize load balancing costs:

Current setup:
- Cloud provider: [AWS / GCP / Azure]
- Load balancer type: [ALB / NLB / etc.]
- Configuration: [describe]
- Monthly cost: [current spend]

Traffic patterns:
- Average traffic: [RPS/bandwidth]
- Peak traffic: [RPS/bandwidth]
- Off-peak periods: [describe]
- Geographic distribution: [regions]

Usage details:
- Data processed: [GB/month]
- Rules/listeners: [count]
- Target groups: [count]

Please analyze:
1. Cost breakdown
2. Optimization opportunities
3. Alternative architectures
4. Reserved capacity options
5. Expected savings
6. Trade-offs to consider
```

---

*Load Balancing LLM Prompts | faion-cicd-engineer*
