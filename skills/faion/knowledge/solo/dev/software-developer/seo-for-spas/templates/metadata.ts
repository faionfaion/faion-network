// purpose: Next.js app-router metadata + structured data per route.
// consumes: see content/02-output-contract.xml inputs for seo-for-spas
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `https://example.com/blog/${post.slug}`,
      languages: { en: `/en/blog/${post.slug}`, uk: `/uk/blog/${post.slug}`, 'x-default': `/blog/${post.slug}` },
    },
    openGraph: { title: post.title, description: post.excerpt, type: 'article', images: [post.cover] },
  };
}

export default async function Page({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  const jsonLd = { '@context': 'https://schema.org', '@type': 'Article', headline: post.title, datePublished: post.date };
  return (<><script type='application/ld+json'>{JSON.stringify(jsonLd)}</script><article>{post.body}</article></>);
}

async function getPost(_slug: string) { return { slug: _slug, title: 'x', excerpt: 'y', date: '2026-01-01', body: 'z', cover: '/og.png' }; }
