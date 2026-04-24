# React Patterns

**Modern React patterns and best practices**

---

## Component Architecture

```
src/
├── components/           # Shared/reusable components
│   ├── ui/              # Base UI primitives (Button, Input)
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   ├── forms/           # Form-related components
│   └── layout/          # Layout components (Header, Footer)
├── features/            # Feature-based modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.ts
│   │   └── types.ts
│   └── dashboard/
├── hooks/               # Shared custom hooks
├── utils/               # Pure utility functions
├── types/               # Shared TypeScript types
├── lib/                 # Third-party wrappers
└── app/                 # Next.js app directory / routes
```

---

## Functional Components

```tsx
// Always use function declarations for components
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
  className?: string;
}

export function UserCard({
  user,
  onEdit,
  className
}: UserCardProps): React.ReactElement {
  const handleEdit = () => {
    onEdit?.(user.id);
  };

  return (
    <div className={cn('card', className)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={handleEdit}>Edit</button>
      )}
    </div>
  );
}
```

---

## Hooks Patterns

```tsx
// Custom hook with proper typing
interface UseUserResult {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useUser(userId: string): UseUserResult {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const refetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchUser(userId);
      setUser(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    void refetch();
  }, [refetch]);

  return { user, isLoading, error, refetch };
}
```

---

## Context Pattern

```tsx
// types.ts
interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

// context.tsx
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = useCallback(async (credentials: Credentials) => {
    const userData = await authService.login(credentials);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
  }, []);

  const value = useMemo(() => ({
    user,
    isAuthenticated: user !== null,
    login,
    logout,
  }), [user, login, logout]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook with runtime check
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

---

## State Management Decision Tree

```
What kind of state?
│
├─► Server state (API data)?
│   └─► TanStack Query / SWR
│
├─► Form state?
│   └─► React Hook Form
│
├─► Global UI state (theme, sidebar)?
│   └─► Zustand (simple) / Jotai (atomic)
│
├─► Component-local state?
│   └─► useState / useReducer
│
└─► Cross-component state (same feature)?
    └─► Context + useReducer
```

---

## Performance Patterns

```tsx
// Memoize expensive computations
const sortedItems = useMemo(() => {
  return items.slice().sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// Memoize callbacks passed to children
const handleItemClick = useCallback((id: string) => {
  setSelectedId(id);
}, []);

// Memoize components with stable props
const MemoizedList = memo(function List({
  items,
  onItemClick
}: ListProps) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id} onClick={() => onItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
});

// Avoid: inline objects in JSX
<Component style={{ color: 'red' }} />  // Creates new object each render

// Prefer: stable reference
const redStyle = { color: 'red' };
<Component style={redStyle} />
```

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Render props pattern | sonnet | Pattern expertise |
| Compound components design | sonnet | API design |
| Higher-order components | sonnet | Pattern trade-offs |

## Sources

- [React Documentation](https://react.dev/) - Official React docs
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/) - TypeScript patterns
- [TanStack Query](https://tanstack.com/query/) - Server state management
- [Zustand](https://zustand-demo.pmnd.rs/) - Lightweight state management
- [Jotai](https://jotai.org/) - Atomic state management
