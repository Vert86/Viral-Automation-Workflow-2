"""Data models for viral content automation"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrendingTopic:
    """Represents a trending topic from social media"""
    id: str
    title: str
    url: str
    score: int
    comment_count: int
    retrieved_at: datetime
    subreddit: str = ""
    author: str = ""

    def __str__(self) -> str:
        return (
            f"📈 {self.title}\n"
            f"   ⬆️  Score: {self.score:,} | 💬 Comments: {self.comment_count:,}\n"
            f"   🔗 {self.url}\n"
        )
