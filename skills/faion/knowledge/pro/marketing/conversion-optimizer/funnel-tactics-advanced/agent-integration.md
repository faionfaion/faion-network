# Agent Integration — Funnel Optimization Tactics (Advanced)

## When to use
- After basics tactics are exhausted: industry-specific drops (SaaS / Ecom / Mobile) need targeted plays.
- Building personalization rules by traffic source, geo, device, returning-vs-new, or stated user intent.
- Designing exit-intent + retargeting flows (email + ad) that recover abandoning users with measured uplift.
- Producing an ICE-prioritized advanced experiment backlog where multiple high-impact tests compete for the same surface.

## When NOT to use
- Foundational quick wins (route to `funnel-tactics-basics`).
- Funnel mapping, diagnosis, ICE rubric (route to `funnel-basics-framework`).
- Benchmarks and worked examples (route to `funnel-basics-examples`).
- Pre-traffic products — personalization needs ≥1K segmented sessions/week to be measurable.

## Where it fails / limitations
- Industry "Biggest drops" bands are aggregate; subverticals (DevTools vs HR-tech vs PLG SaaS) deviate substantially.
- Personalization lifts (+15–40%) assume working segmentation and good baseline copy — bad copy personalized doesn't beat good copy generic.
- The exit-intent JS sketch is conceptually correct but real implementations need debouncing, frequency caps, mobile-tap-out detection, and consent gates (GDPR/ePrivacy).
- Retargeting tables ignore creative fatigue and frequency caps; ad-retargeting CVR collapses after ~10 impressions to the same user.
- ICE matrix encourages local optima — agents must guard against shipping 10 high-ICE tweaks that conflict.

## Agentic workflow
An advanced-tactics agent runs after a leak is diagnosed and basics tactics are stale. The orchestrator passes (industry, segment, current rate, baseline tactics already shipped). A `personalization-rule-builder` produces segment-specific variants, an `exit-intent-designer` generates the trigger spec + frequency caps, a `retargeting-orchestrator` schedules cross-channel follow-ups (Klaviyo email + Meta/Google retargeting), and a `tracking-spec-writer` ensures every variant is instrumented with the README's "essential events". Variants flow to A/B test platform via PR; nothing auto-publishes.

### Recommended subagents
- `industry-pattern-matcher` — maps a product to the README's SaaS / Ecom / Mobile patterns and surfaces the matching tactic list.
- `personalization-rule-builder` — emits segment → variant rule JSON for the personalization platform.
- `exit-intent-designer` — produces a debounced, frequency-capped, mobile-aware exit-intent spec.
- `retargeting-orchestrator` — schedules email + ad retargeting per the README timing table (immediate / 24h / 1–7d).
- `tracking-spec-writer` — emits the analytics event spec from the "Essential events" snippet.

### Prompt pattern
```
You are personalization-rule-builder. Read knowledge/pro/marketing/conversion-optimizer/funnel-tactics-advanced/README.md.
Input: { surface, segments: ["traffic_source","geo","device","returning","intent"], variants_max: 4 }.
Output JSON rules:
[{ segment_predicate, variant_id, copy_changes, asset_changes, expected_lift_band, fallback }].
Cap variants at 4 per surface; require explicit fallback to control.
```

```
You are exit-intent-designer. Generate a spec:
{ trigger: { desktop: "mouse_leave_top", mobile: "scroll_up_velocity OR back_button" },
  frequency_cap: "1 per 7 days per device",
  consent_gate: "GDPR + ePrivacy required",
  offer, cta, dismiss_behavior, success_metric, sample_size }.
Reject any spec without consent gating.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dynamic-yield` / `mutiny` API | Server-side personalization rule deployment | https://www.dynamicyield.com/api/ |
| `optimizely` Personalization API | Targeted experiences by segment | https://docs.developers.optimizely.com/ |
| `growthbook` | OSS A/B + targeted attributes | https://docs.growthbook.io/features/targeting |
| `optinmonster` API | Exit-intent campaigns CRUD | https://api.optinmonster.com/ |
| `klaviyo` API | Cart-abandonment + retargeting email flows | https://developers.klaviyo.com/ |
| `meta` Marketing API | Retargeting custom audiences | https://developers.facebook.com/docs/marketing-apis/ |
| `google-ads` API | Search/display retargeting | https://developers.google.com/google-ads/api/docs/start |
| `segment` / `rudderstack` | Event routing + identity stitching for personalization | https://segment.com/docs/connections/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mutiny / Dynamic Yield | SaaS | Yes | Server + edge personalization |
| Optimizely / VWO | SaaS | Yes | A/B + targeted experiences |
| GrowthBook | OSS | Yes | Self-hosted, agent-controllable |
| OptinMonster / Sleeknote | SaaS | Partial | Exit-intent specialty |
| Klaviyo / Customer.io / Iterable | SaaS | Yes | Email retargeting + automation |
| Meta Ads / Google Ads / TikTok Ads | SaaS | Yes — with auth scopes | Ad retargeting; agents need OAuth + budget guardrails |
| AdRoll / RollWorks | SaaS | Partial | Retargeting orchestration across channels |
| Segment / RudderStack | SaaS / OSS | Yes | Event pipeline; required for clean personalization |

## Templates & scripts
Inline exit-intent helper that respects mobile + consent (extends README's JS sketch):

```javascript
// exit_intent.js — production-grade extension of the README sketch
const KEY = "exitIntentShown:v1";
const CAP_DAYS = 7;

function withinCap() {
  const last = Number(localStorage.getItem(KEY) || 0);
  return Date.now() - last < CAP_DAYS * 86_400_000;
}

function ensureConsent() {
  return window.__consent?.marketing === true; // CMP integration
}

function showExitIntent(opts) {
  if (!ensureConsent() || withinCap() || opts.dismissed || opts.converted) return;
  localStorage.setItem(KEY, String(Date.now()));
  opts.render();
}

if (matchMedia("(pointer: fine)").matches) {
  document.addEventListener("mouseout", (e) => {
    if (!e.relatedTarget && e.clientY <= 0) showExitIntent(window.__exitOpts);
  });
} else {
  // Mobile: detect rapid scroll-up + back-button
  let lastY = window.scrollY, lastT = Date.now();
  window.addEventListener("scroll", () => {
    const dy = window.scrollY - lastY, dt = Date.now() - lastT;
    if (dy < -300 && dt < 400) showExitIntent(window.__exitOpts);
    lastY = window.scrollY; lastT = Date.now();
  }, { passive: true });
  window.addEventListener("popstate", () => showExitIntent(window.__exitOpts));
}
```

See `templates.md` (industry-specific tactic checklists) and `examples.md` (worked SaaS / Ecom / Mobile cases) in this directory.

## Best practices
- Anchor every personalization rule to a measurable segment and a fallback to control; orphan rules silently degrade.
- Cap concurrent personalization variants per surface at 4 — beyond that, sample sizes split too thin for significance.
- Match ad-creative message to landing-page hero precisely; "scent" mismatch wipes the +15–30% traffic-source lift.
- Run exit-intent ONCE per device per 7 days; the README warns about user annoyance — agents must enforce frequency caps.
- For retargeting, sequence offers progressively (reminder → social proof → discount) over 7 days; don't lead with discount.
- Pair every advanced tactic with the basics tactic it depends on — exit-intent on a slow page wastes the recovery.
- Track creative fatigue: rotate retargeting assets every ~2 weeks or after impressions/user > 10.
- For mobile apps, route ASO + permission-prompt-delay before in-app onboarding tactics.

## AI-agent gotchas
- LLMs over-personalize on weak segments; require minimum sample (e.g., ≥1000 sessions/segment/week) before activating a rule.
- Auto-generated personalization copy will leak segment names ("Hi enterprise visitor!") — explicitly forbid surfacing internal segment labels.
- Exit-intent on mobile requires careful detection; agents that copy the desktop `mouseleave` pattern verbatim ship broken UX.
- Retargeting to users who already converted is a brand-damage class bug; agents must always read the suppression list (paying customers, recent purchasers, opt-outs).
- Ad-spend automation requires a hard budget cap; never let the agent push live ad-set budget mutations without a per-day ceiling.
- ICE scoring at this tier inflates "Confidence" unfairly; force the agent to cite peer benchmarks or own past wins for any C ≥ 7.
- Don't ship personalization without a consent gate (GDPR/ePrivacy/CCPA); the README's JS sketch lacks one — agents must add it.
- Agents conflate "personalization" with "manipulation" (dark patterns, fake urgency); enforce a brand-policy filter on outputs.

## References
- `README.md` (this directory)
- Reforge growth-loops + advanced funnel — https://www.reforge.com/blog/growth-loops
- Dynamic Yield personalization lessons — https://www.dynamicyield.com/lesson/personalization-strategies/
- OptinMonster exit-intent best practices — https://optinmonster.com/exit-intent-popups/
- AdRoll retargeting guide — https://www.adroll.com/guides/retargeting
- GrowthHackers ICE prioritization — https://growthhackers.com/growth-studies/the-ice-score-prioritization-framework
