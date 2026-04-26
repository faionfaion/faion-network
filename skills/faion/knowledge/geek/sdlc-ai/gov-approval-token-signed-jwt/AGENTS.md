# Human Approval as a Signed, Scoped, Single-Use JWT

## Summary

Whenever an agent needs human approval for a write/destructive action (deploy, rollback, `kubectl delete`, secret rotation, money movement), the approval is delivered as a cryptographically signed JWT, not a Slack thumbs-up. The token carries `sub` (approver identity), `scope` (the exact tool + target tuple being approved), `iat`, a short `exp` (≤5 minutes), an `aud` for the calling agent, a `jti` for single-use, and the originating `incident_id` / `task_id`. The agent's tool layer verifies the signature, scope match, expiry, and replay flag at call time. Slack reactji can initiate the approval, but only the signed callback satisfies the gate.

## Why

"Did Bob really approve this?" is unanswerable from a chat log: messages can be edited, channels are not signed, and reactji do not bind to a specific tool call. A signed token replaces social proof with cryptographic proof — the audit record is verifiable months later by replaying the signature against the public key. Microsoft's Agent Governance Toolkit (April 2026) and BeyondTrust's identity governance pattern converge on the same shape: scope-bound, time-boxed, single-use approval tokens are the only mechanism that survives both regulatory audit (EU AI Act, SOC2 CC6) and post-incident forensics. Without it, "agent abuse via social engineering of the chat channel" becomes a real attack surface.

## When To Use

- Any agent that can perform Tier 1+ (writes / destructive / money-moving) actions in production.
- Incident-response agents that propose remediations a human must authorize before the agent executes them.
- Deploy / rollback bots, `kubectl` operators, IAM-mutation agents, customer-data-export agents.
- Regulated environments (EU AI Act enforcement Aug 2026, SOC2 / GDPR audited orgs) where approval evidence is non-optional.

## When NOT To Use

- Pure read-only agents — no write means no approval token is needed.
- Tier 0 actions inside a sandboxed dev environment with no production blast radius.
- Multi-step approvals with quorum and complex policy — escalate to a full IAM/policy engine (OPA, Cedar) instead of a hand-rolled JWT.
- One-off scratch scripts that are never reused — bootstrap cost dominates.

## Content

| File | What's inside |
|------|---------------|
| `content/01-token-shape.xml` | Required claims, expiry, scope binding, single-use replay protection. |
| `content/02-issuance-and-verification.xml` | Slack-initiated → signed callback flow and per-call verification rule. |

## Templates

| File | Purpose |
|------|---------|
| `templates/approval-token.json` | Decoded JWT payload showing the required claims. |
| `templates/verify-token.py` | Reference verifier: signature + scope + expiry + replay check. |
