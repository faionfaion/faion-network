---
name: free-auth-supabase
description: Add email/password auth to your app using Supabase free tier — signup, login, session listener, env vars — no backend required.
tier: free
group: cost-free-stack
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working email/password auth flow in your Next.js or vanilla JS app: users can sign up, sign in, and your app reacts to session changes automatically. Everything runs on Supabase's free tier (up to 50,000 monthly active users).

## Prerequisites

- A free Supabase account (sign up at https://supabase.com).
- Node.js 18+ and npm or pnpm installed.
- An existing Next.js project (or a vanilla JS app with a module bundler like Vite).
- Ability to set environment variables (a `.env.local` file or your host's env panel).

## Steps

1. Sign in at https://supabase.com/dashboard and click **New project**.

2. Fill in the project name (e.g. `myapp-auth`), choose a region close to your users, and set a strong database password. Click **Create new project** and wait ~60 seconds for provisioning.

3. Open **Project Settings → API**. Copy two values:
   - **Project URL** (looks like `https://abcdefghijklm.supabase.co`)
   - **anon / public key** (a long JWT string starting with `eyJ`)

4. Create (or open) `.env.local` in your project root and add:

   ```
   NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklm.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-anon-key>
   ```

   Replace the URL with your project URL and `<your-anon-key>` with the anon key you copied.

5. Install the Supabase JS client:

   ```bash
   npm install @supabase/supabase-js
   ```

6. Create `lib/supabaseClient.js` (or `.ts`) with:

   ```js
   import { createClient } from '@supabase/supabase-js'

   const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
   const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

   export const supabase = createClient(supabaseUrl, supabaseAnonKey)
   ```

7. Wire up **sign-up** in your registration form handler:

   ```js
   import { supabase } from '../lib/supabaseClient'

   async function handleSignUp(email, password) {
     const { data, error } = await supabase.auth.signUp({ email, password })
     if (error) {
       console.error('Sign-up error:', error.message)
       return
     }
     // data.user is set; Supabase sends a confirmation email by default
     console.log('Signed up:', data.user?.email)
   }
   ```

8. Wire up **sign-in** in your login form handler:

   ```js
   async function handleSignIn(email, password) {
     const { data, error } = await supabase.auth.signInWithPassword({
       email,
       password,
     })
     if (error) {
       console.error('Sign-in error:', error.message)
       return
     }
     console.log('Signed in, session expires:', data.session?.expires_at)
   }
   ```

9. Add a **session listener** so your UI reacts whenever the session changes (sign-in, sign-out, token refresh). In Next.js, add this to your root layout or `_app.js`:

   ```js
   import { useEffect, useState } from 'react'
   import { supabase } from '../lib/supabaseClient'

   export default function App({ Component, pageProps }) {
     const [session, setSession] = useState(null)

     useEffect(() => {
       // Load current session on mount
       supabase.auth.getSession().then(({ data }) => {
         setSession(data.session)
       })

       // Subscribe to future auth changes
       const { data: listener } = supabase.auth.onAuthStateChange(
         (_event, newSession) => {
           setSession(newSession)
         }
       )

       // Unsubscribe on component unmount
       return () => listener.subscription.unsubscribe()
     }, [])

     return <Component {...pageProps} session={session} />
   }
   ```

10. Add a **sign-out** button:

    ```js
    async function handleSignOut() {
      const { error } = await supabase.auth.signOut()
      if (error) console.error('Sign-out error:', error.message)
    }
    ```

11. (Optional) Disable email confirmation during development: in the Supabase dashboard go to **Authentication → Providers → Email** and turn off **Confirm email**. Re-enable before going to production.

## Verify

Open your browser's Network tab, submit the sign-up form, and check for a `POST` request to `https://abcdefghijklm.supabase.co/auth/v1/signup` returning HTTP `200` with a `user` object in the response body.

Alternatively, run this one-shot check from the terminal after installing the client in a test script:

```js
// check-auth.mjs
import { createClient } from '@supabase/supabase-js'
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
const { data, error } = await sb.auth.signUp({ email: 'testuser@mailinator.com', password: 'Test1234!' })
console.log(error ?? `user id: ${data.user.id}`)
```

```bash
node --env-file=.env.local check-auth.mjs
```

A line like `user id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` confirms auth is working.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Invalid API key` error on every request | Wrong or missing anon key | Re-copy the anon key from **Project Settings → API**; make sure `.env.local` uses `NEXT_PUBLIC_` prefix so the value reaches the browser bundle |
| Sign-up returns `User already registered` | The email was used before | Use a different test email or delete the user in **Authentication → Users** in the dashboard |
| `signUp` succeeds but login always fails with `Email not confirmed` | Email confirmation is enabled | For dev: disable **Confirm email** in **Authentication → Providers → Email**; for prod: instruct users to click the confirmation link |
| Session is `null` after page reload | `getSession()` not called on mount | Ensure the `useEffect` block that calls `supabase.auth.getSession()` runs in your root component (step 9 above) |
| `process.env.NEXT_PUBLIC_SUPABASE_URL` is `undefined` | Env vars not loaded | Next.js requires a restart after adding `.env.local`; stop and rerun `npm run dev` |

## Next

- Add **OAuth providers** (Google, GitHub) via **Authentication → Providers** in the Supabase dashboard — no backend code required.
- Protect pages with server-side session checks using `@supabase/ssr` package for Next.js App Router.
- Upgrade to Supabase Pro ($25/mo) when you exceed 50k MAU or need daily backups and custom SMTP.

## References

- [knowledge/free/dev/javascript-developer/react-hooks](../../../knowledge/free/dev/javascript-developer/react-hooks) — the `useEffect` cleanup pattern (step 9) relies on the hook's return-value unsubscribe contract to prevent the auth listener from leaking across re-renders.
- [knowledge/free/dev/javascript-developer/nodejs-patterns](../../../knowledge/free/dev/javascript-developer/nodejs-patterns) — service-layer separation used to isolate `supabaseClient.js` from form handlers, matching the controllers-call-services pattern this methodology defines.
