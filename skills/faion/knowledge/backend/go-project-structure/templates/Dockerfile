# purpose: Multi-stage distroless Dockerfile for Go services
# consumes: Go source + go.mod
# produces: distroless OCI image
# depends-on: scripts/validate-go-project-structure.py
# token-budget-impact: ~200 tokens
# Multi-stage distroless Dockerfile for Go services.
# Build stage
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

# The build context is filtered by the .dockerignore beside this file. Without
# it this line bakes .env, private keys and the whole .git history into a
# pushed image, and `docker history` reads them back out of the layer — a
# later RUN rm does not remove them.
COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/api

# Runtime stage — distroless for minimal attack surface
FROM gcr.io/distroless/static-debian12

WORKDIR /app

COPY --from=builder /app/server .

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/app/server"]
