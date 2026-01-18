# M-DO-024: Feature Flags

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #feature-flags, #deployment, #releases, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Deploying risky features is all-or-nothing. Rollbacks require redeployment. A/B testing requires infrastructure changes.

## Promise

After this methodology, you will control feature rollout with flags. You'll deploy code anytime and enable features when ready.

## Overview

Feature flags decouple deployment from release. They enable gradual rollouts, A/B testing, and instant kill switches without code changes.

---

## Framework

### Step 1: Simple Implementation

```javascript
// config/features.js
const features = {
  newCheckout: {
    enabled: process.env.FEATURE_NEW_CHECKOUT === 'true',
    rolloutPercentage: parseInt(process.env.FEATURE_NEW_CHECKOUT_PERCENT || '0'),
  },
  darkMode: {
    enabled: true,
    allowList: ['user-123', 'user-456'],
  },
};

function isEnabled(featureName, userId = null) {
  const feature = features[featureName];
  if (!feature) return false;

  // Check allowlist first
  if (userId && feature.allowList?.includes(userId)) {
    return true;
  }

  // Check if globally enabled
  if (!feature.enabled) return false;

  // Check rollout percentage
  if (feature.rolloutPercentage && userId) {
    const hash = hashCode(userId + featureName);
    return (hash % 100) < feature.rolloutPercentage;
  }

  return feature.enabled;
}

function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

module.exports = { isEnabled };
```

```javascript
// Usage
const { isEnabled } = require('./config/features');

app.get('/checkout', (req, res) => {
  if (isEnabled('newCheckout', req.user?.id)) {
    return renderNewCheckout(req, res);
  }
  return renderOldCheckout(req, res);
});
```

### Step 2: LaunchDarkly Integration

```javascript
// Node.js SDK
const LaunchDarkly = require('launchdarkly-node-server-sdk');

const client = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY);

async function initFeatureFlags() {
  await client.waitForInitialization();
  console.log('LaunchDarkly initialized');
}

async function isEnabled(flagKey, user) {
  const ldUser = {
    key: user.id,
    email: user.email,
    custom: {
      plan: user.plan,
      country: user.country,
    },
  };

  return client.variation(flagKey, ldUser, false);
}

// Usage in Express
app.use(async (req, res, next) => {
  req.features = {
    newDashboard: await isEnabled('new-dashboard', req.user),
    betaFeatures: await isEnabled('beta-features', req.user),
  };
  next();
});

app.get('/dashboard', (req, res) => {
  if (req.features.newDashboard) {
    return res.render('dashboard-v2');
  }
  return res.render('dashboard');
});
```

### Step 3: Flagsmith (Self-Hosted Option)

```yaml
# docker-compose.yml
version: '3.9'

services:
  flagsmith:
    image: flagsmith/flagsmith:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/flagsmith
      DJANGO_SECRET_KEY: your-secret-key
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: flagsmith
    volumes:
      - flagsmith_data:/var/lib/postgresql/data

volumes:
  flagsmith_data:
```

```javascript
// Flagsmith client
const Flagsmith = require('flagsmith-nodejs');

const flagsmith = new Flagsmith({
  environmentKey: process.env.FLAGSMITH_ENV_KEY,
});

async function getFlags(userId) {
  const flags = await flagsmith.getIdentityFlags(userId);
  return {
    newFeature: flags.isFeatureEnabled('new_feature'),
    maxItems: flags.getFeatureValue('max_items') || 10,
  };
}
```

### Step 4: React Integration

```jsx
// React context
import { createContext, useContext, useState, useEffect } from 'react';

const FeatureContext = createContext({});

export function FeatureProvider({ children, userId }) {
  const [features, setFeatures] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadFeatures() {
      const response = await fetch(`/api/features?userId=${userId}`);
      const data = await response.json();
      setFeatures(data);
      setLoading(false);
    }
    loadFeatures();
  }, [userId]);

  if (loading) return <Loading />;

  return (
    <FeatureContext.Provider value={features}>
      {children}
    </FeatureContext.Provider>
  );
}

export function useFeature(flagName) {
  const features = useContext(FeatureContext);
  return features[flagName] ?? false;
}

// Usage
function Dashboard() {
  const showNewWidget = useFeature('new-widget');

  return (
    <div>
      {showNewWidget && <NewWidget />}
      <OldWidget />
    </div>
  );
}
```

### Step 5: Gradual Rollout

```javascript
// Percentage-based rollout
class FeatureRollout {
  constructor(config) {
    this.config = config;
  }

  isEnabled(flagName, userId) {
    const flag = this.config[flagName];
    if (!flag) return false;

    // Killed switch
    if (flag.killed) return false;

    // Force enable for specific users
    if (flag.forceEnable?.includes(userId)) return true;

    // Force disable for specific users
    if (flag.forceDisable?.includes(userId)) return false;

    // Percentage rollout
    if (flag.percentage !== undefined) {
      return this.isInRollout(userId, flagName, flag.percentage);
    }

    return flag.enabled ?? false;
  }

  isInRollout(userId, flagName, percentage) {
    // Consistent hashing ensures same user always gets same result
    const hash = this.hash(`${userId}:${flagName}`);
    return hash < percentage;
  }

  hash(str) {
    let hash = 5381;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) + hash) + str.charCodeAt(i);
    }
    return Math.abs(hash % 100);
  }
}

// Config
const rollout = new FeatureRollout({
  newCheckout: {
    enabled: true,
    percentage: 10,  // 10% of users
    forceEnable: ['user-123'],
    forceDisable: ['user-456'],
  },
  betaFeatures: {
    enabled: false,
    killed: true,  // Emergency shutoff
  },
});
```

### Step 6: A/B Testing

```javascript
// Experiment configuration
const experiments = {
  checkoutButtonColor: {
    variants: ['blue', 'green', 'orange'],
    weights: [50, 25, 25],  // 50% blue, 25% green, 25% orange
  },
  pricingPageLayout: {
    variants: ['control', 'variant-a', 'variant-b'],
    weights: [34, 33, 33],
  },
};

function getVariant(experimentName, userId) {
  const experiment = experiments[experimentName];
  if (!experiment) return null;

  const hash = hashCode(`${userId}:${experimentName}`) % 100;
  let cumulative = 0;

  for (let i = 0; i < experiment.variants.length; i++) {
    cumulative += experiment.weights[i];
    if (hash < cumulative) {
      return experiment.variants[i];
    }
  }

  return experiment.variants[0];
}

// Usage
app.get('/checkout', (req, res) => {
  const buttonColor = getVariant('checkoutButtonColor', req.user.id);

  // Track for analytics
  analytics.track('experiment_exposure', {
    userId: req.user.id,
    experiment: 'checkoutButtonColor',
    variant: buttonColor,
  });

  res.render('checkout', { buttonColor });
});
```

---

## Templates

### Feature Flag API

```javascript
// routes/features.js
const express = require('express');
const router = express.Router();

// Get all flags for user
router.get('/', async (req, res) => {
  const userId = req.user?.id || req.query.userId;

  const flags = {
    newDashboard: isEnabled('newDashboard', userId),
    darkMode: isEnabled('darkMode', userId),
    betaFeatures: isEnabled('betaFeatures', userId),
  };

  res.json(flags);
});

// Admin: Update flag
router.put('/:flagName', requireAdmin, (req, res) => {
  const { flagName } = req.params;
  const { enabled, percentage, forceEnable, forceDisable } = req.body;

  updateFlag(flagName, {
    enabled,
    percentage,
    forceEnable,
    forceDisable,
  });

  res.json({ success: true });
});

module.exports = router;
```

### Monitoring

```javascript
// Track flag evaluations
const metrics = require('./metrics');

function isEnabled(flagName, userId) {
  const result = evaluateFlag(flagName, userId);

  metrics.increment('feature_flag_evaluation', {
    flag: flagName,
    result: result ? 'true' : 'false',
  });

  return result;
}
```

---

## Common Mistakes

1. **No cleanup** - Old flags accumulate as tech debt
2. **No monitoring** - Can't see flag impact
3. **Long-lived flags** - Should be temporary
4. **Complex conditions** - Keep flags simple
5. **No kill switch** - Can't disable quickly

---

## Checklist

- [ ] Feature flag service configured
- [ ] Consistent user bucketing
- [ ] Percentage rollout supported
- [ ] Kill switch capability
- [ ] Admin UI for flag management
- [ ] Flag evaluation logging
- [ ] Stale flag cleanup process
- [ ] A/B testing capability

---

## Next Steps

- M-DO-001: GitHub Actions
- M-DO-010: Infrastructure Patterns
- M-DO-011: Prometheus Monitoring

---

*Methodology M-DO-024 v1.0*
