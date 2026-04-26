// next.config.ts — production-ready baseline
// Requires: npm i -D @next/bundle-analyzer
import type { NextConfig } from 'next';
import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
});

const config: NextConfig = {
  experimental: {
    typedRoutes: true,
    serverActions: { bodySizeLimit: '2mb' },
  },
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }],
  },
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=()' },
        ],
      },
    ];
  },
};

export default withBundleAnalyzer(config);
