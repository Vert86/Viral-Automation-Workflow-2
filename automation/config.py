"""Configuration for Reddit API client"""

from dataclasses import dataclass
from typing import List


@dataclass
class RedditConfig:
    """Configuration for Reddit API access"""
    subreddits: List[str]
    limit: int = 25
    minimum_score: int = 100
    user_agent: str = "ViralContentAutomation/1.0"

    @property
    def url(self) -> str:
        """Get the Reddit API URL for the configured subreddit"""
        # For multiple subreddits, we'll join them with +
        subreddit_path = "+".join(self.subreddits)
        return f"https://www.reddit.com/r/{subreddit_path}/hot.json"


# Predefined configs for different content types
VIRAL_NEWS_CONFIG = RedditConfig(
    subreddits=["worldnews", "news", "upliftingnews"],
    limit=25,
    minimum_score=500
)

VIRAL_TRENDING_CONFIG = RedditConfig(
    subreddits=["trending", "TikTokCringe", "videos", "interesting"],
    limit=25,
    minimum_score=300
)

VIRAL_ALL_CONFIG = RedditConfig(
    subreddits=["all"],
    limit=50,
    minimum_score=1000
)
