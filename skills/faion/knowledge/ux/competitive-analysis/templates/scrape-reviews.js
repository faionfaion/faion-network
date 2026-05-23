// scrape-reviews.js — scrape App Store critical reviews for competitor sentiment analysis
// Usage: node scrape-reviews.js <app-id> <num-reviews>
// Example: node scrape-reviews.js 284882215 100
// Requires: npm install app-store-scraper

const store = require('app-store-scraper');

const appId = process.argv[2];
const count = parseInt(process.argv[3] || '100', 10);

if (!appId) {
  console.error('Usage: node scrape-reviews.js <app-id> [num-reviews]');
  process.exit(1);
}

store
  .reviews({ id: appId, sort: store.sort.CRITICAL, num: count })
  .then((reviews) => {
    const critical = reviews
      .filter((r) => r.score <= 2)
      .map((r) => ({
        score: r.score,
        title: r.title,
        text: r.text.slice(0, 300),
        date: r.updated,
      }));

    console.log(JSON.stringify(critical, null, 2));
    console.log(`\n--- Total critical reviews: ${critical.length} of ${reviews.length} fetched ---`);
    console.log('\nNext steps:');
    console.log('  1. Feed output to Claude: extract top 5 recurring UX complaints');
    console.log('  2. Categorize each complaint by Nielsen heuristic violated');
    console.log('  3. Rate severity (1-4) for each complaint category');
  })
  .catch((err) => {
    console.error('Error:', err.message);
    process.exit(1);
  });
