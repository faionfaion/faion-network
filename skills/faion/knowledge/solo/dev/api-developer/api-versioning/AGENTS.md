# API Versioning

## Summary

Version REST APIs only for breaking semantic changes; additive changes (new field, new optional input, new endpoint) never require a new version. Use URL path versioning (`/api/v1/`) — cacheable, debuggable, unambiguous. Support N and N-1 simultaneously; emit `Deprecation`, `Sunset`, and `Link: rel=successor-version` headers from deprecated routes; measure per-version traffic before sunsetting.

## Why

Maintaining 3+ active major versions is exponentially expensive. Header/Accept-version routing breaks CDN cache keys. Without `oasdiff` in CI, breaking changes ship undetected. Without measured traffic before sunset, v1 removal strands real clients — enforce sunset with 410 Gone responses, not blog posts.

## When To Use

- Public APIs with external consumers you cannot redeploy in lockstep (partners, mobile apps)
- Major contract changes: renamed/removed fields, changed types, new required inputs
- Two-team handoffs where producer ships ahead of consumers
- Long-tail clients (mobile apps from 2 years ago still hitting prod)

## When NOT To Use

- Internal-only API with one consumer redeployed atomically — additive fields beat versions
- Additive changes (new field, new endpoint, new optional input) — never a new version
- GraphQL APIs — use `@deprecated` + field evolution + persisted queries instead
- After-the-fact for breaking changes already merged — that is a hotfix, not a `/v2`

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategies.xml` | Versioning strategy comparison, URL path implementation, header versioning |
| `content/02-deprecation.xml` | Deprecation/Sunset headers, response warnings, oasdiff CI gate, sunset lifecycle |

## Templates

| File | Purpose |
|------|---------|
| `templates/versioned_router.py` | FastAPI v1/v2 router setup with prefix separation |
| `templates/oasdiff-ci.sh` | CI breaking-change gate: oasdiff diff + changelog-pending enforcement |

## Scripts

none
