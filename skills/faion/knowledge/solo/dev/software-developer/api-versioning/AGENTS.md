# API Versioning

## Summary

A methodology for managing breaking changes in HTTP APIs. Use URL path versioning (`/api/v1/`, `/api/v2/`) for public REST APIs. Announce deprecation via `Deprecation`, `Sunset`, and `Link: rel="successor-version"` headers at least 180 days before removal. Classify every change as additive (no bump), behavioral (warn), or breaking (new version). Maintain at least two concurrent versions; implement v(n+1) atop shared services, never by copying v(n) handlers.

## Why

External consumers — mobile apps, B2B SDKs, LLM tool schemas — cannot move in lockstep with your deploys. Without versioning, any breaking change silently breaks clients. Deprecation headers give programmatic notice to API consumers and automated monitors. The shared-service architecture prevents silent behavioral drift between versions.

## When To Use

- Public APIs with external consumers who can't deploy atomically with you
- Mobile apps where old client versions stay in the wild for months
- B2B integrations where SDKs are pinned per customer
- Any breaking change to a stable resource shape, status code, or auth scheme
- LLM tool-use — pin a stable version so the agent's tool schema keeps working

## When NOT To Use

- Internal-only APIs where you control all consumers and can deploy atomically — use expand-then-contract without versions
- Pre-1.0 / pre-launch — commit to v1 only when an external user exists
- Pure additive changes (new optional field, new endpoint) — no version bump needed
- Experimental endpoints behind feature flags — the flag is the version axis

## Content

| File | What's inside |
|------|---------------|
| `content/01-versioning-rules.xml` | Strategy comparison, URL vs header, deprecation header protocol, shared-service rule |
| `content/02-antipatterns.xml` | Copy-paste handlers, missing Deprecation headers, query-param versioning, CDN Vary header |

## Templates

| File | Purpose |
|------|---------|
| `templates/versioning.py` | FastAPI multi-version router with deprecation middleware |
| `templates/spectral-rules.yaml` | Spectral lint rules enforcing version prefix and deprecation headers |
