"""Reddit API client for fetching viral content"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import urlparse
import re

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from automation.config import RedditConfig
from automation.models import TrendingTopic


class RedditClient:
    """Client for fetching trending topics from Reddit"""

    # Known news domains that are acceptable article sources
    NEWS_DOMAINS = {
        'bbc.com', 'bbc.co.uk', 'cnn.com', 'nytimes.com', 'theguardian.com',
        'reuters.com', 'apnews.com', 'bloomberg.com', 'cnbc.com', 'forbes.com',
        'wsj.com', 'washingtonpost.com', 'npr.org', 'abcnews.go.com', 'cbsnews.com',
        'nbcnews.com', 'usatoday.com', 'latimes.com', 'time.com', 'newsweek.com',
        'theverge.com', 'techcrunch.com', 'arstechnica.com', 'wired.com', 'vice.com',
        'vox.com', 'axios.com', 'politico.com', 'thehill.com', 'huffpost.com',
        'businessinsider.com', 'space.com', 'scientificamerican.com', 'nature.com',
        'nationalgeographic.com', 'espn.com', 'skysports.com', 'variety.com',
        'hollywoodreporter.com', 'rollingstone.com', 'pitchfork.com'
    }

    def __init__(self, config: RedditConfig) -> None:
        self._config = config

    def _is_news_article(self, url: str) -> bool:
        """Check if URL is from a known news source"""
        try:
            domain = urlparse(url).netloc.lower()
            # Remove www. prefix
            domain = domain.replace('www.', '')
            return any(news_domain in domain for news_domain in self.NEWS_DOMAINS)
        except Exception:
            return False

    def _extract_source_name(self, url: str) -> str:
        """Extract readable source name from URL"""
        try:
            domain = urlparse(url).netloc.lower().replace('www.', '')
            # Map common domains to readable names
            name_map = {
                'nytimes.com': 'New York Times',
                'washingtonpost.com': 'Washington Post',
                'bbc.com': 'BBC',
                'bbc.co.uk': 'BBC',
                'cnn.com': 'CNN',
                'reuters.com': 'Reuters',
                'apnews.com': 'AP News',
                'bloomberg.com': 'Bloomberg',
                'theguardian.com': 'The Guardian',
                'wsj.com': 'Wall Street Journal',
                'forbes.com': 'Forbes',
                'cnbc.com': 'CNBC',
                'npr.org': 'NPR',
                'space.com': 'Space.com',
            }
            return name_map.get(domain, domain.split('.')[0].title())
        except Exception:
            return "Unknown"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def fetch_hot_topics(self) -> List[TrendingTopic]:
        """
        Fetch hot/trending topics from Reddit
        Only includes posts that link to news articles from known sources

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

            # Get the URL from the post
            url = data.get("url", "")

            # Skip if it's a self post without external URL
            if not url or url.startswith("https://www.reddit.com/r/"):
                continue

            # IMPORTANT: Only include posts that link to news articles
            if not self._is_news_article(url):
                continue

            # Extract source name for display
            source_name = self._extract_source_name(url)

            topic = TrendingTopic(
                id=data.get("id", ""),
                title=data.get("title", "Untitled"),
                url=f"https://www.reddit.com{data.get('permalink', '')}",  # Reddit discussion link
                score=int(data.get("score", 0)),
                comment_count=int(data.get("num_comments", 0)),
                retrieved_at=now,
                subreddit=data.get("subreddit", ""),
                author=data.get("author", ""),
                article_url=url,  # The actual news article
                article_source=source_name
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
