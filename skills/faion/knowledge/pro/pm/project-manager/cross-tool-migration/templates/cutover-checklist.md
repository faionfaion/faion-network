# Migration Cutover Checklist

## T-24 Hours
- [ ] Final data export from source — stored in git
- [ ] Backup target environment
- [ ] Notify all users of timeline and read-only window
- [ ] Prepare support team and on-call schedule
- [ ] Disable target-side automations (Slack notifs, escalations, CI hooks)

## T-4 Hours (Source Goes Read-Only)
- [ ] Set source tool to read-only — confirm with admin
- [ ] Communicate read-only start to all users
- [ ] Run final migration sync
- [ ] Validate issue counts (source count = target count)
- [ ] Test critical integrations end-to-end

## T-0 (Human Declares Go-Live — No Auto-Cutover)
- [ ] Human-typed confirmation received: [project key or token]
- [ ] Enable target tool for all users
- [ ] Send go-live announcement (all channels)
- [ ] Support team on standby
- [ ] Monitor for errors

## T+1 Hour
- [ ] Check user login success across all roles
- [ ] Verify automations running in target
- [ ] Address immediate blockers
- [ ] Update status to stakeholders

## T+24 Hours
- [ ] Review error logs
- [ ] Collect user feedback
- [ ] Document known issues with severity
- [ ] Plan immediate remediation

## T+1 Week
- [ ] User adoption metrics: [target over 80%]
- [ ] Complete any missing migrations (edge cases)
- [ ] Conduct migration retrospective
- [ ] Schedule source decommission review (no earlier than T+30 days)

## T+30 Days
- [ ] Confirm no team has needed source for 2 weeks
- [ ] Plan source decommission (human approval required before delete)
