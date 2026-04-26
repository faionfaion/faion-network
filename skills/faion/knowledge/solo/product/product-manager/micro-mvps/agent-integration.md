# Agent Integration — Micro-MVPs

## When to use
- Validating one specific assumption (demand, willingness-to-pay, workflow fit) before committing engineering time.
- Pre-PMF stage where every shipped feature is a learning bet, not a delivery.
- Validating a new segment for an existing product (fake-door, smoke-test).
- Solo / 2-person team with limited capacity — micro-MVPs preserve runway.
- Founder is "in love with a feature" — a micro-MVP is the cheapest way to disprove the hypothesis.

## When NOT to use
- Post-PMF feature work for an established product where users expect polish — fake-door damages trust.
- Compliance, security, or infrastructure work — there is no demand to validate.
- Teams with no monitoring/instrumentation — you cannot learn from the experiment if you cannot measure.
- Brand-sensitive launches where being seen running an experiment is itself reputational risk.
- B2B enterprise sales cycles where "video demo" is table stakes, not a validation experiment.

## Where it fails / limitations
- Wizard-of-Oz scales to ~50 concurrent users; past that, manual operation collapses or you discover you are now running a service business.
- Fake-door / smoke-test data is noisy at <1000 visitors — you need real traffic to read the signal.
- Concierge MVPs distort feedback: users praise a hand-held experience that does not survive automation.
- Landing page demand signals over-index on novelty; "people clicked Sign Up" is not "people will pay."
- Ethical edge: if a fake-door collects emails and never delivers, you owe users a transparent unwinding.

## Agentic workflow
A hypothesis-extraction agent reads the product brief and surfaces the riskiest unverified assumption with a one-line falsifiability statement. An experiment-design agent picks the cheapest micro-MVP type (landing / video / fake-door / Wizard-of-Oz / concierge / smoke-test) matched to that assumption, plus a numeric success criterion set before launch. An asset-build agent generates the landing copy / fake-door UI / video script. After launch, a measurement agent reads analytics and answers a single question: "did the criterion clear?" Human owns the pivot/persevere/next-assumption call.

### Recommended subagents
- A hypothesis-extractor agent (Opus) — strategy work; ranking risky assumptions is high-leverage.
- A copy/asset-build agent (Sonnet) — writes the landing / video script / FAQ for the experiment.
- An analytics-reader agent — connects to Plausible / Mixpanel / GA4 and reports against the pre-registered criterion.
- `faion-mlp-impl-planner-agent` — once an experiment validates, plans the real build.

### Prompt pattern
```
Product brief: <brief>. List 3-5 unverified assumptions ranked by:
- Falsifiability (can we test it cheaply?)
- Impact if wrong (would the product fail?)
Output: ranked list, with the riskiest at top.
For #1, propose 2 candidate experiments (type, cost in days, success criterion).
The success criterion must be a number set BEFORE running the experiment.
```

```
For experiment <name> with success criterion <metric>=<threshold>:
Generate the minimum viable assets:
- Headline (max 12 words)
- Sub-headline (one sentence stating the outcome, not the feature)
- 3-bullet value prop
- Single CTA copy
Reject any output that names internal features rather than user outcomes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `vercel` / `netlify` / `cloudflare pages` CLI | Ship landing page in <1 hour | https://vercel.com/docs/cli |
| `plausible` / `umami` / `simpleanalytics` API | Measure landing-page conversion | https://plausible.io/docs |
| `mixpanel-cli` / Amplitude API | Read funnel data for fake-door experiments | https://docs.mixpanel.com |
| `airtable` CLI / API | Concierge MVP backend with no engineering | https://airtable.com/api |
| `tally` / `typeform` API | Demand-validation forms with logic | https://tally.so/help/developer-resources |
| `loom` (manual) + `ffmpeg` | Video MVP — record + trim + caption | https://ffmpeg.org |
| `posthog` self-hosted | OSS analytics + session replay for behavioral signal | https://posthog.com/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Carrd | SaaS | Limited (no API) | Cheapest one-page landing builder. |
| Framer / Webflow | SaaS | Yes (CMS API) | Higher-fidelity landing; good for fake-door. |
| Tally | SaaS | Yes (API + webhooks) | Free demand-collection forms. |
| Typeform | SaaS | Yes (REST API) | Higher conversion for long demand surveys. |
| Airtable | SaaS | Yes (REST API) | Concierge MVP backend; humans operate the workflow. |
| Zapier / Make | SaaS | Yes (webhooks) | Automate concierge handoffs without writing code. |
| Stripe Payment Links | SaaS | Yes (REST API) | Smoke-test pricing without building checkout. |
| PostHog Cloud | SaaS / OSS | Yes (REST API) | Behavioral analytics + session replay; reads cleanly for agents. |
| Loom | SaaS | Limited | Video MVP host; share-link analytics suffice. |

## Templates & scripts
The `templates.md` lists experiment-card and pre-registration formats. Inline minimal pre-registration block:

```yaml
# experiment.yaml — commit BEFORE launching the micro-MVP
hypothesis: "Solo PMs will pay $20/mo for AI-generated PRDs"
type: smoke_test  # landing | video | fake_door | wizard_of_oz | concierge | smoke_test
duration_days: 7
traffic_source: "twitter + ph upcoming page"
success_criterion:
  metric: "checkout_clicks / unique_visitors"
  threshold: 0.05  # 5% click-to-pay rate
  min_visitors: 500
ethical_unwind:
  if_fail: "redirect signups to a 'product not built yet' page with refund offer"
decision_rule:
  pass: "build feature behind feature flag, ship to 10 users"
  fail: "drop hypothesis, move to assumption #2"
  inconclusive: "extend by 7 days OR change traffic source, max 1 extension"
```

## Best practices
- Pre-register the success criterion. If you decide the threshold after seeing the data, you are post-hoc rationalizing.
- Cap experiment cost at 1 week. If a "micro" MVP takes longer, it is not micro.
- Plan the ethical unwind before launch — what happens to the 200 emails on a fake-door waitlist?
- One assumption per experiment. Compound experiments yield ambiguous results.
- The traffic source matters more than the asset. Same landing page hits 10% on Hacker News and 0.5% on cold ads.
- Smoke-test pricing with a Stripe Payment Link before building checkout — the "credit-card moment" is the only reliable willingness-to-pay signal.
- After 3 failed micro-MVPs on the same problem space, drop the problem space, not the experiment design.

## AI-agent gotchas
- LLMs ship "validation theatre" — beautifully written landing pages with no real distribution plan. Force the prompt to include a traffic-source section.
- Models hallucinate plausible conversion-rate benchmarks ("industry standard is 8%"). Require citation or omit; otherwise the success criterion is anchored on fiction.
- Agents will inflate the asset bundle (case studies, logos, testimonials) for a 1-week experiment. Cap copy length explicitly.
- Post-experiment, agents have a strong bias to declare "inconclusive, extend." Force the decision rule with a hard cap (e.g. max 1 extension).
- Human-in-loop checkpoint: pre-registration commit before any traffic touches the asset. Agents can draft, humans must approve.
- Human-in-loop checkpoint: ethical unwind plan must be human-signed, especially for fake-door experiments that collect data.
- Do not let the agent run the post-mortem alone — it tends to weave a coherent narrative regardless of result, masking learning.

## References
- Steve Blank, "The Four Steps to the Epiphany" — assumption-mapping foundation.
- Eric Ries, "The Lean Startup" — Wizard-of-Oz, concierge, smoke-test definitions.
- Drew Houston / Dropbox 3-minute video MVP case: https://www.lennysnewsletter.com/p/lessons-from-dropbox
- IDEO "Tiny Tests" framework: https://www.ideou.com/blogs/inspiration/the-power-of-tiny-tests
- Reforge "Pre-mortems and pre-registration": https://www.reforge.com/blog
