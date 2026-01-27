# Service Mesh

Infrastructure layer for secure, observable service-to-service communication in microservices architectures.

## What is a Service Mesh?

A dedicated infrastructure layer that handles:
- **Service discovery** - Automatic endpoint detection
- **Load balancing** - Traffic distribution across instances
- **mTLS encryption** - Mutual TLS for zero-trust security
- **Observability** - Metrics, tracing, logging
- **Traffic management** - Routing, retries, circuit breaking
- **Policy enforcement** - Access control, rate limiting

## Architecture

### Data Plane

The data plane consists of proxies deployed alongside each service:

| Approach | Description | Examples |
|----------|-------------|----------|
| **Sidecar** | Proxy container per pod | Istio (Envoy), Linkerd |
| **Per-node** | Single proxy per node | Cilium, Istio Ambient (ztunnel) |
| **Kernel-level** | eBPF in Linux kernel | Cilium |

### Control Plane

Centralized management component:
- Configuration distribution
- Certificate management (mTLS)
- Policy enforcement
- Telemetry aggregation

## Service Mesh Comparison (2025)

### Quick Selection Guide

| Requirement | Best Choice |
|-------------|-------------|
| Full features, enterprise | **Istio** |
| Simplicity, low latency | **Linkerd** |
| eBPF, network policies | **Cilium** |
| HashiCorp ecosystem | **Consul Connect** |
| Minimal overhead, mTLS only | **Istio Ambient** |

### Detailed Comparison

| Feature | Istio | Linkerd | Cilium |
|---------|-------|---------|--------|
| Architecture | Sidecar (Envoy) or Ambient | Sidecar (Rust proxy) | eBPF + Envoy |
| mTLS | Yes (configurable) | Yes (default on) | Yes |
| Traffic management | Advanced | Basic-moderate | Moderate |
| Observability | Excellent | Good | Good |
| Multi-cluster | Yes | Yes (paid) | Yes |
| Gateway API | Full support | Partial | Partial |
| Learning curve | High | Low | Moderate |
| CNCF status | Graduated | Graduated | Graduated |

### Performance Benchmarks (2025)

Based on recent benchmarks with mTLS enabled:

| Metric | Istio Sidecar | Istio Ambient | Linkerd | Cilium |
|--------|---------------|---------------|---------|--------|
| Latency increase (3200 RPS) | +166% | +8% | +33% | +99% |
| CPU per 1000 RPS | ~0.35 vCPU | ~0.06 vCPU | ~0.1 vCPU | Low (kernel) |
| Memory per proxy | ~60 MB | ~12 MB (ztunnel) | ~20 MB | Per-node |
| Best for | Features | Low overhead | Simplicity | Scale |

### Architecture Approaches

**Sidecar Model (Traditional)**
- Proxy per pod (Envoy, Linkerd proxy)
- Full L7 features
- Higher resource overhead
- Complete isolation

**Sidecarless Model (2025 Trend)**
- **Istio Ambient**: ztunnel (L4) per node + waypoint (L7) per namespace
- **Cilium**: eBPF in kernel + optional Envoy for L7
- Lower resource usage
- Reduced latency
- Simpler operations

## When to Use a Service Mesh

### Good Use Cases

| Scenario | Why Service Mesh Helps |
|----------|------------------------|
| 10+ microservices | Centralized traffic management |
| Zero-trust security | Automatic mTLS everywhere |
| Complex deployments | Canary, blue-green, A/B testing |
| Observability needs | Uniform metrics, tracing |
| Multi-cluster | Cross-cluster communication |
| Compliance (SOC2, HIPAA) | Encryption, audit trails |

### When NOT to Use

| Scenario | Better Alternative |
|----------|-------------------|
| <5 services | Direct HTTP/gRPC with manual TLS |
| Monolith | Not needed |
| Extreme latency requirements (<1ms) | Direct communication |
| Resource-constrained env | Lightweight mTLS only |
| Simple traffic patterns | Kubernetes Services + Ingress |
| Team unfamiliar with K8s | Master K8s first |

### Decision Framework

```
Need mTLS only?
  YES → Istio Ambient or cert-manager + manual config
  NO → Continue

Need advanced L7 features?
  YES → Istio or Linkerd
  NO → Cilium (network policies + basic mesh)

Resource constrained?
  YES → Linkerd or Istio Ambient
  NO → Istio (full features)

Need multi-cluster?
  YES → Istio or Cilium
  NO → Any

Value simplicity?
  YES → Linkerd
  NO → Istio
```

## Key Features

### mTLS (Mutual TLS)

Automatic encryption and identity verification:
- Zero-trust by default
- No code changes required
- Automatic certificate rotation
- SPIFFE identity standard

**Best Practices:**
1. Start with permissive mode, migrate to strict
2. Use short-lived certificates (24h or less)
3. Don't use self-signed CA in production
4. Monitor certificate expiry
5. Use SPIFFE/SPIRE for multi-cluster

### Traffic Management

| Pattern | Use Case |
|---------|----------|
| **Canary** | Gradual rollout (1% → 10% → 50% → 100%) |
| **Blue-Green** | Instant switch between versions |
| **A/B Testing** | Route by headers/cookies |
| **Traffic mirroring** | Test with production traffic |
| **Circuit breaking** | Prevent cascade failures |
| **Retries** | Handle transient failures |
| **Timeouts** | Fail fast |

### Observability Integration

Standard stack:
- **Prometheus** - Metrics collection
- **Grafana** - Dashboards
- **Jaeger/Tempo** - Distributed tracing
- **Kiali** - Service topology (Istio)

Key metrics:
- Request rate, error rate, duration (RED)
- p50/p95/p99 latencies
- Success rate per service
- Certificate expiry

## Performance Overhead

### Expected Impact

| Mesh | Latency Overhead | Memory per Pod | CPU per 1000 RPS |
|------|------------------|----------------|------------------|
| Istio (sidecar) | 2-5ms | 50-70 MB | 0.35 vCPU |
| Istio Ambient | <1ms | 12 MB (shared) | 0.06 vCPU |
| Linkerd | <1ms | 20-30 MB | 0.1 vCPU |
| Cilium | Minimal | Per-node only | Kernel-level |

### Optimization Tips

1. **Right-size proxy resources** - Don't over-provision
2. **Disable unused features** - Turn off tracing if not needed
3. **Use ambient mode** - For mTLS-only use cases
4. **Tune telemetry** - Sampling rate for high-traffic
5. **Consider eBPF** - Cilium for network-heavy workloads

## External Resources

### Official Documentation
- [Istio Documentation](https://istio.io/latest/docs/)
- [Linkerd Documentation](https://linkerd.io/docs/)
- [Cilium Documentation](https://docs.cilium.io/)
- [Consul Connect](https://developer.hashicorp.com/consul/docs/connect)

### Learning Resources
- [Service Mesh Comparison (LiveWyer)](https://livewyer.io/blog/service-meshes-decoded-istio-vs-linkerd-vs-cilium/)
- [Istio Ambient Deep Dive](https://seifrajhi.github.io/blog/kubernetes-networking-istio-sidecarless/)
- [mTLS Best Practices (Tetrate)](https://tetrate.io/blog/mtls-best-practices-for-kubernetes)
- [Performance Benchmarks (2025)](https://arxiv.org/html/2411.02267v1)

### Tools
- [Flagger](https://flagger.app/) - Progressive delivery operator
- [Kiali](https://kiali.io/) - Istio observability console
- [Buoyant Cloud](https://buoyant.io/) - Linkerd enterprise

## LLM Usage Tips

### Effective Prompting

When using LLMs for service mesh design:

1. **Provide context** - Cluster size, service count, current stack
2. **Specify constraints** - Latency requirements, resource limits
3. **Ask for trade-offs** - Not just "best" solution
4. **Request configurations** - Get actual YAML, not just concepts

### Common LLM Tasks

| Task | Prompt Focus |
|------|--------------|
| Mesh selection | Requirements, constraints, team experience |
| Configuration | Specific version, environment details |
| Troubleshooting | Error messages, observed behavior |
| Migration | Current state, target state, constraints |
| Performance tuning | Metrics, bottlenecks, SLOs |

### What LLMs Can Help With

- Generating initial configurations
- Explaining complex concepts
- Debugging configuration issues
- Comparing approaches with trade-offs
- Creating observability dashboards

### What LLMs Cannot Do Well

- Real-time performance analysis
- Cluster-specific recommendations without metrics
- Security audit (need actual scanning)
- Cost estimation (varies by provider)

## Related Methodologies

| Methodology | Relationship |
|-------------|--------------|
| [microservices-architecture/](../microservices-architecture/) | Service design patterns |
| [security-architecture/](../security-architecture/) | Zero-trust, mTLS details |
| [observability-architecture/](../observability-architecture/) | Monitoring integration |
| [reliability-architecture/](../reliability-architecture/) | Circuit breaking, retries |
| [api-gateway-design/](../api-gateway-design/) | North-south traffic |

## File Index

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts (this file) |
| [checklist.md](checklist.md) | Step-by-step implementation guide |
| [examples.md](examples.md) | Real-world configurations |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM assistance |
