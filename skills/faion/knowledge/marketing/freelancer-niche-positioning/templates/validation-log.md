<!-- purpose: 3-signal validation log per positioning -->
<!-- consumes: live positioning surfaces + peer + buyer access -->
<!-- produces: validation evidence per content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~300 tokens when filled -->

# Positioning Validation — `<POSITIONING_ID>`

- Owner: `@<handle>`
- One-liner: I `<X>` for `<Y>` so they `<Z>`

## Search-find test

- Query: `<X + Y phrase>`
- Surface: Google / LinkedIn / Upwork
- Top-5 rank on `<DATE>`: `<rank>`
- Pass: `<y/n>`

## Peer-recall test

| Peer | Paraphrase | Specific? |
|------|------------|-----------|
| @p1 | ... | y/n |
| @p2 | ... | y/n |
| @p3 | ... | y/n |
| @p4 | ... | y/n |
| @p5 | ... | y/n |

≥3 of 5 specific = pass.

## Buyer-paraphrase test

- Buyer: `<handle>`
- Discovery date: `<YYYY-MM-DD>`
- Quote: "<verbatim from transcript>"
- Pass: `<y/n>`
