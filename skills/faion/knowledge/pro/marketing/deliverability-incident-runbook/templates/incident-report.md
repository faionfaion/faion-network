<!-- purpose: Markdown skeleton for the deliverability incident postmortem -->
<!-- consumes: detect + isolate + diagnose + contain outputs -->
<!-- produces: report artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400 tokens when filled -->

# Deliverability Incident — `<INCIDENT_ID>`

- **Detected at:** `<YYYY-MM-DDTHH:MM:SSZ>`
- **Owner:** `@<handle>`
- **Version:** `1.0.0`

## Metrics at detection

| Metric | Value | Threshold | Tripped |
|--------|------:|----------:|:-------:|
| Complaint rate (%) | <X> | 0.1 | <Y/N> |
| Bounce rate (%) | <X> | 5.0 | <Y/N> |
| Unsub rate (%) | <X> | 2× baseline | <Y/N> |

Segment: `<SEGMENT>`

## Diagnostics

| Check | Result | Source |
|-------|--------|--------|
| SPF | <pass/fail> | <DNS lookup URL> |
| DKIM | <pass/fail> | <DNS lookup URL> |
| DMARC | <pass/fail> | <DNS lookup URL> |
| ESP reputation | <score> | <dashboard URL> |
| Complaint sample | <summary> | <ESP query URL> |

## Containment

- Action: <throttle | pause-segment | suppress-list | escalate>
- Auto-resume at: `<YYYY-MM-DDTHH:MM:SSZ>`
- Warm-up curve: `10/30/100 over 3 sends`

## Postmortem (≥100 chars)

<Cause, evidence, decisions, owner, follow-ups. Cite at least one diagnostic source.>

## Follow-ups

- [ ] Lint rule added: <subject token blocklist, suppression policy>
- [ ] Re-warm completed at <date>
