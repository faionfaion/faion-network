# purpose: multi-stage Dockerfile for Poetry projects — builder exports, final stage runs pip.
# consumes: pyproject.toml + poetry.lock.
# produces: production image without Poetry runtime.
# depends-on: docker, python:3.11-slim base.
# token-budget-impact: ~30 lines.
# Multi-stage Dockerfile for Poetry projects.
# Builder: export requirements.txt. Final: pip install only.
# Never run poetry install in the final stage.

FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install poetry==1.8.5

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "-m", "my_project.main"]
