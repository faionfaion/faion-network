# Conversion Tracking Plan: [Site/App]

## Macro Conversions (Primary Goals)

| Conversion         | Value     | Meta Event          | Google Event    | LinkedIn Event |
|--------------------|-----------|---------------------|-----------------|----------------|
| Purchase           | Dynamic   | Purchase            | purchase        | conversion     |
| Trial start        | $50       | StartTrial          | trial_started   | —              |
| Lead form submit   | $25       | Lead                | generate_lead   | lead           |

## Micro Conversions (Optimization Signals)

| Conversion         | Meta Event       | Google Event    | LinkedIn Event |
|--------------------|------------------|-----------------|----------------|
| Pricing page view  | ViewContent      | page_view       | pageLoad       |
| Add to cart        | AddToCart        | add_to_cart     | —              |
| Begin checkout     | InitiateCheckout | begin_checkout  | —              |
| Sign up            | CompleteRegistration | sign_up     | signUp         |

## Implementation Checklist

### Meta
- [ ] Pixel base code on all pages
- [ ] Standard events firing on correct pages
- [ ] Dynamic values passing (Purchase)
- [ ] CAPI server-side configured
- [ ] Event IDs matching between browser and server
- [ ] Events Manager shows Active status

### Google
- [ ] gtag base code on all pages
- [ ] Conversion actions created in Google Ads
- [ ] Conversion tags on thank-you pages
- [ ] Transaction IDs passing (purchase deduplication)
- [ ] Tag Assistant shows events firing

### LinkedIn
- [ ] Insight Tag on all pages
- [ ] Conversion events configured
- [ ] Events firing verified

## Attribution Windows

| Platform  | Click Window | View Window |
|-----------|-------------|-------------|
| Meta      | 7 days      | 1 day       |
| Google    | 30 days     | —           |
| LinkedIn  | 30 days     | 7 days      |
