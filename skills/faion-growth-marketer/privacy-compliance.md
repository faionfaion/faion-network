# Privacy Compliance

**Part of faion-marketing-manager skill**

## 1. GDPR Compliance

### Cookie Consent Integration

```javascript
// Cookie consent manager integration
class AnalyticsManager {
  constructor() {
    this.consentGiven = false;
    this.queuedEvents = [];
  }

  init() {
    // Check for existing consent
    const consent = localStorage.getItem('analytics_consent');
    if (consent === 'granted') {
      this.enableAnalytics();
    }
  }

  grantConsent() {
    localStorage.setItem('analytics_consent', 'granted');
    this.consentGiven = true;
    this.enableAnalytics();
    this.flushQueue();
  }

  revokeConsent() {
    localStorage.setItem('analytics_consent', 'denied');
    this.consentGiven = false;
    this.disableAnalytics();
  }

  enableAnalytics() {
    // GA4 consent update
    gtag('consent', 'update', {
      'analytics_storage': 'granted'
    });
    this.consentGiven = true;
  }

  disableAnalytics() {
    gtag('consent', 'update', {
      'analytics_storage': 'denied'
    });
    // Clear existing cookies
    this.clearAnalyticsCookies();
  }

  track(eventName, params = {}) {
    if (this.consentGiven) {
      gtag('event', eventName, params);
      plausible(eventName, { props: params });
    } else {
      // Queue events for later
      this.queuedEvents.push({ eventName, params, timestamp: Date.now() });
    }
  }

  flushQueue() {
    this.queuedEvents.forEach(({ eventName, params }) => {
      gtag('event', eventName, params);
      plausible(eventName, { props: params });
    });
    this.queuedEvents = [];
  }

  clearAnalyticsCookies() {
    // GA4 cookies
    const gaCookies = ['_ga', '_ga_*', '_gid', '_gat'];
    gaCookies.forEach(name => {
      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=.${window.location.hostname}`;
    });
  }
}

const analytics = new AnalyticsManager();
analytics.init();
```

### GA4 Consent Mode

```javascript
// Default consent state (before user choice)
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied'
});

// After user grants consent
function onConsentGranted(preferences) {
  gtag('consent', 'update', {
    'analytics_storage': preferences.analytics ? 'granted' : 'denied',
    'ad_storage': preferences.marketing ? 'granted' : 'denied',
    'ad_user_data': preferences.marketing ? 'granted' : 'denied',
    'ad_personalization': preferences.marketing ? 'granted' : 'denied'
  });
}
```

### Data Retention Settings

```javascript
// Configure data retention (in GA4 Admin)
// Options: 2 months, 14 months

// Reset user data on logout
gtag('config', 'G-XXXXXXXXXX', {
  'user_id': undefined  // Clear user identification
});
```

## 2. CCPA Compliance

### Do Not Sell Implementation

```javascript
// Check for Global Privacy Control signal
function checkGPC() {
  return navigator.globalPrivacyControl === true;
}

// Honor Do Not Sell preference
function initAnalyticsWithCCPA() {
  const doNotSell = localStorage.getItem('ccpa_opt_out') === 'true' || checkGPC();

  if (doNotSell) {
    // Disable data sharing/selling
    gtag('set', 'restricted_data_processing', true);
  }
}

// Opt-out handler
function handleCCPAOptOut() {
  localStorage.setItem('ccpa_opt_out', 'true');
  gtag('set', 'restricted_data_processing', true);
}
```

## 3. IP Anonymization

### GA4 (Automatic)

GA4 automatically anonymizes IP addresses. No additional configuration needed.

### Custom Server-Side

```python
# For server-side tracking
import hashlib

def anonymize_ip(ip_address: str) -> str:
    """Anonymize IP by hashing."""
    # Remove last octet for IPv4
    if '.' in ip_address:
        parts = ip_address.split('.')
        parts[-1] = '0'
        return '.'.join(parts)
    # Remove last 80 bits for IPv6
    elif ':' in ip_address:
        return ip_address.rsplit(':', 5)[0] + '::'
    return ip_address
```

## 4. Implementation Checklist

### Pre-Launch

- [ ] Choose analytics platform(s) (GA4, Plausible, or both)
- [ ] Set up properties/sites
- [ ] Install tracking code
- [ ] Configure consent management
- [ ] Define key events and conversions
- [ ] Set up custom dimensions/metrics
- [ ] Configure data retention
- [ ] Test tracking in development

### Event Naming

| Convention | Example | Description |
|------------|---------|-------------|
| snake_case | `button_click` | GA4 recommended |
| Title Case | `Button Click` | Plausible goals |
| Consistent | Always use same format | Easier analysis |

### Parameter Guidelines

- Keep parameter names short but descriptive
- Use consistent naming across events
- Limit to 25 parameters per event (GA4)
- Use numbers for metrics, strings for dimensions

## 5. Performance

### Async Loading

```html
<!-- GA4 - async by default -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>

<!-- Plausible - defer loading -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

### Lazy Loading Analytics

```javascript
// Load analytics after user interaction
let analyticsLoaded = false;

function loadAnalytics() {
  if (analyticsLoaded) return;
  analyticsLoaded = true;

  // Load GA4
  const gaScript = document.createElement('script');
  gaScript.async = true;
  gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
  document.head.appendChild(gaScript);

  gaScript.onload = () => {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  };
}

// Trigger on first interaction
['scroll', 'click', 'touchstart'].forEach(event => {
  document.addEventListener(event, loadAnalytics, { once: true, passive: true });
});
```

### Batch Events

```javascript
// Batch multiple events
class EventBatcher {
  constructor(flushInterval = 5000) {
    this.queue = [];
    this.flushInterval = flushInterval;
    setInterval(() => this.flush(), flushInterval);
  }

  add(eventName, params) {
    this.queue.push({ eventName, params, timestamp: Date.now() });
  }

  flush() {
    if (this.queue.length === 0) return;

    // Send batched events
    this.queue.forEach(({ eventName, params }) => {
      gtag('event', eventName, params);
    });

    this.queue = [];
  }
}
```

---

*Privacy Compliance Guide v1.0*
*GDPR, CCPA, Consent Management, IP Anonymization, Performance*
