---
name: scope-cutting
description: Halve an over-specified feature's AC list by rewriting spec.md with an explicit "Out of scope (defer to v2)" section.
tier: solo
group: sdd-workflow
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a rewritten `spec.md` for one feature that contains no more than half the original acceptance criteria, a clear "Out of scope (defer to v2)" section listing every deferred AC with a one-line reason, and a revised `implementation-plan.md` that reflects the reduced scope — so you can start building immediately without second-guessing what was cut.

## Prerequisites

- An existing `spec.md` with a numbered acceptance-criteria list (≥6 ACs; if you have fewer, the feature is already small enough).
- The feature's SDD folder exists under `.aidocs/in-progress/<feature-name>/` or `.aidocs/todo/<feature-name>/`.
- The feature has NOT entered active development yet (no tasks in `in-progress/`). If tasks are in flight, finish the current task first.
- Familiarity with [writing-first-spec](../writing-first-spec) — you know what an AC is and why it matters.

## Steps

### Step 1 — Read the spec and count acceptance criteria

Open the feature's `spec.md`. Find the acceptance-criteria section (usually `## Acceptance Criteria` or `## Success Criteria`). Count the ACs. Write the number down — call it N.

Example: a checkout flow spec with 12 ACs:

```
1. Guest checkout (no account required)
2. Registered user checkout with saved address
3. Stripe payment: credit/debit card
4. PayPal payment option
5. Order confirmation email sent within 60 s
6. Cart persists across browser sessions
7. Coupon/discount code input on cart page
8. Real-time inventory check before payment
9. Address validation via postal API
10. Tax calculation by country
11. Multi-currency display (EUR, USD, GBP)
12. Order history page in user account
```

### Step 2 — Sort ACs into Keep and Defer columns

Create a two-column scratch table (paste it in a comment at the bottom of spec.md temporarily, or open a scratch file):

| AC | Column | Reason |
|----|--------|--------|
| (each AC) | Keep / Defer | one-line rationale |

Apply this rule to each AC: **"Can a user complete the primary transaction without this AC?"** If yes → Defer. If no → Keep.

For the checkout example, applied strictly to "user can pay for an order":

| AC | Column | Reason |
|----|--------|--------|
| 1. Guest checkout | Keep | no account required = no barrier |
| 2. Registered checkout with saved address | Defer | address save is convenience, not required to pay |
| 3. Stripe card payment | Keep | core payment path |
| 4. PayPal | Defer | second payment method; card alone validates the flow |
| 5. Confirmation email within 60 s | Keep | user needs proof of purchase |
| 6. Cart persists across sessions | Defer | session-only cart is sufficient to test checkout |
| 7. Coupon code input | Defer | no revenue impact until you have coupons to issue |
| 8. Real-time inventory check | Keep | prevents overselling on first real orders |
| 9. Address validation via postal API | Defer | manual address entry works for validation phase |
| 10. Tax calculation by country | Defer | single-country or flat-rate tax suffices initially |
| 11. Multi-currency display | Defer | one currency is enough to test willingness to pay |
| 12. Order history page | Defer | users can check email; history page is nice-to-have |

Result: 4 Keep, 8 Defer. Target is N/2 or fewer — 4 out of 12 passes.

If you end up with more than N/2 in Keep, re-read each Keep AC and ask: "Is there a reduced version of this AC that still validates the core?" If yes, scope the AC down and keep the narrower version; the broader version becomes a Defer.

### Step 3 — Rewrite spec.md: replace AC list with the Keep set

Open `spec.md` in your editor. Replace the full acceptance-criteria section with only the Keep ACs, renumbered from 1.

```markdown
## Acceptance Criteria

1. Guest checkout: user can complete a purchase without creating an account.
2. Stripe card payment: user can pay with a credit or debit card via Stripe Checkout.
3. Order confirmation email is delivered within 60 s of successful payment.
4. Real-time inventory check prevents checkout if stock is 0.
```

Keep each AC as a single, testable statement. Do not add explanation or rationale inside the AC — that belongs in a task's description.

### Step 4 — Add "Out of scope (defer to v2)" section

Immediately after the Acceptance Criteria section, add a new section:

```markdown
## Out of scope (defer to v2)

| AC | Deferred reason |
|----|-----------------|
| Registered checkout with saved address | Address persistence is a UX improvement; not needed to validate payment flow |
| PayPal payment | Second payment method adds integration complexity; Stripe card covers the hypothesis |
| Cart persistence across sessions | Session-local cart is sufficient for checkout validation |
| Coupon/discount code input | No active coupon campaign; defer until promotions are planned |
| Address validation via postal API | Manual entry is acceptable at this volume; API adds a paid dependency |
| Tax calculation by country | Flat-rate or zero tax is acceptable for the launch country |
| Multi-currency display | Single currency (EUR) covers the initial target market |
| Order history page | Confirmation email is the receipt; account history is a retention feature |
```

This section is permanent — it survives into v2 planning and prevents scope creep from re-entering through "we already discussed this" conversations.

### Step 5 — Update implementation-plan.md task count

Open `implementation-plan.md`. Each original AC likely maps to 1–3 tasks. Remove or mark as `[v2]` any task that implements a deferred AC. Adjust phase totals and token estimates to reflect only the Keep ACs.

For the checkout example: 4 Keep ACs × ~3 tasks each = ~12 tasks instead of the original ~30. Update the task table accordingly. Do not remove deferred tasks from the file — move them under a `## Deferred (v2)` heading at the bottom of the plan so they are not lost.

### Step 6 — Commit the updated docs

```bash
cd /home/nero/workspace/projects/<your-project>
git add .aidocs/in-progress/<feature-name>/spec.md .aidocs/in-progress/<feature-name>/implementation-plan.md
git commit -m "docs(<feature-name>): scope-cut spec to <N/2> ACs, defer <N - N/2> to v2"
```

Update `CHANGELOG.md` under `## [Unreleased]` before committing — the pre-commit hook requires it.

## Verify

Run a two-check gate on the rewritten `spec.md`:

1. Count lines in `## Acceptance Criteria` — must be ≤ original N/2.
2. Count rows in `## Out of scope (defer to v2)` table — must equal original N minus the new AC count.

```bash
# count ACs
grep -c "^[0-9]\+\." .aidocs/in-progress/<feature-name>/spec.md

# count deferred rows (subtract 2 for header + separator)
grep -c "^|" .aidocs/in-progress/<feature-name>/spec.md
```

If the two counts sum to the original N and the Keep count is ≤ N/2, the scope cut is complete.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Every AC feels like a Keep | Primary transaction statement is too broad ("a full e-commerce experience") | Rewrite the feature's one-sentence goal in spec.md `## Goal` to the narrowest possible transaction, then re-sort |
| Keep count is still > N/2 after sorting | Some Keep ACs can be scoped down to a narrower version | For each Keep AC, write a "v1 version" that tests the hypothesis with 80% less work; replace the AC with the v1 version |
| Stakeholder insists a deferred AC is required | Feature preference presented as necessity | Ask: "If we ship without this AC and show it to 10 users, will zero of them complete the primary transaction?" If no — defer it; document the disagreement in the Deferred table's reason column |
| The v2 deferred table grows > 20 rows | The feature was actually two features | Split spec.md into two separate feature folders; each gets its own AC list and scope cut |
| implementation-plan.md task count does not reduce proportionally | Tasks were not written against specific ACs | Trace each task back to its AC; if it serves a deferred AC, move it to the `## Deferred (v2)` section |

## Next

- [writing-first-spec](../writing-first-spec) — write a tight spec from scratch so the next feature starts with a manageable AC list.
- [sdd-for-solos](../sdd-for-solos) — run the full SDD cycle on the now-reduced feature.
- Once v1 ships and you have real user feedback, revisit the `## Out of scope (defer to v2)` table; promote ACs that users actually request.

## References

- [knowledge/solo/sdd/sdd-planning/spec-requirements](../../../knowledge/solo/sdd/sdd-planning/spec-requirements) — the AC atomicity and testability rules that determine whether an AC qualifies as a single Keep item or should be split into a Keep sub-AC and a Defer sub-AC.
- [knowledge/solo/sdd/sdd-planning/writing-specifications](../../../knowledge/solo/sdd/sdd-planning/writing-specifications) — the spec structure contract that defines where `## Out of scope (defer to v2)` sits relative to other spec sections and how the deferred table maps to implementation-plan tasks.
