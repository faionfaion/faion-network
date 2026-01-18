# Performance & Core Web Vitals Reference

## Core Web Vitals (2025)

### Current Metrics

| Metric | Description | Good | Needs Improvement | Poor |
|--------|-------------|------|-------------------|------|
| **LCP** | Largest Contentful Paint | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** | Interaction to Next Paint | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** | Cumulative Layout Shift | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

> **Note:** FID (First Input Delay) was replaced by INP in March 2024.

### Passing Assessment

To pass Core Web Vitals:
- 75% of page views must meet "Good" threshold for each metric
- Measured from real user data (CrUX)

---

## LCP Optimization (Largest Contentful Paint)

### What Counts as LCP?

- `<img>` elements
- `<image>` inside `<svg>`
- `<video>` poster images
- Background images via `url()`
- Block-level elements with text

### Quick Wins

```html
<!-- 1. Preload LCP image -->
<link rel="preload" as="image" href="/hero-image.webp" fetchpriority="high">

<!-- 2. Use fetchpriority on LCP image -->
<img src="/hero.webp" fetchpriority="high" alt="Hero">

<!-- 3. Avoid lazy loading LCP -->
<!-- ❌ Bad -->
<img src="/hero.webp" loading="lazy" alt="Hero">
<!-- ✅ Good -->
<img src="/hero.webp" alt="Hero">
```

### Server Optimization

```nginx
# Nginx - Enable compression
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# Enable caching
location ~* \.(jpg|jpeg|png|gif|ico|css|js|webp|avif)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Checklist

- [ ] LCP element loads in first 2.5 seconds
- [ ] Preload LCP image with `fetchpriority="high"`
- [ ] Use modern formats (WebP, AVIF)
- [ ] Compress images (Squoosh, Sharp)
- [ ] Use CDN for static assets
- [ ] Minimize server response time (TTFB < 800ms)
- [ ] Avoid render-blocking CSS/JS
- [ ] Inline critical CSS

---

## INP Optimization (Interaction to Next Paint)

### What INP Measures

INP measures the delay between user interaction (click, tap, key press) and the browser painting the visual response. It captures the *worst* interaction during the page visit.

### Main Thread Blocking

```javascript
// ❌ Long task blocks main thread
function processData(data) {
  // 500ms of synchronous work
  for (let i = 0; i < 1000000; i++) {
    // Heavy computation
  }
}

// ✅ Break into chunks
async function processDataChunked(data) {
  for (let i = 0; i < data.length; i += 100) {
    processChunk(data.slice(i, i + 100));
    await new Promise(resolve => setTimeout(resolve, 0)); // Yield to main thread
  }
}
```

### Using `requestIdleCallback`

```javascript
// Schedule low-priority work
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && tasks.length > 0) {
    performTask(tasks.shift());
  }
});
```

### Checklist

- [ ] No single task longer than 50ms
- [ ] Defer non-critical JavaScript
- [ ] Use `requestIdleCallback` for low-priority work
- [ ] Avoid forced synchronous layouts
- [ ] Minimize JavaScript bundle size
- [ ] Use Web Workers for heavy computation
- [ ] Implement code splitting

---

## CLS Optimization (Cumulative Layout Shift)

### Common Causes

1. Images without dimensions
2. Ads, embeds, iframes without reserved space
3. Dynamically injected content
4. Web fonts causing FOIT/FOUT
5. Actions waiting for network before updating DOM

### Image Dimensions

```html
<!-- ❌ Bad - No dimensions -->
<img src="/photo.jpg" alt="Photo">

<!-- ✅ Good - Explicit dimensions -->
<img src="/photo.jpg" width="800" height="600" alt="Photo">

<!-- ✅ Good - Aspect ratio CSS -->
<img src="/photo.jpg" alt="Photo" style="aspect-ratio: 4/3; width: 100%;">
```

### Reserving Space

```css
/* Reserve space for ads */
.ad-container {
  min-height: 250px; /* Expected ad height */
  background: #f0f0f0;
}

/* Reserve space for embeds */
.video-container {
  aspect-ratio: 16/9;
  width: 100%;
}
```

### Font Loading

```css
/* Prevent FOIT (Flash of Invisible Text) */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately */
}
```

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
```

### Checklist

- [ ] All images have width/height or aspect-ratio
- [ ] Reserve space for ads and embeds
- [ ] Use `font-display: swap` with font preload
- [ ] Don't insert content above existing content
- [ ] Transform animations instead of layout-changing animations
- [ ] Use `contain: layout` where appropriate

---

## Image Optimization

### Modern Formats

| Format | Use Case | Browser Support |
|--------|----------|-----------------|
| **WebP** | General purpose | 97%+ |
| **AVIF** | Best compression | 85%+ |
| **JPEG** | Photos (fallback) | 100% |
| **PNG** | Transparency needed | 100% |
| **SVG** | Icons, logos | 100% |

### Responsive Images

```html
<!-- srcset for different sizes -->
<img
  src="/image-800.jpg"
  srcset="
    /image-400.jpg 400w,
    /image-800.jpg 800w,
    /image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
>

<!-- Picture for format switching -->
<picture>
  <source srcset="/image.avif" type="image/avif">
  <source srcset="/image.webp" type="image/webp">
  <img src="/image.jpg" alt="Description">
</picture>
```

### Lazy Loading

```html
<!-- Native lazy loading (below-fold images) -->
<img src="/photo.jpg" loading="lazy" alt="Photo">

<!-- Never lazy load LCP image -->
<img src="/hero.jpg" alt="Hero"> <!-- No loading attribute -->
```

---

## JavaScript Optimization

### Code Splitting

```javascript
// Dynamic import
const module = await import('./heavy-module.js');

// React lazy loading
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

### Defer vs Async

```html
<!-- Defer: Execute after HTML parsing, in order -->
<script defer src="/app.js"></script>

<!-- Async: Execute as soon as downloaded -->
<script async src="/analytics.js"></script>
```

### Bundle Analysis

```bash
# Webpack
npx webpack-bundle-analyzer stats.json

# Vite
npx vite-bundle-visualizer

# Next.js
ANALYZE=true npm run build
```

---

## CSS Optimization

### Critical CSS

```html
<!-- Inline critical CSS -->
<style>
  /* Above-the-fold styles only */
  header { ... }
  .hero { ... }
</style>

<!-- Load rest asynchronously -->
<link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles.css"></noscript>
```

### Avoid Render Blocking

```html
<!-- ❌ Render blocking -->
<link rel="stylesheet" href="/styles.css">

<!-- ✅ Non-blocking (print media, then switch) -->
<link rel="stylesheet" href="/styles.css" media="print" onload="this.media='all'">
```

---

## Caching Strategy

### Cache-Control Headers

```nginx
# Static assets (images, fonts, JS, CSS)
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2|webp|avif)$ {
    expires 1y;
    add_header Cache-Control "public, max-age=31536000, immutable";
}

# HTML pages
location ~* \.html$ {
    add_header Cache-Control "no-cache, must-revalidate";
}

# API responses
location /api/ {
    add_header Cache-Control "private, max-age=0, no-cache";
}
```

### Service Worker

```javascript
// Basic caching strategy
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

---

## Measurement Tools

| Tool | Use Case |
|------|----------|
| [PageSpeed Insights](https://pagespeed.web.dev/) | Lab + field data, recommendations |
| [web.dev/measure](https://web.dev/measure/) | Lighthouse-based |
| Chrome DevTools → Lighthouse | Local testing |
| Chrome DevTools → Performance | Detailed profiling |
| [WebPageTest](https://www.webpagetest.org/) | Multi-location, filmstrip |
| Search Console → Core Web Vitals | Real user data |
| [CrUX Dashboard](https://developer.chrome.com/docs/crux/) | Historical field data |

---

## Performance Budget

### Example Budget

| Resource | Budget |
|----------|--------|
| Total page weight | < 1.5 MB |
| JavaScript | < 300 KB (compressed) |
| CSS | < 100 KB (compressed) |
| Images | < 1 MB |
| Fonts | < 100 KB |
| LCP | < 2.5s |
| INP | < 200ms |
| CLS | < 0.1 |

### Monitoring

```javascript
// Report Web Vitals
import { onCLS, onINP, onLCP } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id,
  });
  navigator.sendBeacon('/analytics', body);
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
```
