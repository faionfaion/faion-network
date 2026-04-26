# Agent Integration — Grafana Setup & Provisioning

## When to use
- Standing up a new Grafana stack (Docker Compose dev, Kubernetes Helm prod, or HA on VMs).
- Migrating off Grafana Agent (EOL 2025-11-01) to Grafana Alloy.
- Codifying datasources, dashboards, alert rules, and contact points as files in Git (provisioning).
- Setting up HA with shared PostgreSQL/MySQL behind a load balancer.
- Bootstrapping the kube-prometheus-stack / k8s-monitoring 2.0 chart and tuning it.
- Hardening: HTTPS, OIDC/SAML, RBAC, secrets, audit logging.

## When NOT to use
- Single-user lab / quick demo — `docker run grafana/grafana` is enough; provisioning overhead is wasted.
- When you can use Grafana Cloud (free tier covers most solo workloads) — managed beats self-hosted ops.
- For pure log search where Kibana/OpenSearch dashboards are already entrenched.
- As a CI dashboard tool (use the CI vendor's native UI for run history; Grafana adds latency).

## Where it fails / limitations
- Grafana Agent → Alloy migration silently changes config syntax (River vs YAML) and metric names (`agent_*` → `alloy_*`); agents copy old configs and dashboards break.
- Helm chart values schema changes between minor versions; pinning the chart but not reviewing release notes leads to "deploy succeeds, alerts disappear".
- Provisioning + UI-edited objects collide: a UI-edited dashboard reverts on next reconcile; agents that "fix dashboards in UI" lose changes.
- HA needs shared storage for plugins, image rendering, and alerting state — without shared storage, alerts duplicate or vanish across replicas.
- SQLite is fine for single node; agents leave it on for HA and lose data on schema migration.
- Image renderer (PDF/PNG export) is a separate service with chrome dependencies; provisioning forgets it and "send PDF report" silently fails.
- LDAP/SAML/OIDC: each has separate provisioning files and gotchas (group_search_base_dns, attribute mappings). Agents copy a half-config and authentication breaks for one IdP edge case.
- Mimir/Loki/Tempo + Grafana stack: the integration of multiple charts is fragile across versions. Use the umbrella `k8s-monitoring` chart (2.0+) when possible.
- `admin_password` env var is honored only on first start; rotating after install requires CLI reset, not env change.

## Agentic workflow
Provisioning is the cornerstone — everything in Git, deploys via Helm/values + ConfigMaps. One agent generates the Helm values + provisioning ConfigMaps from a template (org name, OIDC issuer, datasources, alerting contact points). A reviewer agent (Opus) checks: (1) HA preconditions (DB, replicas, session cache), (2) Alloy not Agent, (3) provisioning paths mounted, (4) admin password from secret not literal, (5) `serve_from_sub_path` consistency with ingress. A deploy agent runs `helm upgrade --install` with `--atomic --timeout 5m`; on success runs smoke tests (`/api/health`, sample dashboard render).

### Recommended subagents
- `faion-sdd-executor-agent` — drives Helm/values PRs through quality gates.
- A custom `grafana-provisioning-validator` (Opus, read-only) — given values + provisioning ConfigMaps, checks UI-edit risk, datasource UID stability, alert rule schema, contact point references, version compatibility (chart vs Grafana vs Alloy).
- `password-scrubber-agent` — Helm values often inline OIDC client secrets, SMTP passwords, S3 keys for image renderer.

### Prompt pattern
```
Generate Helm values for grafana/grafana on Kubernetes.
Inputs: replicas, persistence (PVC size, storageClass), DB (postgres host/db/secret), OIDC config, ingress host + cert, smtp config, datasources list (Prometheus/Loki/Tempo URLs).
Output: (1) values.yaml, (2) provisioning ConfigMaps (datasources/, dashboards/, alerting/), (3) sealed-secret stubs, (4) NetworkPolicy, (5) post-install smoke tests.
Forbid: SQLite for replicas>1, admin password literal, Grafana Agent (use Alloy), `serve_from_sub_path: true` without `root_url`, datasource without UID.
```

```
Validate values.yaml + provisioning ConfigMaps. JSON: {ha_safe:bool, agent_uses_alloy:bool, secrets_externalized:bool, datasource_uids_stable:bool, dashboards_provisioned:bool, blockers:[]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `helm` | Install/upgrade Grafana + stacks | https://helm.sh/docs/ |
| `helm diff` plugin | Preview chart changes | https://github.com/databus23/helm-diff |
| `kubectl` + `kustomize` | Inspect/patch manifests | https://kubernetes.io/docs/reference/kubectl/ |
| `grafana-cli` | Plugin install, admin reset | https://grafana.com/docs/grafana/latest/cli/ |
| `grizzly` (`grr`) | kubectl-like for Grafana resources | https://grafana.github.io/grizzly/ |
| `alloy` (CLI) | Alloy config validate/run | https://grafana.com/docs/alloy/latest/reference/cli/ |
| `mimirtool` / `cortextool` | Validate rules, dashboards, alertmanager configs | https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/ |
| `lokitool` | Loki config & rule validate | https://grafana.com/docs/loki/latest/manage/tools/lokitool/ |
| `prom-client` / `promtool` | Validate scrape configs / rules | https://prometheus.io/ |
| `kube-prometheus-stack` chart docs | Companion stack | https://github.com/prometheus-community/helm-charts |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Grafana OSS | OSS | Yes | Self-host, full provisioning surface. |
| Grafana Cloud | SaaS | Yes | Free tier; tokens with stack scope. |
| Grafana Enterprise | Commercial | Yes | RBAC, reporting, data source permissions, SSO. |
| Grafana Alloy | OSS | Yes | Replaces Grafana Agent (EOL 2025-11). |
| Mimir / Cortex / Thanos | OSS | Yes | Long-term Prometheus storage. |
| Loki | OSS / SaaS | Yes | LogQL; same provisioning model. |
| Tempo | OSS / SaaS | Yes | Trace backend; agent must wire `derivedFields` for trace links. |
| Pyroscope | OSS / SaaS | Yes | Continuous profiling. |
| OnCall (Grafana) | SaaS / OSS | Yes | Alert routing + on-call. |
| k8s-monitoring Helm chart 2.0 | OSS | Yes | Umbrella stack: Grafana + Alloy + Loki + Tempo + Mimir presets. |

## Templates & scripts
See `templates.md` for full Helm values + ConfigMap + Compose. Inline minimal `values.yaml` for HA prod (≤40 lines):

```yaml
# helm install grafana grafana/grafana -f values.yaml
replicas: 2
admin:
  existingSecret: grafana-admin
  userKey: admin-user
  passwordKey: admin-password
persistence:
  enabled: true
  storageClassName: standard
  size: 10Gi
grafana.ini:
  server:
    root_url: "https://grafana.example.com"
  database:
    type: postgres
    host: pg.example.com:5432
    name: grafana
    user: grafana
  remote_cache:
    type: redis
    connstr: addr=redis.example.com:6379
  auth.generic_oauth:
    enabled: true
    name: SSO
    client_id: ${OIDC_CLIENT_ID}
    client_secret: ${OIDC_CLIENT_SECRET}
    auth_url: https://idp.example.com/oauth2/authorize
    token_url: https://idp.example.com/oauth2/token
    api_url: https://idp.example.com/userinfo
    role_attribute_path: contains(groups[*], 'grafana-admin') && 'Admin' || 'Viewer'
envFromSecret: grafana-oidc
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
      - { name: Prometheus, uid: prom, type: prometheus, url: http://prometheus:9090, isDefault: true, jsonData: { timeInterval: 15s } }
      - { name: Loki,       uid: loki, type: loki,       url: http://loki:3100,       jsonData: { maxLines: 1000 } }
ingress:
  enabled: true
  hosts: [ grafana.example.com ]
  tls: [ { secretName: grafana-tls, hosts: [grafana.example.com] } ]
serviceMonitor:
  enabled: true
```

## Best practices
- Pin `chart.version` and `image.tag`; review release notes on every bump (Grafana minor versions change provisioning schemas).
- Externalize secrets (Sealed Secrets / External Secrets / SOPS) — never inline OIDC, SMTP, DB creds in values.yaml.
- Stable UIDs on every datasource, dashboard, alert rule, contact point — references break otherwise.
- Disable UI editing of provisioned objects (`allowUiUpdates: false`) to prevent drift; force PRs.
- Use the `k8s-monitoring` Helm chart (2.0+) over individual stacks when possible; less glue to maintain.
- Image renderer as a separate Deployment with proper resource limits; otherwise PDFs eat all memory.
- `/metrics` and `/api/health` scraped by your own Prometheus — meta-monitoring is non-negotiable.
- Backups: PostgreSQL DB + provisioning Git + plugins PVC (if used). Test restore quarterly.
- Audit log to a long-term sink (S3/Loki); audit logs in Grafana itself defeats the point.
- Reverse proxy with `serve_from_sub_path: true` only when actually under a subpath; misconfiguration breaks all asset URLs.

## AI-agent gotchas
- Agents reach for Grafana Agent or Promtail in tutorials; both deprecated for new installs in favor of Alloy. Force Alloy in templates.
- HA without shared DB: agents start `replicas: 2` with default SQLite; one replica handles writes, the other reads stale data. Always switch DB type before scaling.
- Plugin install via env (`GF_INSTALL_PLUGINS`) downloads at boot; in air-gapped envs this fails silently. Use a custom image with plugins baked in.
- Provisioning paths: `/etc/grafana/provisioning/{datasources,dashboards,alerting,plugins,notifiers}` — agents put files in wrong subdir and Grafana ignores them silently (warning at INFO, not WARN).
- Dashboards as JSON without `uid` get a fresh UID per pod and dashboards multiply.
- Alert rule provisioning conflicts with UI-edited rules — Grafana 10.x onwards requires `disableProvision` flag awareness; agents miss it.
- OIDC `role_attribute_path` (JMESPath) confuses LLMs; they generate invalid expressions and everyone becomes Viewer or Admin. Test in `Settings → Test`.
- LLMs forget that Grafana 11+ default unified alerting is on; legacy alerting docs lead them astray.
- Image renderer needs egress to internet for self-checks unless explicitly configured `RENDERING_VERIFICATION_DISABLED=true`.
- Human-in-loop checkpoint: any change to OIDC, RBAC, alerting routing, or admin password must go through human review with staged rollout.
- Anonymous access: agents enable for "easy demos" then forget to disable; production exposure follows.

## References
- Grafana docs (admin) — https://grafana.com/docs/grafana/latest/setup-grafana/
- Provisioning — https://grafana.com/docs/grafana/latest/administration/provisioning/
- Helm chart — https://github.com/grafana/helm-charts
- HA setup — https://grafana.com/docs/grafana/latest/setup-grafana/set-up-for-high-availability/
- Grafana Alloy — https://grafana.com/docs/alloy/latest/
- Agent → Alloy migration — https://grafana.com/docs/alloy/latest/tasks/migrate/
- k8s-monitoring chart 2.0 — https://grafana.com/blog/2025/01/23/kubernetes-monitoring-helm-chart-2.0
- Mimirtool — https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/
- Grizzly — https://grafana.github.io/grizzly/
