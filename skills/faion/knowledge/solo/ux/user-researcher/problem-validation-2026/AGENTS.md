# Problem Validation 2026

## Summary

A focused variant of the problem-validation methodology adding: a 5-step interview opener (Vision → Framing → Weakness → Pedestal → Ask), a commitment signal taxonomy (Time / Reputation / Money), a Mom Test replacement question table, and the 2026 principle that validation is a recurring weekly loop during discovery, not a one-time gate. For full agent tooling, CLI, and process depth see the adjacent `problem-validation/` directory.

## Why

The 2026 update addresses three failure modes of classic problem validation: (1) researchers pitch too early — the opener sequence delays pitching by positioning the researcher as a learner, not a seller; (2) interviewers accept stated interest as validation — the commitment signal taxonomy gives a concrete reject/accept criterion; (3) teams treat validation as a one-time gate — the recurring loop principle prevents stale assumptions from accumulating.

## When To Use

- Before any discovery interview: use the 5-step opener verbatim to set up a non-selling conversation
- After an interview: classify evidence by commitment signal type (Time / Reputation / Money) before deciding PROCEED
- When reviewing a validation plan: apply the recurring loop principle to check if validation is scheduled as a weekly task
- Quickly reframing a set of interview questions to remove hypothetical framing (use the Mom Test replacement table)

## When NOT To Use

- As a replacement for `problem-validation/` — this file adds specific techniques, not a full methodology
- When n &lt; 5 interviews — the commitment signal taxonomy requires a pattern across multiple conversations
- When all evidence consists of compliments and hypotheticals — that is negative validation; stop and pivot regardless of opener quality

## Content

| File | What's inside |
|------|---------------|
| `content/01-2026-additions.xml` | Validation hierarchy with ranks, Mom Test replacement table, 5-step opener, commitment signals, red flags |

## Templates

| File | Purpose |
|------|---------|
| `templates/opener-sequence.txt` | Verbatim 5-step interview opener ready to paste |
| `templates/commitment-classifier.txt` | Post-interview prompt to classify evidence by signal type |

## See Also

- `../problem-validation/` — full methodology with process, CLI tools, scripts, and agent guidance
