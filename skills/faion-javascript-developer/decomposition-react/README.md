# React Decomposition Patterns

LLM-friendly code organization for React and Next.js projects.

---

## Anti-Pattern: God Components

```tsx
// BAD: Dashboard.tsx (600+ lines)
export function Dashboard() {
  // 20 useState hooks
  // 10 useEffect hooks
  // 15 handler functions
  // Inline styles
  // API calls mixed with UI
  // Render logic 300+ lines
}
```

---

## LLM-Friendly Structure

```
src/
├── components/
│   ├── ui/                           # Reusable UI components
│   │   ├── Button/
│   │   │   ├── Button.tsx            # Component (30-50 lines)
│   │   │   ├── Button.styles.ts      # Styles (20-40 lines)
│   │   │   ├── Button.types.ts       # Types (10-20 lines)
│   │   │   └── index.ts              # Export (5 lines)
│   │   ├── Input/
│   │   ├── Card/
│   │   └── Modal/
│   └── features/
│       └── Dashboard/
│           ├── Dashboard.tsx         # Main component (40-60 lines)
│           ├── DashboardHeader.tsx   # Header (30-50 lines)
│           ├── DashboardMetrics.tsx  # Metrics (50-70 lines)
│           ├── DashboardChart.tsx    # Chart (40-60 lines)
│           ├── DashboardTable.tsx    # Table (60-80 lines)
│           └── hooks/
│               ├── useDashboardData.ts   # Data fetching (40-60 lines)
│               └── useDashboardFilters.ts # Filters (30-50 lines)
├── hooks/
│   ├── useAuth.ts                    # Auth hook (40-60 lines)
│   ├── useApi.ts                     # API hook (50-70 lines)
│   └── useDebounce.ts                # Debounce (15-25 lines)
├── services/
│   ├── api/
│   │   ├── client.ts                 # API client (40-60 lines)
│   │   ├── users.ts                  # User API (50-70 lines)
│   │   └── orders.ts                 # Order API (50-70 lines)
│   └── auth/
│       └── authService.ts            # Auth service (60-80 lines)
├── stores/
│   ├── authStore.ts                  # Auth state (40-60 lines)
│   └── uiStore.ts                    # UI state (30-50 lines)
├── types/
│   ├── user.types.ts                 # User types (20-40 lines)
│   ├── order.types.ts                # Order types (20-40 lines)
│   └── api.types.ts                  # API types (30-50 lines)
└── utils/
    ├── formatters.ts                 # Formatting (40-60 lines)
    └── validators.ts                 # Validation (40-60 lines)
```

---

## Component Composition Pattern

```tsx
// components/features/Dashboard/Dashboard.tsx (~50 lines)
import { DashboardHeader } from './DashboardHeader';
import { DashboardMetrics } from './DashboardMetrics';
import { DashboardChart } from './DashboardChart';
import { DashboardTable } from './DashboardTable';
import { useDashboardData } from './hooks/useDashboardData';
import { useDashboardFilters } from './hooks/useDashboardFilters';

export function Dashboard() {
  const { filters, setFilters } = useDashboardFilters();
  const { data, isLoading, error } = useDashboardData(filters);

  if (isLoading) return <DashboardSkeleton />;
  if (error) return <DashboardError error={error} />;

  return (
    <div className="dashboard">
      <DashboardHeader
        filters={filters}
        onFilterChange={setFilters}
      />
      <DashboardMetrics metrics={data.metrics} />
      <DashboardChart data={data.chartData} />
      <DashboardTable items={data.items} />
    </div>
  );
}
```

---

## Custom Hook Pattern

```tsx
// components/features/Dashboard/hooks/useDashboardData.ts (~50 lines)
import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@/services/api/dashboard';
import type { DashboardFilters, DashboardData } from '@/types';

export function useDashboardData(filters: DashboardFilters) {
  return useQuery<DashboardData>({
    queryKey: ['dashboard', filters],
    queryFn: () => dashboardApi.getData(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

---

## Presentational Component Pattern

```tsx
// components/features/Dashboard/DashboardMetrics.tsx (~60 lines)
import { Card } from '@/components/ui/Card';
import { formatCurrency, formatNumber } from '@/utils/formatters';
import type { DashboardMetrics as Metrics } from '@/types';

interface Props {
  metrics: Metrics;
}

export function DashboardMetrics({ metrics }: Props) {
  return (
    <div className="grid grid-cols-4 gap-4">
      <MetricCard
        title="Revenue"
        value={formatCurrency(metrics.revenue)}
        change={metrics.revenueChange}
      />
      <MetricCard
        title="Orders"
        value={formatNumber(metrics.orders)}
        change={metrics.ordersChange}
      />
      <MetricCard
        title="Customers"
        value={formatNumber(metrics.customers)}
        change={metrics.customersChange}
      />
      <MetricCard
        title="Conversion"
        value={`${metrics.conversion}%`}
        change={metrics.conversionChange}
      />
    </div>
  );
}

function MetricCard({ title, value, change }: MetricCardProps) {
  return (
    <Card>
      <h3 className="text-sm text-gray-500">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
      <ChangeIndicator value={change} />
    </Card>
  );
}
```

---

## Next.js App Router Structure

```
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx              # Login page (40-60 lines)
│   └── register/
│       └── page.tsx              # Register page (40-60 lines)
├── (dashboard)/
│   ├── layout.tsx                # Dashboard layout (30-50 lines)
│   ├── page.tsx                  # Dashboard home (40-60 lines)
│   └── users/
│       ├── page.tsx              # Users list (50-70 lines)
│       ├── [id]/
│       │   └── page.tsx          # User detail (40-60 lines)
│       └── _components/
│           ├── UserList.tsx      # List component (50-70 lines)
│           └── UserCard.tsx      # Card component (30-50 lines)
├── api/
│   └── users/
│       ├── route.ts              # GET, POST (40-60 lines)
│       └── [id]/
│           └── route.ts          # GET, PUT, DELETE (50-70 lines)
lib/
├── actions/
│   └── users.ts                  # Server actions (60-80 lines)
├── db/
│   ├── schema.ts                 # DB schema (50-80 lines)
│   └── queries/
│       └── users.ts              # User queries (40-60 lines)
└── validations/
    └── user.ts                   # Zod schemas (30-50 lines)
```

---

## Server Actions Pattern (Next.js)

```tsx
// lib/actions/users.ts (~70 lines)
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';
import { db } from '@/lib/db';
import { users } from '@/lib/db/schema';
import { createUserSchema, updateUserSchema } from '@/lib/validations/user';

export async function createUser(formData: FormData) {
  const validated = createUserSchema.parse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  await db.insert(users).values(validated);

  revalidatePath('/users');
  redirect('/users');
}

export async function updateUser(id: string, formData: FormData) {
  const validated = updateUserSchema.parse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  await db.update(users)
    .set(validated)
    .where(eq(users.id, id));

  revalidatePath(`/users/${id}`);
  revalidatePath('/users');
}

export async function deleteUser(id: string) {
  await db.delete(users).where(eq(users.id, id));

  revalidatePath('/users');
  redirect('/users');
}
```

---

## Key Principles

1. **Component Composition** - Small components composed into larger ones
2. **Custom Hooks** - Reusable stateful logic extracted
3. **Separation of Concerns** - UI, logic, data fetching separated
4. **Co-location** - Feature-specific code grouped together
5. **Type Safety** - TypeScript for all components and hooks

---

## File Size Guidelines

| Type | Target | Max |
|------|--------|-----|
| Component | 50-80 | 150 |
| Hook | 40-60 | 100 |
| Service | 50-70 | 150 |
| Page | 50-70 | 150 |
| Action | 60-80 | 150 |
| Test | 100-150 | 300 |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Component decomposition strategy | sonnet | Refactoring expertise |
| Reusability analysis | sonnet | Code quality assessment |

## Sources

- [Bulletproof React](https://github.com/alan2207/bulletproof-react) - React architecture guide
- [React Documentation](https://react.dev/) - Official React docs
- [Next.js App Router](https://nextjs.org/docs/app) - Next.js routing patterns
- [Feature-Sliced Design](https://feature-sliced.design/) - Frontend architecture methodology
- [Clean Code React](https://github.com/ryanmcdermott/clean-code-javascript) - Clean patterns for JavaScript/React
