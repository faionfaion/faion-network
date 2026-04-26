# Micro-MVPs

## Summary

Micro-MVPs are extremely small, high-signal experiments — each designed to validate
one key assumption in hours to days rather than weeks. Six experiment types (landing
page, concierge, Wizard of Oz, video demo, fake door, smoke test) map to specific
assumption categories. The process forces assumption identification, success-metric
definition, and a pivot/persevere decision before starting, not after.

## Why

Traditional MVPs still take weeks or months to build, yet most failed products fail
on assumptions that could be tested in a day. Micro-MVPs compress the
validate-or-kill cycle by orders of magnitude: Dropbox validated file-sync demand
with a 3-minute video before writing a line of sync code. The pattern is: identify
the riskiest assumption, design the smallest experiment, define success in advance.

## When To Use

- New product idea where demand, willingness-to-pay, or workflow fit is unvalidated.
- Feature hypothesis that can be faked before building (Wizard of Oz, fake door).
- Budget or time is too constrained for a full MVP build.
- Iterating rapidly post-MVP to validate the next bet without a full sprint.

## When NOT To Use

- Assumption already validated by strong existing evidence — skip to build.
- Regulated domains where a "fake" product violates compliance (fintech, medical).
- Infrastructure/platform work with no user-facing surface to fake.
- When the experiment would damage brand trust with early adopters.

## Content

| File | What's inside |
|------|---------------|
| `content/01-experiment-types.xml` | Six micro-MVP types with effort range, what each validates, and the Dropbox example. |
| `content/02-process.xml` | Six-step micro-MVP process from assumption identification to pivot/persevere decision. |

## Templates

None — experiments are lightweight by design; no standardised document artifact required.
