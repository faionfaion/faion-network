# Python Web Frameworks

## Summary

A routing-layer methodology for choosing between Django, FastAPI, and Flask. Lock the choice in `constitution.md` before writing any code — do not let agents switch frameworks mid-feature. Use this methodology only for the framework decision; once the choice is made, load the framework-specific methodology (`python-fastapi`, `django-models`, etc.) and skip this one.

## Why

The three frameworks serve distinct needs: Django for full-stack apps with admin panels and ORM, FastAPI for high-concurrency async APIs and ML serving, Flask for small tools and prototypes. Picking the wrong framework is expensive to reverse. Mixing idioms (`@app.route` in FastAPI, `User.objects` in FastAPI routes) is a common LLM failure mode that a locked framework choice prevents.

## When To Use

- Greenfield Python web project where framework choice is still open
- Migration planning: comparing an existing Flask/Django app against FastAPI
- "Hybrid" review: FastAPI for public APIs + Django for admin sharing a DB schema
- Tech-debt audit: deciding if a Flask app has outgrown its minimalism
- Onboarding: routing "where do I add X?" to the right framework's conventions

## When NOT To Use

- Single-framework codebase where team has already committed — load only that framework's specific methodology
- Choosing between Litestar/Sanic/Quart/Starlette — this methodology covers only Django/FastAPI/Flask
- Non-web Python work (ML batch jobs, scripts, CLIs) — wrong abstraction layer
- Performance-critical pure async scenarios where FastAPI is already chosen

## Content

| File | What's inside |
|------|---------------|
| `content/01-decision-matrix.xml` | Framework comparison table, when to choose each, decision rules |
| `content/02-async-and-hybrid.xml` | Async support depth per framework, FastAPI+Django hybrid pattern, deployment commands |
| `content/03-antipatterns.xml` | Mixing idioms, deprecated lifecycle hooks, unsourced benchmarks, LLM gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/pick-framework.sh` | Keyword-scoring script: reads a project brief, outputs framework choice as JSON |
