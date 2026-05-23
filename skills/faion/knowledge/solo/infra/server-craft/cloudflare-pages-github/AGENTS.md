---
slug: cloudflare-pages-github
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Connect a GitHub repo to Cloudflare Pages so production-branch pushes deploy to the global CDN and every PR gets a preview URL. Includes build env vars, wrangler local preview, custom domain, branch deploy rules."
content_id: "ea301b0e8ef20ac9"
complexity: medium
produces: report
est_tokens: 6000
tags: [cloudflare, pages, static-site, github, cdn, preview-deploys]
---
# Cloudflare Pages + GitHub

## Summary

**One-sentence:** Connect a GitHub repo to Cloudflare Pages so production-branch pushes deploy to the global CDN and every PR gets a preview URL. Includes build env vars, wrangler local preview, custom domain, branch deploy rules.

**One-paragraph:** Cloudflare Pages turns a static-site repo into a globally CDN-fronted product with zero ops: every production push deploys in ~30 seconds and every PR gets an isolated preview URL for review. This methodology produces a verified Pages deployment report with build settings + env vars + custom-domain mapping + branch rules + preview URL evidence from at least one PR.

## Applies If (ALL must hold)

- Repo is a static-site builder (Gatsby, Astro, Next.js export, Hugo, Eleventy, plain HTML).
- Operator wants per-PR preview URLs without standing up own infra.
- Custom domain is on Cloudflare DNS or can be moved there.

## Skip If (ANY kills it)

- Site needs a long-running server / API surface (Pages is static + Functions only).
- Build > 20 minutes or > 25 MB single file — Cloudflare Pages limits.
- Closed-source repo + Pages free tier requires public or paid plan.

**Ефективно для:**

- Marketing-сайти на Gatsby / Astro з PR-preview-флоу.
- Open-source docs під теплою CDN без власних серверів.
- Команди де PM хоче 'покажи на staging' за 5 хвилин.
- Соло-фаундери що хочуть Pages-функції без Vercel-замку.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/cloudflare-domain-dns` | Custom domain attached to Pages requires DNS already on Cloudflare. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Pages deploy report listing project + env + domain + preview evidence. |
| `templates/_smoke-test.md` | Minimum viable filled-in Pages deploy report. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cloudflare-pages-github.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[cloudflare-domain-dns]]
- [[deploy-scripts]]
- [[git-server-workflow]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
