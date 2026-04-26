# Viral Loop Optimization

## Summary

Viral loop optimization iterates on an existing measured K-factor by decomposing it into its two drivers — i (invites sent per user) and c (invitee conversion rate) — identifying the bottleneck, and running A/B tests on the weakest leg. Optimize c first (invite landing page) before optimizing i (share moments); every improvement to c multiplies all future loop turns.

## Why

K-factor is a compound metric: K = i * c. A small improvement to the lower leg often has larger absolute impact than a large improvement to the higher one. Without funnel decomposition, optimization effort is directed by intuition rather than math. Cycle time is a secondary lever — halving cycle time roughly squares compounding over a quarter.

## When To Use

- Product has a working invite/share path and a measured baseline K (even K = 0.05 is enough to start).
- Full event chain is tracked: invite_shown → invite_sent → invite_clicked → invitee_signup → invitee_active.
- A live A/B test framework is available (no code deploy needed to split variants).
- At least 5,000 weekly users entering the loop (otherwise sample size kills experiments).

## When NOT To Use

- Pre-PMF: optimizing K of a product nobody loves yields K = 0.0X times any multiplier — still nothing.
- B2B enterprise where sharing is gated by procurement or security — viral mechanics do not translate.
- Markets with strict anti-spam rules (regulated finance, EU consumer) where contact-import is non-compliant.
- Products where the inviter's value requires the invitee to join but the invitee has no standalone reason — forced virality churns invitees fast.

## Content

| File | What's inside |
|------|---------------|
| `content/01-k-factor-decomposition.xml` | K = i * c formula, cycle time lever, funnel metrics, optimization priority order |
| `content/02-optimization-tactics.xml` | Tactics by component: increasing i (share moments, contact import), increasing c (landing page, one-click signup) |
| `content/03-fraud-and-monitoring.xml` | Fraud signals, quality checks on referred user retention, weekly/monthly review cadence |

## Templates

| File | Purpose |
|------|---------|
| `templates/k-factor.py` | K-factor decomposition from event stream CSV |
| `templates/loop-projection.py` | Naive compounding model for K + cycle time projection |
| `templates/experiment-spec.md` | K-factor experiment spec template (hypothesis, primary metric, MDE, variants) |
