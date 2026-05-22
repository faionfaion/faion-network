<!--
purpose: Monorepo CLAUDE.md skeleton — root brief + per-app addenda.
consumes: Workspace layout + per-app commands + ownership map.
produces: Root CLAUDE.md plus per-app CLAUDE.md children.
depends-on: templates/extract-commands.sh per workspace.
token-budget-impact: ~700 tokens when fully filled across the root brief.
-->
# [Monorepo Name]

Monorepo containing [N] apps. See per-app files for app-specific instructions.

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
# Run all
turbo dev         # Start all services
turbo build       # Build all
turbo test        # Test all

# Per-app (cd into app dir first)
cd apps/api && make dev
cd apps/web && npm run dev
```

## Shared Types

All shared types in `packages/types/`. Import as:
```typescript
import { User, ApiResponse } from '@repo/types'
```

## Per-App Instructions

- `apps/web/`: @apps/web/AGENTS.md
- `apps/api/`: @apps/api/AGENTS.md
- `apps/worker/`: @apps/worker/AGENTS.md
