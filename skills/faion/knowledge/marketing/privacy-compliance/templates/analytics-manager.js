// analytics-manager.js — GDPR/CCPA-compliant analytics wrapper
// Implements: default-deny, GA4 Consent Mode v2, GPC, event queue, cookie clearing

class AnalyticsManager {
  constructor() {
    this.consentGiven = false;
    this.queuedEvents = [];
  }

  init() {
    // Set GA4 default-deny BEFORE gtag loads
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });

    // Honor CCPA Global Privacy Control signal
    if (navigator.globalPrivacyControl === true) {
      gtag("set", "restricted_data_processing", true);
    }
    const stored = localStorage.getItem("analytics_consent");
    if (stored === "granted") this._enable();
  }

  grantConsent(preferences = { analytics: true, marketing: false }) {
    localStorage.setItem("analytics_consent", "granted");
    this.consentGiven = true;
    gtag("consent", "update", {
      analytics_storage: preferences.analytics ? "granted" : "denied",
      ad_storage: preferences.marketing ? "granted" : "denied",
      ad_user_data: preferences.marketing ? "granted" : "denied",
      ad_personalization: preferences.marketing ? "granted" : "denied",
    });
    this._flushQueue();
  }

  revokeConsent() {
    localStorage.setItem("analytics_consent", "denied");
    this.consentGiven = false;
    gtag("consent", "update", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    this._clearCookies();
  }

  track(eventName, params = {}) {
    if (this.consentGiven) {
      gtag("event", eventName, params);
    } else {
      this.queuedEvents.push({ eventName, params });
    }
  }

  _enable() {
    this.consentGiven = true;
  }

  _flushQueue() {
    this.queuedEvents.forEach(({ eventName, params }) => {
      gtag("event", eventName, params);
    });
    this.queuedEvents = [];
  }

  _clearCookies() {
    ["_ga", "_gid", "_gat"].forEach((name) => {
      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=.${window.location.hostname}`;
    });
    // Clear _ga_* measurement IDs
    document.cookie.split(";").forEach((c) => {
      const name = c.trim().split("=")[0];
      if (name.startsWith("_ga_")) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
      }
    });
  }
}

export const analytics = new AnalyticsManager();
