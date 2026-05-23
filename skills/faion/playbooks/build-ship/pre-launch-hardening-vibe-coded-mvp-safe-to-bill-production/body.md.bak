# Pre-launch hardening: vibe-coded MVP → safe-to-bill production

## Intent

Take an MVP that works on localhost and make it survive paying customers without a co-founder/SRE.

## Scope

Take an MVP that works on localhost and make it survive paying customers without a co-founder/SRE. End state: Stripe live, RLS audited, backups proven, legal docs live, support inbox routed.

## Stages

### 1. Security audit

Find what a vibe-coded MVP missed.

Tasks:
- Run a security-testing checklist against the codebase
- Audit RLS / authz on the database
- Scan git history for leaked secrets

Outputs:
- Security audit report
- RLS audit notes
- Secret-scan results

Decision gate: Advance only when all critical security findings are fixed.

### 2. Stripe + payment hardening

Make billing un-funny.

Tasks:
- Wire Stripe live keys with separate webhook secret
- Harden webhook validation against replay + spoof
- Cover subscription lifecycle edge cases

Outputs:
- Live Stripe config
- Webhook hardening notes
- Lifecycle test coverage

Decision gate: Advance only when test mode + live mode behave identically.

### 3. Backup + restore drill

Prove you can recover, not assume.

Tasks:
- Run a backup snapshot
- Restore to a scratch environment
- Time the restore + sanity-check data

Outputs:
- Backup snapshot
- Restore log
- Restore time

Decision gate: Advance only when restored environment matches prod within tolerance.

### 4. Secrets + ops cleanup

Get secrets out of .env clutter.

Tasks:
- Move secrets to a managed store
- Rotate any leaked or shared keys
- Document the secret rotation runbook

Outputs:
- Managed secret store
- Rotation log
- Runbook

Decision gate: Advance only when no plaintext secret is in repo or local file.

### 5. Support inbox + SLA

Route customer messages somewhere you actually read.

Tasks:
- Pick the support inbox tool (email-only is fine)
- Define the SLA per category
- Wire alerts for new tickets

Outputs:
- Inbox set up
- SLA doc
- Alert wiring

Decision gate: Advance only when a test ticket reaches you within SLA.

### 6. Legal docs live

Ship Terms / Privacy / Refund pages before billing.

Tasks:
- Draft Terms + Privacy from a solo-saas pack
- Add the refund policy + cookie banner
- Link from footer + checkout

Outputs:
- Legal pages live
- Refund policy
- Cookie banner

Decision gate: Advance only when checkout shows the policy link.

### 7. Pre-bill checklist sweep

Final sweep before turning on live billing.

Tasks:
- Walk the launch-operations checklist
- Fire smoke transactions in live mode
- Confirm refund + dispute flow end-to-end

Outputs:
- Checklist signed off
- Live smoke receipts
- Refund/dispute test log

Decision gate: Advance only when every checklist item is green.

### 8. Flip live + monitor

Flip billing live and watch the first 72 hours.

Tasks:
- Switch payment processor to live
- Watch first transactions
- Stand by for first-100-tickets

Outputs:
- Live mode active
- First-transaction log
- First-72h notes

Decision gate: Cycle closes when the first 72 hours pass without a P0 incident.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
