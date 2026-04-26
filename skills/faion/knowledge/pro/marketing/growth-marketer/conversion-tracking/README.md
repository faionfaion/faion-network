# Conversion Tracking

**Part of faion-marketing-manager skill**

## 1. GA4 Conversion Goals

### Setting Up Conversions

1. Admin → Events
2. Mark event as conversion (toggle)
3. Or create via API

### Key Conversion Events

```javascript
// Subscription conversion
gtag('event', 'generate_lead', {
  currency: 'USD',
  value: 19.00,
  lead_source: 'landing_page'
});

// Trial started
gtag('event', 'start_trial', {
  plan_name: 'Pro',
  trial_duration_days: 14
});

// Upgrade conversion
gtag('event', 'upgrade_plan', {
  from_plan: 'Free',
  to_plan: 'Plus',
  value: 19.00
});
```

### Conversion Value

```javascript
// Assign monetary value to conversions
gtag('event', 'purchase', {
  value: 99.99,
  currency: 'USD',
  transaction_id: 'T12345'
});
```

## 2. Funnel Tracking

### Funnel Definition (in GA4 UI)

```
Funnel: Subscription Flow
Step 1: landing_page_view
Step 2: pricing_view
Step 3: begin_checkout
Step 4: payment_info_entered
Step 5: purchase
```

### Track Funnel Steps

```javascript
// Step 1: Landing page
gtag('event', 'landing_page_view', {
  page_variant: 'A',
  utm_source: 'google'
});

// Step 2: Pricing view
gtag('event', 'pricing_view', {
  displayed_plans: ['Free', 'Plus', 'Pro']
});

// Step 3: Checkout started
gtag('event', 'begin_checkout', {
  selected_plan: 'Plus',
  value: 19.00,
  currency: 'USD'
});

// Step 4: Payment info
gtag('event', 'add_payment_info', {
  payment_type: 'credit_card'
});

// Step 5: Purchase
gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 19.00,
  currency: 'USD'
});
```

### Funnel Analysis Queries

Use GA4 Explorations:
1. Explore → Funnel exploration
2. Configure steps
3. Analyze drop-off rates

## 3. Multi-Step Funnel Tracker

```javascript
class FunnelTracker {
  constructor(funnelName) {
    this.funnelName = funnelName;
    this.startTime = null;
  }

  trackStep(stepNumber, stepName, metadata = {}) {
    if (stepNumber === 1) {
      this.startTime = Date.now();
    }

    const timeFromStart = this.startTime
      ? Math.floor((Date.now() - this.startTime) / 1000)
      : 0;

    gtag('event', 'funnel_step', {
      funnel_name: this.funnelName,
      step_number: stepNumber,
      step_name: stepName,
      time_from_start: timeFromStart,
      ...metadata
    });

    plausible('Funnel Step', {
      props: {
        funnel: this.funnelName,
        step: stepNumber,
        name: stepName,
        ...metadata
      }
    });
  }

  trackCompletion(value = 0, currency = 'USD') {
    const totalTime = this.startTime
      ? Math.floor((Date.now() - this.startTime) / 1000)
      : 0;

    gtag('event', 'funnel_complete', {
      funnel_name: this.funnelName,
      value,
      currency,
      total_time_seconds: totalTime
    });

    plausible('Funnel Complete', {
      revenue: { currency, amount: value },
      props: {
        funnel: this.funnelName,
        time_seconds: totalTime
      }
    });
  }

  trackAbandonment(lastStep) {
    gtag('event', 'funnel_abandon', {
      funnel_name: this.funnelName,
      last_step: lastStep
    });

    plausible('Funnel Abandon', {
      props: {
        funnel: this.funnelName,
        last_step: lastStep
      }
    });
  }
}

// Usage
const checkoutFunnel = new FunnelTracker('checkout');
checkoutFunnel.trackStep(1, 'cart_view', { items_count: 2 });
checkoutFunnel.trackStep(2, 'shipping_info');
checkoutFunnel.trackStep(3, 'payment_info');
checkoutFunnel.trackStep(4, 'review_order');
checkoutFunnel.trackCompletion(99.99, 'USD');
```

## 4. A/B Test Tracking

```javascript
// Track experiment exposure
function trackExperiment(experimentId, variant) {
  gtag('event', 'experiment_exposure', {
    experiment_id: experimentId,
    variant_id: variant
  });

  // Set as user property for segmentation
  gtag('set', 'user_properties', {
    [`exp_${experimentId}`]: variant
  });

  plausible('Experiment', {
    props: {
      experiment: experimentId,
      variant
    }
  });
}

// Track conversion within experiment
function trackExperimentConversion(experimentId, variant, conversionType, value = 0) {
  gtag('event', 'experiment_conversion', {
    experiment_id: experimentId,
    variant_id: variant,
    conversion_type: conversionType,
    value
  });

  plausible('Experiment Conversion', {
    revenue: value > 0 ? { currency: 'USD', amount: value } : undefined,
    props: {
      experiment: experimentId,
      variant,
      type: conversionType
    }
  });
}
```

## 5. SaaS Metrics Events

### User Lifecycle

```javascript
// Acquisition
function trackSignup(method, source) {
  // GA4
  gtag('event', 'sign_up', { method, source });
  // Plausible
  plausible('Signup', { props: { method, source } });
}

// Activation
function trackActivation(feature) {
  gtag('event', 'activation', { first_feature: feature });
  plausible('Activation', { props: { feature } });
}

// Retention
function trackReturn(daysSinceLastVisit) {
  gtag('event', 'user_return', { days_away: daysSinceLastVisit });
  plausible('Return', { props: { days_away: daysSinceLastVisit } });
}

// Revenue
function trackPurchase(plan, price, currency) {
  gtag('event', 'purchase', {
    value: price,
    currency,
    items: [{ item_name: plan, price }]
  });
  plausible('Purchase', {
    revenue: { currency, amount: price },
    props: { plan }
  });
}

// Referral
function trackReferral(referrerId) {
  gtag('event', 'referral_signup', { referrer_id: referrerId });
  plausible('Referral', { props: { referrer_id: referrerId } });
}
```

### Feature Usage

```javascript
// Generic feature tracker
function trackFeatureUsage(featureName, action, metadata = {}) {
  gtag('event', 'feature_usage', {
    feature_name: featureName,
    feature_action: action,
    ...metadata
  });
  plausible('Feature', {
    props: {
      name: featureName,
      action,
      ...metadata
    }
  });
}

// Examples
trackFeatureUsage('dark_mode', 'enabled');
trackFeatureUsage('export', 'pdf_downloaded', { page_count: 5 });
trackFeatureUsage('ai_assistant', 'query', { query_length: 150 });
```

## 6. Content Engagement

### Article Tracking

```javascript
// Read progress tracking
function trackReadProgress(articleId, percentage) {
  const milestones = [25, 50, 75, 100];
  if (milestones.includes(percentage)) {
    gtag('event', 'article_progress', {
      article_id: articleId,
      progress: percentage
    });
    plausible('Article Progress', {
      props: { article_id: articleId, progress: percentage }
    });
  }
}

// Time on page
function trackTimeOnPage(articleId, seconds) {
  const milestones = [30, 60, 120, 300];
  milestones.forEach(milestone => {
    if (seconds >= milestone) {
      gtag('event', 'time_milestone', {
        article_id: articleId,
        seconds: milestone
      });
    }
  });
}

// Scroll depth with IntersectionObserver
function trackScrollDepth() {
  const markers = [25, 50, 75, 100];
  markers.forEach(depth => {
    const marker = document.getElementById(`scroll-${depth}`);
    if (marker) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            gtag('event', 'scroll_depth', { depth });
            observer.unobserve(entry.target);
          }
        });
      });
      observer.observe(marker);
    }
  });
}
```

### Video Tracking

```javascript
// Video engagement
function trackVideo(videoId, action, progress = null) {
  const data = { video_id: videoId, action };
  if (progress !== null) data.progress = progress;

  gtag('event', 'video_engagement', data);
  plausible('Video', { props: data });
}

// Usage
video.addEventListener('play', () => trackVideo('intro-video', 'play'));
video.addEventListener('pause', () => trackVideo('intro-video', 'pause'));
video.addEventListener('ended', () => trackVideo('intro-video', 'complete'));

// Progress tracking
video.addEventListener('timeupdate', () => {
  const progress = Math.floor((video.currentTime / video.duration) * 100);
  if ([25, 50, 75].includes(progress)) {
    trackVideo('intro-video', 'progress', progress);
  }
});
```

---

*Conversion Tracking Guide v1.0*
*GA4 Conversions, Funnels, A/B Tests, SaaS Metrics, Engagement*

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
