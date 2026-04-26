# Agent Integration — Interface Analysis (Business Analyst angle)

Companion to `pro/ba/ba-modeling/interface-analysis` (which focuses on per-interface
REST/AsyncAPI specs and contract testing). This file covers the **business-analyst
angle**: enterprise integration landscape, cross-system interface inventory, and
API contract governance across many product/IT teams.

## When to use
- Pre-discovery for an enterprise-wide programme (ERP migration, M&A integration, core-system replacement) where the BA must produce a portfolio-level interface inventory before any team writes code.
- Drafting an integration target operating model: which team owns which interface, who approves changes, where the single source of truth lives.
- Building a cross-system traceability matrix from business capabilities → processes → systems → interfaces, used to scope SOWs and impact analysis.
- API contract governance: defining the standards (naming, versioning, deprecation, SLAs, security baseline) that all internal/external interfaces must comply with, and the review cadence.
- Vendor/partner onboarding where a single supplier exposes 20+ interfaces and the BA needs a register, owners, criticality ratings, and renewal dates.
- Producing the IT general controls evidence (SOC2, ISO 27001, GDPR Art. 30, DORA) that lists every system-to-system data flow with PII classification.

## When NOT to use
- A single feature with one external call — the per-interface spec in `ba-modeling/interface-analysis` is enough; do not stand up a governance board.
- Greenfield startup with <5 systems: maintain a one-page integration diagram, skip the formal landscape model.
- Pure technical refactor (e.g., bumping protobuf version) where business capability mapping adds no decision value.
- When the organisation lacks a system-of-record for applications (no APM/CMDB) — first build that, then layer interface inventory on top.

## Where it fails / limitations
- **Inventory rot**: an interface register collected by spreadsheet ages within one quarter; without an automated feed (CMDB + API gateway logs + iPaaS catalogue) the doc becomes a liability.
- **Shadow integrations** (Zapier, Make, manual SFTP scripts on someone's laptop, Excel macros pulling from SharePoint) never make it onto the BA's diagram and cause every audit finding.
- **Capability-to-system mapping** disagrees across Architecture, Finance, and IT — the BA inherits the political fight, not just the modelling task.
- **Governance theatre**: contract review boards approve in hours what teams need to ship in minutes; ungoverned channels appear (slack DMs, untracked dev keys).
- **PII/data-classification** is best-guessed at landscape level; field-level truth lives in the per-interface spec, so the landscape view is structurally lossy.
- LLM agents over-collapse heterogeneous flows ("all integrations are REST") — async/file/EDI/SWIFT/HL7 channels are routinely misclassified.

## Agentic workflow
Run this as a portfolio-scale discovery loop, not a single agent call. Pass 1: a discovery subagent ingests CMDB exports, API gateway access logs, iPaaS (Workato/Boomi/MuleSoft) catalogues, and produces a raw inventory. Pass 2: a BA subagent classifies each interface by business capability, criticality (1–4), data sensitivity (public/internal/confidential/restricted), and ownership; emits the integration landscape register. Pass 3: a governance subagent diffs the register against the enterprise contract standard (naming, versioning, auth, SLA fields) and opens findings. Pass 4: human-in-the-loop review with architecture and security before publication. The orchestrator stores artefacts under `.product/<programme>/landscape/` with stable IDs (`IF-XXX`, `CAP-XXX`, `SYS-XXX`) so other SDD docs can reference them.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the BA discovery task with quality gates; blocks `design.md` until inventory + criticality classification exist.
- `faion-improver` — quarterly audit pass: re-pulls CMDB + iPaaS feeds, diffs against committed register, opens SDD tasks for new/retired interfaces.
- `faion-brainstorm` — diverge/converge on "what integrations exist that nobody documented" (shadow IT discovery workshop simulation).
- Custom `landscape-cartographer` Task agent — given a CMDB export + access logs, returns the filled register template only (no prose).
- `faion-software-architect` knowledge — pulled in for boundary-decision conflicts (where does responsibility for an interface land?).

### Prompt pattern
```
You are an enterprise BA producing an integration landscape register.
Inputs: CMDB export <path>, API gateway access log <path>, iPaaS export <path>.
For each unique source-target pair produce one row matching the register
template at templates.md. Do NOT invent interfaces not present in inputs.
Mark sensitivity as "unknown" if no data-classification tag is found.
Output: register rows in Markdown table, plus a list of suspected shadow
integrations (signals: high traffic, no CMDB entry).
```

```
You are governing API contracts. Diff the register at <path> against the
enterprise standard at <standards.md>. For each non-compliance return:
IF-id, rule violated, severity (block/warn/info), and the minimal remediation.
Cite the standard line number for every finding.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `oasdiff` | Detect breaking OpenAPI changes across portfolio | `go install github.com/oasdiff/oasdiff@latest` |
| `redocly cli` | Lint OpenAPI against an org-wide ruleset | `npm i -g @redocly/cli` |
| `spectral` | Custom governance rules (naming, versioning, auth) on OpenAPI/AsyncAPI | `npm i -g @stoplight/spectral-cli` |
| `apigeectl` / `gcloud apigee` | Pull API proxy inventory from Google Apigee | gcloud SDK |
| `aws apigatewayv2 get-apis` | AWS API Gateway inventory | AWS CLI |
| `az apim api list` | Azure API Management inventory | Azure CLI |
| `kong-cli` / `decK` | Kong gateway config + drift detection | `brew install kong/kong/deck` |
| `mulesoft-cli` (anypoint) | MuleSoft Anypoint Exchange/API Manager inventory | npm |
| `archi` (cli) | ArchiMate models for capability/interface mapping | https://www.archimatetool.com/ |
| `plantuml` / `mermaid-cli` | Generate landscape diagrams from text | `npm i -g @mermaid-js/mermaid-cli` |
| `cmdb-cli` (per vendor: ServiceNow `snow`, BMC `bmc-cli`) | Pull application inventory | vendor docs |
| `gron` / `jq` | Flatten CMDB/API exports for grep + diff | distro pkg |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ServiceNow CMDB | SaaS | Yes (REST + Table API) | Authoritative app/system inventory; agent reads `cmdb_ci_appl` and relations. |
| LeanIX / Ardoq / iServer | SaaS | Yes (REST) | Enterprise architecture; capability-to-system mapping, integration matrix views. |
| Apigee / Kong / AWS API GW / Azure APIM | SaaS+OSS | Yes (REST/CLI) | Gateway = ground truth for active REST traffic; export proxy list as inventory. |
| MuleSoft Anypoint Exchange | SaaS | Yes (REST) | iPaaS interface registry; pulls connectors + flows. |
| Workato / Boomi / Tray.io | SaaS | Partial (REST) | Often hides shadow IT — query for active recipes per system. |
| Postman / Stoplight / Bump.sh | SaaS | Yes (Git or REST) | Portfolio API catalogue with governance rules; Bump.sh good for changelog automation. |
| Pact Broker / PactFlow | SaaS+OSS | Yes (CLI + REST) | Consumer-driven contracts at portfolio scale; can_i_deploy gates. |
| Confluent / Apicurio Registry | SaaS+OSS | Yes (REST) | Schema registry for async (Avro/Protobuf/JSON-Schema). |
| Backstage (Spotify) | OSS | Yes (file + REST) | Service catalogue + TechDocs; agent edits `catalog-info.yaml` per service. |
| OpenLineage / Marquez | OSS | Yes (REST) | Captures actual data-flow events from pipelines (catches shadow batch flows). |
| Microsoft Purview / Collibra / Atlan | SaaS | Yes (REST) | Data catalogues that surface classifications agents need for sensitivity tags. |
| Mendix / OutSystems / Power Platform CoE Kit | SaaS | Partial | Low-code platforms harbour the most shadow interfaces; CoE Kit reports help. |

## Templates & scripts

`templates.md` covers the per-interface specification. Below: an integration
landscape register template (portfolio level) and a tiny script to merge
CMDB + gateway exports into a starter register the BA can refine.

```markdown
# Integration Landscape Register — <Programme / Domain>

| IF-ID | Source SYS | Target SYS | Channel | Data | Direction | Frequency | Criticality (1-4) | Sensitivity | Owner | SLA | Standard? | Notes |
|-------|------------|------------|---------|------|-----------|-----------|-------------------|-------------|-------|-----|-----------|-------|
| IF-001 | CRM        | Billing    | REST    | Customer master | Out | Real-time | 1 | Confidential | Team A | 99.9% | OpenAPI in repo X | replaces legacy SFTP IF-014 |
| IF-002 | HRIS       | IDP        | SCIM    | User accounts | Out | Hourly    | 1 | Restricted   | Team B | 99.5% | yes | scoped to active employees only |
| IF-003 | DWH        | BI         | JDBC    | Sales facts   | Out | Nightly   | 3 | Internal     | Team C | next-day | n/a (read-only) | candidate for retirement |
```

```bash
#!/usr/bin/env bash
# landscape-merge.sh — seed an integration register from CMDB + gateway dumps.
# Inputs: cmdb-apps.json (id,name,owner), gw-apis.json (name,upstream,downstream,traffic).
# Output: register.csv ready for BA enrichment (criticality, sensitivity).
set -euo pipefail
CMDB="${1:?cmdb json required}"; GW="${2:?gateway json required}"; OUT="${3:-register.csv}"

# Build {sys_id -> {name, owner}} index from CMDB
jq -r '.[] | [.id,.name,.owner] | @tsv' "$CMDB" > /tmp/cmdb.tsv

# Emit register rows: IF-id, src, tgt, channel(REST), traffic
awk 'BEGIN{OFS=","; n=0; print "IF-ID,Source,Target,Channel,TrafficPerDay,SourceOwner,TargetOwner,Criticality,Sensitivity,SLA,Notes"}
     NR==FNR{owner[$1]=$3; name[$1]=$2; next}
     {n++; printf "IF-%03d,%s,%s,REST,%s,%s,%s,tbd,unknown,tbd,from-gateway\n",
            n, name[$2], name[$3], $4, owner[$2], owner[$3]}' \
     /tmp/cmdb.tsv <(jq -r '.[] | [.name,.upstream,.downstream,.traffic] | @tsv' "$GW") \
     > "$OUT"

echo "Seeded $(wc -l < "$OUT") rows -> $OUT. BA must fill criticality, sensitivity, SLA."
```

Wire into a quarterly job: re-run, diff against committed `register.csv`,
open SDD tasks for added/removed rows. Shadow IT shows up as gateway traffic
without a matching CMDB owner.

## Best practices
- **Single source of truth per interface**: the OpenAPI/AsyncAPI/Protobuf file in the owning team's repo. The landscape register only references it (link + commit hash), never copies field-level details.
- **Capability-first IDs**: tie every interface to a business capability code (`CAP-FIN-AR-01`) so retirement decisions are made at capability level, not by team.
- **Criticality tiers drive policy**: tier-1 interfaces require contract tests, breaking-change review, and 24/7 monitoring; tier-4 needs only the register row.
- **Standards as code**: encode the API contract standard as Spectral rules and run them in every team's CI; written PDFs alone are ignored.
- **Deprecation calendar**: every interface has a `valid-until` date or "evergreen"; agents scan quarterly and warn on stale ones.
- **Data sensitivity inherited from data catalogue**: do not re-classify at interface level; pull from Purview/Collibra/Atlan.
- **Two views, one register**: capability view for executives (heatmap), technical view for engineers (sequence + auth); generate both from the same register.
- **Active-traffic reality check**: any interface in the register without traffic in the gateway for 90 days → candidate for retirement; any traffic without a register entry → governance violation.
- **Federated governance over central**: a small standards team curates rules; product teams own their interfaces; quarterly review board handles exceptions only.
- **Plain-text artefacts**: register in Markdown/CSV in Git, not in a proprietary EA tool only — agents need to read and diff.

## AI-agent gotchas
- Agents conflate "interface" with "endpoint" — one interface can have many endpoints; force the prompt to use IF-ID = logical contract, not URL path.
- Direction perspective drift: across a portfolio, "inbound" depends on which system you sit at. Anchor each row to source→target, never relative terms.
- Channel misclassification (REST vs RPC vs Webhook vs Event) — require the agent to cite a payload sample or gateway log line per row.
- Capability mapping invented from system names: agents hallucinate capability codes; require a closed list (the org's capability map) as input.
- Sensitivity classification: agents default to "internal" when unsure — instead instruct them to emit `unknown` and surface for human review.
- Owner fields auto-filled from system name pattern guesses; only accept owners present in CMDB output.
- Criticality is a business judgement, not a technical metric — never let the agent set tier-1 without explicit human sign-off.
- Long-tail integrations (EDI X12, SWIFT, HL7 v2, EDIFACT, fixed-width files) get squashed into "file transfer" — preserve the protocol family in a separate column.
- Shadow IT: agents will not find what is not in their inputs. Explicitly task a separate pass against email/Slack/Workato/Power Automate to surface candidates.
- Human-in-the-loop checkpoints: (1) capability-to-system mapping sign-off by Architecture, (2) sensitivity classification confirmed by Data Office, (3) tier-1 criticality approved by business owner, (4) deprecation decisions reviewed before retirement.

## References
- BABOK v3 §10.21 Interface Analysis (IIBA).
- TOGAF 9.2 — Information Systems Architecture / Application Architecture views.
- ArchiMate 3.2 — Application Layer (Application Component, Application Service, Application Interface).
- ISO/IEC 19770-1 (IT Asset Management) and CMDB definition guidance.
- NIST SP 800-95 — Guide to Secure Web Services (interface security baseline).
- DORA (EU 2022/2554) Art. 28 — third-party ICT contractual register.
- GDPR Art. 30 — Records of Processing Activities (data flows across systems).
- "API Governance: A Practical Guide", Erik Wilde — apievangelist.com governance series.
- Spotify Backstage Software Catalog — https://backstage.io/docs/features/software-catalog/
- Spectral rulesets — https://docs.stoplight.io/docs/spectral/
- OpenLineage spec — https://openlineage.io/docs/
