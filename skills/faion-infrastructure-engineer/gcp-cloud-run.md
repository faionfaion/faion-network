---
name: faion-gcp-cloud-run-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# GCP Cloud Run & Serverless

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Cloud Functions

### Function Deployment

```bash
# Deploy HTTP function (Python)
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=main \
    --trigger-http \
    --allow-unauthenticated

# Deploy with environment variables
gcloud functions deploy my-function \
    --gen2 \
    --runtime=nodejs20 \
    --region=us-central1 \
    --source=. \
    --entry-point=handler \
    --trigger-http \
    --set-env-vars=API_KEY=xxx,DEBUG=true

# Deploy with secrets
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=main \
    --trigger-http \
    --set-secrets=API_KEY=my-secret:latest

# Deploy event-triggered function (Pub/Sub)
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=process_message \
    --trigger-topic=my-topic

# Deploy with Cloud Storage trigger
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=process_file \
    --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
    --trigger-event-filters="bucket=my-bucket"
```

### Function Management

```bash
# List functions
gcloud functions list

# Describe function
gcloud functions describe my-function --region=us-central1

# Call function (HTTP)
gcloud functions call my-function \
    --region=us-central1 \
    --data='{"name": "World"}'

# View logs
gcloud functions logs read my-function --region=us-central1

# Delete function
gcloud functions delete my-function --region=us-central1
```

## Cloud Run

### Service Deployment

```bash
# Deploy from source (builds container automatically)
gcloud run deploy my-service \
    --source=. \
    --region=us-central1 \
    --allow-unauthenticated

# Deploy from container image
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated

# Deploy with environment variables
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --set-env-vars=DATABASE_URL=xxx,API_KEY=yyy

# Deploy with secrets
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --set-secrets=API_KEY=my-secret:latest

# Deploy with resource limits
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --memory=2Gi \
    --cpu=2 \
    --concurrency=100 \
    --max-instances=10 \
    --min-instances=1
```

### Service Management

```bash
# List services
gcloud run services list

# Describe service
gcloud run services describe my-service --region=us-central1

# Get service URL
gcloud run services describe my-service \
    --region=us-central1 \
    --format='value(status.url)'

# Update service
gcloud run services update my-service \
    --region=us-central1 \
    --memory=4Gi

# Delete service
gcloud run services delete my-service --region=us-central1
```

### Traffic Management

```bash
# Deploy new revision
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:v2 \
    --region=us-central1 \
    --tag=v2 \
    --no-traffic

# Split traffic (blue-green)
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-revisions=my-service-00001=50,my-service-00002=50

# Route all traffic to latest
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-latest
```

## Common Patterns

### Blue-Green Deployment

```bash
# Deploy to green (no traffic)
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:v2 \
    --region=us-central1 \
    --no-traffic \
    --tag=green

# Test green deployment
curl https://green---my-app-xxxx.run.app

# Shift traffic
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=green=100
```

---

*GCP Cloud Run & Serverless Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*

## Sources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Deploying to Cloud Run](https://cloud.google.com/run/docs/quickstarts/deploy-container)
- [Cloud Run Service Identity](https://cloud.google.com/run/docs/securing/service-identity)
