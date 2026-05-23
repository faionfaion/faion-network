<!-- purpose: Pages deploy report listing project + env + domain + preview evidence. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Cloudflare Pages — Deploy Report

## Project

- name:
- repo:
- production_branch: main
- build_command:
- build_output_dir: public/

## Env vars

| key | env | value (redacted) |
|-----|-----|------------------|
| SENTRY_DSN | production | https://<...>@sentry.io/<...> |
| NEXT_PUBLIC_API | preview | https://api-dev.<...>/v1 |

## Custom domain

- domain:
- cname: <pages.dev target>
- ssl: full_strict

## Preview evidence

- PR #: <url>
- preview_url:

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
