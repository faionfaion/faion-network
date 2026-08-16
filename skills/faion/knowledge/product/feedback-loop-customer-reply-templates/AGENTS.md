# Feedback Loop Customer Reply Templates

## Summary

**One-sentence:** Customer-reply templates closing the feedback loop: acknowledge, route, follow-up — each ticket emerges with a tagged outcome (build / waitlist / decline / bug) and a customer-facing reply.

**One-paragraph:** Most support tools collect feedback but don't close the loop with the customer. This methodology pins five reply templates (acknowledge, build, waitlist, decline, bug) and a routing rule per template. Each ticket exits with both an internal classification AND a customer-facing reply within 72h. Decline replies cite the anti-roadmap entry; waitlist replies link the smoke page; build replies cite the roadmap slot.

**Ефективно для:**

- Solo SaaS founder fielding daily Intercom / Pylon / email feedback.
- Indie operator with no support team and growing inbox.
- Founder whose customers say 'I never heard back about my request'.
- Tech-lead acting as support owner with no triage discipline.

## Applies If (ALL must hold)

- Feedback inflow ≥5 tickets/week.
- Founder owns the support tool.
- Anti-roadmap exists or is being authored in parallel.
- Founder can commit to 72h reply SLA.

## Skip If (ANY kills it)

- Feedback volume <1/week — manual replies fine.
- Team has a dedicated support engineer with own templates.
- Anti-roadmap doesn't exist and won't be authored — decline replies have nothing to cite.
- Customers receive enterprise-grade SLAs different from the templates.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Support tool URL | Intercom / Pylon / email | vendor |
| Anti-roadmap doc | url | anti-roadmap-template output |
| Roadmap reference | url | roadmap tool |
| Bug-tracker URL | url | tracker |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/product/build-or-waitlist-decision-tree` | routing rule for build vs decline |
| `solo/product/anti-roadmap-template` | decline-reply citation source |
| `solo/comms/communicator` | reply tone + voice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-feedback-loop-customer-reply-templates` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/feedback-loop-customer-reply-templates.md.j2` | Markdown skeleton for the playbook-step artefact, matching content/02-output-contract.xml |
| `templates/feedback-loop-customer-reply-templates.md` | Markdown skeleton for the playbook-step artefact, matching content/02-output-contract.xml Generated from `templates/feedback-loop-customer-reply-templates.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/feedback-loop-customer-reply-templates.schema.json` | JSON Schema seed + filled fixture for the playbook-step artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-feedback-loop-customer-reply-templates.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `[[anti-roadmap-template]]`
- `[[build-or-waitlist-decision-tree]]`
- `[[friction-to-backlog]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feedback-loop-customer-reply-templates.schema.json`

```json
{
  "artefact_id": "REPLACE-WITH-ULID",
  "trigger": "Feedback Loop Customer Reply Templates engagement",
  "rules_applied": [
    "REPLACE-WITH-RULE-ID"
  ],
  "evidence": [
    {
      "rule_id": "REPLACE-WITH-RULE-ID",
      "citation": "REPLACE-WITH-VERIFIABLE-CITATION",
      "source_type": "url"
    }
  ],
  "output_payload": {
    "status": "draft"
  },
  "consumer": "REPLACE-WITH-NAMED-CONSUMER",
  "owner": "REPLACE-WITH-NAMED-OWNER",
  "last_touched": "2026-05-23T10:00:00Z"
}
```
