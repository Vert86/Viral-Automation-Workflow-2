"""Reddit API client for fetching viral content"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from automation.config import RedditConfig
from automation.models import TrendingTopic


class RedditClient:
    """Client for fetching trending topics from Reddit"""

    def __init__(self, config: RedditConfig) -> None:
        self._config = config

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def fetch_hot_topics(self) -> List[TrendingTopic]:
        """
        Fetch hot/trending topics from Reddit

        Returns:
            List of TrendingTopic objects sorted by score
        """
        params = {"limit": self._config.limit}
        headers = {"User-Agent": self._config.user_agent}

        try:
            response = requests.get(
                self._config.url, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch Reddit data: {e}")

        now = datetime.now(timezone.utc)
        topics: List[TrendingTopic] = []

        for child in payload.get("data", {}).get("children", []):
            data = child.get("data", {})

            # Skip posts below minimum score
            if data.get("score", 0) < self._config.minimum_score:
                continue

            # Skip if it's a self post without external URL
            url = data.get("url", "")
            if not url or url.startswith("https://www.reddit.com/r/"):
                continue

            topic = TrendingTopic(
                id=data.get("id", ""),
                title=data.get("title", "Untitled"),
                url=url,
                score=int(data.get("score", 0)),
                comment_count=int(data.get("num_comments", 0)),
                retrieved_at=now,
                subreddit=data.get("subreddit", ""),
                author=data.get("author", "")
            )
            topics.append(topic)

        # Sort by score (highest first)
        topics.sort(key=lambda t: t.score, reverse=True)

        return topics

    def fetch_multiple_sources(self, configs: List[RedditConfig]) -> List[TrendingTopic]:
        """
        Fetch from multiple Reddit configurations and combine results

        Args:
            configs: List of RedditConfig objects

        Returns:
            Combined and deduplicated list of trending topics
        """
        all_topics: List[TrendingTopic] = []
        seen_urls = set()

        for config in configs:
            client = RedditClient(config)
            topics = client.fetch_hot_topics()

            for topic in topics:
                if topic.url not in seen_urls:
                    all_topics.append(topic)
                    seen_urls.add(topic.url)

        # Sort by score
        all_topics.sort(key=lambda t: t.score, reverse=True)

        return all_topics
