# Agent Integration — Viral Loops & Growth Mechanics

## When to use
- Designing or auditing a growth loop where user output (content, invites, embedded artifacts) creates distribution that brings new users.
- Choosing among loop types (inherent / WOM / incentivized / social / collaborative / content / embedded) for a new product or vertical.
- Strategic-level work: matching loop to product type, sizing the realistic K for the category, planning measurement infrastructure.
- Companion to `viral-optimization` (which is the *iterating* layer) and `growth-referral-programs` (one specific incentivized loop).

## When NOT to use
- Pre-PMF: weak product → weak inviter motivation → loop fizzles. Fix value, then design loops.
- Pure paid-acquisition or sales-led businesses where the unit economics already work — adding a viral loop adds complexity for marginal lift.
- Regulated categories (finance, health, gambling) where unsolicited shares can violate compliance (FTC endorsement rules, MiFID II, HIPAA).
- Products where the inviter pays a social cost to invite (sensitive niches) — virality there is anti-loyalty.

## Where it fails / limitations
- K > 1 is rare and unstable; designing for it leads to dark-pattern shares that backfire.
- Loop math assumes invitees behave like inviters — they often retain worse, especially in incentivized loops.
- "Embedded branding" loops (Made-with-X) decay as the brand becomes ambient; require continuous design refresh.
- Cross-platform attribution (web → mobile, email → app) is broken by ITP, mail-open prefetch, and iOS Mail Privacy Protection — your K may be under-counted by 30–60%.
- Forced sharing (gated content) drives short-term K but kills long-term retention and brand.

## Agentic workflow
Use subagents at design time, not at runtime. The flow: agent reads product brief → maps to loop-type taxonomy → drafts loop anatomy (action / artifact / distribution / motivation / friction) → estimates plausible K range from category benchmarks → proposes a measurement plan (events + funnel + cycle-time tracker). A human PM and growth lead approve before engineering. Iteration happens under `viral-optimization`.

### Recommended subagents
- `growth-marketer` (opus for strategic design, sonnet for drafts) — loop selection and design.
- `product-strategist` (opus) — match loop to product DNA and PMF stage.
- `data-analyst` (sonnet) — define K-funnel events and cycle-time measurement.
- `legal-reviewer` (opus) — flag CASL / GDPR / FTC issues in incentivized or contact-import loops.

### Prompt pattern
```
Input: product brief (what it does, who pays, ICP, current GTM)
Task: 1) recommend ONE primary loop type with a one-paragraph fit argument
      2) draft loop anatomy: action -> artifact -> distribution -> motivation -> friction
      3) estimate realistic K range citing 2 comparable products
      4) list 5 events to instrument before launch
Output: markdown using the README "Loop: <Name>" template
Forbidden: claiming K > 0.5 without a comparable consumer-social precedent
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `branch.io` CLI | Deferred-deeplink attribution for cross-platform invites | https://help.branch.io |
| `posthog` CLI | Funnel + cohort instrumentation for loop measurement | `npm i -g posthog-node` |
| `growthbook` CLI | A/B test loop variants once shipped | `npm i -g @growthbook/cli` |
| `viral-loops` API | Templated referral loop scaffolding | https://docs.viral-loops.com |
| `dbt-core` | Materialize K-factor models in warehouse | `pip install dbt-core` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Viral Loops | SaaS | Yes — REST | Templated campaigns: waitlist, referral, milestone |
| GrowSurf | SaaS | Yes — REST | Lightweight referral / waitlist |
| Friendbuy | SaaS | Yes — REST | Two-sided referral, fraud controls |
| ReferralCandy | SaaS | Yes — REST | Ecommerce referral, Shopify-native |
| Branch | SaaS | Yes — REST + SDKs | Invite link attribution across web + mobile |
| AppsFlyer / Adjust | SaaS | Yes — REST | Mobile attribution incl. SKAdNetwork |
| Loops.so / Customer.io | SaaS | Yes — REST | Trigger lifecycle messages from loop events |
| PostHog | OSS + SaaS | Yes — REST + HogQL | Funnel + retention for loop measurement |

## Templates & scripts
See the README's "Loop: [Name]" template and "Referral Program Design" template. For a back-of-envelope loop projection (compounding model), this 25-line script shows whether your assumed K + cycle yields self-sustaining growth:

```python
# loop_projection.py — naive compounding model
def project(starting_users, K, cycle_days, days):
    """K = invites_per_user * conversion_rate; per cycle."""
    cycles = days / cycle_days
    if K >= 1:
        # exponential
        return starting_users * (K ** cycles)
    # geometric series sum (decaying contribution)
    total = starting_users * (1 - K ** (cycles + 1)) / (1 - K)
    return total

for K in (0.1, 0.3, 0.5, 0.7, 1.0):
    n = project(1000, K, cycle_days=14, days=180)
    print(f"K={K:.2f}  cycle=14d  180d_users≈{n:,.0f}")
```

## Best practices
- Pick *one* primary loop and instrument it deeply before adding a second; multi-loop products without baseline K cannot debug regressions.
- Cycle time is a primary lever — halving cycle time roughly squares the compounded effect over a quarter.
- Embed branding in user output where it adds value to the recipient (link preview, watermark with credit) rather than as a tax.
- Tie inviter rewards to invitee value-realization, not invitee signup, to push fraud below noise.
- Treat the invitee landing page as a top-priority surface — most loops fail at conversion, not at sharing.
- Re-design loops every 12–18 months; users learn the pattern and `c` decays.

## AI-agent gotchas
- LLMs over-cite Dropbox / Spotify Wrapped / Notion as if any product can clone them. Force comparable-precedent matching by stage and category.
- "Inherent" virality is rare — agents will label collaborative-tool features as inherent when they are merely incentivized. Demand the inherent-loop test: "does the product fail to deliver core value without inviting someone?"
- Agents propose mechanics that violate platform TOS (auto-DM friends, contact upload without consent). Filter at template level.
- K-projection math depends on invitee retention; agent models that assume invitee behaves like inviter overstate compounding by 2–5×.
- Generated copy invents social proof ("join 100,000 people") that is factually wrong; numeric claims must be passed in, not produced.
- Cross-platform attribution gaps invalidate K reported by single-tool dashboards — instruct the agent to specify which tool measures which leg.

## References
- Andrew Chen, "What's your viral loop?" — https://andrewchen.com/whats-your-viral-loop
- Reforge, "Growth Loops are the new Funnels" — https://www.reforge.com/blog/growth-loops
- Adam Penenberg, "Viral Loop" (book)
- Jonah Berger, "Contagious: Why Things Catch On"
- David Skok, "Lessons learned: Viral marketing" — https://www.forentrepreneurs.com/lessons-learnt-viral-marketing/
- Lenny Rachitsky, "How the biggest consumer apps got their first 1000 users"
- Brian Balfour, "Why product-channel fit determines startup outcomes" — https://brianbalfour.com
