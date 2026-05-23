<!-- purpose: Minimum viable filled-in Pages deploy report. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Cloudflare Pages — Deploy Report

## Project

- name: faion-net-fe
- repo: faionfaion/faion-net-fe
- production_branch: main
- build_command: npm run build
- build_output_dir: public/

## Env vars

| key | env | value (redacted) |
|-----|-----|------------------|
| SENTRY_DSN | production | https://***@sentry.io/*** |

## Custom domain

- domain: faion.net
- cname: faion-net-fe.pages.dev
- ssl: full_strict

## Preview evidence

- PR #: https://github.com/faionfaion/faion-net-fe/pull/42
- preview_url: https://42.faion-net-fe.pages.dev

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
