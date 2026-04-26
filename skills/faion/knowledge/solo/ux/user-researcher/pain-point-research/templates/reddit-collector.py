# reddit_collector.py — collect top posts matching pain keywords from a subreddit
# Input:  PRAW credentials + subreddit name + keyword list
# Output: top 20 posts by score, with title and URL
import praw

reddit = praw.Reddit(
    client_id="ID",
    client_secret="SECRET",
    user_agent="pain-research/1.0",
)
subreddit = reddit.subreddit("freelance")
keywords = ["hate", "frustrated", "annoying", "waste", "can't figure", "broken"]

results = []
for submission in subreddit.search(" OR ".join(keywords), sort="top", limit=50):
    results.append({
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "body": submission.selftext[:300],
    })

for r in sorted(results, key=lambda x: -x["score"])[:20]:
    print(f"{r['score']:5d}  {r['title']}")
    print(f"       {r['url']}")
