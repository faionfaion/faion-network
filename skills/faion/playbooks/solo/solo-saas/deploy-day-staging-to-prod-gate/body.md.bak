# Deploy-day staging-to-prod gate

## Intent

Safe push to prod with rollback ready: CI green, smoke pass on staging, feature-flagged where risky, deploy script run, post-deploy health verified, rollback path proven.

## Scope

Safe push to prod with rollback ready: CI green, smoke pass on staging, feature-flagged where risky, deploy script run, post-deploy health verified, rollback path proven.

## Stages

### 1. CI green check

No deploy without green main.

Tasks:
- Verify CI green on the target SHA
- Re-run flakies if needed
- Block if any required check fails

Outputs:
- CI status snapshot
- Re-run log
- Block/proceed call

Decision gate: Advance only with a fully green CI.

### 2. Staging smoke

Smoke-test the slice end-to-end on staging.

Tasks:
- Deploy to staging
- Run smoke pack (auth, payment, primary AC)
- Verify integrations (Stripe / email) are wired

Outputs:
- Staging deploy URL
- Smoke results
- Integration check log

Decision gate: Advance only when every smoke step passes.

### 3. Flag decision

Risky changes go behind a flag.

Tasks:
- Decide flag posture (off / canary / all-users)
- Pre-write the canary cohort + kill criteria
- Confirm the rollback path is automated

Outputs:
- Flag config
- Canary cohort
- Rollback verification

Decision gate: Advance only when flag config is committed.

### 4. Deploy to prod

Run the script with eyes on health.

Tasks:
- Trigger production deploy
- Watch logs and metrics during the deploy
- Confirm health checks turn green

Outputs:
- Deploy receipt
- Live health snapshot
- Error budget delta

Decision gate: Advance only when health checks stay green for 15 minutes.

### 5. Verify in production

Walk the AC against production.

Tasks:
- Run a manual pass of the acceptance criteria on prod
- Verify analytics + logs receive the new events
- Notify channels (TG / status page)

Outputs:
- AC verification on prod
- Analytics check
- Notification posted

Decision gate: Advance only when every AC passes on prod.

### 6. Rollback drill

Prove the rollback path actually works.

Tasks:
- Run a synthetic rollback in staging
- Verify the rollback returns prod-equivalent state
- Time the rollback (should be <=15 minutes)

Outputs:
- Drill log
- Rollback timing
- Updated rollback runbook

Decision gate: Advance only when rollback completes <=15 minutes.

### 7. Close the deploy

Write the deploy ticket and move on.

Tasks:
- Close the deploy ticket with notes
- Update the changelog and release-planning doc
- Stamp the runbook with todays lessons

Outputs:
- Deploy ticket closed
- Changelog entry
- Runbook delta

Decision gate: Cycle closes when ticket is closed and changelog is committed.

## Common pitfalls

- Skipping the decision-gate write-up to keep moving - closes the loop with vibes, not evidence.
- Treating each stages outputs as optional - every output is a gate input for the next stage.
- Letting one bad week stretch a fixed-cadence ritual into a quarterly one.

## Quality checklist

- Every stage has at least one referenced methodology that resolves under `knowledge/`.
- Every output is a real artefact, not a feeling.
- The final decision is a written commitment, not we will see.
