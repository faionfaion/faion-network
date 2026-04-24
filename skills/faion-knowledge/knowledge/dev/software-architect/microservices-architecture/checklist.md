# Microservices Checklist

Step-by-step checklist for designing and implementing microservices architecture.

## Phase 1: Assessment

### Prerequisites Check

- [ ] **DevOps maturity assessment**
  - [ ] CI/CD pipelines exist and are reliable
  - [ ] Infrastructure as Code practices in place
  - [ ] Automated testing culture established
  - [ ] Incident response procedures documented

- [ ] **Team readiness**
  - [ ] Team size justifies microservices (30+ developers)
  - [ ] Teams can own services end-to-end
  - [ ] On-call rotation capability exists
  - [ ] Service ownership model defined

- [ ] **Technical foundation**
  - [ ] Container orchestration ready (Kubernetes)
  - [ ] Centralized logging infrastructure
  - [ ] Monitoring and alerting system
  - [ ] Service discovery mechanism

### Decision Validation

- [ ] Documented why microservices (not just "because Netflix does it")
- [ ] Evaluated alternatives (modular monolith, serverless)
- [ ] Executive sponsorship secured
- [ ] Budget for operational complexity approved

## Phase 2: Domain Analysis

### Domain Discovery

- [ ] **Stakeholder interviews**
  - [ ] Business stakeholders identified
  - [ ] Domain experts engaged
  - [ ] Key business processes documented

- [ ] **Event Storming session**
  - [ ] Domain events identified
  - [ ] Commands mapped
  - [ ] Aggregates discovered
  - [ ] Bounded contexts emerged

- [ ] **Context mapping**
  - [ ] Bounded contexts defined
  - [ ] Context relationships documented (upstream/downstream)
  - [ ] Integration patterns chosen (ACL, OHS, Partnership)

### Service Identification

- [ ] **Business capabilities mapped**
  - [ ] Core capabilities identified (build in-house)
  - [ ] Supporting capabilities identified (build or buy)
  - [ ] Generic capabilities identified (use existing)

- [ ] **Service boundaries defined**
  - [ ] Each service has single business capability
  - [ ] Data ownership clear per service
  - [ ] Communication patterns identified

- [ ] **Decomposition validated**
  - [ ] Services can deploy independently
  - [ ] Services can scale independently
  - [ ] Team can own 2-3 services max

## Phase 3: Architecture Design

### Communication Design

- [ ] **Sync vs async decision per interaction**
  - [ ] Query operations → sync (REST/gRPC)
  - [ ] Commands → async where possible
  - [ ] Notifications → async

- [ ] **API design**
  - [ ] API contracts defined (OpenAPI/Protobuf)
  - [ ] Versioning strategy chosen
  - [ ] Error handling standardized
  - [ ] Rate limiting designed

- [ ] **Event design**
  - [ ] Event schemas defined
  - [ ] Event naming conventions established
  - [ ] Event versioning strategy chosen

### Data Architecture

- [ ] **Database per service**
  - [ ] Each service has own database
  - [ ] No shared databases between services
  - [ ] Database technology chosen per service needs

- [ ] **Data consistency strategy**
  - [ ] Saga pattern chosen (choreography vs orchestration)
  - [ ] Compensating transactions designed
  - [ ] Eventual consistency acceptable where needed

- [ ] **Data migration plan**
  - [ ] Data split strategy documented
  - [ ] Migration scripts prepared
  - [ ] Rollback plan exists

### Resilience Design

- [ ] **Failure handling**
  - [ ] Circuit breakers configured
  - [ ] Retry policies defined (with backoff)
  - [ ] Timeouts set for all external calls
  - [ ] Bulkheads designed

- [ ] **Graceful degradation**
  - [ ] Fallback behaviors defined
  - [ ] Feature flags for quick disable
  - [ ] Cache strategies for resilience

## Phase 4: Infrastructure Setup

### Container Orchestration

- [ ] **Kubernetes cluster**
  - [ ] Cluster provisioned (managed K8s recommended)
  - [ ] Namespaces strategy defined
  - [ ] Resource quotas configured
  - [ ] Network policies defined

- [ ] **Service deployment**
  - [ ] Deployment manifests created
  - [ ] ConfigMaps/Secrets managed
  - [ ] HPA (Horizontal Pod Autoscaler) configured
  - [ ] PDB (Pod Disruption Budget) defined

### Service Mesh (Optional but Recommended)

- [ ] **Service mesh choice**
  - [ ] Evaluated Linkerd vs Istio
  - [ ] Service mesh installed
  - [ ] mTLS enabled

- [ ] **Traffic management**
  - [ ] Traffic policies defined
  - [ ] Canary deployment configured
  - [ ] Traffic splitting ready

### API Gateway

- [ ] **Gateway setup**
  - [ ] Gateway chosen (Kong, Ambassador, Nginx)
  - [ ] Authentication configured
  - [ ] Rate limiting enabled
  - [ ] Request routing configured

## Phase 5: Observability

### Logging

- [ ] **Centralized logging**
  - [ ] Log aggregation system deployed (ELK/Loki)
  - [ ] Structured logging format defined
  - [ ] Log retention policy set
  - [ ] Log access controls configured

- [ ] **Correlation**
  - [ ] Correlation ID propagation implemented
  - [ ] Request tracing through all services
  - [ ] Log levels standardized

### Metrics

- [ ] **Metrics collection**
  - [ ] Prometheus/metrics system deployed
  - [ ] Application metrics exposed
  - [ ] Infrastructure metrics collected
  - [ ] Custom business metrics defined

- [ ] **Dashboards**
  - [ ] Service-level dashboards created
  - [ ] System-wide overview dashboard
  - [ ] SLO/SLI dashboards

### Tracing

- [ ] **Distributed tracing**
  - [ ] Tracing system deployed (Jaeger/Zipkin/Tempo)
  - [ ] Instrumentation added to all services
  - [ ] Sampling strategy defined
  - [ ] Trace retention configured

### Alerting

- [ ] **Alert definitions**
  - [ ] SLO-based alerts configured
  - [ ] Error rate alerts
  - [ ] Latency alerts (p95, p99)
  - [ ] Resource utilization alerts

- [ ] **Alert routing**
  - [ ] On-call rotation configured
  - [ ] Escalation policies defined
  - [ ] Runbooks created for common alerts

## Phase 6: CI/CD

### Pipeline Setup

- [ ] **Per-service pipelines**
  - [ ] Build pipeline per service
  - [ ] Independent versioning per service
  - [ ] Artifact storage configured

- [ ] **Testing in pipeline**
  - [ ] Unit tests required
  - [ ] Integration tests automated
  - [ ] Contract tests (Pact) configured
  - [ ] Security scans (SAST/DAST)

### Deployment Strategy

- [ ] **Deployment automation**
  - [ ] GitOps workflow (ArgoCD/Flux)
  - [ ] Environment promotion process
  - [ ] Rollback automation

- [ ] **Release strategies**
  - [ ] Blue-green deployment ready
  - [ ] Canary deployment configured
  - [ ] Feature flags integrated

## Phase 7: Security

### Service Security

- [ ] **Authentication**
  - [ ] Service-to-service auth (mTLS or JWT)
  - [ ] API authentication (OAuth2/OIDC)
  - [ ] Service accounts managed

- [ ] **Authorization**
  - [ ] RBAC policies defined
  - [ ] Service-level permissions
  - [ ] API endpoint authorization

### Data Security

- [ ] **Encryption**
  - [ ] Data at rest encrypted
  - [ ] Data in transit encrypted (TLS)
  - [ ] Secrets management (Vault/AWS Secrets Manager)

- [ ] **Compliance**
  - [ ] Data classification done
  - [ ] PII handling documented
  - [ ] Audit logging enabled

## Phase 8: Documentation

### Technical Documentation

- [ ] **Architecture documentation**
  - [ ] C4 diagrams created
  - [ ] ADRs for key decisions
  - [ ] Service catalog maintained

- [ ] **API documentation**
  - [ ] OpenAPI specs published
  - [ ] API versioning documented
  - [ ] Integration guides written

### Operational Documentation

- [ ] **Runbooks**
  - [ ] Common incident runbooks
  - [ ] Service-specific troubleshooting
  - [ ] Deployment procedures

- [ ] **Onboarding**
  - [ ] New service creation guide
  - [ ] Developer onboarding docs
  - [ ] Architecture overview for new team members

## Phase 9: Migration (If Extracting from Monolith)

### Strangler Fig Approach

- [ ] **Preparation**
  - [ ] Identified first service to extract
  - [ ] Anti-corruption layer designed
  - [ ] Data synchronization strategy

- [ ] **Extraction**
  - [ ] New service implemented
  - [ ] Traffic gradually shifted
  - [ ] Old code deprecated

- [ ] **Cleanup**
  - [ ] Monolith code removed
  - [ ] Data migration completed
  - [ ] Anti-corruption layer simplified/removed

## Phase 10: Ongoing Operations

### Health Monitoring

- [ ] Regular service health reviews
- [ ] SLO compliance tracking
- [ ] Dependency health monitoring
- [ ] Cost optimization reviews

### Continuous Improvement

- [ ] Post-incident reviews (blameless)
- [ ] Architecture fitness functions
- [ ] Technical debt tracking
- [ ] Regular dependency updates

## Quick Reference: Minimum Viable Microservices

For teams just starting, prioritize:

1. **Must have:**
   - [ ] CI/CD per service
   - [ ] Centralized logging
   - [ ] Health checks
   - [ ] Basic monitoring

2. **Should have:**
   - [ ] Distributed tracing
   - [ ] Circuit breakers
   - [ ] API gateway

3. **Nice to have:**
   - [ ] Service mesh
   - [ ] Advanced traffic management
   - [ ] Chaos engineering
