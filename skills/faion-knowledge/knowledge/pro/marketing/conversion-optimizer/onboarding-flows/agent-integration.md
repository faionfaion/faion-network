# Agent Integration — User Onboarding Flow Design

## When to use
- Designing or rebuilding the first-run experience for a SaaS web/mobile product where activation rate is below 50%.
- Choosing between onboarding patterns (template-first, wizard, interactive tutorial, self-serve, concierge) based on segment intent.
- Reducing onboarding step count without losing necessary configuration steps.
- Adding progressive disclosure, contextual tooltips, and progress checklists to an existing flow.
- Coordinating in-app guidance with a triggered email sequence for the same activation goal.

## When NOT to use
- The activation event is not yet defined; pause and run activation analysis first.
- Pre-PMF startups where onboarding optimization masks a value-prop problem.
- Highly bespoke, deal-by-deal enterprise products where every onboarding is concierge — focus on Customer Success playbooks instead.
- Products with extremely simple value (no setup needed); over-engineered onboarding hurts more than it helps.

## Where it fails / limitations
- Generic onboarding for all segments — individual users get team setup screens, evaluators get power-user prompts. Drop-off compounds.
- Tooltip tour overload: 8+ tooltips create dismiss-and-forget behavior; users miss everything.
- Required profile completion blocks the activation event and tanks Day-0 retention.
- Empty states with no concrete action ("create your first project" with no template) make the user think before they have context.
- Email sequences that fire after activation has occurred (no listener for the activation event) produce embarrassing "still need help?" messages to active users.
- A/B testing onboarding without segmentation conflates wins from segment X with losses from segment Y.

## Agentic workflow
A Claude subagent can: (1) interview the team to extract user-segment intents and propose onboarding patterns per segment; (2) draft the critical-path step list with each step's required vs optional status; (3) write microcopy for tooltips, empty states, and progress checklists; (4) draft the triggered email sequence keyed to the same activation event; (5) read funnel drop-off data and propose 3 A/B tests per critical step. The agent should NOT auto-publish copy to production CMS — operator approves each microcopy string.

### Recommended subagents
- `faion-growth-agent` (referenced in README) — sonnet for flow design and microcopy; opus for cross-segment strategy and pattern selection.
- A `microcopy-agent` (suggested) — haiku for tooltip / empty state / button label generation under tight character limits.
- `faion-content-marketer` — for the email sequence accompanying the in-app flow.
- `faion-sdd-executor-agent` — model the onboarding redesign as an SDD spec with measurable activation targets.

### Prompt pattern
```
Segments: <individual / team-admin / evaluator / power-user>. Activation
event: <"created 1 project with 3+ tasks">. Constraint: ≤4 critical-path
steps before activation. Output a per-segment flow with step name, UI
pattern, copy, completion criterion, and which segment can skip it.
```

```
Tooltip microcopy: 5 candidates each ≤80 chars for these UI anchors:
{create-project, invite-member, connect-integration, settings, save}.
Voice: warm, direct, no exclamations, no emojis. Mark the strongest pick.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog-cli` | Query funnel + drop-off per step | https://posthog.com/docs/cli |
| `growthbook` | Run flow A/B tests with feature flags | https://www.growthbook.io/ |
| `dbt` | Define activation event + funnel models | https://docs.getdbt.com/ |
| `playwright` / `cypress` | Snapshot the new flow for visual review | https://playwright.dev/ , https://www.cypress.io/ |
| `figma-cli` (community) | Pull mocks of onboarding screens for context | https://www.figma.com/developers |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Appcues | SaaS | Yes (API) | No-code onboarding flows, segments, A/B |
| Pendo | SaaS | Yes (API) | Onboarding + product analytics in one |
| Userflow | SaaS | Yes (API) | Lightweight, developer-friendly |
| Userpilot | SaaS | Yes (API) | Mid-market alternative with checklists |
| Chameleon | SaaS | Yes (API) | UI walkthroughs and microsurveys |
| Whatfix | SaaS | Yes (API) | Enterprise-grade in-app guidance |
| Customer.io | SaaS | Yes (API) | Behavioral email sequences for activation |
| Loops | SaaS | Yes (API) | Modern email sequences with event triggers |
| Intercom | SaaS | Yes (API) | Messenger + email + product tours |
| Trayce / Frigade | SaaS | Yes (API) | Headless onboarding components for devs |
| FullStory / Hotjar | SaaS | Yes (API) | Watch real users go through the flow |
| Maze | SaaS | Yes (API) | Unmoderated tests of new flow concepts |

## Templates & scripts
See `templates.md` for welcome modal, tooltip tour, progress checklist, and empty state templates. Inline minimal flow validator:

```bash
#!/usr/bin/env bash
# validate-flow.sh — fail if any onboarding step has no event mapping.
# Inputs: flow.yaml (steps[].id, .event, .required), events.yaml (defined events).
set -euo pipefail
yq -r '.steps[] | "\(.id) \(.event)"' flow.yaml | while read id evt; do
  yq -e ".events[] | select(.name == \"$evt\")" events.yaml >/dev/null \
    || { echo "MISSING event: step=$id event=$evt"; exit 1; }
done
echo "OK: all flow steps map to defined events."
```

## Best practices
- Define the activation event before designing the flow. Without it, optimization has no target.
- Cap the critical path at 3-5 steps. Move everything else behind contextual triggers ("you used X → here is how to configure it").
- Segment at signup with one question; route to per-segment flows. Generic flow + 1 question outperforms perfectly generic flow.
- Pre-fill defaults (timezone, language, plan) wherever inferable; stop asking.
- Pair each in-app step with a matching email — but kill the email when the user activates. No exceptions.
- Run a no-onboarding control cell (5%) to measure what onboarding actually adds; the answer is sometimes "nothing".
- Watch 10+ session recordings of the new flow before declaring success; metrics hide UX disasters.

## AI-agent gotchas
- Microcopy generated by LLMs trends toward exclamatory ("Welcome aboard!"). Constrain to neutral/direct in every prompt.
- Character limits matter — Appcues/Pendo enforce them. Always include `≤80 chars` and validate post-generation.
- Agents miss right-to-left and i18n constraints in copy; specify locale and force translator-friendly phrasing.
- "Best-practice" pattern selection from training data leads to template-first recommendations everywhere; force the agent to defend pattern choice against the actual product surface.
- Empty-state suggestions become checklists of features ("create / import / template") regardless of context — force a single primary action with two secondary fallbacks.
- Triggered email sequences proposed by the agent often fire on the wrong event; require the agent to map every email to one named event from the canonical list.
- Privacy: session recording snippets used for ideation must be redacted (names, emails, IDs).

## References
- Samuel Hulick, "User Onboarding Teardowns" — https://www.useronboard.com/user-onboarding-teardowns/
- Appcues, "User onboarding best practices" — https://www.appcues.com/blog/user-onboarding-best-practices
- Nielsen Norman Group, "Progressive disclosure" — https://www.nngroup.com/articles/progressive-disclosure/
- Reforge, "Product-led growth onboarding" — https://www.reforge.com/blog/product-led-growth-onboarding
- Mixpanel, "User onboarding metrics guide" — https://mixpanel.com/blog/user-onboarding-metrics/
- Frigade, "Headless onboarding patterns" — https://frigade.com/
- Customer.io, "Activation email playbook" — https://customer.io/blog/onboarding-email-best-practices/
