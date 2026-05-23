<!-- purpose: ChangeOrder email + record skeleton -->
<!-- consumes: client request + master SOW + rate card -->
<!-- produces: scaffold consumed by compose-co-email step -->
<!-- depends-on: content/01-core-rules.xml#r1 (master SOW anchor) -->
<!-- token-budget-impact: ~150 tokens -->

# Change Order — [co_id]

**Anchor SOW:** [master_sow.name] dated [date] (identifier: [identifier])
**Owner:** [freelancer role] / [person]
**Version:** [semver]

## Email subject

Change Order [co_id] — [project name] SOW dated [date]

## Email body

Hi [client],

Per our chat today, here is the change order for [scope summary], applying under our master SOW dated [date].

| Field | Delta |
|-------|-------|
| Scope | [scope_delta] |
| Price | [price_delta] |
| Schedule | [schedule_delta] |
| Payment | [payment_terms_delta] |

Reply YES to this email to authorize this change order under the terms of the master agreement.

— [freelancer]

## Acceptance

- reply_yes_captured: false (set true on YES)
- captured_at: ...
- channel: email | chat | signed_doc

## Artefact

- immutable_link: drive://... (PDF after signing)
- invoice_line_ref: INV-... (set on next invoice)
- verbal_authorization_hours: 0 (must stay ≤ 8 if work started before YES)
