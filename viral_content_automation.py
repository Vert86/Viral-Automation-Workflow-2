#!/usr/bin/env python3
"""
Viral Content Automation Tool
Scrapes viral social media trends from Reddit and generates YouTube video prompts
"""

import anthropic
import os
from datetime import datetime
from pathlib import Path
from typing import List

from automation.reddit_client import RedditClient
from automation.config import VIRAL_ALL_CONFIG, VIRAL_NEWS_CONFIG, VIRAL_TRENDING_CONFIG
from automation.models import TrendingTopic


class ViralContentAutomation:
    def __init__(self):
        # Try to load from .env file first
        self._load_env_file()

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set.\n\n"
                "Please set it using:\n"
                "PowerShell: $env:ANTHROPIC_API_KEY=\"your_key_here\"\n"
                "CMD: set ANTHROPIC_API_KEY=your_key_here\n"
                "Or create a .env file with: ANTHROPIC_API_KEY=your_key_here"
            )
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def _load_env_file(self):
        """Load environment variables from .env file if it exists"""
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    def fetch_viral_content_from_reddit(self) -> List[TrendingTopic]:
        """Fetch viral content from Reddit"""
        print("\n🔍 Fetching viral content from Reddit...\n")

        # Fetch from multiple sources
        reddit_client = RedditClient(VIRAL_ALL_CONFIG)
        topics = reddit_client.fetch_multiple_sources([
            VIRAL_ALL_CONFIG,
            VIRAL_NEWS_CONFIG,
            VIRAL_TRENDING_CONFIG
        ])

        return topics[:10]  # Return top 10

    def analyze_article_with_ai(self, url: str, title: str) -> str:
        """Use Claude to analyze and summarize the article"""
        print(f"\n📄 Analyzing: {title}\n")

        prompt = f"""Analyze this viral content and provide a brief summary suitable for creating a YouTube video:

Title: {title}
URL: {url}

Extract:
1. The main topic/story
2. Why it's going viral (emotional appeal, timing, uniqueness)
3. Key facts or details
4. Target audience appeal

Keep it concise (3-4 paragraphs)."""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text

    def generate_video_prompt(self, topic: TrendingTopic, article_summary: str):
        """Generate AI video creation prompt and YouTube metadata"""
        print("\n🎬 Generating video creation materials...\n")

        article_info = f"Article: {topic.article_url} ({topic.article_source})" if topic.article_url else f"URL: {topic.url}"

        prompt = f"""Based on this viral content:

Title: {topic.title}
{article_info}
Reddit Score: {topic.score:,}
Reddit Comments: {topic.comment_count:,}

Content Analysis:
{article_summary}

Create a complete YouTube video package including:

1. A detailed AI text-to-video prompt (30-60 seconds) that includes:
   - Hook in first 5 seconds that grabs attention
   - Visual storyboard suggestions
   - Key explanations/facts to include
   - Emotional elements to emphasize
   - Call-to-action
   - Tone direction (energetic, shareable, suitable for both long-form and Shorts)

2. SEO-optimized YouTube title (under 60 characters, attention-grabbing)

3. YouTube description with:
   - Engaging intro paragraph
   - Key points with emojis
   - Call-to-action
   - Source link
   - 15-20 relevant hashtags

4. 20-25 YouTube tags for maximum discoverability

Format everything clearly with headers so it's ready to copy and paste."""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return message.content[0].text

    def run(self):
        """Main automation workflow"""
        print("=" * 60)
        print("🚀 VIRAL CONTENT AUTOMATION TOOL")
        print("=" * 60)

        # Step 1: Fetch viral content from Reddit
        try:
            topics = self.fetch_viral_content_from_reddit()

            if not topics:
                print("❌ No viral content found. Please try again later.")
                return

            # Display the top trending topics
            print("📊 TOP VIRAL CONTENT FROM REDDIT:\n")
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
                print()

        except Exception as e:
            print(f"❌ Error fetching Reddit content: {e}")
            return

        # Step 2: Interactive link selection with confirmation loop
        print("=" * 60)
        selected_topic = None
        confirmed = False

        while not confirmed:
            print("\n📌 OPTIONS:")
            print("1. Select one of the trending topics above (enter number 1-10)")
            print("2. Provide your own article URL")
            print("3. Refresh and fetch new viral content")

            choice = input("\nEnter your choice (1/2/3): ").strip()

            if choice == "1":
                try:
                    topic_num = int(input("\n✅ Enter topic number (1-10): ").strip())
                    if 1 <= topic_num <= len(topics):
                        selected_topic = topics[topic_num - 1]
                    else:
                        print(f"❌ Please enter a number between 1 and {len(topics)}")
                        continue
                except ValueError:
                    print("❌ Invalid number. Please try again.")
                    continue

            elif choice == "2":
                url = input("\n✅ Paste your article URL: ").strip()
                title = input("✅ Enter a title for this content: ").strip()
                selected_topic = TrendingTopic(
                    id="custom",
                    title=title,
                    url=url,
                    score=0,
                    comment_count=0,
                    retrieved_at=datetime.now()
                )

            elif choice == "3":
                print("\n🔄 Fetching fresh viral content...")
                topics = self.fetch_viral_content_from_reddit()
                print("\n📊 TOP VIRAL CONTENT FROM REDDIT:\n")
                for i, topic in enumerate(topics, 1):
                    print(f"{i}. {topic}")
                    print()
                continue

            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                continue

            # Step 3: Confirm selection
            if selected_topic:
                print(f"\n✅ Selected: {selected_topic.title}")
                if selected_topic.article_url:
                    print(f"   📰 Article ({selected_topic.article_source}): {selected_topic.article_url}")
                    print(f"   💬 Reddit Discussion: {selected_topic.url}")
                else:
                    print(f"   🔗 URL: {selected_topic.url}")
                confirm = input("\nIs this correct? (yes/no): ").strip().lower()

                if confirm in ['yes', 'y']:
                    confirmed = True
                else:
                    print("\n🔄 No problem! Let's choose a different topic.\n")
                    selected_topic = None
                    # Show topics again for convenience
                    print("📊 TOP VIRAL CONTENT FROM REDDIT:\n")
                    for i, topic in enumerate(topics, 1):
                        print(f"{i}. {topic}")
                        print()

        # Step 4: Analyze the content
        # Use article_url if available, otherwise fall back to url
        analysis_url = selected_topic.article_url if selected_topic.article_url else selected_topic.url
        article_summary = self.analyze_article_with_ai(
            analysis_url,
            selected_topic.title
        )
        print(article_summary)

        # Step 5: Generate video creation materials
        video_package = self.generate_video_prompt(selected_topic, article_summary)

        print("\n" + "=" * 60)
        print("🎉 YOUR YOUTUBE VIDEO PACKAGE IS READY!")
        print("=" * 60)
        print(video_package)

        # Step 6: Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_package_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("YOUTUBE VIDEO CREATION PACKAGE\n")
            f.write(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
            f.write(f"Topic: {selected_topic.title}\n")
            if selected_topic.article_url:
                f.write(f"Article URL: {selected_topic.article_url}\n")
                f.write(f"Article Source: {selected_topic.article_source}\n")
            f.write(f"Reddit Discussion: {selected_topic.url}\n")
            f.write(f"Reddit Score: {selected_topic.score:,}\n")
            f.write(f"Comments: {selected_topic.comment_count:,}\n")
            f.write("=" * 60 + "\n\n")
            f.write("CONTENT ANALYSIS:\n")
            f.write(article_summary)
            f.write("\n\n" + "=" * 60 + "\n\n")
            f.write(video_package)

        print(f"\n💾 Saved to: {filename}")
        print("\n✨ Copy the content above and paste into your AI video creator!")


if __name__ == "__main__":
    try:
        automation = ViralContentAutomation()
        automation.run()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
