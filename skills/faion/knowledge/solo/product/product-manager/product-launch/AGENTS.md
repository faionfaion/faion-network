# Product Launch

## Summary

A product launch is the coordinated introduction of a product to its target market. Plan 6-8 weeks ahead using a T-8-to-T+2 timeline. Required for any public or beta launch: a launch DRI, an asset checklist (landing page, announcement email, demo/screenshots, social posts, documentation), a channel-per-timing matrix, success metrics with targets set before launch day, and a rollback narrative written before launch. Launch Tuesday or Wednesday, mid-month, avoiding major industry events.

## Why

Launches without a structured playbook either underwhelm (ship quietly, no momentum) or collapse into last-minute chaos. The T-8 timeline forces asset creation and audience building well before launch day; the asset checklist prevents the single most common failure (missing materials discovered at T-0). A rollback narrative written in advance removes decision paralysis on launch day — if you never publish it, no harm done.

## When To Use

- Public release with a coordinated marketing moment (Product Hunt, press, partner amplification).
- Major version bump where existing users need migration messaging and new acquisition push.
- Beta-to-GA transition where pricing, positioning, or audience changes.
- Geographic or segment expansion of an existing product into a new market.

## When NOT To Use

- Bug-fix releases or quiet shipping behind a feature flag — use a release-notes template, not a launch playbook.
- Solo founder shipping iteratively to fewer than 100 users — the playbook overhead exceeds the value; ship to a Discord and write a tweet.
- Internal tools — coordinate with stakeholders, but the GTM machinery is unnecessary.
- Markets where a loud launch backfires (regulated industries, B2B enterprise where field sales owns timing).

## Content

| File | What's inside |
|------|---------------|
| `content/01-planning.xml` | Launch types, T-8-to-T+2 timeline, positioning and messaging requirements, asset checklist rules. |
| `content/02-execution.xml` | Launch-day sequencing, monitoring rules, post-launch retrospective, and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-plan.md` | Full launch plan: overview, audience, timeline table, asset checklist, channel matrix, risk mitigation. |
| `templates/launch-day-checklist.md` | Launch-day runbook: pre-launch checks, go-live steps, announcement sequence, monitoring, EOD debrief. |
| `templates/launch-pulse.sh` | Bash monitor: polls signup and visitor metrics every 5 minutes, posts to Slack webhook. |
