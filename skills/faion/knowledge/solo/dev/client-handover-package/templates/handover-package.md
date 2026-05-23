<!--
purpose: Handover-package skeleton authors fill at engagement end.
consumes: scope record, runbook fragments, credentials, open items.
produces: package ready for the validator + dual sign-off.
depends-on: rotated credentials; named successor.
token-budget-impact: ~250 tokens when copied.
-->

# Handover package — &lt;client&gt; — &lt;engagement_end&gt;

## 1. Scope summary
What was delivered, in 3–5 sentences. Reference the engagement contract.

## 2. Runbook
- **Start:** exact commands.
- **Stop:** exact commands.
- **Debug:** where logs live, how to read them, top 5 known failure modes.

## 3. Architecture
- Diagram (link to docs/architecture.png).
- Services + ports.
- External integrations (APIs, queues, DBs).

## 4. Ops surface
- Dashboards (links).
- Alerts (where they fire, who responds).
- Logs (location, retention).

## 5. Credentials transfer log
| name | vault_path | rotation_date | acknowledged_by | acknowledged_at |
|------|-----------|---------------|------------------|------------------|
|      |           |               |                  |                  |

## 6. Open items
| title | severity | effort | blast_radius | next_step |
|-------|----------|--------|--------------|-----------|
|       | high/med/low | S/M/L | 1/3/5 |       |

## 7. Support window
- Days: 30
- Scope: bug-fixes only / new work not included
- SLA: response within 24h business hours
- Channel: Slack #consultant-handover (or email)
- After window: hourly rate $XXX/h, billed monthly

## Sign-off
- Consultant: &lt;name@email&gt; — &lt;ISO date&gt;
- Client: &lt;name@email&gt; — &lt;ISO date&gt;
