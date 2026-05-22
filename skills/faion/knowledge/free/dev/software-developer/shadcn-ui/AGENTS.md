---
slug: shadcn-ui
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a shadcn/ui installation spec (CLI-added components owned by the codebase, `cn` utility, design-token CSS vars, drift-check on upstream) without runtime npm dep.
content_id: "5e4f9c1c8b6e2901"
complexity: medium
produces: config
est_tokens: 3700
tags: [shadcn, ui, react, tailwind, radix, components]
---
# shadcn/ui

## Summary

**One-sentence:** Configures shadcn/ui as code (`npx shadcn@latest add`) — components live in `src/components/ui/`, owned by the consumer, with `cn` utility, CSS-var design tokens, and a drift-check script that diffs local copies against upstream.

**One-paragraph:** shadcn/ui is not an npm dependency — the CLI copies React + Radix + Tailwind component code into `src/components/ui/` where the consumer owns and edits it. The trade is: zero version-lock-in and full restyling freedom, but no automatic upgrades. This methodology pins the `cn` utility location, the `globals.css` design-token block (color CSS vars in HSL), forbids importing from `@/components/ui/*` outside `src/components/`, and ships a drift-check shell script that warns when an upstream component diverges from the local copy (so you upgrade intentionally).

**Ефективно для:**

- Solopreneur SaaS: контрольована візуальна ідентичність без vendor lock-in.
- AI-loop генерації UI: фіксована поверхня компонентів → агент знає, що писати.
- Багатотенентні landing pages з різним брендингом — CSS-vars дозволяють swap themes per-tenant.
- Audit accessibility: Radix primitives під капотом — ARIA correct out of the box.

## Applies If (ALL must hold)

- Next.js / Vite / Remix project with React ≥18 and Tailwind ≥3.
- TypeScript-friendly codebase (shadcn CLI emits `.tsx`).
- Project does not already vendor a competing UI kit (MUI, Chakra, Ant) at scale.

## Skip If (ANY kills it)

- Server-only Node app without React.
- Codebase needs animated runtime themes — shadcn assumes light/dark via CSS class on `&lt;html&gt;`, not arbitrary mid-session swaps.
- Strict-CSP environment forbidding inline styles — Tailwind JIT + dark-mode class needs configuration.
- Sub-1kb-budget marketing landing — Radix + Tailwind bundle is heavier than hand-written.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `package.json` | JSON | repo root |
| `tailwind.config.ts` | TS / JS | repo root |
| Component manifest | path list | `components.json` (CLI-managed) |
| Design-token plan | brand spec | `src/styles/globals.css` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tailwind]] | shadcn requires a configured Tailwind setup; design-token block lives there. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: cli-add-not-npm-install, cn-utility-canonical, css-vars-tokens, no-cross-import, drift-check, components-json-committed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for shadcn install spec + components.json shape | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: importing-as-package, mixing-ui-kits, undeclared-drift, dark-mode-class-missing | 700 |
| `content/04-procedure.xml` | essential | 5-step setup: init Tailwind → run shadcn init → add components → wire dark mode → run drift-check | 600 |
| `content/06-decision-tree.xml` | essential | Routing: greenfield vs adopt → component picking → drift policy | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick_components` | sonnet | Map design intent → component list. |
| `add_component` | haiku | Run `npx shadcn add` — mechanical. |
| `customize` | sonnet | Per-component variant additions. |
| `drift_review` | opus | Decide accept/reject upstream changes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cn-util.ts` | `cn` clsx + twMerge utility canonical location at `src/lib/utils.ts` |
| `templates/globals.css` | Design-token CSS vars block + dark-mode class config |
| `templates/shadcn-drift-check.sh` | Script comparing local component to upstream repo HEAD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadcn-ui.py` | Validate shadcn install spec JSON against schema | Post-init; pre-PR drift detection |

## Related

- [[tailwind]] — shadcn rides Tailwind tokens.
- [[storybook-setup]] — shadcn components live happily in Storybook stories.

## Decision tree

See `content/06-decision-tree.xml`. Routes setup mode (greenfield vs adopt-existing-UI), component selection (composition primitives vs full layouts), and drift policy (accept-all vs review-each). All leaves reference rules from `01-core-rules.xml`.
