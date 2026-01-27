# Software Architect

> **Entry point:** `/faion-net` — invoke for automatic routing.

System design, technology selection, Architecture Decision Records (ADRs), quality attributes.

**Methodologies:** 40 | **Agents:** 2

## When to Use

- Designing system architecture
- Technology selection decisions
- Architecture style selection (monolith, microservices, etc.)
- Database selection and data modeling
- Creating Architecture Decision Records (ADRs)
- Quality attributes analysis (scalability, performance, security)
- Communication patterns (REST, GraphQL, gRPC, async)

## Key Decision Trees

**Architecture Style:**
```
Small team / MVP → Monolith or Modular Monolith
Large team / Independent deploy → Microservices
Unclear boundaries → Modular Monolith (extract later)
```

**Database:**
```
Relational → PostgreSQL / MySQL
NewSQL (distributed) → CockroachDB / TiDB / Spanner
Document → MongoDB / DynamoDB
Key-value → Redis
Time-series → TimescaleDB / InfluxDB / ClickHouse
Graph → Neo4j / Neptune
Vector (AI/RAG) → Qdrant / Weaviate / Pinecone / pgvector
Search → Elasticsearch / Meilisearch
```

**Communication:**
```
Sync internal → gRPC or REST
Sync external → REST or GraphQL
Async ordered → Kafka
Async unordered → RabbitMQ / SQS
Real-time → WebSockets or SSE
```

## Quality Attributes

| Attribute | Key Question |
|-----------|--------------|
| Scalability | Handle 10x load? |
| Performance | Latency p95 < 200ms? |
| Availability | 99.9% or 99.99%? |
| Security | Threat model done? |
| Maintainability | Deploy daily? |

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Navigation hub with decision reference |
| [system-design-process/](system-design-process/) | System design methodology folder |
| - [README.md](system-design-process/README.md) | Process overview, LLM-assisted design |
| - [checklist.md](system-design-process/checklist.md) | Step-by-step design checklist |
| - [examples.md](system-design-process/examples.md) | Twitter, Uber, Netflix case studies |
| - [templates.md](system-design-process/templates.md) | ADR templates, C4 Mermaid diagrams |
| - [llm-prompts.md](system-design-process/llm-prompts.md) | Prompts for architecture discussions |
| [architectural-patterns/](architectural-patterns/) | Domain-centric architecture patterns |
| - [README.md](architectural-patterns/README.md) | Clean, Hexagonal, Onion, DDD overview |
| - [checklist.md](architectural-patterns/checklist.md) | Pattern selection checklist |
| - [examples.md](architectural-patterns/examples.md) | E-commerce implementations |
| - [templates.md](architectural-patterns/templates.md) | Code templates by pattern |
| - [llm-prompts.md](architectural-patterns/llm-prompts.md) | Architecture prompts for LLMs |
| [microservices-architecture/](microservices-architecture/) | Microservices architecture guide |
| - [README.md](microservices-architecture/README.md) | When to use, decomposition, communication |
| - [checklist.md](microservices-architecture/checklist.md) | Implementation checklist |
| - [examples.md](microservices-architecture/examples.md) | E-commerce, fintech, streaming examples |
| - [templates.md](microservices-architecture/templates.md) | Docker, K8s, service templates |
| - [llm-prompts.md](microservices-architecture/llm-prompts.md) | Prompts for microservices design |
| [event-driven-architecture/](event-driven-architecture/) | Event-driven architecture guide |
| - [README.md](event-driven-architecture/README.md) | EDA patterns, brokers, CloudEvents |
| - [checklist.md](event-driven-architecture/checklist.md) | EDA design checklist (146 items) |
| - [examples.md](event-driven-architecture/examples.md) | E-commerce, trading, IoT examples |
| - [templates.md](event-driven-architecture/templates.md) | Event schemas, producer/consumer templates |
| - [llm-prompts.md](event-driven-architecture/llm-prompts.md) | Prompts for EDA design |
| [database-selection/](database-selection/) | Database selection framework |
| - [README.md](database-selection/README.md) | Categories, CAP theorem, comparison matrices |
| - [checklist.md](database-selection/checklist.md) | Selection checklist (6 phases) |
| - [examples.md](database-selection/examples.md) | E-commerce, SaaS, RAG, IoT, fintech examples |
| - [templates.md](database-selection/templates.md) | Decision matrix, ADR, migration templates |
| - [llm-prompts.md](database-selection/llm-prompts.md) | Prompts for database discussions |
| [monolith-architecture/](monolith-architecture/) | Traditional monolith architecture guide |
| - [README.md](monolith-architecture/README.md) | When to use, advantages, scaling, deployment |
| - [checklist.md](monolith-architecture/checklist.md) | Step-by-step monolith design checklist (12 phases) |
| - [examples.md](monolith-architecture/examples.md) | E-commerce, SaaS, fintech, content platform examples |
| - [templates.md](monolith-architecture/templates.md) | Django, FastAPI, Docker, nginx, CI/CD templates |
| - [llm-prompts.md](monolith-architecture/llm-prompts.md) | Prompts for monolith design and optimization |
| [modular-monolith/](modular-monolith/) | Modular monolith architecture guide |
| - [README.md](modular-monolith/README.md) | When to use, principles, communication patterns |
| - [checklist.md](modular-monolith/checklist.md) | Step-by-step implementation checklist |
| - [examples.md](modular-monolith/examples.md) | Shopify, GitHub, Kraken case studies |
| - [templates.md](modular-monolith/templates.md) | Module structure, Python/Go/Java templates |
| - [llm-prompts.md](modular-monolith/llm-prompts.md) | Prompts for modular design |
| [architecture-decision-records/](architecture-decision-records/) | Architecture Decision Records guide |
| - [README.md](architecture-decision-records/README.md) | ADR overview, formats, lifecycle, tools, LLM tips |
| - [checklist.md](architecture-decision-records/checklist.md) | Step-by-step ADR writing checklist (5 phases) |
| - [examples.md](architecture-decision-records/examples.md) | Nygard, MADR, Y-statement, migration, rejection examples |
| - [templates.md](architecture-decision-records/templates.md) | Copy-paste templates (10 formats) |
| - [llm-prompts.md](architecture-decision-records/llm-prompts.md) | Prompts for LLM-assisted ADR writing |
| [trade-off-analysis/](trade-off-analysis/) | Trade-off analysis framework |
| - [README.md](trade-off-analysis/README.md) | ATAM, quality attributes, build vs buy, decision frameworks |
| - [checklist.md](trade-off-analysis/checklist.md) | Quick, standard, and ATAM-style checklists |
| - [examples.md](trade-off-analysis/examples.md) | Database, architecture, build vs buy, technical debt examples |
| - [templates.md](trade-off-analysis/templates.md) | Decision matrix, ADR, ATAM utility tree, stakeholder templates |
| - [llm-prompts.md](trade-off-analysis/llm-prompts.md) | Prompts for LLM-assisted trade-off analysis |
| [c4-model/](c4-model/) | C4 model for architecture visualization |
| - [README.md](c4-model/README.md) | C4 overview, four levels, tooling, LLM tips |
| - [checklist.md](c4-model/checklist.md) | Step-by-step checklist for each diagram type |
| - [examples.md](c4-model/examples.md) | E-commerce, banking, microservices case studies |
| - [templates.md](c4-model/templates.md) | Structurizr DSL, PlantUML, Mermaid templates |
| - [llm-prompts.md](c4-model/llm-prompts.md) | Prompts for AI-assisted diagram creation |
| [caching-architecture/](caching-architecture/) | Caching architecture and patterns |
| - [README.md](caching-architecture/README.md) | Caching patterns overview, layer design, LLM tips |
| - [checklist.md](caching-architecture/checklist.md) | Step-by-step caching design checklist |
| - [examples.md](caching-architecture/examples.md) | E-commerce, social media, SaaS, analytics examples |
| - [templates.md](caching-architecture/templates.md) | Redis, Django, FastAPI, CDN configurations |
| - [llm-prompts.md](caching-architecture/llm-prompts.md) | Prompts for caching design discussions |
| [serverless-architecture/](serverless-architecture/) | Serverless architecture guide |
| - [README.md](serverless-architecture/README.md) | Serverless patterns, providers, when to use/avoid |
| - [checklist.md](serverless-architecture/checklist.md) | Step-by-step serverless design checklist |
| - [examples.md](serverless-architecture/examples.md) | E-commerce, data pipeline, SaaS, ML inference examples |
| - [templates.md](serverless-architecture/templates.md) | AWS SAM, Serverless Framework, SST, CDK templates |
| - [llm-prompts.md](serverless-architecture/llm-prompts.md) | Prompts for serverless design discussions |
| [security-architecture/](security-architecture/) | Security architecture guide |
| - [README.md](security-architecture/README.md) | Zero Trust, auth patterns, OWASP, threat modeling |
| - [checklist.md](security-architecture/checklist.md) | Step-by-step security design checklist (11 phases) |
| - [examples.md](security-architecture/examples.md) | SaaS, healthcare, fintech, microservices, mobile examples |
| - [templates.md](security-architecture/templates.md) | OAuth, Vault, Istio, K8s security configurations |
| - [llm-prompts.md](security-architecture/llm-prompts.md) | Prompts for security architecture discussions |
| [observability-architecture/](observability-architecture/) | Observability architecture guide |
| - [README.md](observability-architecture/README.md) | Three pillars, OTEL, SLOs, cost optimization, LLM tips |
| - [checklist.md](observability-architecture/checklist.md) | Step-by-step observability design checklist (12 phases) |
| - [examples.md](observability-architecture/examples.md) | Startup, enterprise, e-commerce, SaaS examples |
| - [templates.md](observability-architecture/templates.md) | Prometheus, OTEL, Loki, Tempo, Grafana configurations |
| - [llm-prompts.md](observability-architecture/llm-prompts.md) | Prompts for observability design discussions |
| [performance-architecture/](performance-architecture/) | Performance architecture guide |
| - [README.md](performance-architecture/README.md) | SLOs, scalability, caching, database optimization, CDN |
| - [checklist.md](performance-architecture/checklist.md) | Step-by-step performance design checklist (120 items) |
| - [examples.md](performance-architecture/examples.md) | E-commerce, analytics, API, IoT optimization examples |
| - [templates.md](performance-architecture/templates.md) | Redis, PostgreSQL, k6, Kubernetes HPA configurations |
| - [llm-prompts.md](performance-architecture/llm-prompts.md) | Prompts for performance analysis and optimization |
| [api-gateway-design/](api-gateway-design/) | API gateway architecture guide |
| - [README.md](api-gateway-design/README.md) | Gateway patterns, Kong/Traefik/Envoy/AWS comparison, LLM tips |
| - [checklist.md](api-gateway-design/checklist.md) | Step-by-step gateway design checklist (173 items, 12 phases) |
| - [examples.md](api-gateway-design/examples.md) | E-commerce, SaaS, K8s, GraphQL federation examples |
| - [templates.md](api-gateway-design/templates.md) | Kong, AWS APIGW, Traefik, Envoy, Apollo Router templates |
| - [llm-prompts.md](api-gateway-design/llm-prompts.md) | Prompts for gateway design and configuration |
| [data-modeling/](data-modeling/) | Data modeling guide |
| - [README.md](data-modeling/README.md) | Conceptual/logical/physical modeling, NoSQL patterns, LLM tips |
| - [checklist.md](data-modeling/checklist.md) | Step-by-step data modeling checklist (9 phases) |
| - [examples.md](data-modeling/examples.md) | E-commerce, IoT, social network, Data Vault examples |
| - [templates.md](data-modeling/templates.md) | PostgreSQL, MongoDB, Cassandra, Neo4j, TimescaleDB templates |
| - [llm-prompts.md](data-modeling/llm-prompts.md) | Prompts for data modeling design discussions |
| [distributed-patterns/](distributed-patterns/) | Distributed system patterns guide |
| - [README.md](distributed-patterns/README.md) | Saga, CQRS, Event Sourcing, resilience patterns overview |
| - [checklist.md](distributed-patterns/checklist.md) | Step-by-step distributed patterns checklist (182 items, 11 phases) |
| - [examples.md](distributed-patterns/examples.md) | E-commerce, banking, analytics, microservices examples |
| - [templates.md](distributed-patterns/templates.md) | Temporal, Kafka, Resilience4j, Redis, etcd templates |
| - [llm-prompts.md](distributed-patterns/llm-prompts.md) | Prompts for distributed system design discussions |
| [reliability-architecture/](reliability-architecture/) | Reliability architecture guide |
| - [README.md](reliability-architecture/README.md) | SLOs, fault tolerance, redundancy, chaos engineering overview |
| - [checklist.md](reliability-architecture/checklist.md) | Step-by-step reliability design checklist (197 items, 10 phases) |
| - [examples.md](reliability-architecture/examples.md) | E-commerce, fintech, real-time data, multi-region SaaS examples |
| - [templates.md](reliability-architecture/templates.md) | Circuit breaker, retry, health check, DR configurations |
| - [llm-prompts.md](reliability-architecture/llm-prompts.md) | Prompts for reliability architecture discussions |
| [service-mesh/](service-mesh/) | Service mesh architecture guide |
| - [README.md](service-mesh/README.md) | Istio/Linkerd/Cilium comparison, mTLS, when to use |
| - [checklist.md](service-mesh/checklist.md) | Step-by-step service mesh implementation checklist (180+ items) |
| - [examples.md](service-mesh/examples.md) | E-commerce, SaaS, analytics, multi-cluster examples |
| - [templates.md](service-mesh/templates.md) | Istio, Linkerd, Cilium, Flagger configurations |
| - [llm-prompts.md](service-mesh/llm-prompts.md) | Prompts for service mesh design and troubleshooting |
| [cloud-architecture/](cloud-architecture/) | Cloud architecture guide |
| - [README.md](cloud-architecture/README.md) | Well-Architected, multi-cloud, landing zones, FinOps, provider comparison |
| - [checklist.md](cloud-architecture/checklist.md) | Step-by-step cloud architecture checklist (12 phases) |
| - [examples.md](cloud-architecture/examples.md) | E-commerce, SaaS, FinTech, ML, IoT, startup examples |
| - [templates.md](cloud-architecture/templates.md) | Terraform, AWS CDK, Pulumi, Kubernetes configurations |
| - [llm-prompts.md](cloud-architecture/llm-prompts.md) | Prompts for cloud design, review, migration, troubleshooting |
| [container-orchestration/](container-orchestration/) | Container orchestration guide |
| - [README.md](container-orchestration/README.md) | K8s architecture, pod patterns, deployment strategies, RBAC, storage |
| - [checklist.md](container-orchestration/checklist.md) | Step-by-step orchestration design checklist (180 items, 12 phases) |
| - [examples.md](container-orchestration/examples.md) | Web app, StatefulSet, KEDA, sidecar, canary, network policy examples |
| - [templates.md](container-orchestration/templates.md) | Deployment, Service, HPA, KEDA, RBAC, NetworkPolicy templates |
| - [llm-prompts.md](container-orchestration/llm-prompts.md) | Prompts for K8s design, security review, troubleshooting |
| [quality-attributes/](quality-attributes/) | Quality attributes framework |
| - [README.md](quality-attributes/README.md) | ISO 25010, quality attributes overview, SLI/SLO framework, LLM tips |
| - [checklist.md](quality-attributes/checklist.md) | Step-by-step quality requirements checklist (12 phases) |
| - [examples.md](quality-attributes/examples.md) | E-commerce, analytics, healthcare, API gateway, SaaS examples |
| - [templates.md](quality-attributes/templates.md) | QA scenarios, NFR specs, SLO docs, ATAM, alert templates |
| - [llm-prompts.md](quality-attributes/llm-prompts.md) | Prompts for quality analysis and trade-off decisions |
| [quality-attributes-analysis/](quality-attributes-analysis/) | NFR and quality attribute analysis using ATAM |
| - [README.md](quality-attributes-analysis/README.md) | ATAM methodology, utility trees, scenarios, tactics, stakeholder analysis |
| - [checklist.md](quality-attributes-analysis/checklist.md) | Quick, standard, and full ATAM analysis checklists |
| - [examples.md](quality-attributes-analysis/examples.md) | E-commerce, healthcare, trading, SaaS, IoT analysis examples |
| - [templates.md](quality-attributes-analysis/templates.md) | Scenario, utility tree, ATAM report, NFR spec, SLO templates |
| - [llm-prompts.md](quality-attributes-analysis/llm-prompts.md) | 30+ prompts for LLM-assisted quality analysis |
| [data-pipeline-design/](data-pipeline-design/) | Data pipeline design guide |
| - [README.md](data-pipeline-design/README.md) | ETL/ELT patterns, modern data stack, orchestration tools, Kafka, Spark, dbt |
| - [checklist.md](data-pipeline-design/checklist.md) | Step-by-step pipeline design checklist (10 phases) |
| - [examples.md](data-pipeline-design/examples.md) | E-commerce, fraud detection, SaaS analytics, IoT, ML feature store examples |
| - [templates.md](data-pipeline-design/templates.md) | Airflow DAGs, Kafka configs, Spark jobs, dbt models, Great Expectations |
| - [llm-prompts.md](data-pipeline-design/llm-prompts.md) | Prompts for pipeline design, optimization, troubleshooting |
| [creational-patterns/](creational-patterns/) | Creational design patterns guide |
| - [README.md](creational-patterns/README.md) | Factory, Builder, Singleton, Prototype, DI, Object Pool overview |
| - [checklist.md](creational-patterns/checklist.md) | Pattern selection and implementation checklist |
| - [examples.md](creational-patterns/examples.md) | Python, TypeScript, Go implementations |
| - [templates.md](creational-patterns/templates.md) | Copy-paste pattern templates |
| - [llm-prompts.md](creational-patterns/llm-prompts.md) | Prompts for pattern design and review |
| [behavioral-patterns/](behavioral-patterns/) | Behavioral design patterns guide |
| - [README.md](behavioral-patterns/README.md) | Strategy, Observer, Command, State, CoR, Template Method, Mediator, Iterator, Visitor overview |
| - [checklist.md](behavioral-patterns/checklist.md) | Pattern selection and implementation checklist |
| - [examples.md](behavioral-patterns/examples.md) | Python, TypeScript, Go implementations |
| - [templates.md](behavioral-patterns/templates.md) | Copy-paste pattern templates |
| - [llm-prompts.md](behavioral-patterns/llm-prompts.md) | Prompts for pattern design and review |
| [structural-patterns/](structural-patterns/) | Structural design patterns guide |
| - [README.md](structural-patterns/README.md) | Adapter, Bridge, Composite, Decorator, Facade, Proxy, Flyweight overview |
| - [checklist.md](structural-patterns/checklist.md) | Pattern selection and implementation checklist |
| - [examples.md](structural-patterns/examples.md) | Python, TypeScript, Go implementations |
| - [templates.md](structural-patterns/templates.md) | Copy-paste pattern templates |
| - [llm-prompts.md](structural-patterns/llm-prompts.md) | Prompts for pattern design and review |
| [patterns-overview/](patterns-overview/) | Design patterns overview and quick reference |
| - [README.md](patterns-overview/README.md) | All pattern categories, cloud-native patterns, LLM tips, external resources |
| - [checklist.md](patterns-overview/checklist.md) | Step-by-step pattern selection checklist |
| - [examples.md](patterns-overview/examples.md) | Factory, Builder, Decorator, Strategy, Observer, State, Circuit Breaker, Saga examples |
| - [templates.md](patterns-overview/templates.md) | Copy-paste templates for Python, TypeScript, Go |
| - [llm-prompts.md](patterns-overview/llm-prompts.md) | Prompts for pattern selection, implementation, and review |
| [decision-trees/](decision-trees/) | Architecture decision trees and frameworks |
| - [README.md](decision-trees/README.md) | Decision trees overview, LLM tips, external links (2025-2026 best practices) |
| - [checklist.md](decision-trees/checklist.md) | Step-by-step decision making checklist (6 phases) |
| - [examples.md](decision-trees/examples.md) | E-commerce, SaaS, FinTech, frontend decision examples |
| - [templates.md](decision-trees/templates.md) | Decision tree, matrix, ADR, and TCO templates |
| - [llm-prompts.md](decision-trees/llm-prompts.md) | 20+ prompts for LLM-assisted architecture decisions |
| [workflows/](workflows/) | Architecture workflows guide (2025-2026 best practices) |
| - [README.md](workflows/README.md) | Workflows overview, LLM-assisted design, external resources |
| - [checklist.md](workflows/checklist.md) | Step-by-step checklists for 7 workflow types |
| - [examples.md](workflows/examples.md) | URL shortener, chat system, migration, ATAM examples |
| - [templates.md](workflows/templates.md) | System design, ADR, ATAM, migration planning templates |
| - [llm-prompts.md](workflows/llm-prompts.md) | 50+ prompts for LLM-assisted architecture workflows |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Implements the architecture |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | Implements infrastructure |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Provides product requirements |
| [faion-business-analyst](../faion-business-analyst/CLAUDE.md) | Provides business requirements |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Uses architecture in design docs |
