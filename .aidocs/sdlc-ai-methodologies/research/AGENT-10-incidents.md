# AGENT-10: Incident Response with AI Agents

**Summary:** Playbook-driven SRE/oncall agents that consume runbook-as-code, triage alerts, run safe read-only investigations, gate destructive actions behind human approval, and auto-draft postmortems.
By April 2026 the field has converged on: read-only-by-default agents, runbook-as-markdown, signed audit trails, and tier-based approval gates (restart=auto, delete=human).

---

## inc-001 — Runbook-as-Markdown consumed by agent

**Rule:** Author runbooks as Markdown files in the project repo (`runbooks/<alert-name>.md`). The agent fetches the runbook for the firing alert, parses sections (Symptoms / Diagnostics / Remediation / Escalation), and executes only the steps tagged `<!-- agent:auto -->`. Steps tagged `<!-- agent:approval -->` require human OK.

**URL:** https://incident.io/blog/automated-runbook-guide ; https://github.com/kjkuan/Runbook.md

**When to use:** Any team with >10 alert types and stable architecture. Markdown gives writers freedom + agent-readable structure.
**When NOT:** Throwaway alerts, one-off diagnostics — overhead not worth it. Pure-code runbooks (Python) when steps are highly conditional/branching.

**Snippet:**
```markdown
# Runbook: HighDBLatency

## Diagnose <!-- agent:auto -->
- Run: `kubectl top pods -n db`
- Query: prometheus `pg_stat_activity_count{state="active"}`

## Remediate
- [auto] Scale read replicas: `kubectl scale --replicas=+1 sts/pg-replica`
- [approval] Failover primary: `patroni failover` # destructive
```

---

## inc-002 — PagerDuty SRE Agent / AIOps end-to-end

**Rule:** Connect PagerDuty AIOps to your alert sources; enable the SRE Agent on the service. It runs diagnostics + surfaces context automatically; remediation actions require explicit approval per runbook. Pair with Insights Agent for "what changed since last incident".

**URL:** https://www.pagerduty.com/platform/aiops/ ; https://www.pagerduty.com/blog/product/product-launch-2025-h2/

**When to use:** Already on PagerDuty; want managed agent with built-in approval flow + Process Automation runbooks. Customers report up to 50% MTTR reduction.
**When NOT:** Cost-sensitive small teams; heavy custom action requirements (PD's action library is finite).

**Snippet:**
```yaml
# pagerduty service config
sre_agent:
  enabled: true
  mode: diagnose+suggest      # not auto-remediate
  approval_required_for: [restart, scale, failover, delete]
  runbook_source: github://org/runbooks
```

---

## inc-003 — incident.io AI SRE: Slack-native autonomous investigation

**Rule:** Run the AI SRE in Slack-native mode: it auto-joins the incident channel, pulls telemetry + recent code changes + similar past incidents, and posts a working hypothesis within 60s. The bot is read-only by default; it never executes mutations without `/incident approve <action>`.

**URL:** https://incident.io/blog/5-best-ai-powered-incident-management-platforms-2026

**When to use:** Slack-first orgs; want investigation speed without surrendering remediation control.
**When NOT:** Teams without observability/code-change feeds wired in (agent will hallucinate without grounding).

**Snippet:**
```
# Slack channel #inc-1234
@incident-io investigate
> Found: deploy abc123 at 14:02 changed connection pool from 20→5
> Correlated: pg_connections_max alert at 14:04
> Hypothesis: pool exhaustion. Suggest revert. Run `/incident approve revert`?
```

---

## inc-004 — Rootly AI postmortem automation

**Rule:** On incident close, Rootly auto-drafts the postmortem: timeline (from Slack + alerts + deploys), root cause hypothesis, action items extracted from chat. Human edits and publishes — never auto-publish.

**URL:** https://rootly.com/sre/ai-generated-postmortems-transform-outage-data-fast ; https://rootly.com/sre/rootlys-timeline-powers-clear-postmortem-insights

**When to use:** Teams that skip postmortems because writing them is painful. Auto-draft removes 80% of the friction.
**When NOT:** Highly regulated incidents (legal/compliance) where every word needs human authorship from scratch.

**Snippet:**
```yaml
# rootly workflow: on_incident_resolved
trigger: incident.status == resolved
actions:
  - generate_postmortem:
      sections: [summary, timeline, root_cause_hypothesis, action_items]
      tone: blameless
      assignee: incident_commander
      auto_publish: false   # human review required
```

---

## inc-005 — FireHydrant context-aware runbooks via service catalog

**Rule:** Tie every runbook to a service in the FireHydrant catalog. When an incident is declared, the agent fetches the service's runbook + ownership + dependencies, drafts status-page updates and Slack/email comms specific to the affected audience.

**URL:** https://firehydrant.com/runbooks/ ; https://firehydrant.com/ai/

**When to use:** Microservice estates where "which team owns this?" matters as much as "what broke?".
**When NOT:** Monoliths with one team — service-catalog overhead is wasted.

**Snippet:**
```yaml
service: payments-api
owner: team-payments
runbook: runbooks/payments-api.md
ai_actions:
  - draft_status_update
  - draft_internal_summary
  - suggest_similar_incidents
```

---

## inc-006 — Tier-based approval gates (restart=auto, delete=human)

**Rule:** Classify every tool the agent can call into 3 tiers:
- **Tier 0 (auto):** read-only — `kubectl get`, `prom-query`, `log tail`
- **Tier 1 (auto-with-audit):** safe mutations — `restart pod`, `scale +1 replica`, `clear cache`
- **Tier 2 (human-required):** destructive — `delete pvc`, `drop table`, `failover primary`, `terminate node`

Agent must refuse Tier 2 without approval token. Enforced at the MCP/tool layer, not the prompt.

**URL:** https://maniak.io/articles/2026-03-11-human-in-the-loop-kagent/ ; https://particula.tech/blog/ai-agent-production-safety-kiro-incident

**When to use:** Always. This is the core safety pattern after the Kiro incident (AWS production deletion).
**When NOT:** Never skip. Even "dev" environments: data loss is data loss.

**Snippet:**
```python
# tool registry
TOOLS = {
    "kubectl_get":      Tier.AUTO,
    "kubectl_restart":  Tier.AUTO_AUDIT,
    "kubectl_delete":   Tier.HUMAN_REQUIRED,
    "db_drop":          Tier.HUMAN_REQUIRED,
}
def call_tool(name, args, approval_token=None):
    tier = TOOLS[name]
    if tier == Tier.HUMAN_REQUIRED and not verify(approval_token):
        raise PermissionError(f"{name} requires human approval")
```

---

## inc-007 — Auto-rollback on regression metrics (Argo Rollouts)

**Rule:** All deploys go through Argo Rollouts with an `AnalysisTemplate` querying Prometheus/Datadog. Define SLO breach thresholds; if violated during canary, the rollout aborts itself — no agent or human in the loop. Agent only files the incident + posts to Slack.

**URL:** https://argoproj.github.io/rollouts/ ; https://argo-rollouts.readthedocs.io/en/stable/features/analysis/

**When to use:** Any Kubernetes service with measurable SLOs (latency, error rate). The fastest rollback is one that doesn't need humans.
**When NOT:** Stateful migrations (DB schema) — rollback is more dangerous than rolling forward.

**Snippet:**
```yaml
# AnalysisTemplate
metrics:
- name: error-rate
  successCondition: result[0] < 0.01
  failureLimit: 3
  provider:
    prometheus:
      query: |
        sum(rate(http_requests{status=~"5..",svc="api"}[2m]))
        / sum(rate(http_requests{svc="api"}[2m]))
```

---

## inc-008 — Triage agent: classify severity, decide page-or-wait

**Rule:** Front every alert with a classifier agent. Inputs: alert text + recent metrics + deploy history + similar past incidents. Outputs: `{severity: SEV1|SEV2|SEV3, action: page|notify|suppress, reason: ...}`. SEV1 always pages; SEV3 goes to `#alerts-noisy`. Misclassification feedback loops into prompt.

**URL:** https://stackgen.com/blog/how-to-automate-alert-triage-with-ai-sres ; https://thehackernews.com/2025/09/how-to-automate-alert-triage-with-ai.html

**When to use:** Teams with >50 alerts/day, alert fatigue. Cuts noise 60-80% in published case studies.
**When NOT:** Low-volume environments — manual triage is fine; AI overhead doesn't pay back.

**Snippet:**
```python
def triage(alert):
    return llm.classify(
        prompt=TRIAGE_PROMPT,
        alert=alert,
        context={
            "recent_deploys": gh.recent_deploys(svc=alert.service, hours=2),
            "similar": vector_search(alert.title, k=3),
            "current_metrics": prom.query(alert.related_metrics),
        },
        schema=TriageDecision,  # {severity, action, reason}
    )
```

---

## inc-009 — Audit trail: every agent action signed and stored

**Rule:** Every tool invocation by the agent writes an immutable audit record: `{ts, agent_id, incident_id, tool, args, result, approval_token_id, llm_session_id}`. Stored in append-only log (S3 + Object Lock, or audit table with no UPDATE/DELETE grants). Retain ≥1 year for SOC2.

**URL:** https://policylayer.com/blog/soc2-compliance-ai-agents ; https://goteleport.com/blog/ai-agents-soc-2/

**When to use:** Always for production. Required for SOC2/ISO27001/EU AI Act (Aug 2026 deadline for destructive-action approvals).
**When NOT:** Never skip — even internal tools generate audit data; ship it later if the company gets serious about compliance.

**Snippet:**
```python
@audit_log(retention_days=400, immutable=True)
def agent_tool_call(incident_id, tool, args, approval_token=None):
    record = {
        "ts": now_utc(),
        "agent_id": AGENT_ID,
        "incident_id": incident_id,
        "tool": tool,
        "args": redact_secrets(args),
        "approval_token_id": approval_token.id if approval_token else None,
        "llm_session_id": current_session(),
    }
    audit_store.append_signed(record)
    return execute(tool, args)
```

---

## inc-010 — Read-only investigation mode by default (Azure SRE Agent pattern)

**Rule:** Agent boots in `mode=read_only`. It can inspect anything (logs, metrics, configs, code) but cannot mutate. To enter `mode=remediate`, an on-call engineer issues `/agent escalate-trust <incident_id>` with MFA. Trust auto-revokes when incident closes. Permission level > prompt quality.

**URL:** https://techcommunity.microsoft.com/blog/appsonazureblog/autonomous-aks-incident-response-with-azure-sre-agent-from-alert-to-verified-rec/4511343 ; https://www.causely.ai/blog/why-your-ai-sre-agent-is-stuck-on-read-only

**When to use:** First 6 months of agent rollout. Build trust on diagnostics before granting writes.
**When NOT:** Mature setups with proven runbooks may graduate Tier 1 actions to always-auto. Tier 2 stays human-gated forever.

**Snippet:**
```yaml
# k8s rbac for SRE agent
roles:
  - name: sre-agent-readonly      # default
    verbs: [get, list, watch]
    resources: [pods, deploys, services, events, logs]
  - name: sre-agent-remediate     # MFA-elevated, time-boxed (1h)
    verbs: [delete, patch]
    resources: [pods]             # restart only — no PVC, no namespace
```

---

## inc-011 — Status-page auto-update agent (Statuspage / BetterStack)

**Rule:** When an incident is declared SEV1/SEV2 and customer-impacting, the agent posts a draft status update to Statuspage/BetterStack — but in `unpublished` state. Incident commander reviews + clicks publish. Subsequent updates can auto-publish if labelled `routine` (e.g. "investigating continues, no new info"); resolution always needs human.

**URL:** https://betterstack.com/docs/uptime/creating-status-report-and-status-update/ ; https://www.checklyhq.com/blog/status-page-tools/

**When to use:** Customer-facing services with SLA commitments. Removes the "we forgot to update statuspage" failure mode.
**When NOT:** Internal services with no external customers.

**Snippet:**
```python
def on_incident_declared(inc):
    if inc.severity in ("SEV1", "SEV2") and inc.customer_impact:
        statuspage.create_draft(
            title=llm.draft_public_title(inc),
            body=llm.draft_public_body(inc, audience="customer"),
            components=inc.affected_components,
            published=False,  # commander must click publish
        )
```

---

## inc-012 — GameDay / chaos automation via MCP

**Rule:** Wire LitmusChaos (or Chaos Mesh) to MCP so the agent can trigger chaos experiments during scheduled GameDays. Agent reads the GameDay plan (`gameday-2026-q2.md`), runs experiments, observes detection/response, fills out the gap report. Quarterly cadence; never on production without paging on-call first.

**URL:** https://litmuschaos.io/ ; https://github.com/litmuschaos/litmus

**When to use:** Mature SRE orgs running quarterly GameDays. Agentifying turns 1-day exercise into 4 hours.
**When NOT:** Pre-resilience teams — chaos when you don't have monitoring/runbooks just creates real incidents.

**Snippet:**
```markdown
# gameday-2026-q2.md
## Experiment 1: pod-delete on payments-api
- agent: trigger litmus pod-delete, count=3, interval=30s
- expect: PagerDuty alert fires within 90s, runbook auto-engaged
- pass_criteria: MTTD < 2min, MTTR < 10min, no customer SLO breach
- on_fail: file gap ticket, link to runbook
```

---

## kb-001 — Project KB integration: agent reads architecture before acting

**Rule:** Maintain a `docs/architecture/` Markdown KB indexed in a vector store. On incident open, agent queries KB with `{service, alert_type, error_text}` to fetch: architecture diagram, dependency map, known-failure-modes. KB facts ground the LLM and reduce hallucination ~40% in published agentic-RAG benchmarks.

**URL:** https://www.ibm.com/think/topics/agentic-rag ; https://weaviate.io/blog/what-is-agentic-rag

**When to use:** Always. Without grounding, the agent invents plausible-but-wrong remediations. Update KB on every postmortem.
**When NOT:** Never skip. If you don't have KB, build the minimum: 1 page per service with deps + known issues.

**Snippet:**
```python
def gather_context(incident):
    kb_chunks = vector_db.query(
        f"{incident.service} {incident.alert_type}",
        k=5,
        filter={"namespace": "architecture"},
    )
    return {
        "arch": kb_chunks,
        "recent_changes": git.log(svc=incident.service, since="24h"),
        "similar_incidents": pm_db.similar(incident.title, k=3),
    }
```

---

## gov-001 — Approval token = signed JWT with TTL + scope

**Rule:** Human approval is not a Slack thumbs-up. It's a cryptographically signed token: `{sub: user@org, scope: [tool=kubectl_delete, target=pod/foo], iat, exp:5min, incident_id}`. Token verified at tool-call time, single-use, audit-logged. Slack reactji can *initiate* the approval, but the token comes from a signed callback.

**URL:** https://techcommunity.microsoft.com/blog/linuxandopensourceblog/agent-governance-toolkit-architecture-deep-dive-policy-engines-trust-and-sre-for/4510105

**When to use:** Anywhere agent can perform Tier 1+ actions. Replaces "did Bob really approve this?" with cryptographic proof.
**When NOT:** Pure read-only agents (no writes, no token needed).

**Snippet:**
```python
def request_approval(incident, tool, target):
    approval_url = f"https://approve.faion.net/{incident.id}"
    slack.post(channel=incident.channel,
               text=f"Approve `{tool}` on `{target}`? {approval_url}")
    token = wait_for_signed_callback(timeout=300)
    return verify_jwt(token, scope={"tool": tool, "target": target})
```

---

# Cross-cutting principles (April 2026 consensus)

1. **Read-only by default.** Permission level is the safety, not the prompt.
2. **Tiered tools.** Tier 0 auto, Tier 1 auto+audit, Tier 2 human-required. Enforced at tool layer.
3. **Markdown runbooks.** Author for humans, parse for agents. Tag steps `agent:auto` / `agent:approval`.
4. **Audit everything.** Append-only, signed, retained ≥1y. SOC2 + EU AI Act demand it (Aug 2026).
5. **KB-grounded.** Agent reads service architecture + similar incidents before acting. No KB = no agent.
6. **Auto-rollback > auto-remediate.** Argo Rollouts kills bad deploys without an agent; safer than agent intervention.
7. **Postmortem auto-draft, never auto-publish.** Human owns the narrative.
8. **Trust escalates, then auto-revokes.** Time-boxed elevated permissions per incident.
