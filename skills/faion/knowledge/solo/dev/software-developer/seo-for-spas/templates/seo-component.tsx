// purpose: Reusable SEO head component with JSON-LD + canonical + OG tags.
// consumes: see content/02-output-contract.xml inputs for seo-for-spas
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// seo-component.tsx — Universal SEO component
// Supports Next.js (pages router via next/head) and non-Next React (react-helmet-async).
// All fields are required. og:image must be absolute URL 1200x630.

import Head from 'next/head'; // swap for Helmet from 'react-helmet-async' if not Next.js

interface SEOProps {
  title: string;            // 30-65 chars
  description: string;      // 120-160 chars
  canonicalUrl: string;     // absolute URL from env, never window.location
  ogImage: string;          // absolute URL, 1200x630 recommended
  ogType?: 'website' | 'article' | 'product';
  noIndex?: boolean;        // true only for admin/preview routes
}

export function SEO({
  title,
  description,
  canonicalUrl,
  ogImage,
  ogType = 'website',
  noIndex = false,
}: SEOProps) {
  const siteName = process.env.NEXT_PUBLIC_SITE_NAME ?? 'My Site';

  return (
    <Head>
      {/* Primary */}
      <title>{`${title} | ${siteName}`}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={canonicalUrl} />
      {noIndex && <meta name="robots" content="noindex, nofollow" />}

      {/* Open Graph */}
      <meta property="og:type" content={ogType} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:site_name" content={siteName} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />
    </Head>
  );
}

// JSON-LD injection helper (safe escaping)
interface JsonLdProps {
  data: object;
}

export function JsonLd({ data }: JsonLdProps) {
  // Escape </script> to prevent early tag close
  const safeJson = JSON.stringify(data).replace(/</g, '\\u003c');
  return (
    <Head>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: safeJson }}
      />
    </Head>
  );
}
