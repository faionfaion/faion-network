<!--
purpose: CLAUDE.md skeleton tuned for LLM-friendly architecture rules.
consumes: Repo facts: commands, file conventions, owners.
produces: A project CLAUDE.md committed at the repo root.
depends-on: templates/llm-arch-audit.sh for the audit-output section.
token-budget-impact: ~400 tokens when fully filled.
-->
# [Project Name]

## Commands

```bash
# Development
npm run dev       # Start dev server
npm run build     # Production build
npm test          # Run tests
npm run lint      # Lint + format check
```

## Structure

```
src/
  components/   Shared UI components (flat, no nesting)
  features/     Feature modules (one folder per feature)
  data/         Static data and constants
  hooks/        Shared custom hooks
  utils/        Pure utility functions
  types/        Shared TypeScript types
  pages/        Route entry points (30-50 lines each)
```

## Conventions

- Components: PascalCase (`UserProfile.tsx`), max 200 lines
- Hooks: kebab-case with use- prefix (`use-auth.ts`)
- Utils: kebab-case, one function per file (`format-currency.ts`)
- Data files: kebab-case (`pricing-plans.ts`)
- Constants: SCREAMING_SNAKE_CASE in file
- Imports: direct, never barrel re-exports from internal modules

## Key Files

| File | Purpose |
|------|---------|
| `src/data/pricing.ts` | Pricing plans and feature lists |
| `src/types/api.ts` | API response types (shared 3+ places) |
| `src/features/auth/use-auth.ts` | Auth state and operations |
