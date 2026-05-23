// gatsby-config.js — Plausible plugin configuration
// Install: npm install gatsby-plugin-plausible

module.exports = {
  plugins: [
    {
      resolve: 'gatsby-plugin-plausible',
      options: {
        domain: 'yourdomain.com',
        // Use this when Nginx proxy is deployed:
        customDomain: 'yourdomain.com',  // proxies /js/script.js and /api/event
      },
    },
  ],
};
