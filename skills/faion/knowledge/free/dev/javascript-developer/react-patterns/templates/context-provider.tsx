// purpose: canonical Context provider + consumer hook with null sentinel + memoized value
// consumes: nothing
// produces: AuthContext + AuthProvider + useAuth (template — replace Auth* with feature name)
// depends-on: react
// token-budget-impact: ~280 tokens

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
