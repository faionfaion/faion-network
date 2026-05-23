// purpose: canonical event-schema snippet for funnel tactic instrumentation
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~400-1000 tokens when loaded as context

// Funnel Analytics Event Tracking
// Instrument all 6 events before running any funnel optimization.

// Step 1: Awareness
analytics.track('Homepage Viewed', {
  trafficSource: utm_source,       // google, meta, organic, direct
  device: 'mobile|desktop|tablet',
  timestamp: new Date()
});

// Step 2: Interest — CTA interaction
analytics.track('CTA Clicked', {
  ctaText: '[Button text]',
  ctaLocation: 'hero|navbar|footer|sidebar',
  device: 'mobile|desktop'
});

// Step 3: Consideration — Form viewed
analytics.track('Signup Form Viewed', {
  formType: 'email|oauth|phone',
  device: 'mobile|desktop',
  entryPoint: '[Traffic source or referrer]'
});

// Step 4: Decision — Signup complete
analytics.track('Signup Completed', {
  method: 'google|email|password|phone',
  planSelected: 'free|starter|pro',
  signupTime: '[Seconds from form view to submit]'
});

// Step 5: Activation — Onboarding start
analytics.track('Onboarding Started', {
  planType: 'free|paid',
  flow: 'guided|self-serve'
});

// Step 6: Usage — Core action completed
analytics.track('First Action Completed', {
  actionType: '[Specific product action]',
  timeToAction: '[Minutes from signup]',
  planType: 'free|paid'
});
