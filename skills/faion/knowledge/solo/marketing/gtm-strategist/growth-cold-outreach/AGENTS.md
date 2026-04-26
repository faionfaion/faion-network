# Cold Outreach

## Summary

A structured approach for converting strangers into customers via targeted cold email and
LinkedIn: build a focused prospect list, personalize using research, keep emails under 5
sentences, and follow up 4–5 times. Deliverability infrastructure (separate domain,
SPF/DKIM/DMARC, warm-up) is a prerequisite — without it, emails never reach the inbox.

## Why

Inbound marketing takes months; cold outreach can produce customers this week. Done right
it outperforms paid ads on a cost-per-meeting basis at early stage. The mechanism: tight
ICP targeting reduces wasted effort, personalization improves open and reply rates, and
systematic follow-up captures the 80% of replies that come after the first message.

## When To Use

- Zero or small audience; need customers before inbound scales.
- Targeting a specific niche (role + industry + company size) where lists are buildable.
- B2B products or services where individual decision-makers can be identified.
- Outreach to potential partners, collaborators, or press.

## When NOT To Use

- B2C consumer products — cold outreach doesn't scale to consumer segments.
- Regulated industries with anti-spam laws that prohibit unsolicited commercial email (check GDPR, CAN-SPAM, CASL for jurisdiction).
- Low-ACV products where the CAC of manual outreach exceeds LTV.
- When deliverability infrastructure is not set up — sending from primary domain risks blacklisting.

## Content

| File | What's inside |
|------|---------------|
| `content/01-targeting-and-research.xml` | ICP criteria (BANT+Reach); prospect sources; personalization levels and research sources. |
| `content/02-email-writing.xml` | Anatomy of cold email (4 elements); subject line, opening, body formulas; follow-up cadence (5 emails over 21 days). |
| `content/03-infrastructure-and-metrics.xml` | Deliverability checklist (domain, warmup, SPF/DKIM, volume caps); metrics benchmarks; common mistakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cold-email.txt` | Cold email template with subject, personalized opening, value prop, CTA. |
| `templates/linkedin-outreach.txt` | Connection request + follow-up message pair. |
