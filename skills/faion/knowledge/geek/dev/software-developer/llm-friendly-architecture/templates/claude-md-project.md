# [Project Name]

## Commands

```bash
npm run dev       # Dev server
npm test          # Tests
npm run build     # Production build
npm run lint      # ESLint + Prettier check
```

## Structure

```
src/
  components/   Shared UI — flat, PascalCase, max 150 lines each
  features/     Feature modules — one folder per feature, max 2 levels
  data/         Static data and constants (extracted from components)
  hooks/        Shared hooks (use-*.ts)
  utils/        Pure functions (kebab-case, one function per file)
  types/        Shared types (centralized when used in 3+ files)
  pages/        Route entry points (30-50 lines, orchestrators only)
```

## Conventions

- Components: PascalCase, direct imports only (no barrels)
- Hooks: `use-feature.ts` naming
- Utils: `format-currency.ts` naming, one exported function per file
- Data: extracted to `src/data/`, never inline in components
- Types: colocated if used once; `src/types/` if used in 3+ files
- Max file size: 250 lines (audit with `bash scripts/audit.sh`)
