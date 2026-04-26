#!/bin/bash
# cloud-run-deploy.sh — Deploy to Cloud Run with traffic management and WIF auth
# Usage: ./cloud-run-deploy.sh <image-tag> [--traffic 100]
# Requires: gcloud authenticated (CI: OIDC/WIF; local: gcloud auth login)

set -euo pipefail

IMAGE_TAG="${1:?Usage: $0 <image-tag> [--traffic PERCENT]}"
TRAFFIC="${3:-100}"   # default: route 100% traffic to new revision

# Config — override via env vars
PROJECT="${GCP_PROJECT:?GCP_PROJECT required}"
REGION="${GCP_REGION:-us-central1}"
SERVICE="${SERVICE_NAME:?SERVICE_NAME required}"
IMAGE="${IMAGE_REPO:-gcr.io/$PROJECT/$SERVICE}"
SA_EMAIL="${SERVICE_ACCOUNT:?SERVICE_ACCOUNT required}"  # dedicated SA, not default Compute SA

FULL_IMAGE="$IMAGE:$IMAGE_TAG"

# Verify image exists before deploy
if ! gcloud container images describe "$FULL_IMAGE" --project="$PROJECT" &>/dev/null; then
  echo "ERROR: Image not found: $FULL_IMAGE" >&2
  exit 1
fi

echo "Deploying $SERVICE → $FULL_IMAGE (traffic: ${TRAFFIC}%)"

# Deploy new revision (no traffic yet if TRAFFIC < 100)
gcloud run deploy "$SERVICE" \
  --image="$FULL_IMAGE" \
  --project="$PROJECT" \
  --region="$REGION" \
  --service-account="$SA_EMAIL" \
  --platform=managed \
  --no-allow-unauthenticated \          # internal service; use --allow-unauthenticated for public
  --ingress=internal-and-cloud-load-balancing \
  --concurrency=80 \                    # max concurrent requests per instance
  --min-instances=1 \                   # avoid cold starts (cost vs latency tradeoff)
  --max-instances=100 \
  --cpu=1 \
  --memory=512Mi \
  --cpu-throttling \                    # CPU only allocated during request handling (cost saving)
  --timeout=300 \
  --set-env-vars="ENVIRONMENT=production,PROJECT_ID=$PROJECT" \
  --set-secrets="DATABASE_URL=myapp-database-url:latest,API_KEY=myapp-api-key:latest" \
  --execution-environment=gen2 \        # gen2: full Linux compatibility, better performance
  --no-traffic                          # deploy without shifting traffic (canary support)

# Get new revision name
NEW_REVISION=$(gcloud run revisions list \
  --service="$SERVICE" \
  --project="$PROJECT" \
  --region="$REGION" \
  --format="value(name)" \
  --limit=1 \
  --sort-by="~creationTimestamp")

echo "New revision: $NEW_REVISION"

# Health check before shifting traffic
REVISION_URL=$(gcloud run services describe "$SERVICE" \
  --project="$PROJECT" \
  --region="$REGION" \
  --format="value(status.url)")

echo "Running health check..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  "$REVISION_URL/healthz" 2>/dev/null || echo "000")

if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "ERROR: Health check failed (HTTP $HTTP_STATUS). Aborting traffic shift." >&2
  exit 1
fi

echo "Health check passed. Shifting ${TRAFFIC}% traffic to $NEW_REVISION"

# Shift traffic to new revision
gcloud run services update-traffic "$SERVICE" \
  --project="$PROJECT" \
  --region="$REGION" \
  --to-revisions="$NEW_REVISION=$TRAFFIC"

echo "Deploy complete: $SERVICE @ $FULL_IMAGE (${TRAFFIC}% traffic)"
echo "Service URL: $REVISION_URL"
