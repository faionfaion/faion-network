# Docker Compose

## Overview

Docker Compose defines and runs multi-container Docker applications using YAML configuration. It simplifies development environments, testing, and single-host deployments by orchestrating services, networks, and volumes declaratively.

**Compose version:** 2.39+ (2025) | **Spec version:** 3.9+ or no version field

## When to Use

| Use Case | Fit |
|----------|-----|
| Local development with multiple services | Excellent |
| Integration testing with real dependencies | Excellent |
| Single-host deployments (staging, small prod) | Good |
| CI/CD pipeline testing | Good |
| Prototyping microservices | Good |
| Large-scale production (multi-host) | Use Kubernetes |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Service** | Container configuration (image, ports, env, volumes) |
| **Network** | Communication channel between services |
| **Volume** | Persistent storage shared between containers |
| **Profile** | Group services for selective startup |
| **depends_on** | Service startup order and health dependencies |
| **Override** | Environment-specific configuration layering |
| **Watch** | Live reload for development (2025 feature) |

## 2025-2026 Updates

| Feature | Description |
|---------|-------------|
| No `version:` field | Modern files start directly with `services:` |
| `docker compose watch` | Built-in live reload for development |
| Compose Bridge | Convert to K8s manifests or Helm charts |
| GPU support | Native GPU acceleration for AI/ML workloads |
| Docker Offload | Shift workloads to cloud resources |
| Improved secrets | Better integration with external vaults |

## File Structure

```
project/
├── docker-compose.yml          # Base configuration
├── docker-compose.override.yml # Development overrides (auto-loaded)
├── docker-compose.prod.yml     # Production overrides
├── docker-compose.test.yml     # Testing overrides
├── .env.example                # Environment template
├── .env                        # Actual env (gitignored)
└── Dockerfile                  # Application image
```

## Quick Reference

### Common Commands

```bash
# Start services
docker compose up -d

# Start with profile
docker compose --profile worker up -d

# Start with production config
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Build and start
docker compose up -d --build

# Live development (2025)
docker compose watch

# View logs
docker compose logs -f [service]

# Scale service
docker compose up -d --scale app=3

# Execute command
docker compose exec app python manage.py migrate

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Service Dependencies

```yaml
depends_on:
  db:
    condition: service_healthy    # Wait for health check
  redis:
    condition: service_started    # Just wait for start
  init:
    condition: service_completed_successfully  # One-time init
```

### Network Isolation

```yaml
networks:
  frontend:
    driver: bridge      # External access
  backend:
    driver: bridge
    internal: true      # No external access
```

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment verification |
| [examples.md](examples.md) | Common stack configurations |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for LLM assistance |

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |

---

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices 2026](https://thinksys.com/devops/docker-best-practices/)
- [Modern Docker Best Practices 2025](https://talent500.com/blog/modern-docker-best-practices-2025/)
- [Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/)
