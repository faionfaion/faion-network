# Product Operations (PM-side)

## Summary

When a Product Ops function exists, the PM is a consumer and partner — not its operator. PM-side agents are pure readers of the canonical store (Linear/Jira/Productboard rollups) and authors of narrative artifacts (specs, decision memos, discovery memos). Hand-offs are explicit: PM drafts land in a Product Ops queue (PR, Slack thread, Notion draft) where the Product Ops agent applies the write. The PM never bypasses that queue.

## Why

96% of organizations now have a Product Ops function; 50% report to CPO. PMs who run parallel rollups in their own subagents produce numbers that diverge from org-published figures — trust collapses when two decks contradict each other in the same meeting. The hard rule: PM-side agents read, Product Ops agents write.

## When To Use

- PM onboarding into an org with an existing Product Ops function — needs explicit RACI between own subagents and Product Ops automations.
- Multiple PMs requesting inconsistent artifacts — route through the Product Ops canonical store.
- Preparing a board/exec/portfolio review — consume Product Ops outputs instead of re-deriving.
- PM proposes a new ceremony or template — hand off the converged output to Product Ops to ship org-wide.
- PM receives a Product Ops insight and needs to convert it into a discovery or kill decision.

## When NOT To Use

- Solopreneur / single-PM team with no Product Ops function — use solo-tier skills directly.
- Product Ops charter is undefined — drive `faion-brainstorm` on the charter first.
- Strategic decisions (pricing, positioning, kill/scale, hiring) — the PM owns these, not Product Ops.
- Customer-facing comms (release notes, interviews, positioning copy) — PM owns the content.
- First 30 days of a new product where the workflow is unstable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pm-ops-boundary.xml` | RACI table, read-only rule, canonical store, hand-off queue pattern |
| `content/02-product-ops-maturity.xml` | Maturity model (Tactical → Strategic → Transformational), AI-native ops, failure modes |

## Templates

| File | Purpose |
|------|---------|
| `templates/pm-ops-contract-check.sh` | Block PM-side write attempts to system-of-record owned by Product Ops |
