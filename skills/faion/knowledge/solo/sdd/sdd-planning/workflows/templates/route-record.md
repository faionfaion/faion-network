<!--
purpose: Canonical SDD phase route-record skeleton emitted by the workflows navigation hub.
consumes: feature_dir listing + frontmatter status fields of spec.md / design.md / plan
produces: a workflows artefact validating against scripts/validate-workflows.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~200-500 tokens once filled
-->
---
artefact_id: route-<feature>-<YYYY-MM-DD>
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
feature_dir: .aidocs/features/<status>/<feature>/
active_phase: <spec|design|plan|execution|done|blocked>
next_methodology: solo/sdd/sdd-planning/<phase-methodology>
phase_statuses:
  spec: <missing|Draft|Accepted>
  design: <missing|Draft|Accepted>
  plan: <missing|Draft|Accepted>
blocker: <null|specific-blocker-name>
---

# SDD Phase Route: <feature>

Active phase: **<phase>**
Next methodology to dispatch: **<path>**

If `active_phase: blocked`, the `blocker` field names the specific reason routing failed.
