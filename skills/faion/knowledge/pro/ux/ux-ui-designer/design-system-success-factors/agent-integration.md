# Agent Integration — Design System Success Factors

## When to use
- Standing up a brand-new design system or evaluating whether to invest in one (build vs. adopt vs. wrap an existing system).
- Quarterly health check on an existing system: ownership, adoption, contribution, debt.
- Diagnosing why an existing system is being ignored by product teams (low component coverage, parallel snowflake CSS).
- Pre-merger or rebrand audit when two systems must be unified.
- Setting OKRs / KPIs for a platform team that owns the system.

## When NOT to use
- One-off marketing landing pages — a system is overkill; a tokens file + Tailwind config is enough.
- Pre-product-market-fit prototyping — the four pillars optimise for adoption, which presupposes a stable surface to adopt.
- When the team is < 3 designers and 1 frontend engineer; ownership pillar collapses and overhead exceeds value.
- For pure motion / brand-illustration systems — adoption metrics are not meaningful.

## Where it fails / limitations
- "Adoption rate" defined as "% of teams using the package" hides depth of usage; teams may import once and override everything.
- The four pillars are necessary but not sufficient — they say nothing about API design, theming model, or release cadence.
- Component coverage is gameable — counting "Button" once vs counting every variant inflates the metric.
- "Strong documentation" can be confused with "lots of documentation"; success depends on findability and currency, not page count.
- The MVP-first lean does not work in regulated industries where accessibility/legal review must precede first release.

## Agentic workflow
Use agents for the measurable parts of the four pillars: documentation freshness, token-design parity, contribution telemetry, and adoption scans across consumer repos. Run a scheduled audit subagent that crawls the monorepo or the org's GitHub for `package.json` references to the system, computes coverage by AST-scanning component imports, and emits a markdown health report against the metrics table in `README.md`. Keep ownership and "real adoption" framing in the human review loop — agents cannot decide whether to fund a platform team.

### Recommended subagents
- `faion-improver` — drives the audit-and-improve loop quarterly using the Adoption Metrics table.
- `faion-sdd-executor-agent` — opens PRs that replace ad-hoc CSS with system tokens once the audit identifies them.
- A purpose-built `ds-coverage` subagent that parses TSX/Vue files, counts `<Button>` from system vs raw `<button>` styled inline, and produces the `% of UI using system` metric.
- A `docs-freshness` subagent that flags MDX files with `lastUpdated` older than the component's last source commit.

### Prompt pattern
"Crawl the `apps/` workspace. For each consumer app, list components imported from `@org/ui`, count usages, and list visual primitives (button, input, card, modal) implemented locally instead. Emit a `coverage.json` with `{app, system_uses, snowflake_uses, coverage_pct}`."

"Given Storybook's `index.json` and the system's source `src/components/*`, list components that exist in source but have no Storybook story (`docs gap`) or whose story has not changed in 180+ days while source has."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Style Dictionary | Token build → CSS/JS/iOS/Android | `npm i -D style-dictionary` — https://styledictionary.com |
| Storybook + Chromatic | Visual regression + docs | https://storybook.js.org / https://www.chromatic.com |
| Backlight (CLI) | Token + component pipeline | https://backlight.dev |
| zeroheight CLI | Sync Figma libraries to docs | https://zeroheight.com |
| Knapsack | Design-system platform CLI | https://www.knapsack.cloud |
| jscodeshift / ts-morph | AST scanning for adoption metrics | `npm i -D jscodeshift ts-morph` |
| Repo-stats / Sourcegraph | Cross-repo usage queries | https://sourcegraph.com |
| changesets | Versioning + changelog discipline | https://github.com/changesets/changesets |
| Figma REST API | Library publish / consumer counts | https://www.figma.com/developers/api |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Chromatic | SaaS | Yes (CLI + GitHub Actions) | Visual review, baseline storage |
| zeroheight | SaaS | Partial (REST API) | Doc portal; agents can push MDX |
| Knapsack | SaaS | Yes (CLI) | End-to-end DS platform |
| Supernova.io | SaaS | Yes (REST + CLI) | Token + doc workspace, AI assist |
| Specify | SaaS | Yes (REST + CLI) | Token distribution to GitHub |
| Tokens Studio (Figma) | Plug-in | Limited | Design-side authoring only |
| Backlight | SaaS | Yes (CLI) | Multi-package monorepo focus |
| Penpot | OSS | Limited | Open-source design-tool source |
| Storybook OSS | OSS | Yes | Pair with addon-a11y, addon-themes |
| Figma Variables | SaaS | Yes (REST API) | Source of truth for semantic tokens |

## Templates & scripts
See `templates.md` and `examples.md` for the audit report and metric definitions.

Inline coverage probe (Node, AST-based):

```javascript
// ds-coverage.mjs — scans repo for system-vs-snowflake usage
import { Project, SyntaxKind } from 'ts-morph';
import { readFileSync } from 'node:fs';

const SYSTEM_PKG = '@org/ui';
const PRIMITIVES = ['button', 'input', 'select', 'modal', 'card'];
const project = new Project({ tsConfigFilePath: 'tsconfig.json' });

let sys = 0, snow = 0;
for (const sf of project.getSourceFiles('apps/**/*.{ts,tsx}')) {
  const importsSystem = sf.getImportDeclarations().some(
    d => d.getModuleSpecifierValue() === SYSTEM_PKG,
  );
  sf.getDescendantsOfKind(SyntaxKind.JsxOpeningElement).forEach(el => {
    const tag = el.getTagNameNode().getText().toLowerCase();
    if (PRIMITIVES.includes(tag)) {
      importsSystem ? sys++ : snow++;
    }
  });
}
console.log(JSON.stringify({ system_uses: sys, snowflake_uses: snow, coverage_pct: sys / (sys + snow) }, null, 2));
```

## Best practices
- Treat the system as a product with a roadmap, customers (consumer teams), and SLAs — not as a side-project of the platform team.
- Define adoption tiers (Bronze/Silver/Gold) per consumer app and publish them; peer pressure outperforms top-down mandates.
- Pair every component release with a codemod (jscodeshift) that migrates consumers; "documentation only" releases erode trust.
- Run a contribution day each quarter — measured contribution rate is meaningless without a working contribution path.
- Keep tokens and components in different release trains; tokens move slowly, components iterate.
- Make breaking changes loud (changesets `major`, codemod, deprecation warnings) and silent fixes silent (`patch`).
- Capture support-ticket categories per quarter; the dominant category is your next roadmap item.

## AI-agent gotchas
- Agents can fabricate "adoption %" by counting imports without counting renders; require runtime telemetry (e.g., DOM marker / data-ds attribute scans) for the headline metric.
- LLMs will write components that re-implement existing primitives because they do not see the library — feed them the system's catalogue (Storybook `index.json`) before code generation.
- Documentation-generation agents tend to drift from source; pin doc generation to the component's source AST, not the writer's memory.
- Token rename PRs from agents often miss CSS-in-JS template literals and Tailwind config — run a second-pass regex sweep before merging.
- Bot-authored PRs without a human reviewer in the system's CODEOWNERS file should be blocked at merge; ownership is the first pillar.
- Agents merging codemods to consumer repos must respect each app's release train; never auto-merge into `main` of unrelated apps.

## References
- Brad Frost — *Atomic Design* (2016)
- Nathan Curtis — *Modular Web Design* and EightShapes essays — https://medium.com/eightshapes-llc
- Sparkbox Design Systems Survey 2024 — https://designsystemssurvey.sparkbox.com
- Adobe Spectrum design system principles — https://spectrum.adobe.com
- Shopify Polaris contribution model — https://polaris.shopify.com
- Design Systems Repo metrics templates — https://designsystemsrepo.com
