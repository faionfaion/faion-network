# Plausible Analytics

**Part of faion-marketing-manager skill**

## 1. Setup

### Script Installation

```html
<!-- Basic installation -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>

<!-- Self-hosted -->
<script defer data-domain="yourdomain.com" src="https://analytics.yourdomain.com/js/script.js"></script>

<!-- With custom events -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.tagged-events.js"></script>

<!-- With file downloads -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.file-downloads.js"></script>

<!-- All extensions -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.tagged-events.file-downloads.outbound-links.js"></script>
```

### Custom Domain (Proxy)

```nginx
# Nginx proxy for privacy
location /js/script.js {
    proxy_pass https://plausible.io/js/script.js;
    proxy_set_header Host plausible.io;
}

location /api/event {
    proxy_pass https://plausible.io/api/event;
    proxy_set_header Host plausible.io;
}
```

```html
<!-- Use proxied script -->
<script defer data-domain="yourdomain.com" data-api="/api/event" src="/js/script.js"></script>
```

### Gatsby Integration

```javascript
// gatsby-config.js
module.exports = {
  plugins: [
    {
      resolve: 'gatsby-plugin-plausible',
      options: {
        domain: 'yourdomain.com',
        // Optional: self-hosted
        customDomain: 'analytics.yourdomain.com',
      },
    },
  ],
};
```

### React Integration

```javascript
// PlausibleProvider.jsx
import { useEffect } from 'react';

export function PlausibleProvider({ domain, children }) {
  useEffect(() => {
    const script = document.createElement('script');
    script.defer = true;
    script.dataset.domain = domain;
    script.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };
  }, [domain]);

  return children;
}
```

## 2. Event Tracking

### Custom Events

```javascript
// Basic event
plausible('signup');

// Event with props (custom properties)
plausible('signup', {
  props: {
    plan: 'premium',
    source: 'landing_page'
  }
});

// Revenue tracking
plausible('purchase', {
  revenue: { currency: 'USD', amount: 99.99 },
  props: {
    plan: 'Pro',
    billing: 'annual'
  }
});
```

### Goal Tracking

```javascript
// Define goals in Plausible dashboard first

// Track goal completion
plausible('Download', {
  props: {
    file: 'sdd-guide.pdf',
    format: 'pdf'
  }
});

// Track 404 errors
plausible('404', {
  props: {
    path: document.location.pathname
  }
});
```

### CSS Class Events (Tagged Events)

```html
<!-- Auto-track clicks with class -->
<a href="/pricing" class="plausible-event-name=Pricing+View">View Pricing</a>

<!-- With props -->
<button class="plausible-event-name=CTA+Click plausible-event-position=header">
  Get Started
</button>
```

## 3. Plausible Stats API

### Authentication

```bash
# API key from Plausible Settings → API Keys
export PLAUSIBLE_API_KEY="your-api-key"
```

### Aggregate Stats

```bash
# Get aggregate stats
curl "https://plausible.io/api/v1/stats/aggregate?site_id=yourdomain.com&period=30d&metrics=visitors,pageviews,bounce_rate,visit_duration" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Response:
{
  "results": {
    "visitors": {"value": 12500},
    "pageviews": {"value": 45000},
    "bounce_rate": {"value": 42.5},
    "visit_duration": {"value": 185}
  }
}
```

### Timeseries Data

```bash
# Daily visitors over 30 days
curl "https://plausible.io/api/v1/stats/timeseries?site_id=yourdomain.com&period=30d&metrics=visitors" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Response:
{
  "results": [
    {"date": "2026-01-01", "visitors": 450},
    {"date": "2026-01-02", "visitors": 520},
    ...
  ]
}
```

### Breakdown Reports

```bash
# Top pages
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=event:page&metrics=visitors,pageviews" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Top sources
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=visit:source&metrics=visitors" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Device breakdown
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=visit:device&metrics=visitors" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Custom event breakdown
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=event:name&metrics=visitors,events" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"
```

### Realtime Stats

```bash
# Current visitors (last 5 minutes)
curl "https://plausible.io/api/v1/stats/realtime/visitors?site_id=yourdomain.com" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Response:
10  # Number of current visitors
```

### Python Client

```python
import requests

class PlausibleClient:
    def __init__(self, api_key: str, site_id: str, base_url: str = "https://plausible.io"):
        self.api_key = api_key
        self.site_id = site_id
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def aggregate(self, period: str = "30d", metrics: list = None):
        """Get aggregate stats."""
        metrics = metrics or ["visitors", "pageviews", "bounce_rate"]
        params = {
            "site_id": self.site_id,
            "period": period,
            "metrics": ",".join(metrics)
        }
        response = requests.get(
            f"{self.base_url}/api/v1/stats/aggregate",
            headers=self.headers,
            params=params
        )
        return response.json()

    def timeseries(self, period: str = "30d", metrics: list = None):
        """Get timeseries data."""
        metrics = metrics or ["visitors"]
        params = {
            "site_id": self.site_id,
            "period": period,
            "metrics": ",".join(metrics)
        }
        response = requests.get(
            f"{self.base_url}/api/v1/stats/timeseries",
            headers=self.headers,
            params=params
        )
        return response.json()

    def breakdown(self, property: str, period: str = "30d", metrics: list = None):
        """Get breakdown by property."""
        metrics = metrics or ["visitors"]
        params = {
            "site_id": self.site_id,
            "period": period,
            "property": property,
            "metrics": ",".join(metrics)
        }
        response = requests.get(
            f"{self.base_url}/api/v1/stats/breakdown",
            headers=self.headers,
            params=params
        )
        return response.json()

    def realtime_visitors(self):
        """Get current visitors."""
        response = requests.get(
            f"{self.base_url}/api/v1/stats/realtime/visitors",
            headers=self.headers,
            params={"site_id": self.site_id}
        )
        return int(response.text)


# Usage
client = PlausibleClient(
    api_key="your-api-key",
    site_id="yourdomain.com"
)

# Get last 30 days stats
stats = client.aggregate(period="30d", metrics=["visitors", "pageviews"])
print(f"Visitors: {stats['results']['visitors']['value']}")

# Get top pages
pages = client.breakdown(property="event:page", metrics=["visitors", "pageviews"])
for page in pages['results'][:10]:
    print(f"{page['page']}: {page['visitors']} visitors")
```

## 4. Privacy-First Analytics

Plausible is GDPR-compliant by design:
- No cookies
- No personal data collection
- No cross-site tracking
- EU-hosted option available

```html
<!-- Plausible - no consent needed in most cases -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>

<!-- Optional: Exclude yourself from tracking -->
<script>
  if (localStorage.getItem('plausible_ignore') === 'true') {
    window.plausible = function() {};
  }
</script>
```

## 5. Debugging

```javascript
// Check if Plausible loaded
console.log('Plausible loaded:', typeof window.plausible === 'function');

// Log Plausible calls
const originalPlausible = window.plausible;
window.plausible = function() {
  console.log('plausible call:', arguments);
  if (originalPlausible) originalPlausible.apply(this, arguments);
};
```

## 6. Performance

### Async Loading

```html
<!-- Plausible - defer loading -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

---

*Plausible Analytics Guide v1.0*
*Setup, Events, Goals, Stats API, Privacy, Debugging*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Pull analytics data from Mixpanel, format report | haiku | Data extraction and formatting |
| Analyze A/B test results for statistical significance | sonnet | Statistical analysis and interpretation |
| Generate cohort retention curve analysis | sonnet | Data interpretation and visualization |
| Design growth loop for new product vertical | opus | Strategic design with multiple levers |
| Recommend optimization tactics for viral coefficient | sonnet | Metrics understanding and recommendations |
| Plan AARRR framework for pre-launch phase | opus | Comprehensive growth strategy |
| Implement custom analytics event tracking schema | sonnet | Technical setup and validation |
