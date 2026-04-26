// Exit Intent Configuration Template
// Trigger when user is about to leave without converting.
// Recovery target: 5-15% of abandoning users.

exitIntentManager.configure({
  triggers: {
    mouseLeaveViewport: true,
    idleTime: null,        // seconds; null = disabled
    scrollDepth: null      // percentage; null = disabled
  },

  exclusions: {
    ifAlreadyConverted: true,
    ifAlreadyDismissed: true,
    ifCookie: 'exit-intent-shown'
  },

  offer: {
    title: "[Compelling offer — 5-8 words]",
    description: "[Value proposition — 10-15 words]",
    cta: {
      text: "[Action button — 2-4 words]",
      url: "/[destination]"
    },
    discount: "[10% off / $100 credit / free trial]",
    urgency: "[Limited time / today only]"
  },

  styling: {
    position: "center",
    animation: "fadeIn"
  },

  tracking: {
    onShow:    () => analytics.track('Exit Intent Shown'),
    onConvert: () => analytics.track('Exit Intent Converted'),
    onDismiss: () => analytics.track('Exit Intent Dismissed')
  }
});
