#!/usr/bin/env bash
# deploy-with-rollback.sh — set image, wait for rollout, smoke test, rollback on failure
# Usage: ./scripts/deploy-with-rollback.sh <namespace> <deployment> <image:tag> <smoke-url>
set -euo pipefail

NS="${1:?namespace required}"
DEP="${2:?deployment name required}"
IMAGE="${3:?image:tag required}"
URL="${4:?smoke-url required}"

PREV=$(kubectl -n "$NS" get deploy "$DEP" \
  -o jsonpath='{.spec.template.spec.containers[0].image}')

echo "Deploying $IMAGE (was $PREV)..."
kubectl -n "$NS" set image "deploy/$DEP" "$DEP=$IMAGE"

if ! kubectl -n "$NS" rollout status "deploy/$DEP" --timeout=5m; then
  echo "Rollout failed — reverting to $PREV"
  kubectl -n "$NS" rollout undo "deploy/$DEP"
  kubectl -n "$NS" rollout status "deploy/$DEP" --timeout=5m
  exit 1
fi

echo "Running smoke test against $URL..."
if ! curl -fsS --max-time 10 --retry 6 --retry-delay 5 "$URL/health/ready" >/dev/null; then
  echo "Smoke failed — reverting to $PREV"
  kubectl -n "$NS" set image "deploy/$DEP" "$DEP=$PREV"
  kubectl -n "$NS" rollout status "deploy/$DEP" --timeout=5m
  exit 1
fi

echo "Deploy OK: $IMAGE"
