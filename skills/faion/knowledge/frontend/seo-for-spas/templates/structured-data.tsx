// StructuredData component + Product, Article, Breadcrumb JSON-LD factories.
// Inject in page head; works with Next.js Head or react-helmet-async.
import Head from 'next/head';

// ----- Component -----

export function StructuredData({ data }: { data: object }) {
  return (
    <Head>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
      />
    </Head>
  );
}

// ----- Schema factories -----

export function productSchema(product: {
  name: string; description: string; images: string[]; sku: string;
  brand: string; slug: string; price: number; inStock: boolean;
  rating?: { average: number; count: number };
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.images,
    sku: product.sku,
    brand: { '@type': 'Brand', name: product.brand },
    offers: {
      '@type': 'Offer',
      url: `https://example.com/products/${product.slug}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
      seller: { '@type': 'Organization', name: 'Example Store' },
    },
    ...(product.rating && {
      aggregateRating: {
        '@type': 'AggregateRating',
        ratingValue: product.rating.average,
        reviewCount: product.rating.count,
      },
    }),
  };
}

export function articleSchema(post: {
  title: string; excerpt: string; coverImage: string;
  publishedAt: string; updatedAt: string;
  author: { name: string; profileUrl: string }; slug: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: { '@type': 'Person', name: post.author.name, url: post.author.profileUrl },
    publisher: {
      '@type': 'Organization', name: 'Example Blog',
      logo: { '@type': 'ImageObject', url: 'https://example.com/logo.png' },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://example.com/blog/${post.slug}`,
    },
  };
}

export function breadcrumbSchema(items: Array<{ name: string; url: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}
