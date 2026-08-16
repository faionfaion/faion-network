# React Patterns

## Summary

**One-sentence:** Produces a feature-module spec naming the folder tree, the named function-declaration component shape, the Context provider pattern, and the state-routing decision (server / form / global / local) for a new React feature.

**Ефективно для:** Onboarding a feature module into an existing React codebase where the team needs deterministic structure and consistent state-ownership choices across people and PRs.

**One-paragraph:** Turns "where does this feature go and how is it shaped?" into one auditable spec. The output names the feature folder under src/features/&lt;name&gt;/, lists its components/hooks/api/types files, declares the typed component prop interface (named, not anonymous), wires the Context provider (null sentinel + memoized value + guard hook), and routes each state slice to its owning layer. Forbids `__all__`-style ad-hoc exports, anonymous arrow components, prop-drilling past two levels, and inline object props on memoized children.

## Applies If (ALL must hold)

- Target is React 18.2+ or React 19+ with TypeScript strict mode.
- Codebase uses feature-based organisation (or migrates to it).
- The feature is non-trivial: at least one stateful component + one async data source.
- The team committed to function-declaration components and named prop interfaces.
- Output drives downstream codegen / PR review (not a throwaway scratch).

## Skip If (ANY kills it)

- Component is purely presentational with zero state and zero async — no spec needed.
- File-type-grouped codebase that the team refuses to migrate — patterns conflict.
- React Native pre-0.74 — folder conventions differ.
- One-off page in a marketing site — Astro / Gatsby is the right tool.
- TanStack Router file-based routing already imposes a structure — defer to it.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Feature brief | markdown | product doc |
| List of state slices | bullets | analysis pass (see [[react-hooks]]) |
| Existing folder convention | tree snippet | repo root `src/` |
| External-store inventory | YAML | repo config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[react-hooks]]` | Per-slice hook decision routed by this spec. |
| `[[typescript-patterns]]` | Named interface + discriminated unions used for prop types. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: feature folder, function declarations, named interfaces, Context null sentinel, memoized provider value, state routing | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema for the feature-module spec | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: anonymous components, inline JSX object props, Context default fakery, prop drilling | ~700 |
| `content/04-procedure.xml` | medium | 5 steps: feature → folder → components → context → state routing | ~600 |
| `content/05-examples.xml` | medium | One worked example: auth feature with AuthProvider + useAuth + login flow | ~500 |
| `content/06-decision-tree.xml` | essential | Root: does the feature need a Context? branches into provider vs prop-drill vs external-store | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `expand_folder_tree` | haiku | Template fill from canonical layout. |
| `emit_feature_spec` | sonnet | Bounded transformation: assembly + routing. |
| `review_state_routing` | opus | Cross-cuts server/global/form/local decisions; needs judgement. |

## Templates

| File | Purpose |
|---|---|
| `templates/feature-spec.json` | Reference output document for a feature. |
| `templates/context-provider.tsx` | AuthProvider + useAuth pattern reference. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-react-patterns.py` | Validate a feature-spec JSON against the contract. | After the spec is emitted, before codegen reads it. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[react-hooks]] — per-slice hook decisions consumed by the state_routing field.
- [[typescript-react-2026]] — Server / Client boundary that gates which files in the spec are server-default vs client-marked.
- [[typescript-patterns]] — generic component patterns.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree first asks whether the feature has shared state across more than two component levels: yes → Context provider with memoized value and null-sentinel hook; no → prop-drill. When an external store already owns the slice, the tree routes there instead of creating a parallel Context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-spec.json`

```json
{
  "_purpose": "Reference feature-module spec output for one React feature.",
  "_consumes": "Feature brief + slices + existing folder convention.",
  "_produces": "JSON for downstream codegen / review.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~120 tokens.",
  "artefact_id": "auth-feature-spec",
  "owner": "ruslan@faion.net",
  "feature_name": "auth",
  "react_version": "^19.0.0",
  "folder_tree": [
    "src/features/auth/AuthProvider.tsx",
    "src/features/auth/api.ts",
    "src/features/auth/components/LoginForm.tsx",
    "src/features/auth/hooks/useAuth.ts",
    "src/features/auth/types.ts"
  ],
  "components": [
    {
      "name": "AuthProvider",
      "props_interface": "AuthProviderProps",
      "declaration": "function-declaration"
    },
    {
      "name": "LoginForm",
      "props_interface": "LoginFormProps",
      "declaration": "function-declaration"
    }
  ],
  "context": {
    "name": "AuthContext",
    "null_sentinel": true,
    "value_memoized": true,
    "consumer_hook": "useAuth"
  },
  "state_routing": [
    {
      "slice": "currentUser",
      "layer": "shared-context"
    },
    {
      "slice": "loginForm",
      "layer": "form"
    }
  ],
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```

### `templates/context-provider.tsx`

```tsx
import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';

export interface User {
  id: string;
  email: string;
}

export interface Credentials {
  email: string;
  password: string;
}

export interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

// rule r4-context-null-sentinel: initialise with null, throw in the consumer hook.
const AuthContext = createContext<AuthContextValue | null>(null);

export interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (_credentials: Credentials) => {
    // call the api here
    setUser({ id: 'u-1', email: _credentials.email });
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  // rule r5-memoize-provider-value: stable reference for consumers.
  const value = useMemo<AuthContextValue>(
    () => ({ user, isAuthenticated: user !== null, login, logout }),
    [user, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (ctx === null) {
    throw new Error('useAuth must be used within <AuthProvider>');
  }
  return ctx;
}
```
