// purpose: Sitemap generator stub for Next.js app router.
// consumes: see content/02-output-contract.xml inputs for seo-for-spas
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetchAllPosts();
  return [
    { url: 'https://example.com/', lastModified: new Date(), changeFrequency: 'weekly', priority: 1 },
    ...posts.map((p) => ({ url: `https://example.com/blog/${p.slug}`, lastModified: p.updated })),
  ];
}

async function fetchAllPosts(): Promise<Array<{ slug: string; updated: Date }>> { return [{ slug: 'hello', updated: new Date() }]; }
