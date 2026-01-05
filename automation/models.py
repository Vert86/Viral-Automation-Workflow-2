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
    article_url: str = ""  # Related news article URL
    article_source: str = ""  # Article source (e.g., "CNN", "BBC")

    def __str__(self) -> str:
        article_info = ""
        if self.article_url:
            article_info = f"   📰 Article: {self.article_url}\n"
            if self.article_source:
                article_info = f"   📰 Article ({self.article_source}): {self.article_url}\n"

        return (
            f"📈 {self.title}\n"
            f"   ⬆️  Score: {self.score:,} | 💬 Comments: {self.comment_count:,}\n"
            f"{article_info}"
            f"   🔗 Reddit: {self.url}\n"
        )
