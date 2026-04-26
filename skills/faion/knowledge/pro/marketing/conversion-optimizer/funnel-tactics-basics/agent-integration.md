# Agent Integration — Funnel Optimization Tactics (Basics)

## When to use
- Funnel analysis (via `funnel-basics-framework`) has surfaced a leak; you need a quick-win tactic catalog mapped to the leak's stage.
- Producing a 30-day CRO sprint backlog: form-field reduction, button contrast, social-proof placement, copy simplification.
- Auditing landing pages, signup forms, checkouts, and onboarding screens against a single checklist before a launch.
- Generating ICE-scored hypotheses for A/B tests where each hypothesis can cite a quantified lift band from this README.

## When NOT to use
- Strategy / model-selection work (route to `plg-basics`).
- Industry-specific or personalization tactics (route to `funnel-tactics-advanced`).
- Funnel mapping, diagnosis, or process work (route to `funnel-basics-framework`).
- Brand or positioning work — this README assumes positioning is fixed and only the conversion mechanism is being tuned.

## Where it fails / limitations
- Lift bands ("+10–25%") are aggregate study averages from Formstack / ConversionXL / HubSpot — agents must reframe them as priors, not forecasts.
- Form-field "+220% from 1–3 fields" is a ceiling case from B2C lead gen; B2B SaaS sees +30–80% typically.
- Tactics list is timeless but the underlying tooling (Optimizely pricing, Hotjar features, page-speed targets) drifts; verify before recommending stack-specific moves.
- Mobile-vs-desktop and segment-specific lifts can invert; a tactic that lifts desktop can drop mobile. The README's "Ignoring mobile" warning is real — agents must always segment.

## Agentic workflow
A funnel-tactic agent runs as a recommender given a single drop-off step. The orchestrator passes (stage, current rate, segment, current UX snapshot), the subagent retrieves matching tactics from this README, scores each with ICE, and emits a ranked test backlog plus a "Stage-Specific Optimization Checklist" delta showing which checklist items the current page violates. A copy subagent then rewrites the page following the "Simplify Copy" rules. All ships go through PR + experiment-flag review.

### Recommended subagents
- `funnel-tactic-recommender` — input: stage + current rate + UX snapshot; output: ranked tactic JSON with ICE.
- `cro-checklist-auditor` — runs the four "Stage-Specific Optimization Checklist" sections against a URL/screenshot; reports violations.
- `cro-copy-simplifier` — rewrites long, jargon-heavy copy per the README's before/after example.
- Hand-off to `faion-growth-agent` (named in README's Agent Selection) for execution.

### Prompt pattern
```
You are funnel-tactic-recommender. Read knowledge/pro/marketing/conversion-optimizer/funnel-tactics-basics/README.md.
Input: { stage: "tof|mof|bof|onboarding", current_rate: 0.XX, segment, ux_snapshot }.
Output JSON array:
[{ tactic, source_section, expected_lift_band, hypothesis, ice: {i,c,e}, instrumentation, mobile_risk: bool }].
Cap at 5 tactics; ICE >= 18 only.
```

```
You are cro-checklist-auditor. Walk through the four Stage-Specific checklists in this README.
Output a JSON object: {<page>: {<item>: pass|fail|n/a, evidence: "<one-line>"}}.
Do not invent items not in the README.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` CLI | Page-speed + a11y audit (load-time tactic) | `npm i -g @lhci/cli` |
| `pagespeed-insights` API | Core Web Vitals + bot-friendly speed scoring | https://developers.google.com/speed/docs/insights/v5/get-started |
| `axe-core` CLI | Form a11y + label/contrast checks | `npm i -g @axe-core/cli` |
| `posthog` / `mixpanel` / `amplitude` | Funnel measurement, before/after lift validation | https://posthog.com/docs/api |
| `growthbook` / `flagsmith` | OSS A/B test infra; agents can wire flags + analysis | https://docs.growthbook.io/ |
| `playwright` / `puppeteer` | Headless screenshot + form-field counter for auditor | https://playwright.dev/ |
| `cypress` | Form-flow regression to ensure tactics don't break checkout | https://docs.cypress.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hotjar / FullStory / LogRocket | SaaS | Partial — read APIs limited | Session recordings inform tactic choice but agents rarely drive |
| Crazy Egg | SaaS | Partial | Heatmaps for "Improve Button Contrast" tactic |
| Optimizely / VWO | SaaS | Yes — full Experiment API | Wire test variants + statistical-significance checks |
| GrowthBook | OSS | Yes | Self-hosted A/B testing, agent-friendly |
| Unbounce / Instapage | SaaS | Yes — landing-page CRUD API | Agents can spin variants for landing-page tactics |
| Stripe | SaaS | Yes | "Multiple payment options" tactic; Apple/Google Pay via Payment Element |
| Cloudflare / Fastly | SaaS | Yes | Speed-up tactic: edge cache + image optimization |

## Templates & scripts
Inline auditor agents can call to count form fields and CTAs from a URL:

```python
# form_audit.py — quick checklist auditor for the Signup Form section
from playwright.sync_api import sync_playwright

def audit_signup(url: str) -> dict:
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto(url, wait_until="networkidle")
        fields = page.locator("input:not([type=hidden]), textarea, select").count()
        social_login = page.locator("[data-provider], button:has-text(/google|github|apple/i)").count() > 0
        ctas = page.locator("button[type=submit], a.cta, button.cta").count()
        progress = page.locator("[role=progressbar], .progress").count() > 0
        load_ms = page.evaluate("performance.timing.loadEventEnd - performance.timing.navigationStart")
    return {
        "fields_count": fields,
        "fields_pass": fields <= 3,
        "social_login": social_login,
        "single_cta": ctas == 1,
        "progress_indicator": progress,
        "load_ms": load_ms,
        "load_pass": load_ms <= 3000,
    }
```

See `templates.md` and `examples.md` in this directory for the four checklists (Landing Page / Signup Form / Checkout / Onboarding) the auditor should iterate over.

## Best practices
- Always rank tactics by ICE; never ship a backlog where everything has equal priority.
- Pin every tactic to a measurable stage event before recommending — "improve copy" without a target metric is rejected.
- Run the auditor once per quarter against top 5 funnel pages; track the checklist pass-rate as a KPI.
- For form-field tactics, gather the trimmed fields after signup via progressive profiling — never ship the reduction without the recovery plan.
- For load-time wins, measure CWV LCP/INP, not just "page load"; the README's 0–2s/3s/5s table maps to LCP.
- Always test tactics on mobile + desktop separately; a "Single, clear CTA" tactic must pass both viewports.
- Cap concurrent A/B tests on the same page to one — the README's "Testing too many things" warning is enforced as a hard rule.

## AI-agent gotchas
- LLMs will recommend "remove all form fields" — clamp the recommendation to "minimum required for fulfillment + email verification".
- Auto-generated copy will revert to "powerful, modern, enterprise-grade" tokens; force a banned-words filter.
- The "Urgency/scarcity" tactic must be honest (real stock, real timer); agents must NOT generate fake countdowns or stock numbers — legal + brand risk.
- Exit-intent popups conflict with mobile UX (no mouse-leave); agent must restrict the recommendation to desktop.
- Heatmap-driven button contrast advice requires real data; agents should refuse the recommendation if no heatmap source is provided.
- Don't auto-publish landing-page variants — every variant ship goes through review + experiment flag.
- Statistical significance: agents must enforce a minimum sample (e.g., 95% confidence, MDE 5%) before reporting any "winner"; reject early-stop temptation.

## References
- `README.md` (this directory)
- Formstack form-field study — https://www.formstack.com/resources/form-conversion-study
- ConversionXL Social Proof guide — https://conversionxl.com/blog/social-proof/
- Google Web Performance Budgets — https://web.dev/performance-budgets-101/
- Unbounce CRO benchmarks — https://unbounce.com/conversion-rate-optimization/conversion-benchmark-report/
- HubSpot CRO quick wins — https://blog.hubspot.com/marketing/conversion-rate-optimization
