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

# Entertainment, lifestyle, and non-political content
VIRAL_ENTERTAINMENT_CONFIG = RedditConfig(
    subreddits=["entertainment", "movies", "television", "Music", "popculture"],
    limit=30,
    minimum_score=500
)

VIRAL_FOOD_CONFIG = RedditConfig(
    subreddits=["food", "FoodPorn", "Cooking", "recipes", "EatCheapAndHealthy"],
    limit=30,
    minimum_score=500
)

VIRAL_GAMING_CONFIG = RedditConfig(
    subreddits=["gaming", "Games", "pcgaming", "PS5", "xbox"],
    limit=30,
    minimum_score=500
)

VIRAL_LIFESTYLE_CONFIG = RedditConfig(
    subreddits=["BeautyGuruChatter", "MakeupAddiction", "SkincareAddiction", "fashion", "streetwear"],
    limit=30,
    minimum_score=500
)

VIRAL_HOBBIES_CONFIG = RedditConfig(
    subreddits=["DIY", "crafts", "Art", "photography", "gardening"],
    limit=30,
    minimum_score=500
)

VIRAL_SPORTS_CONFIG = RedditConfig(
    subreddits=["sports", "nba", "nfl", "soccer", "fitness"],
    limit=30,
    minimum_score=500
)

# Combined non-political viral content
VIRAL_ALL_CONFIG = RedditConfig(
    subreddits=["videos", "gifs", "Damnthatsinteresting", "interestingasfuck", "oddlysatisfying", "nextfuckinglevel"],
    limit=50,
    minimum_score=1000
)
