<!-- purpose: prompt-pr-checklist markdown for PR template -->
<!-- consumes: prompt-pr-checklist.json -->
<!-- produces: PR template body -->
<!-- depends-on: content/02-output-contract.xml schema -->
<!-- token-budget-impact: ~200 tokens per PR -->

# Prompt PR Review Checklist — `<artefact_id>`

- **Owner:** `<handle>`
- **Mode:** `READ-DO` (or `DO-CONFIRM` for high-risk PRs)
- **Last reviewed:** `2026-05-22`

## Pre-merge pause-point

- [ ] **i1.** Power-calc spec attached (`git://<repo>/specs/<file>.json`) — *anchor: incident-<id>*
- [ ] **i2.** Refusal-style policy unchanged — *anchor: policy-line:<path>#L<n>*
- [ ] **i3.** Eval delta within tolerance (CI run url) — *anchor: incident-<id>*
- [ ] **i4.** Tool-schema unchanged or migrated — *anchor: incident-<id>*
- [ ] **i5.** Production rollout plan attached — *anchor: postmortem-<id>*

Reviewer + author both sign off in PR comments.
