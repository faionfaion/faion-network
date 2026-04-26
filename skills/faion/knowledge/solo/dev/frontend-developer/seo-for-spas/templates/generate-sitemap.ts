// Build-time sitemap.xml + robots.txt generator for Next.js.
// Run via: ts-node scripts/generate-sitemap.ts
import { writeFileSync } from 'fs';
import { globby } from 'globby';

const BASE_URL = 'https://example.com';

async function generateSitemap() {
  const staticPages = await globby([
    'pages/**/*.tsx',
    '!pages/_*.tsx',
    '!pages/api/**',
    '!pages/**/[*.tsx',
  ]);

  // Replace with actual data fetchers
  const products: Array<{ slug: string; updatedAt: string; image: string; name: string }> = [];
  const posts: Array<{ slug: string; updatedAt: string }> = [];

  const staticUrls = staticPages.map((page) => {
    const path = page.replace('pages', '').replace('.tsx', '').replace('/index', '');
    return `  <url>
    <loc>${BASE_URL}${path}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`;
  });

  const productUrls = products.map((p) => `  <url>
    <loc>${BASE_URL}/products/${p.slug}</loc>
    <lastmod>${p.updatedAt}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>${p.image}</image:loc>
      <image:title>${p.name}</image:title>
    </image:image>
  </url>`);

  const postUrls = posts.map((p) => `  <url>
    <loc>${BASE_URL}/blog/${p.slug}</loc>
    <lastmod>${p.updatedAt}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>`);

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${[...staticUrls, ...productUrls, ...postUrls].join('\n')}
</urlset>`;

  writeFileSync('public/sitemap.xml', sitemap);

  const robots = `User-agent: *
Allow: /
Sitemap: ${BASE_URL}/sitemap.xml
Disallow: /admin/
Disallow: /api/
`;
  writeFileSync('public/robots.txt', robots);
}

generateSitemap();
