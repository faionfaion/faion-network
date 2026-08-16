# Vector Database Production Deployment

## Summary

**One-sentence:** Production deployment manifest — Docker Compose for single-node, K8s StatefulSet/Helm for multi-node, managed for hands-off — with persistence, health checks, resource limits, HA, backup, restore drill, and a pre/post-deploy checklist.

**One-paragraph:** Moving from dev to prod requires more than `docker run`. Persistence: bind to durable storage class (EBS gp3, Ceph RBD); resource limits: CPU + memory requests + limits to prevent neighbour kills; HA: ≥3 replicas for Milvus/Weaviate, single replica + snapshots for Qdrant; backup: snapshot to S3 every 24h with 30-day retention + restore drilled quarterly. Output: a versioned `prod-deploy.yaml` + Terraform / Helm values + ops runbook.

**Ефективно для:**

- Self-host команд що готують Qdrant / Weaviate / Milvus у K8s — стандартизує HA + backup discipline.
- Migrations dev → prod — checklist гарантує що persistence + monitoring + security вже на місці.
- DR drills — quarterly restore тест плюс runbook = real recovery confidence.
- Multi-region — Helm values для cross-region replication.

## Applies If (ALL must hold)

- Vector DB choice committed (`vector-databases` decision done)
- Production environment (real users, real data)
- Operational support exists (on-call, monitoring, backups)

## Skip If (ANY kills it)

- Dev / staging — use vector-db-setup-dev
- Fully managed DB (Pinecone) — provider handles ops; just configure tier
- Air-gapped network with manual operations — different methodology

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `cluster-topology.yaml` | YAML | infra (K8s cluster spec) |
| `storage-class-map.yaml` | YAML | available storage tiers |
| `backup-retention-policy.yaml` | YAML | compliance / DR requirements |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | DB chosen |
| `vector-db-setup-dev` | Dev baseline |
| `vector-db-monitoring` | Monitoring stack |
| `vector-db-security` | Security baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: durable persistence, resource limits, HA per DB class, backup + restore drilled, pre+post deploy checklist | 1100 |
| `content/02-output-contract.xml` | essential | prod-deploy.yaml schema | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: ephemeral volume, no limits, single replica without snapshot, untested backup, no rollback | 900 |
| `content/04-procedure.xml` | essential | 6 steps: storage class → resource sizing → HA mode → backup → checklist → ship | 900 |
| `content/05-examples.xml` | essential | Worked example: Qdrant K8s StatefulSet with EBS + daily snapshot | 600 |
| `content/06-decision-tree.xml` | essential | Routes by DB kind + scale → deploy mode (compose / statefulset / managed) | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `helm_values_drafting` | sonnet | Schema synthesis |
| `runbook_drafting` | opus | Cross-system thinking |
| `prod_deploy_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/qdrant-statefulset.yaml` | K8s StatefulSet for Qdrant |
| `templates/backup-cronjob.yaml` | K8s CronJob for snapshot |
| `templates/prod-deploy.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable spec |
| `templates/deploy-checklist.md.j2` | Pre+post deploy checklist |
| `templates/deploy-checklist.md` | Pre+post deploy checklist Generated from `templates/deploy-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-setup-prod.py` | Lint prod-deploy.yaml | Pre-commit |

## Related

- [[vector-databases]] · [[vector-db-setup-dev]] · [[vector-db-monitoring]] · [[vector-db-security]] · [[vector-db-index-tuning]]
- external: [Qdrant K8s](https://github.com/qdrant/qdrant-helm) · [Milvus on K8s](https://milvus.io/docs/install_cluster-helm.md)

## Decision tree

See `content/06-decision-tree.xml`. Routes by DB kind + scale + ops profile to {single-node compose, StatefulSet/Helm, managed}.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/qdrant-statefulset.yaml`

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: qdrant
  namespace: vector-db
spec:
  serviceName: qdrant
  replicas: 1
  selector:
    matchLabels: {app: qdrant}
  template:
    metadata:
      labels: {app: qdrant}
    spec:
      containers:
        - name: qdrant
          image: qdrant/qdrant:v1.10.0   # pinned
          ports:
            - {name: http, containerPort: 6333}
            - {name: grpc, containerPort: 6334}
          resources:
            requests: {cpu: "2", memory: "16Gi"}
            limits: {cpu: "4", memory: "24Gi"}
          volumeMounts:
            - {name: data, mountPath: /qdrant/storage}
          readinessProbe:
            httpGet: {path: /healthz, port: 6333}
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet: {path: /healthz, port: 6333}
            initialDelaySeconds: 30
            periodSeconds: 30
  volumeClaimTemplates:
    - metadata: {name: data}
      spec:
        accessModes: [ReadWriteOnce]
        storageClassName: ebs-gp3
        resources: {requests: {storage: 200Gi}}
```

### `templates/backup-cronjob.yaml`

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: qdrant-snapshot
  namespace: vector-db
spec:
  schedule: "0 3 * * *"
  successfulJobsHistoryLimit: 7
  failedJobsHistoryLimit: 7
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: snapshot
              image: amazon/aws-cli:2.17.0
              command: ["/bin/sh", "-c"]
              args:
                - |
                  curl -fsS -X POST http://qdrant.vector-db.svc.cluster.local:6333/collections/support-kb/snapshots
                  curl -fsS http://qdrant.vector-db.svc.cluster.local:6333/collections/support-kb/snapshots -o snap.tar
                  aws s3 cp snap.tar s3://prod-backups/qdrant-snapshots/$(date +%F).tar
              envFrom:
                - secretRef: {name: aws-creds}
```

### `templates/prod-deploy.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [deploy_mode, storage, resources, ha, backup, checklist]
properties:
  deploy_mode: {type: string, enum: [docker-compose, k8s-statefulset, managed]}
  storage:
    type: object
    required: [class, size_gb, durable]
    properties:
      class: {type: string}
      size_gb: {type: integer, minimum: 1}
      durable: {type: boolean}
  resources:
    type: object
    required: [cpu_request, cpu_limit, memory_request_gb, memory_limit_gb]
  ha:
    type: object
    required: [strategy, replicas]
  backup:
    type: object
    required: [schedule_cron, retention_days, destination, last_restore_drill]
    properties:
      retention_days: {type: integer, minimum: 7}
      last_restore_drill: {type: string, format: date}
  checklist:
    type: object
    required: [pre_deploy_passed, post_deploy_passed]
    properties:
      pre_deploy_passed: {type: boolean}
      post_deploy_passed: {type: boolean}
```

### `templates/_smoke-test.yaml`

```yaml
deploy_mode: k8s-statefulset
storage: {class: ebs-gp3, size_gb: 200, durable: true}
resources: {cpu_request: "2", cpu_limit: "4", memory_request_gb: 16, memory_limit_gb: 24}
ha: {strategy: single-with-snapshot, replicas: 1}
backup:
  schedule_cron: "0 3 * * *"
  retention_days: 30
  destination: "s3://prod-backups/qdrant/"
  last_restore_drill: "2026-04-15"
checklist:
  pre_deploy_passed: true
  post_deploy_passed: true
```
