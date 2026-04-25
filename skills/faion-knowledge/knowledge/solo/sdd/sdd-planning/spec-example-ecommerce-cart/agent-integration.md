# Agent Integration — Spec Example: E-commerce Cart

## When to use
- As a reference document when an agent or developer needs to see what a fully-populated SDD spec looks like in practice
- When training or calibrating an agent's spec-writing output quality — compare agent output against this example
- When bootstrapping a new e-commerce feature spec — the cart data models and AC patterns (persistence, guest vs. logged-in, quantity limits) recur across many cart-adjacent features
- As a teaching artifact when onboarding a new contributor to the SDD workflow

## When NOT to use
- This directory is an example, not a template — do not derive a new spec by editing this file; use `template-spec` or `spec-advanced-guidelines` instead
- Non-e-commerce domains: the patterns (localStorage guest cart, session merge on login, product-catalog dependency) are domain-specific; they transfer poorly to unrelated domains without significant reframing

## Where it fails / limitations
- The example uses story-point estimates, which the SDD system replaces with token estimates — teams using this as a literal template will carry over story points instead of token budgets
- Security scenarios are explicitly left unchecked in the AC coverage matrix; this is intentional as a teaching point, but agents following the template may inherit the gap rather than fill it
- The example's NFR targets (< 200ms p95, 50k concurrent users) are plausible for a mid-scale e-commerce platform but have no basis in a specific project — they must be replaced with real measurements
- The TypeScript interface in the Appendix is preliminary; agents treating it as an approved data model before design.md is written will create drift between spec and design

## Agentic workflow
An agent can use this example as a few-shot reference when generating a new spec: load this README as context, then instruct the agent to produce an analogous spec for the target feature. The key reusable patterns are the FR → US traceability table, the NFR measurement format, and the AC Given/When/Then scenario structure. The example also demonstrates Out of Scope (with "When" column) and Open Questions — two sections agents consistently omit when drafting without explicit instruction.

### Recommended subagents
- `faion-sdd-executor-agent` — can be invoked with this file as a few-shot context example when drafting specs for new cart-adjacent features

### Prompt pattern
```
Use the following completed spec as a few-shot reference for structure and quality.
Reference spec: <paste this README content>

Now write a spec for: <new feature name>.
Problem: <problem statement>
User types: <list>
Key constraints: <list>

Follow the same section structure. Replace all domain-specific content with content
appropriate to <new feature>. NFRs must use [MEASURE_NEEDED] where targets are unknown.
```

```
Compare this draft spec against the e-commerce cart example spec.
Identify: (1) sections present in example but missing from draft,
(2) AC scenarios in example (error, edge case, persistence) missing from draft,
(3) traceability gaps (FR with no AC, US with no FR).
Output: gap list only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| ripgrep (`rg`) | Search spec for unresolved items: `rg '\[ \]'` finds unchecked AC coverage boxes | System / https://github.com/BurntSushi/ripgrep |
| markdownlint | Validates markdown table formatting and heading structure in the spec | `npm install -g markdownlint-cli` / https://github.com/DavidAnson/markdownlint |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | No (read-only embed links) | Referenced in Appendix for wireframes; not automatable |
| Redis | OSS | Yes — CLI + API | Cart session caching pattern in the example; Valkey (drop-in) also applies |
| Stripe | SaaS | Yes — REST API | Payment flow referenced as downstream dependency of cart → checkout |

## Templates & scripts
This directory is itself a worked example. For reusable templates, use:
- `../template-spec/` — blank spec template
- `../spec-advanced-guidelines/` — section-by-section guidance

Utility to extract all unchecked items from an AC coverage block:
```bash
#!/usr/bin/env bash
# usage: ./check-coverage.sh spec.md
# Prints all unchecked AC coverage items (potential gaps)
grep -n '- \[ \]' "$1" | sed 's/- \[ \]/UNCHECKED:/'
```

## Best practices
- Use the e-commerce cart example's AC coverage matrix (`- [x] happy path`, `- [ ] security scenarios`) as a completeness signal, not a checkbox exercise — every unchecked item is a documented risk, not an optional detail
- The "Out of Scope / When" column ("Phase 2", "v2.0", "Not planned") is the highest-ROI section for preventing feature creep mid-sprint; copy this pattern into every spec
- Dependency tracking (Internal: Product Catalog ✓, Auth ✓; Blocks: Checkout) should be the first section filled in after Overview — it determines whether the feature can even start
- The Open Questions list is a forcing function: if there are no open questions, the spec is either complete or the author didn't look hard enough (cart merge on login is a classic overlooked question)
- Preliminary data models in the Appendix communicate intent but must be explicitly marked as "preliminary" — they feed into design.md and may change

## AI-agent gotchas
- Agents using this as a template will copy the story-point estimates (5 pts, 3 pts, etc.) — explicitly instruct them to remove story points and replace with token estimates per the 100k rule
- The TypeScript interface in the Appendix will be treated as the canonical data model by agents unless the spec explicitly says "subject to change in design.md"
- Agents expand the personas (Busy Parent Sarah, Deal Hunter Mike) to seem realistic but the specific pain points must come from real user research — agents hallucinate persona context fluently
- NFR values without measurement sources will be copied verbatim into new specs and then survive into design and implementation unchanged — add a required `[SOURCE]` tag next to each NFR target when adapting

## References
- https://www.baymard.com/blog/shopping-cart-page-redesigns (Amazon/Baymard e-commerce cart UX research)
- https://redis.io/docs/ (Redis / Valkey for session and cart caching)
- https://microservices.io/patterns/index.html (cart service architecture patterns)
- https://stripe.com/docs/payments/payment-intents (downstream payment flow patterns)
- SDD methodology root: `skills/faion-knowledge/knowledge/solo/sdd/sdd/README.md`
