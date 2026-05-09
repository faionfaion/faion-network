---
type: change-request
cr_id: CR-004
title: "Reuse Storybook Components in Next.js Starter Kit"
priority: P1
created: 2026-01-23
status: approved
affected_components: [faion-starter-nextjs, faion-network-storybook]
related: [TASK-SK-003, CR-003]
---

# Change Request: Reuse Storybook Components in Next.js Starter Kit

## Discovery

Faion Network Storybook (`faion-network-storybook`) contains 62 production-ready React components with CSS styling (no Tailwind), including:

**Pricing Components** (Perfect for Stripe integration):
- `PricingCard.tsx` - Pricing tier cards
- `PricingToggle.tsx` - Monthly/Annual toggle
- `PromoCodeInput.tsx` - Promo code input
- `PlanComparisonTable.tsx` - Plan comparison table
- `FeatureList.tsx` - Feature list with checkmarks

**UI Components:**
- `Button.tsx`, `Card.tsx`, `Badge.tsx`
- `Header.tsx`, `Footer.tsx`
- `Accordion`, `Breadcrumb`, `Checkbox`, `Input`
- 50+ more components

**Landing Page Components:**
- `HeroSection.tsx`
- `FAQSection.tsx`
- `FinalCTASection.tsx`

**Layout Components:**
- `DashboardLayout.tsx`
- `MinimalLayout.tsx`
- `LegalPageLayout.tsx`

**All components use CSS Modules/plain CSS** - perfect match for Next.js starter kit requirements!

## Current Situation

TASK-SK-003 requires building Next.js starter kit from scratch with:
- UI components (Button, Card)
- Pricing components (for Stripe)
- Landing page sections
- Header/Footer
- Dashboard layout

**Problem:** We'd be recreating components that already exist in Storybook.

## Proposed Solution

### Option 1: Copy Components from Storybook (Recommended)

Copy relevant components from `faion-network-storybook/src/components/` to Next.js starter kit.

**Steps:**
1. Create Next.js project (without Tailwind)
2. Copy needed components:
   ```bash
   # Pricing components
   cp -r faion-network-storybook/src/components/pricing/ \
         faion-starter-nextjs/src/components/pricing/

   # UI components
   cp faion-network-storybook/src/components/ui/Button.* \
      faion-starter-nextjs/src/components/ui/
   cp faion-network-storybook/src/components/ui/Card.* \
      faion-starter-nextjs/src/components/ui/

   # Layout
   cp faion-network-storybook/src/components/Header.* \
      faion-starter-nextjs/src/components/
   cp faion-network-storybook/src/components/Footer.* \
      faion-starter-nextjs/src/components/
   ```

3. Adapt for Next.js (minimal changes):
   - Change imports if needed
   - Add `'use client'` directive if using interactivity
   - Test in Next.js environment

4. Add Stripe integration to PricingCard component

**Pros:**
- ✅ Saves 4-6 hours of UI development
- ✅ Components already tested and polished
- ✅ Consistent design system
- ✅ CSS already written (no Tailwind needed)
- ✅ Can customize for starter kit needs

**Cons:**
- ⚠️ May need minor adaptations for Next.js
- ⚠️ Need to maintain two copies (Storybook + starter kit)

### Option 2: Create Shared NPM Package

Publish Storybook components as `@faion/ui` npm package.

**Pros:**
- Single source of truth
- Easy updates
- Can use in multiple projects

**Cons:**
- Requires packaging setup
- Adds dependency to starter kit
- Overkill for v1

### Option 3: Use Storybook as Submodule

Add Storybook as git submodule in starter kit.

**Pros:**
- Shared code
- Version control

**Cons:**
- Complex for users downloading kit
- Not typical for starter kits

## Recommendation

**Option 1: Copy components**

Reasons:
- **Fast:** Saves 4-6 hours vs building from scratch
- **Proven:** Components already tested in Storybook
- **Standalone:** Starter kit remains self-contained
- **Customizable:** Users can modify copied components
- **No dependencies:** No external package needed

## Implementation Plan

### Phase 1: Identify Components to Copy (~30 min)

**Must-have:**
- `components/ui/Button.tsx` + CSS
- `components/ui/Card.tsx` + CSS
- `components/pricing/PricingCard.tsx` + CSS
- `components/pricing/PricingToggle.tsx` + CSS
- `components/Header.tsx` + CSS
- `components/Footer.tsx` + CSS

**Nice-to-have:**
- `components/ui/Badge.tsx`
- `components/ui/Input.tsx`
- `components/landing/HeroSection.tsx`
- `components/layout/DashboardLayout.tsx`

### Phase 2: Copy & Adapt (~1-2 hours)

1. **Create Next.js project:**
   ```bash
   npx create-next-app@latest faion-starter-nextjs \
     --typescript --app --src-dir --eslint --no-tailwind --no-git
   ```

2. **Copy component files:**
   - Copy .tsx and .css files
   - Maintain folder structure

3. **Adapt for Next.js:**
   - Add `'use client'` where needed (interactive components)
   - Fix import paths
   - Test each component

4. **Create index files:**
   ```typescript
   // components/ui/index.ts
   export { Button } from './Button';
   export { Card } from './Card';
   ```

### Phase 3: Integrate Stripe (~2 hours)

1. **Update PricingCard component:**
   - Add Stripe checkout button
   - Connect to `/api/checkout` endpoint

2. **Create Stripe API routes:**
   - `app/api/checkout/route.ts`
   - `app/api/webhooks/stripe/route.ts`
   - `app/api/portal/route.ts`

### Phase 4: Build Pages (~2 hours)

1. **Landing page:** Use copied HeroSection + PricingCard
2. **Pricing page:** PricingToggle + multiple PricingCards
3. **Dashboard:** Use DashboardLayout + SubscriptionStatus

## Updated Effort Estimate

**With component reuse:**
- Project setup: 30 min
- Copy & adapt components: 1-2 hours
- Stripe integration: 2 hours
- Pages: 2 hours
- Documentation: 30 min
- Testing: 1 hour

**Total:** ~6-7 hours (vs ~7-9 hours building from scratch)

**Savings:** 1-2 hours + guaranteed quality

## Acceptance Criteria

- [ ] Components copied from Storybook to Next.js kit
- [ ] All components work in Next.js environment
- [ ] `'use client'` directives added where needed
- [ ] Styling intact (CSS working)
- [ ] Stripe integration functional
- [ ] Landing page uses copied components
- [ ] Pricing page with Stripe checkout working
- [ ] Documentation mentions component source

## References

- [TASK-SK-003](../../todo/TASK-SK-003-create-nextjs-kit.md)
- [CR-003](CR-003-incomplete-nextjs-starter.md)
- [Storybook CLAUDE.md](../../faion-network-storybook/CLAUDE.md)
- Storybook components: `~/Projects/faion-net/faion-network-storybook/src/components/`

---

*Created: 2026-01-23*
*Status: Approved for implementation*
*Reduces TASK-SK-003 effort by 1-2 hours*
