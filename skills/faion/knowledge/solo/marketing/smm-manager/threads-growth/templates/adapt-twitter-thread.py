"""
Adapt a Twitter/X thread into Threads-native conversational posts.
Input: list of tweet strings (the thread), optional max_posts limit.
Output: list of short, conversational Threads posts with a question appended.

Agent should then refine each output for personal voice before posting.

Usage:
  from adapt_twitter_thread import adapt_for_threads
  posts = adapt_for_threads(["1/ Here's how I grew...", "2/ Step one..."], max_posts=3)
"""
import re


def adapt_for_threads(tweets: list[str], max_posts: int = 3) -> list[str]:
    """
    Takes a list of tweet strings and produces up to max_posts
    Threads-native posts. Strips thread numbering, truncates to sentence
    boundaries at ~280 chars, appends a question to the last post.
    """
    combined = " ".join(tweets)
    # Strip tweet numbering (1/, 2/, 10/, etc.)
    cleaned = re.sub(r"\d+/\s*", "", combined).strip()
    # Remove thread emoji if present
    cleaned = cleaned.replace("🧵", "").strip()

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    posts: list[str] = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 < 280:
            current = (current + " " + sentence).strip()
        else:
            if current:
                posts.append(current)
            current = sentence
        if len(posts) >= max_posts - 1:
            break

    if current:
        posts.append(current)

    # Append a genuine question to the last post
    if posts:
        posts[-1] = posts[-1].rstrip(".") + "\n\nHave you experienced this?"

    return posts[:max_posts]


if __name__ == "__main__":
    sample = [
        "1/ I grew from 0 to 10K followers in 6 months.",
        "2/ The key was replying to large accounts first.",
        "3/ One reply on a 100K account beats 5 standalone posts.",
    ]
    for i, post in enumerate(adapt_for_threads(sample), 1):
        print(f"--- Post {i} ---\n{post}\n")
