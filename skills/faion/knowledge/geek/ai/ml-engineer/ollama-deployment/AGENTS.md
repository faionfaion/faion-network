---
slug: ollama-deployment
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production Ollama deployment requires Docker Compose with proper GPU passthrough, volume mounts for model persistence, health checks, nginx reverse proxy with rate limiting and streaming support, and a systemd service for bare-metal installs.
content_id: "61cae8bbdcece36a"
tags: [ollama, docker, deployment, production]
---
# Ollama Production Deployment

## Summary

**One-sentence:** Production Ollama deployment requires Docker Compose with proper GPU passthrough, volume mounts for model persistence, health checks, nginx reverse proxy with rate limiting and streaming support, and a systemd service for bare-metal installs.

**One-paragraph:** Production Ollama deployment requires Docker Compose with proper GPU passthrough, volume mounts for model persistence, health checks, nginx reverse proxy with rate limiting and streaming support, and a systemd service for bare-metal installs. Modelfiles define custom model variants with specific system prompts and generation parameters.

## Applies If (ALL must hold)

- Deploying Ollama as a shared service for multiple applications or users.
- Running Ollama in a containerized environment (Docker, Kubernetes).
- Bare-metal production server where Ollama runs as a background service.
- Exposing Ollama through a reverse proxy with authentication and rate limiting.
- Creating custom model variants with fixed system prompts for specific use cases.

## Skip If (ANY kills it)

- Local development on a single machine — ollama serve directly is simpler.
- One-off batch jobs — Docker overhead is not justified for temporary use.
- Environments without GPU access — CPU-only inference is often better handled by cloud APIs at comparable cost.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
