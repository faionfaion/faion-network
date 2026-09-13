<!--
purpose: Monorepo CLAUDE.md skeleton — root brief with cross-cutting content only; per-app instructions live next to each app and are imported.
consumes: Workspace layout + cross-cutting commands + the list of per-app CLAUDE.md files.
produces: Root CLAUDE.md plus per-app CLAUDE.md children referenced by @path import.
depends-on: templates/extract-commands.sh per workspace; every imported per-app file exists at commit time.
token-budget-impact: ~700 tokens when fully filled across the root brief.
-->
# [Monorepo Name]

Monorepo containing [N] apps. App-specific commands and conventions live in each app's own CLAUDE.md, imported below; this root carries only what applies across the workspace.

## Structure

```
apps/
  web/      Next.js frontend — see apps/web/CLAUDE.md
  api/      FastAPI backend — see apps/api/CLAUDE.md
  worker/   Background jobs — see apps/worker/CLAUDE.md
packages/
  ui/       Shared React components
  config/   Shared configuration (ESLint, TypeScript)
  types/    Shared TypeScript types
```

## Cross-Cutting Commands

```bash
turbo dev         # Start all services
turbo build       # Build all
turbo test        # Test all
turbo lint        # Lint all workspaces with the shared config
```

## Shared Types

All shared types in `packages/types/`. Import as:
```typescript
import { User, ApiResponse } from '@repo/types'
```

## Gotchas

- `packages/config` is the single ESLint and TypeScript config; an app-local override breaks `turbo lint` for every other app.
- `turbo` caches by input hash: `turbo test --force` after changing `packages/types` without a version bump.

## Per-App Instructions

- `apps/web/`: @apps/web/CLAUDE.md
- `apps/api/`: @apps/api/CLAUDE.md
- `apps/worker/`: @apps/worker/CLAUDE.md
