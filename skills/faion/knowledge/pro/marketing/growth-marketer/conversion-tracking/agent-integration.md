# Agent Integration — Conversion Tracking

## When to use
- Pre-launch: setting up GA4 + a privacy-friendly counter (Plausible/Fathom) and a server-side event log before the first user.
- Need a single source-of-truth for conversion events to back A/B tests, paid-channel ROAS, lifecycle messaging, and exec dashboards.
- Replatforming or migrating analytics — codifying the event schema in version control prevents lossy reinstrumentation.
- Implementing a SaaS funnel (signup → activation → trial → paid → expansion) with consistent naming across web, app, and backend.

## When NOT to use
- Pure 1:1 sales with <100 prospects/month — manual CRM tracking outperforms event-stream analytics.
- Pre-launch landing-page test where simple sign-up form + email tool already gives the answer.
- Highly regulated environments (healthcare PHI, child-targeted services with COPPA) without a privacy/legal review of the event payloads first.
- When you can't commit to maintaining the schema; broken events are worse than no events.

## Where it fails / limitations
- Client-side tracking is lossy — ad blockers, ITP, ETP, iOS limit-ad-tracking remove 20-40% of GA4 events. Plan for server-side reconciliation.
- Naming drift: same event tracked as `signup`, `Sign Up`, `user_signup` across team → analytics chaos. Enforce a registry.
- Currency / value units: mixing cents and dollars across `purchase` events corrupts revenue reporting silently.
- iOS/SKAN limits + GDPR consent gating mean some events have null user IDs; aggregate-only metrics for unconsented sessions.
- Funnel exploration in GA4 is limited to predefined steps; complex multi-touch journeys need warehouse + SQL.

## Agentic workflow
Subagents are excellent at producing the event-schema spec, generating typed wrappers, and reviewing PRs that add new tracking calls. The privacy-impact assessment, consent flow, and final cookie configuration stay with humans + privacy/legal. Pipeline: schema spec (agent draft + human review) → codegen typed event SDK (agent) → instrumentation PRs (agent assist) → schema validation in CI (agent rules) → dashboard build (agent + analytics tool) → quarterly hygiene audit (agent).

### Recommended subagents
- `general-purpose` — generate typed event-schema TypeScript/Python wrappers from a YAML spec; verify event-name registry consistency.
- `faion-sdd-executor-agent` — drive instrumentation tasks across PRs with quality gates (every new event references the registry).
- Custom `analytics-qa-agent` (build): scrapes git diff for `gtag()` / `plausible()` / `track()` calls and verifies registry membership + payload schema.

### Prompt pattern
- "Given this funnel description (signup → email-verify → first-action → paid), produce: (1) YAML event registry with required props, (2) TypeScript wrapper with one function per event, (3) GA4 + Plausible call inside each."
- "Audit this PR for new tracking calls. For each call, check: registered name? all required props? value in cents or dollars consistent with registry? Output table: file, line, event, status, fix."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gtm-cli` (community) | Manage GTM containers via API | https://developers.google.com/tag-platform/tag-manager/api/v2 |
| `ga4-admin` Python SDK | Configure conversion events | `pip install google-analytics-admin` |
| Plausible API | Pull realtime aggregated metrics | https://plausible.io/docs/stats-api |
| `segment` CLI | Test event-payload shape against Segment | `npm i -g @segmentio/cli` |
| RudderStack OSS | Self-host event router (open-source Segment alternative) | https://rudderstack.com |
| `mitmproxy` | Inspect outbound analytics calls during QA | `pip install mitmproxy` |
| Snowplow Mini | Local end-to-end event-pipeline testbed | https://docs.snowplow.io |
| `dbt` | Model events into funnels in warehouse | `pip install dbt-core` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GA4 | SaaS | API yes | Free, default web analytics |
| Google Tag Manager | SaaS | API yes | Tag deployment without code changes |
| Plausible | SaaS / OSS | API yes | Privacy-friendly, no cookies |
| Fathom Analytics | SaaS | API yes | Plausible alternative |
| Mixpanel | SaaS | API yes | Product analytics + funnels |
| Amplitude | SaaS | API yes | Product analytics + cohort retention |
| Heap | SaaS | API yes | Auto-capture |
| PostHog | SaaS / OSS | API yes | Self-host product analytics |
| Segment | SaaS | API yes | CDP / event router |
| RudderStack | SaaS / OSS | API yes | OSS Segment alternative |
| Snowplow | OSS | API yes | Enterprise-grade event pipeline |
| Stripe | SaaS | API yes | Server-side `purchase` source-of-truth |
| Meta CAPI / Google Ads Enhanced Conversions | SaaS | API yes | Server-side conversion uploads to ad networks |

## Templates & scripts
The methodology already inlines a `FunnelTracker` JS class. Inline event-registry validator:

```python
# validate_events.py — fail CI if any tracking call uses unregistered event name
import re, sys, yaml, pathlib

REG = yaml.safe_load(open("events.yml"))  # {event_name: [required_props]}
PATTERN = re.compile(r"""(?:gtag\('event',\s*|plausible\(|track\()\s*['"]([\w_]+)['"]""")

bad = []
for path in pathlib.Path("src").rglob("*.{ts,tsx,js,jsx}"):
    for m in PATTERN.finditer(path.read_text()):
        name = m.group(1)
        if name not in REG:
            bad.append(f"{path}: unregistered event '{name}'")

if bad:
    print("\n".join(bad)); sys.exit(1)
```

## Best practices
- Maintain a versioned event registry (YAML/JSON) checked into the repo; treat schema changes like API changes.
- Use snake_case for event names + props, never mix with camelCase mid-project; consistency saves hours in dashboards.
- Always store value in a single unit (recommend integer cents) and document it; mixed units corrupt revenue charts silently.
- Implement server-side `purchase` events from Stripe webhooks — client-side `purchase` is the most fraud-prone, lossy event.
- Pair each conversion with a user-property update (`plan: pro`, `signup_source: organic`) so cohorting works without joins.
- Pipe Stripe → Meta CAPI / Google Ads Enhanced Conversions for >20% recovery of lost client-side attribution.
- Treat A/B test exposure events as first-class: every variant rendering emits an `experiment_exposure` event; without it, post-hoc analysis is unreliable.

## AI-agent gotchas
- LLMs invent GA4 event names — `signup_started` vs `start_sign_up` vs `signup` interchangeably; pin the agent to your registry file.
- Property bloat: agent will add 10 optional props "for completeness"; downstream warehouses charge per row × column.
- PII risk: agent may suggest tracking `email` or `full_name` as event props, breaking GDPR/CCPA. Ban a list of fields explicitly in the prompt.
- Currency unit mistakes: agent oscillates between dollars and cents; force `value_cents` (integer) as canonical.
- Consent gating: agent suggests firing all events without checking CMP state; require `consentMode` checks before dispatch.
- Test mode: prompt should include `if (NODE_ENV !== 'production') return;` guard for tests; otherwise CI burns through GA quotas.
- Event-name renames break dashboards silently — agent should always emit a deprecation alias for one release.

## References
- GA4 Recommended Events: https://support.google.com/analytics/answer/9267735
- GA4 Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- Plausible custom events: https://plausible.io/docs/custom-event-goals
- Mixpanel event-tracking guide: https://docs.mixpanel.com/docs/tracking-events
- PostHog data model: https://posthog.com/docs/data
- Snowplow tracker design principles: https://docs.snowplow.io
- Avo (eventschema-as-code): https://www.avo.app
