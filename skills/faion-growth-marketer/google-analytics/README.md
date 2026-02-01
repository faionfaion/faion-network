# Google Analytics 4 (GA4)

**Part of faion-marketing-manager skill**

## 1. Setup and Configuration

### Measurement ID

GA4 uses Measurement IDs in format `G-XXXXXXXXXX`.

```html
<!-- gtag.js installation -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Data Streams

| Stream Type | Use Case | Configuration |
|-------------|----------|---------------|
| Web | Websites | Domain, enhanced measurement |
| iOS | iOS apps | Bundle ID, App Store ID |
| Android | Android apps | Package name, Firebase |

### Enhanced Measurement

Auto-tracked events when enabled:
- `page_view` - Page loads
- `scroll` - 90% page depth
- `click` - Outbound links
- `view_search_results` - Site search
- `video_start`, `video_progress`, `video_complete` - Video engagement
- `file_download` - File downloads

```javascript
// Disable specific enhanced measurement
gtag('config', 'G-XXXXXXXXXX', {
  'send_page_view': false,  // Disable auto page_view
});
```

### User Properties

```javascript
// Set user properties for segmentation
gtag('set', 'user_properties', {
  subscription_tier: 'premium',
  account_age_days: 365,
  preferred_language: 'en'
});
```

## 2. Event Tracking

### Event Categories

| Category | Description | Examples |
|----------|-------------|----------|
| Automatic | Collected by default | `first_visit`, `session_start` |
| Enhanced | Require enhanced measurement | `scroll`, `click`, `file_download` |
| Recommended | Google-defined schemas | `login`, `sign_up`, `purchase` |
| Custom | Your own events | `feature_used`, `feedback_submitted` |

### Recommended Events

```javascript
// Sign up
gtag('event', 'sign_up', {
  method: 'email'  // or 'google', 'facebook'
});

// Login
gtag('event', 'login', {
  method: 'email'
});

// Purchase (ecommerce)
gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 99.99,
  currency: 'USD',
  items: [{
    item_id: 'SKU_001',
    item_name: 'Premium Plan',
    price: 99.99,
    quantity: 1
  }]
});

// Begin checkout
gtag('event', 'begin_checkout', {
  currency: 'USD',
  value: 99.99,
  items: [...]
});

// Add to cart
gtag('event', 'add_to_cart', {
  currency: 'USD',
  value: 29.99,
  items: [{
    item_id: 'SKU_002',
    item_name: 'Pro Subscription',
    price: 29.99,
    quantity: 1
  }]
});
```

### Custom Events

```javascript
// Feature usage tracking
gtag('event', 'feature_used', {
  feature_name: 'dark_mode',
  feature_category: 'settings'
});

// Content engagement
gtag('event', 'article_read', {
  article_id: 'sdd-intro-001',
  article_category: 'methodology',
  read_percentage: 100,
  time_on_page: 180
});

// Subscription events
gtag('event', 'subscription_started', {
  plan_name: 'Plus',
  plan_price: 19,
  billing_cycle: 'monthly',
  trial: false
});

// Error tracking
gtag('event', 'error_occurred', {
  error_type: 'api_error',
  error_message: 'Payment failed',
  error_code: 402
});
```

### Event Parameters

| Parameter | Type | Max Length | Description |
|-----------|------|------------|-------------|
| event_name | string | 40 chars | Event identifier |
| event_params | object | 25 params | Custom parameters |
| param_name | string | 40 chars | Parameter key |
| param_value | string/number | 100 chars | Parameter value |

## 3. Custom Dimensions and Metrics

### Configuration

Custom dimensions/metrics configured in GA4 Admin:
1. Admin → Data display → Custom definitions
2. Create custom dimension/metric
3. Scope: Event or User

### Event-scoped Dimensions

```javascript
// Register in GA4 Admin first, then send:
gtag('event', 'page_view', {
  content_type: 'article',      // custom dimension
  author_name: 'Ruslan Faion',  // custom dimension
  word_count: 1500              // custom metric
});
```

### User-scoped Dimensions

```javascript
// Persists across sessions
gtag('set', 'user_properties', {
  user_tier: 'premium',
  signup_source: 'product_hunt',
  lifetime_value: 299
});
```

## 4. GA4 Data API (Reporting)

### Authentication

```bash
# Service account setup
# 1. Create service account in Google Cloud Console
# 2. Add to GA4 property as viewer/editor
# 3. Download JSON key
```

### Python Client

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter
)

# Initialize client
client = BetaAnalyticsDataClient()
property_id = "properties/XXXXXXXXX"

# Run report
request = RunReportRequest(
    property=property_id,
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    dimensions=[
        Dimension(name="eventName"),
        Dimension(name="date")
    ],
    metrics=[
        Metric(name="eventCount"),
        Metric(name="totalUsers")
    ]
)

response = client.run_report(request)

for row in response.rows:
    print(f"{row.dimension_values[0].value}: {row.metric_values[0].value}")
```

### Common Dimensions and Metrics

| Dimensions | Description |
|------------|-------------|
| `date` | Date (YYYYMMDD) |
| `eventName` | Event name |
| `pagePath` | Page URL path |
| `sessionSource` | Traffic source |
| `deviceCategory` | Desktop/Mobile/Tablet |
| `country` | User country |

| Metrics | Description |
|---------|-------------|
| `eventCount` | Event occurrences |
| `totalUsers` | Unique users |
| `sessions` | Session count |
| `averageSessionDuration` | Avg session length |
| `bounceRate` | Bounce rate |
| `conversions` | Conversion count |

### REST API

```bash
# Get report via REST
curl -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/XXXXXXXXX:runReport" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "eventName"}],
    "metrics": [{"name": "eventCount"}]
  }'
```

## 5. Debugging

### GA4 DebugView

```javascript
// Enable debug mode
gtag('config', 'G-XXXXXXXXXX', {
  'debug_mode': true
});

// Or via URL parameter
// ?debug_mode=1
```

### Browser DevTools

```javascript
// Log all analytics calls
const originalGtag = window.gtag;
window.gtag = function() {
  console.log('gtag call:', arguments);
  originalGtag.apply(this, arguments);
};
```

## 6. Framework Integration

### React/Gatsby

```javascript
// hooks/useAnalytics.js
import { useCallback } from 'react';

export function useAnalytics() {
  const trackEvent = useCallback((eventName, params = {}) => {
    if (typeof gtag !== 'undefined') {
      gtag('event', eventName, params);
    }
  }, []);

  const trackPageView = useCallback((path, title) => {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'page_view', {
        page_path: path,
        page_title: title
      });
    }
  }, []);

  return { trackEvent, trackPageView };
}

// Usage in component
function PricingPage() {
  const { trackEvent } = useAnalytics();

  const handlePlanSelect = (plan) => {
    trackEvent('plan_selected', { plan_name: plan });
  };

  return (
    <button onClick={() => handlePlanSelect('Pro')}>
      Select Pro Plan
    </button>
  );
}
```

### Django Integration

```python
# analytics/middleware.py
class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track server-side events if needed
        if hasattr(request, 'analytics_events'):
            for event in request.analytics_events:
                # Send to GA4 Measurement Protocol
                self.send_to_ga4(event)

        return response

    def send_to_ga4(self, event):
        import requests

        payload = {
            'client_id': event.get('client_id'),
            'events': [{
                'name': event.get('name'),
                'params': event.get('params', {})
            }]
        }

        requests.post(
            f'https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_SECRET',
            json=payload
        )


# views.py
def purchase_view(request):
    # Server-side event tracking
    if not hasattr(request, 'analytics_events'):
        request.analytics_events = []

    request.analytics_events.append({
        'client_id': request.session.get('ga_client_id'),
        'name': 'purchase',
        'params': {
            'value': 99.99,
            'currency': 'USD',
            'transaction_id': 'T12345'
        }
    })

    return JsonResponse({'status': 'success'})
```

### Server-Side Tracking (Measurement Protocol)

```python
import requests
import uuid

def track_server_event(
    measurement_id: str,
    api_secret: str,
    client_id: str,
    event_name: str,
    params: dict = None
):
    """Send event to GA4 via Measurement Protocol."""
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

    payload = {
        "client_id": client_id,
        "events": [{
            "name": event_name,
            "params": params or {}
        }]
    }

    response = requests.post(url, json=payload)
    return response.status_code == 204


# Usage
track_server_event(
    measurement_id="G-XXXXXXXXXX",
    api_secret="YOUR_API_SECRET",
    client_id="user_123",
    event_name="subscription_renewed",
    params={
        "plan": "Pro",
        "value": 35.00,
        "currency": "USD"
    }
)
```

---

*Google Analytics 4 Guide v1.0*
*Setup, Events, Custom Dimensions, Data API, Debugging, Integrations*

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
