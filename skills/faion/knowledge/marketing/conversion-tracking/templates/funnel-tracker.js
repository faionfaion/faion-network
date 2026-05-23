/**
 * FunnelTracker — multi-step funnel tracking for GA4 + Plausible.
 *
 * Usage:
 *   const checkout = new FunnelTracker('checkout');
 *   checkout.trackStep(1, 'cart_view', { items_count: 2 });
 *   checkout.trackStep(2, 'shipping_info');
 *   checkout.trackCompletion(99.99, 'USD');
 */
class FunnelTracker {
  constructor(funnelName) {
    this.funnelName = funnelName;
    this.startTime = null;
  }

  trackStep(stepNumber, stepName, metadata = {}) {
    if (stepNumber === 1) this.startTime = Date.now();
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
      props: { funnel: this.funnelName, step: stepNumber, name: stepName, ...metadata }
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
      props: { funnel: this.funnelName, time_seconds: totalTime }
    });
  }

  trackAbandonment(lastStep) {
    gtag('event', 'funnel_abandon', {
      funnel_name: this.funnelName,
      last_step: lastStep
    });
    plausible('Funnel Abandon', {
      props: { funnel: this.funnelName, last_step: lastStep }
    });
  }
}
