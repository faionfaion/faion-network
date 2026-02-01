# TypeScript & React 2026

**Modern TypeScript 5.x and React 19 patterns for 2026.**

---

## Quick Reference

| Technology | Version | Status |
|------------|---------|--------|
| TypeScript | 5.x with strict mode | Stable |
| React | 19.x with Server Components | Stable |
| Next.js | 15.x with App Router | Stable |

---

## TypeScript 5.x Patterns

### TypeScript 5 Strict Configuration

**Problem:** TypeScript without proper configuration allows unsafe patterns.

**Framework:**

```json
// tsconfig.json (2026 recommended)
{
  "compilerOptions": {
    // Strict type checking (all enabled)
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,

    // Modern module resolution
    "target": "ES2023",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,

    // TypeScript 5 features
    "allowImportingTsExtensions": true,
    "resolvePackageJsonExports": true,
    "resolvePackageJsonImports": true,

    // Interop
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}
```

**TypeScript 5 Key Features:**

1. **Improved type inference:**
   - Better inference for generics
   - Union enum improvements
   - const type parameters

2. **Decorators (stable):**
   ```typescript
   function logged(target: any, context: ClassMethodDecoratorContext) {
     return function (...args: any[]) {
       console.log(`Calling ${String(context.name)}`);
       return target.apply(this, args);
     };
   }

   class UserService {
     @logged
     createUser(data: UserData): User {
       // implementation
     }
   }
   ```

3. **const type parameters:**
   ```typescript
   function createConfig<const T extends readonly string[]>(items: T): T {
     return items;
   }

   const config = createConfig(['a', 'b', 'c']);
   // Type: readonly ['a', 'b', 'c'] instead of string[]
   ```

**Sources:**
- [TypeScript 5 Design Patterns - Packt](https://www.packtpub.com/en-us/product/typescript-5-design-patterns-and-best-practices-9781835883235)
- [TypeScript Best Practices 2025 - DEV](https://dev.to/mitu_mariam/typescript-best-practices-in-2025-57hb)

---

### TypeScript Advanced Patterns

**Problem:** Complex type transformations and generic patterns.

**Framework:**

1. **Mapped types for transformation:**
   ```typescript
   // Make all properties optional and nullable
   type Partial<T> = { [K in keyof T]?: T[K] | null };

   // Create readonly version
   type Immutable<T> = { readonly [K in keyof T]: Immutable<T[K]> };

   // Extract specific keys
   type Pick<T, K extends keyof T> = { [P in K]: T[P] };
   ```

2. **Template literal types:**
   ```typescript
   type EventName = `on${Capitalize<string>}`;
   type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
   type APIEndpoint = `/api/${string}`;

   // Complex patterns
   type CSSProperty = `${string}-${string}`;
   type LocaleKey = `${string}.${string}`;
   ```

3. **Conditional types:**
   ```typescript
   type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
   type ArrayElement<T> = T extends (infer U)[] ? U : never;

   // Utility for API responses
   type ApiResponse<T> = T extends void
     ? { success: boolean }
     : { success: boolean; data: T };
   ```

4. **Satisfies operator (TS 4.9+):**
   ```typescript
   const config = {
     port: 3000,
     host: 'localhost',
   } satisfies ServerConfig;
   // Type is inferred, but validated against ServerConfig
   ```

**Checklist:**
- [ ] Use `unknown` over `any`
- [ ] Explicit return types for public functions
- [ ] Type guards for runtime checks
- [ ] Discriminated unions for complex state
- [ ] Generic constraints properly defined

---

## React 19 & Server Components

### React 19 Server Components Architecture

**Problem:** Understanding when and how to use Server Components effectively.

**Framework:**

1. **Server vs Client Components:**

   | Feature | Server Component | Client Component |
   |---------|-----------------|------------------|
   | Data fetching | Direct DB/API access | Via hooks/fetch |
   | Interactivity | None | Full |
   | JavaScript sent | Zero | Full bundle |
   | `use client` | Not needed | Required at boundary |

2. **Component tree design:**
   ```tsx
   // Server Component (default in app/)
   async function ProductPage({ id }: { id: string }) {
     const product = await db.products.findById(id);  // Direct DB access

     return (
       <div>
         <ProductInfo product={product} />  {/* Server */}
         <AddToCartButton productId={id} /> {/* Client */}
       </div>
     );
   }

   // Client boundary
   'use client';
   function AddToCartButton({ productId }: { productId: string }) {
     const [loading, setLoading] = useState(false);
     // Interactive client code
   }
   ```

3. **Data fetching patterns:**
   ```tsx
   // Server Component - direct fetch
   async function UserProfile({ userId }: Props) {
     const user = await fetch(`/api/users/${userId}`).then(r => r.json());
     return <Profile user={user} />;
   }

   // Parallel data fetching
   async function Dashboard() {
     const [users, products, orders] = await Promise.all([
       fetchUsers(),
       fetchProducts(),
       fetchOrders(),
     ]);
     return <DashboardView users={users} products={products} orders={orders} />;
   }
   ```

**Key Rules:**
- Server Components can import Client Components
- Client Components CANNOT import Server Components
- Mark client boundary with `'use client'` only when needed
- Children of Client Components become Client Components

**Performance:** 38% faster initial load times (WebPageTest Benchmark, Feb 2025).

**Sources:**
- [React 19 Official - react.dev](https://react.dev/blog/2024/12/05/react-19)
- [Server Components - react.dev](https://react.dev/reference/rsc/server-components)
- [Making Sense of RSC - Josh Comeau](https://www.joshwcomeau.com/react/server-components/)

---

### React 19 Server Actions

**Problem:** Simplifying form handling and data mutations.

**Framework:**

1. **Basic Server Action:**
   ```tsx
   // actions.ts
   'use server';

   import { db } from '@/lib/db';
   import { revalidatePath } from 'next/cache';

   export async function createUser(formData: FormData) {
     const name = formData.get('name') as string;
     const email = formData.get('email') as string;

     await db.users.create({ name, email });
     revalidatePath('/users');
   }
   ```

2. **Using in forms:**
   ```tsx
   // Component
   import { createUser } from './actions';

   function UserForm() {
     return (
       <form action={createUser}>
         <input name="name" required />
         <input name="email" type="email" required />
         <button type="submit">Create User</button>
       </form>
     );
   }
   ```

3. **With useFormState (for client feedback):**
   ```tsx
   'use client';

   import { useFormState, useFormStatus } from 'react-dom';
   import { createUser } from './actions';

   function SubmitButton() {
     const { pending } = useFormStatus();
     return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>;
   }

   function UserForm() {
     const [state, formAction] = useFormState(createUser, { error: null });

     return (
       <form action={formAction}>
         {state.error && <p className="error">{state.error}</p>}
         <input name="name" required />
         <SubmitButton />
       </form>
     );
   }
   ```

4. **Validation pattern:**
   ```tsx
   'use server';

   import { z } from 'zod';

   const UserSchema = z.object({
     name: z.string().min(2),
     email: z.string().email(),
   });

   export async function createUser(prevState: any, formData: FormData) {
     const validatedFields = UserSchema.safeParse({
       name: formData.get('name'),
       email: formData.get('email'),
     });

     if (!validatedFields.success) {
       return { error: validatedFields.error.flatten().fieldErrors };
     }

     await db.users.create(validatedFields.data);
     revalidatePath('/users');
     return { success: true };
   }
   ```

---

### Next.js 15 Patterns

**Problem:** Optimal patterns for Next.js 15 App Router.

**Framework:**

1. **Route structure:**
   ```
   app/
   ├── layout.tsx          # Root layout
   ├── page.tsx            # Home page (/)
   ├── loading.tsx         # Loading UI
   ├── error.tsx           # Error boundary
   ├── not-found.tsx       # 404 page
   │
   ├── (marketing)/        # Route group (no URL segment)
   │   ├── about/
   │   │   └── page.tsx    # /about
   │   └── blog/
   │       └── page.tsx    # /blog
   │
   ├── dashboard/
   │   ├── layout.tsx      # Dashboard layout
   │   ├── page.tsx        # /dashboard
   │   ├── settings/
   │   │   └── page.tsx    # /dashboard/settings
   │   └── @analytics/     # Parallel route
   │       └── page.tsx
   │
   └── api/
       └── users/
           └── route.ts    # API route
   ```

2. **Metadata API:**
   ```tsx
   // Static metadata
   export const metadata = {
     title: 'My App',
     description: 'App description',
   };

   // Dynamic metadata
   export async function generateMetadata({ params }: Props) {
     const product = await getProduct(params.id);
     return {
       title: product.name,
       openGraph: { images: [product.image] },
     };
   }
   ```

3. **Parallel routes:**
   ```tsx
   // app/dashboard/layout.tsx
   export default function DashboardLayout({
     children,
     analytics,
     notifications,
   }: {
     children: React.ReactNode;
     analytics: React.ReactNode;
     notifications: React.ReactNode;
   }) {
     return (
       <div className="dashboard">
         <main>{children}</main>
         <aside>
           {analytics}
           {notifications}
         </aside>
       </div>
     );
   }
   ```

4. **Intercepting routes:**
   ```
   app/
   ├── photos/
   │   └── [id]/
   │       └── page.tsx       # /photos/123 (full page)
   └── @modal/
       └── (.)photos/
           └── [id]/
               └── page.tsx   # Modal intercept
   ```

**Sources:**
- [React 19 and TypeScript Best Practices 2025 - Medium](https://medium.com/@CodersWorld99/react-19-typescript-best-practices-the-new-rules-every-developer-must-follow-in-2025-3a74f63a0baf)
- [React 19.2 - react.dev](https://react.dev/blog/2025/10/01/react-19-2)

---

## Methodologies Index

| Name | Section |
|------|---------|
| TypeScript 5 Strict Configuration | TypeScript |
| TypeScript Advanced Patterns | TypeScript |
| React 19 Server Components Architecture | React 19 |
| React 19 Server Actions | React 19 |
| Next.js 15 Patterns | React 19 |

---

## References

**TypeScript:**
- [TypeScript 5 Design Patterns - Packt](https://www.packtpub.com/en-us/product/typescript-5-design-patterns-and-best-practices-9781835883235)
- [TypeScript Best Practices 2025 - DEV](https://dev.to/mitu_mariam/typescript-best-practices-in-2025-57hb)

**React/Next.js:**
- [React 19 Official](https://react.dev/blog/2024/12/05/react-19)
- [Server Components - react.dev](https://react.dev/reference/rsc/server-components)
- [Making Sense of RSC - Josh Comeau](https://www.joshwcomeau.com/react/server-components/)
- [What's New in React 19 - Vercel](https://vercel.com/blog/whats-new-in-react-19)

---

*TypeScript & React 2026 v1.0*
*Last updated: 2026-01-23*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Modern React with TypeScript | sonnet | Current best practices |
| Type-safe props | sonnet | API design |
