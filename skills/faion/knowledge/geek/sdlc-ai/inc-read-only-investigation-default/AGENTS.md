# Read-Only Investigation Mode by Default

## Summary

The SRE agent boots with `mode=read_only` and is bound to a `*-readonly` Kubernetes / cloud RBAC role that grants only `get/list/watch/log/describe`. To perform any mutation it must transition to `mode=remediate`, which requires (a) a human-issued `/agent escalate-trust <incident_id>` command, (b) a fresh MFA challenge against the on-caller, and (c) a time-boxed elevated role (default 60 minutes) that auto-revokes when the incident closes or the timer expires. The mode is enforced by RBAC, not by the prompt — a jailbroken or confused agent that "decides" to mutate cannot, because its credentials forbid it. This is the Azure SRE Agent / Causely pattern that became the consensus floor in 2026.

## Why

Privilege is the only durable safety. Prompt-level instructions ("be careful with deletes") are routinely bypassed by chained tool calls, persona drift, or jailbreaks; RBAC-bound credentials are not. Booting read-only also matches how organizations build trust in any new operator: ship the diagnostic value first, prove it stable for months, then graduate specific T1 actions to always-on. Time-boxed escalation closes the most common postmortem finding — "the agent still had write creds days after the incident closed". The MFA step weds the elevation to a specific human at a specific moment, which is the audit-friendly form regulators (SOC2, EU AI Act Aug 2026) expect.

## When To Use

- First 6–12 months of any production agent rollout.
- Any environment where a misfired mutation costs more than a delayed remediation.
- Multi-tenant clusters where blast radius can cross customer boundaries.
- Compliance regimes that demand "least privilege by default" (SOC2 CC6.3, ISO 27001 A.9.2.3).

## When NOT To Use

- Pre-production / sandbox clusters with no real data and full reset capability — friction without payoff.
- Mature setups where specific T1 actions (`restart pod`) have run thousands of times safely and graduate to always-on. T2 stays gated forever.
- Single-developer toolchains where there is no separation of duties to enforce.

## Content

| File | What's inside |
|------|---------------|
| `content/01-default-readonly-rbac.xml` | RBAC binding rule; agent identity; role separation; audit. |
| `content/02-time-boxed-escalation.xml` | `/agent escalate-trust` flow; MFA; auto-revoke on incident close or timer. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sre-agent-rbac.yaml` | Two Kubernetes Roles + RoleBindings (readonly default + remediate ephemeral). |
| `templates/escalate_trust.py` | Reference escalation handler that flips the binding and schedules revoke. |
