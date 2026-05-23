# Automation: [Name]

## Purpose
[One sentence: what this automation does and why it replaces the manual process]

## Trigger
- Event: [what starts it — form submit, payment, cron schedule, API webhook]
- Source: [which tool or service fires the trigger]

## Workflow Steps
1. [Step 1 — specific action with tool name]
2. [Step 2]
3. [Step 3]
4. [Delay if needed: X minutes/hours]
5. [Step 4]

## Error Handling
- If [step X fails]: [specific action — retry, notify, skip]
- Notification channel: [Slack channel or email address]
- Retry policy: [retry X times with Y-second delay, then notify]

## Manual Fallback
[Step-by-step instructions to run this process manually if the automation fails]

## Testing Checklist
- [ ] Test with sample data in staging
- [ ] Verify each step fires correctly
- [ ] Test error condition (disable step 2, confirm notification fires)
- [ ] Run in parallel with manual process for 1 week

## Monitoring
- Success metric: [what to track to confirm it's working]
- Check frequency: weekly
- Last reviewed: [date]
