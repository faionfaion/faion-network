# Agent Integration — Design System Success Factors

## When to use
- Diagnosing why a design system has low adoption (components built but unused, designers re-creating UI off-system).
- Bootstrapping a new system at a small team and choosing what to ship in v0 vs v1.
- Establishing adoption metrics and instrumentation before a design-ops review.
- Drafting governance/ownership models when multiple product teams contribute components.

## When NOT to use
- Component-level decisions (button anatomy, color contrast, motion specs) — those need their own methodologies.
- Tooling-only choices (Figma vs Penpot, Storybook vs Histoire) — covered by tools/process methodologies.
- Pure brand/marketing systems with no engineering tie-in — adoption metrics here assume product UI.

## Where it fails / limitations
- "Real adoption" is squishy. Methodology lists metrics but does not prescribe sampling cadence, threshold targets, or weighting — teams must define their own.
- Assumes one design system per org. Federated/multi-brand systems (parent + child themes) need additional alignment patterns not covered here.
- "Strong documentation" is binary in the rubric; in practice docs decay — methodology omits doc-rot detection.
- Ownership pillar conflates governance (who decides) with maintenance (who fixes bugs). Treat as two separate accountabilities in real orgs.

## Agentic workflow
Use a multi-agent audit loop: an inventory agent crawls Figma + Storybook + production HTML to extract component usage, a metrics agent computes the adoption KPIs, a critic agent compares results against the four pillars and emits a prioritized backlog of improvements. Keep humans in the loop on prioritization — agents are good at counting, weak at deciding what to deprecate. Re-run quarterly; persist trend deltas to track the "real adoption" slope.

### Recommended subagents
- `ds-inventory` — sonnet; reconciles components defined (Figma library, code package) vs used (production DOM, screenshots).
- `ds-metrics-collector` — haiku; aggregates raw counts into the five adoption metrics.
- `ds-doc-auditor` — sonnet; reads docs site, flags missing examples, dead links, components without "do/don't" guidance.
- `ds-pillar-critic` — sonnet; scores each pillar 0-4 with evidence and produces an improvement plan.

### Prompt pattern
```
You are ds-pillar-critic. Inputs: <inventory_json>, <metrics_json>, <doc_audit_json>.
Score each pillar (Ownership, Usability, Documentation, Adoption) 0-4 with one
evidence quote per score. Then output 3-5 concrete actions ordered by ROI.
Format: STRICT JSON {scores:{...}, actions:[{pillar, action, owner_hint, effort:S|M|L}]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `chromatic` CLI | Storybook visual review + adoption telemetry | `npm i -D chromatic` · chromatic.com/docs/cli |
| `storybook` CLI | Component catalog, docgen, MDX docs | `npx storybook init` · storybook.js.org |
| `omlet-cli` (or `react-scanner`) | Component usage scanner across codebase | `npm i -g @omlet/cli` · github.com/moroshko/react-scanner |
| `style-dictionary` CLI | Token build/distribution for design-dev parity metric | `npm i -g style-dictionary` · amzn.github.io/style-dictionary |
| `figma-tokens-cli` / Tokens Studio CLI | Sync Figma variables ↔ code tokens | github.com/tokens-studio/figma-plugin |
| `lighthouse-ci` | Track perf/a11y per component page (quality indicator) | github.com/GoogleChrome/lighthouse-ci |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chromatic | SaaS | Yes — REST + CLI | Component coverage, visual diff, usage analytics |
| Knapsack | SaaS | Yes — REST | Multi-brand DS + governance workflows |
| Supernova | SaaS | Yes — REST | Token sync, doc generation, design-dev parity |
| Zeroheight | SaaS | Limited — content APIs | Doc hosting; agent-driven doc updates possible |
| Backstage (Spotify) | OSS | Yes — plugins | Treat the design system as a Backstage entity for ownership/SLOs |
| Omlet | SaaS | Yes — REST | React component analytics across repos |
| Storybook | OSS | Yes — Node/JS APIs | Self-hosted catalog, often the source of truth for "components defined" |

## Templates & scripts
See `templates.md` for ownership charter and adoption scorecard. Quick adoption snapshot:

```bash
#!/usr/bin/env bash
# ds_adoption.sh — usage: ./ds_adoption.sh <repo_glob>
# Counts <Button /> vs <button> across React TSX files; rough proxy for component adoption.
set -euo pipefail
ROOT="${1:-./apps}"
SYS=$(grep -RInE '<(Button|Input|Select|Card|Modal)\b' "$ROOT" --include='*.tsx' | wc -l)
RAW=$(grep -RInE '<(button|input|select)\b[^>]*>' "$ROOT" --include='*.tsx' | wc -l)
TOTAL=$((SYS + RAW))
PCT=$(awk "BEGIN {printf \"%.1f\", ($SYS/$TOTAL)*100}")
echo "design-system: $SYS  raw-html: $RAW  coverage: ${PCT}%"
```

## Best practices
- Ship v0 with a deprecation policy already written, not after the first regret. Set the expectation that components can leave the system.
- Tie adoption metrics to a perf/a11y baseline so "100% coverage" cannot hide quality regressions.
- Make contribution explicit: every PR adding to product UI gets a checkbox "did you check the system?" in the PR template; agents enforce via CI.
- Pair each pillar with a single owner role (DRI), not a committee. Committees produce zero accountability.
- Run a "would I use this?" interview with 5-7 product devs at v0, v1, v2. Numbers lie; a confused dev is signal.
- Embed Figma library version + code package version in the docs site so designers and devs can see drift at a glance.

## AI-agent gotchas
- Component-usage scans miss semantic equivalents (a custom `MyButton` wrapping the system `Button` looks like adoption but may bypass tokens). Walk the import graph, not just JSX.
- LLM-generated component documentation tends toward generic copy. Force the agent to cite at least one repo example file path per doc page.
- "Adoption rate" computed only on new code overstates progress. Always split metrics into greenfield vs legacy and report both.
- Critic agents can hallucinate "missing" components. Provide the agent the full inventory file and require it to reference items by ID, not by name.
- Multi-brand systems break the "one library, one source of truth" assumption. If your DS spans brands, model brand as a token mode (see semantic-tokens-and-modes) and run pillar audits per brand.
- Doc auditors should not auto-fix without human review — confidently incorrect examples are worse than missing ones.

## References
- Brad Frost, "Atomic Design" — atomicdesign.bradfrost.com.
- Nathan Curtis, "Measuring Design System Success" — medium.com/eightshapes-llc.
- "Design Systems Handbook" by InVision/DesignBetter.
- Nielsen Norman Group — "Design System Adoption" articles (nngroup.com).
- "Design System Operations" — Knapsack/Supernova case studies.
