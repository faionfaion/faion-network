<!-- purpose: Referral program design worksheet — value proposition, reward mechanics, offer ladder, fraud rules, tracking, compliance checklist. -->
<!-- consumes: product context, reward budget, legal/compliance constraints (GDPR/CASL/FTC) -->
<!-- produces: referral program design artefact -->
<!-- depends-on: none -->
<!-- token-budget-impact: ~250-500 tokens when loaded as context -->

# Referral Program Design: [Product]

## Value Proposition
Share [Product] with friends and both of you get <reward>.

## Mechanics
- Referred friend gets: [X — delivered at activation, not signup]
- Referrer gets: [Y — delivered at invitee activation, not signup]
- Reward trigger: invitee reaches <activation_milestone> within <reward_trigger> days

## Sharing Options
- [ ] Unique referral link
- [ ] Pre-written email (personalized with inviter name)
- [ ] Social share buttons (Twitter, LinkedIn)
- [ ] Copy referral code

## Offer Ladder
| Referrals | Referrer Reward |
|-----------|-----------------|
| 1 | <base_reward> |
| 5 | [mid-tier reward + badge] |
| 10 | <premium_reward> |

## Fraud Rules
- Maximum rewards per user: [N] per 12 months
- Eligibility: invitee must not be an existing user or past user
- Self-referral block: same IP or device fingerprint invalidates reward
- Reward timing: activation required (not signup)

## Tracking
- Dashboard shows: sent / pending / completed / fraud-blocked
- Rewards: auto-applied after activation milestone confirmed
- Invitee retention: D30 tracked vs organic D30 separately

## Compliance
- [ ] GDPR: referral emails sent only to explicit opt-ins
- [ ] CASL: Canadian contacts require express consent
- [ ] FTC: material disclosure if inviter receives compensation
