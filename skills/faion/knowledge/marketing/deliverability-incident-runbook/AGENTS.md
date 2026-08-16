# Deliverability Incident Runbook

## Summary

**One-sentence:** Email deliverability incident runbook — SPF/DKIM/DMARC check, ESP reputation lookup, segment isolation, throttle, postmortem — with thresholds + owner-named actions per step.

**One-paragraph:** When unsub rate or spam-complaint rate spikes after a lifecycle email send, marketers Google panic-fixes. This runbook codifies a deterministic incident response: detect (threshold-based) → isolate (which segment, which template) → diagnose (SPF/DKIM/DMARC + ESP reputation) → contain (throttle, pause, suppress) → postmortem (versioned incident report). Core rules: every incident produces a versioned report; thresholds are numeric not qualitative; throttle is reversible by default; sender warm-up is mandatory after recovery; postmortem cites at least one diagnostic source.

**Ефективно для:**

- Lifecycle email program — після post-send analytics виявили spike.
- ESP migration — first 2 weeks of new sender's warm-up.
- High-volume nurture sequence — risk of bulk classification.
- Audit / compliance — proof of incident response discipline.

## Applies If (ALL must hold)

- Email lifecycle program with ≥1,000 sends per send.
- Post-send analytics available within 4 hours (bounce + spam complaint + unsub rates).
- DNS + ESP access (SPF/DKIM/DMARC records + reputation dashboard).
- Authority to throttle / pause sends on the affected segment.

## Skip If (ANY kills it)

- Transactional-only sending (1-to-1) — different signal set, different containment.
- No post-send analytics — fix instrumentation first.
- One-off broadcast where the cost of incident-response exceeds the impact.
- ESP / DNS access locked behind weekly tickets — runbook needs same-day reach.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Send analytics (bounce / complaint / unsub per segment + template) | dashboard | ESP |
| DNS records for sending domain | live lookup | DNS provider |
| ESP reputation score | dashboard | ESP (e.g. SendGrid, Postmark) |
| Suppression list write access | API / dashboard | ESP |
| Postmortem template + log store | repo / wiki | growth team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[daily-ads-anomaly-checklist]] | Same threshold-based triage pattern. |
| [[experiment-verdict-template]] | Postmortem format aligned with verdict-template. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: numeric-thresholds, owner-named-actions, reversible-throttle, mandatory-warmup-post-recovery, postmortem-with-sources | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the incident report + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: detect → isolate → diagnose → contain → postmortem | 700 |
| `content/05-examples.xml` | essential | Worked example: spam complaint spike on welcome sequence segment B | 500 |
| `content/06-decision-tree.xml` | essential | Tree: complaint-rate vs DKIM-status vs segment → action | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pull-send-analytics` | haiku | Mechanical API call. |
| `check-dns-and-reputation` | haiku | Lookup + compare. |
| `decide-containment` | sonnet | Bounded judgment on throttle/pause/segment-suppress. |
| `write-postmortem` | sonnet | Synthesis with cited sources. |

## Templates

| File | Purpose |
|------|---------|
| `templates/incident-report.md.j2` | Markdown skeleton for the postmortem |
| `templates/incident-report.md` | Markdown skeleton for the postmortem Generated from `templates/incident-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/incident-report.json` | JSON example matching the output contract |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-deliverability-incident-runbook.py` | Validate the incident report JSON against the schema | After report draft, pre-publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[daily-ads-anomaly-checklist]]
- [[experiment-verdict-template]]
- [[dormant-lead-reactivation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps the observed signals (complaint rate, bounce rate, DKIM/DMARC status, segment isolation result) to the containment action and pins the rule from `01-core-rules.xml`. Use it before throttling — over-throttle damages re-engagement, under-throttle damages sender reputation.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/incident-report.json`

```json
{
  "incident_id": "inc-2026-05-23-welcome-segb",
  "detected_at": "2026-05-23T09:42:00Z",
  "owner": "@alex-email",
  "metrics": {
    "complaint_rate_pct": 0.18,
    "bounce_rate_pct": 2.4,
    "unsub_rate_pct": 1.6,
    "segment": "welcome_seq_segment_b"
  },
  "diagnostics": [
    {
      "check": "dkim",
      "result": "pass",
      "source": "https://mxtoolbox.com/SuperTool?action=dkim%3a"
    },
    {
      "check": "esp_reputation",
      "result": "82 (was 91)",
      "source": "https://app.sendgrid.com/reputation"
    },
    {
      "check": "complaint_sample",
      "result": "5/6 complaints from gmail.com; subject contains all-caps tokens",
      "source": "esp://complaints?from=2026-05-23"
    }
  ],
  "containment": {
    "action": "pause-segment",
    "auto_resume_at": "2026-05-24T09:00:00Z",
    "warmup_curve": "10/30/100 over 3 sends"
  },
  "postmortem": "Spam complaint rate hit 0.18% on welcome_seq_segment_b after subject-line A/B variant rolled out at 08:30. DKIM healthy; ESP reputation dropped 9pp. Containment: pause segment, schedule warm-up recovery; replace subject variant; add subject-line lint rule blocking all-caps tokens.",
  "version": "1.0.0"
}
```
