# Agent Integration — Churn Prevention

## When to use
- Monthly churn ≥3% on a paid SaaS / subscription product, churn analysis (`ops-churn-basics`) already done, root causes segmented.
- You have engagement events (login, feature use), payment events, and a writable lifecycle email tool (Customer.io / Intercom / Braze).
- Cancellation flow is owned by your product (you can ship a "save offer" page, dunning UI, win-back emails).
- At-risk segment is large enough (≥50 accounts/month) for an intervention to move the needle.

## When NOT to use
- B2C apps with no recurring revenue and no contact channel (e.g. anonymous web tools) — there is nobody to "save".
- Pre-product-market-fit: churn is a symptom of weak value, not weak retention ops. Fix the product first.
- Enterprise contracts with manual renewal — handled by AE/CS humans, not by this playbook.
- Free tier with high acquisition volume and zero LTV — saving free users wastes effort.

## Where it fails / limitations
- Save offers train customers to threaten cancellation to extract discounts; cap usage and watch repeat-saver rate.
- Dunning sequences without billing-tool integration (Stripe Smart Retries / Churnkey) recover only a fraction of involuntary churn.
- Health-score thresholds drift; a model trained on Q1 data misclassifies Q3 cohorts after product changes.
- Re-engagement emails to long-dormant users hurt sender reputation (low open + spam complaints) — segment by recency.
- Win-back sends to GDPR-deleted users will leak PII unless suppression lists are honored.

## Agentic workflow
Use Claude subagents to (1) score health daily, (2) author segmented save-offer and win-back copy, (3) propose dunning copy variants, and (4) summarize churn-reason exit surveys. Keep the agent off the actual send button — humans approve creative and offer economics; agents stage drafts and write to a campaign tool's "draft" status. The cycle is: pull events → classify reasons → match playbook → draft message → human reviews → ship.

### Recommended subagents
- `growth-marketer` (sonnet) — segment churn reasons, choose playbook, draft email per segment.
- `data-analyst` (sonnet) — compute health scores, build at-risk lists from warehouse.
- `copy-reviewer` (sonnet) — second pass for tone, claim accuracy, brand voice.
- `pricing-reviewer` (opus) — sanity-check save-offer economics (margin × accept rate × rebound).

### Prompt pattern
```
Input: at_risk_users.json (user_id, plan, mrr, last_login, churn_reason_pred, health_score)
Task: For each user, pick playbook from ops-churn-prevention/templates.md, draft email
Output: csv with [user_id, playbook_id, subject, body, suggested_offer]
Constraint: never offer >50% off, never extend trial >30d, never overlap two campaigns
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe` CLI | Inspect failed invoices, replay dunning webhooks | `brew install stripe/stripe-cli/stripe` |
| `churnkey` API | Cancel-flow save offers, dunning recovery | https://docs.churnkey.co |
| `customer.io` CLI | Trigger lifecycle campaigns from scripts | `npm i -g customerio-cli` |
| `dbt` | Build at-risk cohort models in warehouse | https://docs.getdbt.com |
| `posthog` CLI | Pull cohort definitions, user properties | `npm i -g posthog-node` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Churnkey | SaaS | Yes — REST API | Cancel-flow save offers, dunning, exit surveys |
| ProsperStack | SaaS | Yes — REST API | Cancel-flow alternative; A/B tests offers |
| Stripe Billing | SaaS | Yes — full API | Smart Retries, customer portal, dunning emails |
| Customer.io | SaaS | Yes — Track + App API | Behavioral lifecycle campaigns; agent writes drafts |
| Intercom | SaaS | Yes — REST API | In-app messages, exit surveys, save chat |
| Vitally / Totango | SaaS | Yes — REST API | Health scores, CSM playbooks for B2B |
| Pendo Engage | SaaS | Partial | In-app guides; API mostly for tracking, not auth |
| ChurnZero | SaaS | Partial | Enterprise CS platform; rich API but heavy |

## Templates & scripts
See `templates.md` for the Churn Prevention Playbook (early-warning triggers, save offers, win-back). For health scoring, this 30-line warehouse query is a working baseline:

```sql
-- weekly health-score snapshot
WITH activity AS (
  SELECT user_id,
         COUNT(*) FILTER (WHERE event_date >= CURRENT_DATE - 7)        AS logins_7d,
         COUNT(DISTINCT event_type) FILTER (WHERE event_date >= CURRENT_DATE - 30) AS features_30d,
         MAX(event_date)                                                AS last_seen
    FROM events
   GROUP BY 1
),
support AS (
  SELECT user_id,
         AVG(sentiment_score) AS support_sent
    FROM tickets
   WHERE created_at >= CURRENT_DATE - 60
   GROUP BY 1
)
SELECT u.user_id,
       LEAST(25, a.logins_7d * 5)             AS s_login,
       LEAST(25, a.features_30d * 3)          AS s_feature,
       COALESCE(s.support_sent, 0.5) * 25     AS s_support,
       LEAST(25, EXTRACT(DAY FROM AGE(u.signup_date)) / 30)  AS s_tenure,
       (LEAST(25, a.logins_7d * 5)
        + LEAST(25, a.features_30d * 3)
        + COALESCE(s.support_sent, 0.5) * 25
        + LEAST(25, EXTRACT(DAY FROM AGE(u.signup_date)) / 30))::int AS health
  FROM users u
  LEFT JOIN activity a USING (user_id)
  LEFT JOIN support  s USING (user_id);
```

## Best practices
- Tier the response by reason: price objections get a discount, value objections get a CSM call, feature gaps get a roadmap link — not a flat 50% off.
- Always run a holdout (10% no-treatment) on every save campaign; without it you cannot tell if the offer caused the save or natural reversion did.
- Cap save-offer eligibility (once per 12 months) and track repeat-savers — they are negative-LTV.
- Win-back at 30 and 90 days outperforms 7-day win-backs; the 7-day buyer rarely churned for a product reason.
- Tie dunning emails to specific decline codes (`insufficient_funds` vs `lost_card`) — generic "update card" loses recoverable revenue.
- Net Revenue Retention is the headline metric; raw churn % can mask expansion gains or losses.

## AI-agent gotchas
- Agents will happily invent generous offers ("60% off lifetime"). Hard-code offer ladders in templates and reject anything outside.
- LLMs hallucinate "user mentioned X" — feed only structured signals (events, ticket sentiment) and forbid quoting customer text the agent has not seen.
- Reason classification from free-text exit surveys needs human spot-checks; otherwise you optimize for misread reasons (e.g. "too expensive" tagged as "missing feature").
- Email send is a one-way action — keep the agent at draft creation only; gate send on a human approver or a hard rule (cohort size + economic envelope).
- Re-engagement to suppression-listed users will burn deliverability. The agent must read suppression status before drafting, not after.
- A/B-test result interpretation requires `statistics-application`; do not let an agent declare a winner on <14 days or <1k users per arm.

## References
- "Reducing Churn" — Lincoln Murphy, https://sixteenventures.com/customer-success-strategy
- Churnkey playbooks — https://churnkey.co/playbooks
- Stripe Billing Dunning best practices — https://stripe.com/docs/billing/revenue-recovery
- Brian Balfour, "Retention is the King of SaaS metrics" — https://brianbalfour.com/essays/retention-engagement-growth
- David Skok, "SaaS Metrics 2.0" — https://www.forentrepreneurs.com/saas-metrics-2/
