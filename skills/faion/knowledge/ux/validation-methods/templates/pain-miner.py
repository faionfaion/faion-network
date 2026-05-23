# pain_miner.py — aggregate Reddit pain mentions by keyword theme
# Input:  PRAW credentials + subreddit + search query
# Output: keyword frequency counts sorted by occurrence
import collections
import praw


def mine_pains(subreddit: str, query: str, limit: int = 100) -> dict:
    """Collect and count pain keyword occurrences across top posts."""
    reddit = praw.Reddit(
        client_id="...",
        client_secret="...",
        user_agent="validator/1.0",
    )
    counts: collections.Counter = collections.Counter()
    keywords = ["slow", "broken", "missing", "hate", "wish", "expensive", "confusing"]

    for post in reddit.subreddit(subreddit).search(query, limit=limit):
        text = (post.title + " " + post.selftext).lower()
        for keyword in keywords:
            if keyword in text:
                counts[keyword] += 1

    return dict(counts.most_common())


if __name__ == "__main__":
    results = mine_pains(
        "projectmanagement",
        "frustrating OR hate OR problem",
        limit=200,
    )
    for keyword, count in results.items():
        print(f"{count:3d}  {keyword}")
