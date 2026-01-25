# Code Decomposition Patterns

Practical patterns and language-specific examples for breaking code into manageable pieces.

## Decomposition Patterns

### Pattern 1: Extract Service

Move business logic from views/controllers to services.

```python
# BEFORE: views.py (fat controller)
class OrderView:
    def create(self, request):
        # 50 lines of validation
        # 30 lines of business logic
        # 20 lines of notification
        # 15 lines of logging
        pass

# AFTER: Split into focused files
# views.py (~20 lines)
class OrderView:
    def create(self, request):
        order = OrderService.create(request.data)
        return Response(OrderSerializer(order).data)

# services/order_service.py (~50 lines)
class OrderService:
    @staticmethod
    def create(data: dict) -> Order:
        validated = OrderValidator.validate(data)
        order = Order.objects.create(**validated)
        OrderNotifier.notify_created(order)
        return order

# services/order_validator.py (~30 lines)
# services/order_notifier.py (~20 lines)
```

### Pattern 2: Extract Component

Break large UI components into smaller, focused pieces.

```typescript
// BEFORE: Dashboard.tsx (400+ lines)
export function Dashboard() {
  // State management (50 lines)
  // Data fetching (30 lines)
  // Event handlers (40 lines)
  // Render logic (280 lines)
}

// AFTER: Split by responsibility
// Dashboard.tsx (~50 lines) - Composition only
export function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <DashboardMetrics />
      <DashboardCharts />
      <DashboardTable />
    </DashboardLayout>
  );
}

// components/DashboardHeader.tsx (~40 lines)
// components/DashboardMetrics.tsx (~60 lines)
// components/DashboardCharts.tsx (~80 lines)
// components/DashboardTable.tsx (~100 lines)
// hooks/useDashboardData.ts (~50 lines) - Data fetching
```

### Pattern 3: Extract Module

Group related functionality into cohesive modules.

```
# BEFORE: Flat structure
src/
├── user_model.py
├── user_view.py
├── order_model.py
├── order_view.py
├── payment_model.py
├── payment_view.py
└── utils.py (everything else)

# AFTER: Domain modules
src/
├── users/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   └── tests/
├── orders/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── services.py
│   └── tests/
└── payments/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── services.py
    └── tests/
```

### Pattern 4: Extract Configuration

Separate config from code.

```python
# BEFORE: settings.py (500+ lines)
# Everything in one file

# AFTER: Split by concern
settings/
├── __init__.py      # Load appropriate config
├── base.py          # Common settings (~50 lines)
├── development.py   # Dev overrides (~30 lines)
├── production.py    # Prod settings (~40 lines)
├── testing.py       # Test settings (~20 lines)
└── components/
    ├── database.py  # DB config (~30 lines)
    ├── cache.py     # Cache config (~20 lines)
    ├── logging.py   # Logging config (~40 lines)
    └── security.py  # Security settings (~30 lines)
```

### Pattern 5: Extract Types/Interfaces

Separate type definitions from implementation.

```typescript
// BEFORE: Mixed in implementation files
// user.ts has types + logic + API calls

// AFTER: Separate type definitions
types/
├── user.types.ts     # User interfaces
├── order.types.ts    # Order interfaces
├── api.types.ts      # API response types
└── common.types.ts   # Shared types

services/
├── user.service.ts   # User logic (imports types)
├── order.service.ts  # Order logic (imports types)
└── api.service.ts    # API calls (imports types)
```

---

## Language-Specific Guidelines

### Python/Django

```
app/
├── models/
│   ├── __init__.py      # Export all models
│   ├── user.py          # User model only
│   └── profile.py       # Profile model only
├── services/
│   ├── __init__.py
│   ├── user_service.py  # User business logic
│   └── auth_service.py  # Auth business logic
├── views/
│   ├── __init__.py
│   ├── user_views.py    # User endpoints
│   └── auth_views.py    # Auth endpoints
├── serializers/
│   ├── __init__.py
│   ├── user_serializers.py
│   └── auth_serializers.py
└── tests/
    ├── test_models/
    ├── test_services/
    └── test_views/
```

### TypeScript/React

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.styles.ts
│   │   │   └── Button.test.tsx
│   │   └── Input/
│   └── features/        # Feature components
│       └── Dashboard/
│           ├── Dashboard.tsx
│           ├── DashboardHeader.tsx
│           └── hooks/
├── hooks/               # Shared hooks
├── services/            # API services
├── stores/              # State management
├── types/               # Type definitions
└── utils/               # Utility functions
```

### Go

```
internal/
├── domain/
│   ├── user/
│   │   ├── user.go          # Entity
│   │   ├── repository.go    # Interface
│   │   └── service.go       # Business logic
│   └── order/
│       ├── order.go
│       ├── repository.go
│       └── service.go
├── infrastructure/
│   ├── database/
│   │   ├── postgres.go
│   │   └── migrations/
│   └── http/
│       ├── server.go
│       └── handlers/
└── application/
    ├── commands/
    └── queries/
```

---

## Pattern Examples

### Extract Service Pattern

**When to Use:**
- Controllers/views exceed 100 lines
- Business logic mixed with HTTP handling
- Multiple endpoints share logic

**Benefits:**
- Testable without HTTP layer
- Reusable across endpoints
- Framework-agnostic

### Extract Component Pattern

**When to Use:**
- React components exceed 150 lines
- Multiple UI concerns in one file
- Difficult to test or reuse

**Benefits:**
- Easier to understand and test
- Reusable sub-components
- Better performance (can memoize)

### Extract Module Pattern

**When to Use:**
- Flat structure with 20+ files
- Related files scattered across project
- Team ownership unclear

**Benefits:**
- Clear boundaries
- Easier navigation
- Independent deployment

### Extract Configuration Pattern

**When to Use:**
- Settings file exceeds 150 lines
- Environment-specific config mixed
- Hard to find specific setting

**Benefits:**
- Environment-specific overrides
- Easier to audit
- Clearer security settings

### Extract Types Pattern

**When to Use:**
- TypeScript files mixing types and logic
- Types reused across multiple files
- Circular type dependencies

**Benefits:**
- Single source of truth
- Easier refactoring
- Better IDE support

---

## Real-World Examples

### E-Commerce Service Decomposition

```python
# BEFORE: shop.py (800 lines)
class ShopView:
    def checkout(self, request):
        # Validation
        # Inventory check
        # Payment processing
        # Order creation
        # Email notification
        # Analytics tracking
        pass

# AFTER: Decomposed
# views/checkout_view.py (~30 lines)
class CheckoutView:
    def post(self, request):
        checkout = CheckoutService.process(request.data)
        return Response(CheckoutSerializer(checkout).data)

# services/checkout_service.py (~50 lines)
# services/inventory_service.py (~40 lines)
# services/payment_service.py (~60 lines)
# services/notification_service.py (~30 lines)
# services/analytics_service.py (~25 lines)
```

### Dashboard Component Decomposition

```typescript
// BEFORE: Dashboard.tsx (500 lines)

// AFTER: Decomposed
// pages/Dashboard.tsx (~40 lines)
export function Dashboard() {
  const { data, isLoading } = useDashboardData();

  return (
    <DashboardLayout>
      <MetricsGrid metrics={data.metrics} />
      <RevenueChart data={data.revenue} />
      <RecentOrders orders={data.orders} />
    </DashboardLayout>
  );
}

// components/MetricsGrid.tsx (~60 lines)
// components/RevenueChart.tsx (~80 lines)
// components/RecentOrders.tsx (~70 lines)
// hooks/useDashboardData.ts (~50 lines)
```

---

## Migration Strategies

### Gradual Decomposition

```
1. Create new structure alongside old
2. Copy (don't move) code to new files
3. Update imports in new code
4. Test new structure
5. Migrate one module at a time
6. Delete old files when migration complete
```

### Big Bang Decomposition

```
1. Plan complete structure
2. Create all new files
3. Move code in one commit
4. Update all imports
5. Run full test suite
6. Fix any issues
```

**Recommendation:** Use Gradual for production systems, Big Bang for new projects.

---

## Related

- [code-decomposition-principles.md](code-decomposition-principles.md) - Core principles and best practices
- [llm-friendly-architecture.md](llm-friendly-architecture.md) - LLM-optimized code patterns
- [refactoring-patterns.md](refactoring-patterns.md) - Refactoring techniques
- [react-component-architecture.md](react-component-architecture.md) - React-specific patterns
- [django-code-structure.md](django-code-structure.md) - Django-specific patterns
