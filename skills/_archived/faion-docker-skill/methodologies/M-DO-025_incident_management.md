# M-DO-025: Incident Management

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #incidents, #oncall, #sre, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Incidents cause panic and uncoordinated responses. No runbooks mean every incident is unique. Post-mortems are skipped, mistakes repeat.

## Promise

After this methodology, you will handle incidents systematically. Your team will respond quickly with clear procedures and learn from every incident.

## Overview

Incident management includes detection, response, communication, resolution, and post-incident review. SRE practices formalize this process.

---

## Framework

### Step 1: Severity Levels

```
SEV1 - Critical
├── Complete service outage
├── Data breach or security incident
├── Revenue-impacting for all users
├── Response: Immediate, all hands
└── SLA: 15 min acknowledge, 1 hour resolve

SEV2 - Major
├── Partial outage or degradation
├── Major feature broken
├── Significant user impact
├── Response: Immediate, on-call team
└── SLA: 30 min acknowledge, 4 hours resolve

SEV3 - Minor
├── Minor feature issues
├── Limited user impact
├── Workarounds available
├── Response: Business hours
└── SLA: 4 hours acknowledge, 24 hours resolve

SEV4 - Low
├── Cosmetic issues
├── Minor inconvenience
├── No business impact
├── Response: Next sprint
└── SLA: Best effort
```

### Step 2: On-Call Setup

```yaml
# PagerDuty service configuration
services:
  - name: production-api
    escalation_policy:
      - level: 1
        targets:
          - type: user
            id: primary-oncall
        escalation_delay_in_minutes: 15
      - level: 2
        targets:
          - type: user
            id: secondary-oncall
        escalation_delay_in_minutes: 15
      - level: 3
        targets:
          - type: schedule
            id: engineering-managers

schedules:
  - name: primary-oncall
    rotation_type: weekly
    users:
      - alice
      - bob
      - charlie
    start_day: monday
    start_time: "09:00"
```

```hcl
# Terraform PagerDuty
resource "pagerduty_service" "api" {
  name                    = "Production API"
  escalation_policy       = pagerduty_escalation_policy.primary.id
  alert_creation          = "create_alerts_and_incidents"
  auto_resolve_timeout    = 14400
  acknowledgement_timeout = 1800
}

resource "pagerduty_service_integration" "cloudwatch" {
  name    = "CloudWatch"
  type    = "aws_cloudwatch_inbound_integration"
  service = pagerduty_service.api.id
}
```

### Step 3: Runbooks

```markdown
# Runbook: API High Error Rate

## Overview
This runbook addresses high 5xx error rates on the API service.

## Severity
SEV2 if > 5% errors, SEV1 if > 20% errors

## Detection
- Alert: `api-error-rate-high`
- Dashboard: grafana.example.com/d/api-overview

## Investigation

### Step 1: Check Error Distribution
```bash
# Recent errors by endpoint
aws logs filter-log-events \
  --log-group-name /aws/lambda/api \
  --filter-pattern "ERROR" \
  --start-time $(date -d '15 min ago' +%s000)
```

### Step 2: Check Dependencies
- [ ] Database: `SELECT 1` on RDS
- [ ] Redis: `redis-cli ping`
- [ ] External APIs: Check status pages

### Step 3: Check Recent Deployments
```bash
# Recent deployments
aws ecs describe-services --cluster prod --services api \
  | jq '.services[0].deployments'
```

## Resolution

### Quick Fixes
1. **Bad deployment**: Rollback to previous version
2. **Database overload**: Scale up or add read replica
3. **External dependency down**: Enable circuit breaker

### Rollback Procedure
```bash
# Get previous task definition
PREV=$(aws ecs describe-services --cluster prod --services api \
  | jq -r '.services[0].deployments[1].taskDefinition')

# Deploy previous version
aws ecs update-service --cluster prod --service api \
  --task-definition $PREV
```

## Escalation
- SEV1: Page @engineering-lead
- Data issues: Page @database-team
- Security: Page @security-team

## Communication Template
```
[SEV2] API High Error Rate

Status: Investigating
Impact: ~5% of API requests failing
Start time: HH:MM UTC
ETA: Investigating, update in 15 min
```
```

### Step 4: Incident Response Process

```
1. DETECT (0-5 min)
   ├── Alert fires → On-call paged
   ├── Acknowledge alert
   └── Initial assessment

2. TRIAGE (5-15 min)
   ├── Determine severity
   ├── Open incident channel (#inc-YYYYMMDD-desc)
   ├── Assign Incident Commander
   └── Start status page update

3. INVESTIGATE (15-60 min)
   ├── Follow runbook
   ├── Check recent changes
   ├── Gather evidence
   └── Update stakeholders every 15 min

4. MITIGATE
   ├── Apply quick fix/rollback
   ├── Verify resolution
   ├── Monitor for recurrence
   └── Update status page

5. RESOLVE
   ├── Confirm stable
   ├── Close incident
   ├── Update status page
   └── Schedule post-mortem

6. POST-MORTEM (within 48h)
   ├── Write incident review
   ├── Identify root cause
   ├── Define action items
   └── Share learnings
```

### Step 5: Communication Templates

```markdown
## Initial Notification
**Subject:** [SEV2] Payment Processing Delayed

We are aware of an issue affecting payment processing.

- **Status:** Investigating
- **Impact:** ~10% of payments experiencing delays
- **Start time:** 14:30 UTC
- **Next update:** 15:00 UTC

---

## Update Template
**Subject:** [UPDATE] Payment Processing - Identified

We have identified the root cause.

- **Status:** Identified
- **Root cause:** Database connection pool exhaustion
- **Mitigation:** Scaling database connections
- **ETA:** 30 minutes
- **Next update:** 15:30 UTC

---

## Resolution
**Subject:** [RESOLVED] Payment Processing

This incident has been resolved.

- **Duration:** 14:30 - 15:45 UTC (1h 15m)
- **Impact:** ~500 payments delayed by up to 30 minutes
- **Root cause:** Database connection pool exhaustion due to traffic spike
- **Resolution:** Scaled connection pool, added auto-scaling

A post-mortem will be published within 48 hours.
```

### Step 6: Post-Mortem Template

```markdown
# Post-Mortem: Payment Processing Outage

**Date:** 2024-01-15
**Authors:** @alice, @bob
**Status:** Action items in progress

## Summary
Payment processing was delayed for 1h 15m due to database connection pool exhaustion.

## Impact
- Duration: 14:30 - 15:45 UTC
- Users affected: ~500
- Revenue impact: $15,000 delayed (not lost)
- SLO impact: 99.5% availability (target: 99.9%)

## Timeline (UTC)
| Time  | Event |
|-------|-------|
| 14:25 | Traffic spike begins (3x normal) |
| 14:30 | Error rate exceeds 5%, alert fires |
| 14:32 | On-call acknowledges, begins investigation |
| 14:45 | Root cause identified: connection pool |
| 15:00 | Mitigation started: scaling pool |
| 15:30 | Pool scaled, errors decreasing |
| 15:45 | Resolved, monitoring stable |

## Root Cause
Database connection pool was configured with max 50 connections. Traffic spike required 150 connections, causing requests to queue and timeout.

## Contributing Factors
1. Connection pool limit too low
2. No auto-scaling for database connections
3. Missing alert for connection pool utilization

## What Went Well
- Quick detection (5 min)
- Clear runbook for database issues
- Effective communication

## What Went Wrong
- Connection pool wasn't sized for peak traffic
- Took 15 min to identify root cause
- No playbook for traffic spikes

## Action Items
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Increase connection pool to 200 | @alice | 01/16 | Done |
| Add connection pool monitoring | @bob | 01/20 | In progress |
| Add auto-scaling for DB | @charlie | 01/30 | Not started |
| Create traffic spike playbook | @alice | 01/25 | Not started |

## Lessons Learned
- Size connection pools for peak, not average traffic
- Add monitoring for all resource pools
- Test with 3x expected traffic
```

---

## Templates

### Slack Incident Bot Commands

```
/incident create "API high error rate" SEV2
/incident update "Root cause identified, database connection pool"
/incident resolve "Scaled connection pool, monitoring stable"
/incident page @database-team
```

### Status Page Integration

```javascript
// statuspage.io API
async function updateStatus(incidentId, status, message) {
  await fetch(`https://api.statuspage.io/v1/pages/${pageId}/incidents/${incidentId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `OAuth ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      incident: {
        status: status,  // investigating, identified, monitoring, resolved
        body: message,
      },
    }),
  });
}
```

---

## Common Mistakes

1. **No severity levels** - Everything is SEV1
2. **Missing runbooks** - Ad-hoc troubleshooting
3. **No communication** - Stakeholders in dark
4. **Blame culture** - People hide mistakes
5. **Skipping post-mortems** - Same incidents repeat

---

## Checklist

- [ ] Severity levels defined
- [ ] On-call rotation set up
- [ ] Paging system configured
- [ ] Runbooks for common issues
- [ ] Incident response process documented
- [ ] Communication templates ready
- [ ] Status page configured
- [ ] Post-mortem process established

---

## Next Steps

- M-DO-011: Prometheus Monitoring
- M-DO-012: Centralized Logging
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-025 v1.0*
