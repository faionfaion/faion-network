# M-JS-002: React Patterns and Best Practices

## Metadata
- **Category:** Development/JavaScript
- **Difficulty:** Intermediate
- **Tags:** #dev, #javascript, #react, #patterns, #methodology
- **Agent:** faion-code-agent

---

## Problem

React projects quickly become unmaintainable without clear patterns. Component sprawl, prop drilling, and state management issues slow development. You need proven patterns that scale.

## Promise

After this methodology, you will write React code that is maintainable, testable, and performant. You will know when to use each pattern and why.

## Overview

Modern React (18+) emphasizes function components, hooks, and composition. This methodology covers patterns that work at any scale.

---

## Framework

### Step 1: Component Organization

```
src/
├── components/           # Shared/reusable components
│   ├── ui/              # Generic UI (Button, Input, Modal)
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   └── index.ts     # Barrel export
│   └── features/        # Feature-specific components
│       └── UserProfile/
├── hooks/               # Custom hooks
├── contexts/            # React contexts
├── pages/               # Route pages (Next.js/Remix)
├── lib/                 # Utilities, API clients
├── types/               # TypeScript types
└── styles/              # Global styles
```

### Step 2: Component Patterns

**Presentational Component:**

```typescript
// components/ui/Button/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={isLoading}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}
```

**Container Component:**

```typescript
// components/features/UserList/UserListContainer.tsx
export function UserListContainer() {
  const { data: users, isLoading, error } = useUsers();

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;

  return <UserList users={users} />;
}
```

**Compound Component:**

```typescript
// components/ui/Accordion/Accordion.tsx
const AccordionContext = createContext<AccordionContextType | null>(null);

export function Accordion({ children }: { children: React.ReactNode }) {
  const [openItem, setOpenItem] = useState<string | null>(null);

  return (
    <AccordionContext.Provider value={{ openItem, setOpenItem }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
}

Accordion.Item = function AccordionItem({ id, children }: ItemProps) {
  const { openItem, setOpenItem } = useAccordionContext();
  const isOpen = openItem === id;

  return (
    <div className={`accordion-item ${isOpen ? 'open' : ''}`}>
      {children}
    </div>
  );
};

// Usage
<Accordion>
  <Accordion.Item id="1">
    <Accordion.Trigger>Title</Accordion.Trigger>
    <Accordion.Content>Content</Accordion.Content>
  </Accordion.Item>
</Accordion>
```

### Step 3: Custom Hooks

**Data Fetching Hook:**

```typescript
// hooks/useUsers.ts
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users');
      if (!response.ok) throw new Error('Failed to fetch users');
      return response.json() as Promise<User[]>;
    },
  });
}
```

**Local Storage Hook:**

```typescript
// hooks/useLocalStorage.ts
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;

    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value;
    setStoredValue(valueToStore);
    window.localStorage.setItem(key, JSON.stringify(valueToStore));
  };

  return [storedValue, setValue] as const;
}
```

**Form Hook:**

```typescript
// hooks/useForm.ts
export function useForm<T extends Record<string, unknown>>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const handleChange = (name: keyof T) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setValues((prev) => ({ ...prev, [name]: e.target.value }));
  };

  const handleBlur = (name: keyof T) => () => {
    setTouched((prev) => ({ ...prev, [name]: true }));
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };

  return { values, errors, touched, handleChange, handleBlur, reset, setErrors };
}
```

### Step 4: State Management Patterns

**Context for Theme:**

```typescript
// contexts/ThemeContext.tsx
type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');

  const toggleTheme = useCallback(() => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

**Zustand for Complex State:**

```typescript
// stores/useAuthStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  token: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
      isAuthenticated: () => get().token !== null,
    }),
    { name: 'auth-storage' }
  )
);
```

### Step 5: Performance Patterns

**Memoization:**

```typescript
// Memoize expensive components
const ExpensiveComponent = memo(function ExpensiveComponent({ data }: Props) {
  // Only re-renders when data changes
  return <div>{/* render */}</div>;
});

// Memoize expensive calculations
function DataGrid({ items }: { items: Item[] }) {
  const sortedItems = useMemo(
    () => items.slice().sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  );

  return <Table data={sortedItems} />;
}

// Memoize callbacks
function Form({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const handleSubmit = useCallback(
    (e: FormEvent) => {
      e.preventDefault();
      onSubmit(formData);
    },
    [onSubmit, formData]
  );

  return <form onSubmit={handleSubmit}>{/* fields */}</form>;
}
```

**Code Splitting:**

```typescript
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

---

## Templates

### Feature Component Template

```typescript
// components/features/FeatureName/FeatureName.tsx
import { useState } from 'react';
import { useFeatureData } from './hooks/useFeatureData';
import { FeatureList } from './FeatureList';
import { FeatureForm } from './FeatureForm';
import type { FeatureItem } from './types';

interface FeatureNameProps {
  initialItems?: FeatureItem[];
}

export function FeatureName({ initialItems = [] }: FeatureNameProps) {
  const { items, addItem, removeItem } = useFeatureData(initialItems);
  const [isFormOpen, setIsFormOpen] = useState(false);

  return (
    <div className="feature-name">
      <header>
        <h2>Feature Name</h2>
        <Button onClick={() => setIsFormOpen(true)}>Add Item</Button>
      </header>

      <FeatureList items={items} onRemove={removeItem} />

      {isFormOpen && (
        <FeatureForm
          onSubmit={addItem}
          onClose={() => setIsFormOpen(false)}
        />
      )}
    </div>
  );
}
```

### Barrel Export

```typescript
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Modal } from './Modal';
export { Card } from './Card';
export { Spinner } from './Spinner';
```

---

## Examples

### Modal with Portal

```typescript
import { createPortal } from 'react-dom';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, children }: ModalProps) {
  if (!isOpen) return null;

  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          X
        </button>
        {children}
      </div>
    </div>,
    document.body
  );
}
```

### Error Boundary

```typescript
class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorUI />;
    }
    return this.props.children;
  }
}
```

---

## Common Mistakes

1. **Prop drilling** - Use Context or state management for deeply nested data
2. **Over-memoizing** - Only memoize expensive operations, not everything
3. **useEffect for derived state** - Use useMemo instead
4. **Giant components** - Split into smaller, focused components
5. **Inline functions in JSX** - Use useCallback for frequently re-rendered components

---

## Checklist

- [ ] Components are small and focused
- [ ] Custom hooks extract reusable logic
- [ ] Context used sparingly (theme, auth, locale)
- [ ] Performance optimizations applied where needed
- [ ] TypeScript types are strict and accurate
- [ ] Components are testable in isolation

---

## Next Steps

- M-JS-004: TypeScript Patterns
- M-JS-005: Testing with Jest/Vitest
- M-JS-008: Code Quality

---

*Methodology M-JS-002 v1.0*
