---
type: change-request
cr_id: CR-003
title: "Complete Next.js Starter Kit Implementation"
priority: P1
created: 2026-01-23
status: pending
affected_components: [faion-starter-nextjs]
related_tasks: [TASK-SK-003]
---

# Change Request: Complete Next.js Starter Kit Implementation

## Issue

TASK-SK-003 (Create Next.js Starter Kit) was partially started but not completed. Base project structure exists but is missing key features.

## Current State

**What exists (but INCORRECT):**
- ⚠️ Next.js 16.1.4 project created WITH Tailwind CSS (needs recreation)
- ✅ TypeScript configured
- ✅ ESLint configured
- ✅ Basic project structure (`src/app/`)

**What's missing:**
- ❌ Recreate project WITHOUT Tailwind (use CSS Modules)
- ❌ Prettier configuration
- ❌ Stripe integration
  - Checkout API route
  - Webhook handler
  - Customer portal
  - Subscription components
- ❌ UI components (Button, Card, PricingCard, SubscriptionStatus)
- ❌ Header and Footer components
- ❌ Pages: Landing (hero), Pricing, Dashboard/Settings
- ❌ Example route groups
- ❌ CSS Modules styling
- ❌ Documentation (README with Stripe setup guide)
- ❌ `.env.example` file with Stripe keys
- ❌ `faion.json` metadata
- ❌ Production build verification

## Impact

**Medium Priority:**
- Cannot deliver complete Next.js starter kit
- Users downloading kit will get minimal setup
- Missing polish and example components
- Incomplete documentation

**User Experience:**
- Expected: Production-ready Next.js starter with best practices
- Actual: Basic Next.js + Tailwind setup
- Gap: ~40% of functionality missing (docs, examples, polish)

## Required Work

### Phase 1: Project Recreation (~30 min)

1. **Remove existing faion-starter-nextjs:**
   ```bash
   rm -rf faion-starter-nextjs/
   ```

2. **Create new Next.js project WITHOUT Tailwind:**
   ```bash
   npx create-next-app@latest faion-starter-nextjs \
     --typescript --app --src-dir \
     --import-alias "@/*" --eslint --no-tailwind --no-git --yes
   ```

3. **Add Prettier:**
   ```bash
   npm install -D prettier
   ```

### Phase 2: Stripe Integration (~2-3 hours)

1. **Install Stripe:**
   ```bash
   npm install stripe @stripe/stripe-js
   ```

2. **Setup Stripe client:**
   - `lib/stripe/client.ts` - Client-side Stripe
   - `lib/stripe/server.ts` - Server-side Stripe

3. **API routes:**
   - `app/api/checkout/route.ts` - Create checkout session
   - `app/api/portal/route.ts` - Customer portal
   - `app/api/webhooks/stripe/route.ts` - Handle webhooks

4. **Environment variables:**
   - STRIPE_SECRET_KEY
   - STRIPE_PUBLISHABLE_KEY
   - STRIPE_WEBHOOK_SECRET
   - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY

### Phase 3: UI Components (~2 hours)

1. **Basic UI components (CSS Modules):**
   - `components/ui/Button.tsx` + `Button.module.css`
   - `components/ui/Card.tsx` + `Card.module.css`
   - `components/ui/PricingCard.tsx` + `PricingCard.module.css`

2. **Billing components:**
   - `components/billing/SubscriptionStatus.tsx`
   - `components/billing/ManageSubscription.tsx`

3. **Layout components:**
   - `components/Header.tsx` + `Header.module.css`
   - `components/Footer.tsx` + `Footer.module.css`

### Phase 4: Pages (~2 hours)

1. **Landing page:**
   - `app/page.tsx` - Hero + features + CTA

2. **Pricing page:**
   - `app/pricing/page.tsx` - Pricing tiers with Stripe checkout

3. **Dashboard:**
   - `app/dashboard/page.tsx` - Simple dashboard
   - `app/dashboard/settings/page.tsx` - Subscription management

4. **Global styles:**
   - Update `app/globals.css` with base styles (no Tailwind)

### Phase 5: Documentation (~30 min)

1. **README.md:**
   - Project overview
   - Stripe setup instructions
   - Quick start guide
   - Available scripts
   - Deployment to Vercel

2. **Configuration files:**
   - `.env.example` - All Stripe env vars
   - `faion.json` - Kit metadata

### Phase 6: Testing & Release (~1 hour)

1. **Testing:**
   - Fresh `npm install` test
   - Production build (`npm run build`)
   - Stripe test checkout (test mode)
   - Webhook handling test
   - Type checking
   - Lint test
   - Mobile responsiveness
   - Lighthouse audit

2. **Release:**
   - Clean build artifacts
   - Create ZIP (exclude node_modules, .git, .next)
   - Generate SHA256 checksum
   - Upload to R2 (when available)
   - Create database entry

## Effort Estimate

**Total Time:** ~7-9 hours
**Token Estimate:** ~80-100k tokens

**Breakdown:**
- Project Recreation: 5%
- Stripe Integration: 35%
- UI Components: 25%
- Pages: 20%
- Documentation: 5%
- Testing & Release: 10%

## Alternatives Considered

### Alternative 1: Release Current State

Ship current state as minimal Next.js starter.

**Pros:**
- Quick to release (ready now)

**Cons:**
- Has Tailwind (need to remove)
- Not polished
- Missing Stripe
- Poor documentation

### Alternative 2: Build from Scratch

Complete implementation as originally planned.

**Pros:**
- Professional quality
- Full control

**Cons:**
- 7-9 hours work
- Rebuilding UI components

### Alternative 3: Reuse Storybook Components (Recommended)

Copy components from `faion-network-storybook` - see [CR-004](CR-004-reuse-storybook-components.md).

**Pros:**
- ✅ Saves 1-2 hours
- ✅ Components already tested
- ✅ CSS styling already done (no Tailwind!)
- ✅ Consistent with Faion design system
- ✅ Includes PricingCard perfect for Stripe

**Cons:**
- Need to adapt for Next.js (minimal work)

## Recommendation

**Option 3: Reuse Storybook components (6-7 hours work)**

Reasons:
- **Efficient:** Reuse 62 existing components
- **Quality:** Components already polished and tested
- **Faster:** 1-2 hours saved vs building from scratch
- **Consistent:** Matches Faion design system
- **Perfect match:** No Tailwind, just CSS!
- **Better result:** Professional components day one

See [CR-004](CR-004-reuse-storybook-components.md) for implementation details.

## Dependencies

**Requires:**
- R2 activation (for upload) - see [CR-002](CR-002-r2-activation-blocker.md)
- No external services needed (simple starter kit)

**Blocks:**
- TASK-SK-003 completion
- Next.js kit availability in CLI
- Pro tier value proposition

## Acceptance Criteria

- [ ] All deliverables from TASK-SK-003 completed
- [ ] Prettier configured and working
- [ ] UI components (Button, Card) implemented
- [ ] Header and Footer components created
- [ ] Enhanced landing page with hero section
- [ ] Example route structure
- [ ] Mobile responsive (320px, 768px, 1024px)
- [ ] Lighthouse score > 90
- [ ] README has complete setup instructions
- [ ] `.env.example` exists (if needed)
- [ ] `faion.json` metadata correct
- [ ] Fresh `npm install && npm run dev` works
- [ ] Production build succeeds
- [ ] No TypeScript/ESLint errors

## Next Steps

1. Decide if continuing SK-003 now or after R2 setup
2. If now: Continue implementation (12-16 hours)
3. If after R2: Move to SK-004 (Laravel) or focus on R2 activation
4. Update TASK-SK-003 status accordingly

## References

- [TASK-SK-003](../../todo/TASK-SK-003-create-nextjs-kit.md)
- [CR-002: R2 Activation](CR-002-r2-activation-blocker.md)
- [Feature 024 Design](../../in-progress/feature-024-starter-kits/design.md)

---

*Created: 2026-01-23*
*Status: Awaiting decision on continuation*
*Location: `~/Projects/faion-net/faion-starter-nextjs/`*
