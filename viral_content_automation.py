#!/usr/bin/env python3
"""
Viral Content Automation Tool
Scrapes viral social media trends and generates YouTube video prompts
"""

import anthropic
import os
from datetime import datetime


class ViralContentAutomation:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def search_viral_content(self):
        """Search for current viral social media content and trends"""
        print("\n🔍 Searching for viral content and trends...\n")

        current_date = datetime.now().strftime("%B %d, %Y")

        # Use Claude with web search to find viral content
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": f"Today is {current_date}. Search the web for the most viral social media content, trending topics, and stories happening right now. Find specific articles about viral content that would make great YouTube videos. Return 3 different article options with their URLs, titles, and brief descriptions of what makes them viral."
            }]
        )

        return message.content[0].text

    def get_article_details(self, url):
        """Fetch and analyze article content"""
        print(f"\n📄 Analyzing article: {url}\n")

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"Fetch and summarize the key points from this article: {url}. Extract the main viral content, trends, or story details that would be useful for creating a YouTube video."
            }]
        )

        return message.content[0].text

    def generate_video_prompt(self, article_url, article_summary):
        """Generate AI video creation prompt and YouTube metadata"""
        print("\n🎬 Generating video creation materials...\n")

        prompt = f"""Based on this viral content article:
URL: {article_url}

Summary: {article_summary}

Create a complete YouTube video package including:

1. A detailed AI text-to-video prompt (similar to the Wolf Supermoon example format) that includes:
   - Hook in first 5 seconds
   - Visual storyboard suggestions
   - Key explanations/facts to include
   - Call-to-action
   - Tone direction for both long-form and Shorts

2. SEO-optimized YouTube title (60 characters or less)

3. YouTube description with:
   - Engaging intro
   - Key points with emojis
   - Call-to-action
   - Source link
   - Relevant hashtags

4. 20-25 YouTube tags for maximum discoverability

Format everything clearly so it's ready to copy and paste."""

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

        # Step 1: Search for viral content
        viral_content_results = self.search_viral_content()
        print(viral_content_results)

        # Step 2: Interactive link selection
        print("\n" + "=" * 60)
        while True:
            print("\n📌 OPTIONS:")
            print("1. Use one of the suggested articles above")
            print("2. Provide your own article URL")
            print("3. Search for different viral content")

            choice = input("\nEnter your choice (1/2/3): ").strip()

            if choice == "1":
                article_url = input("\n✅ Paste the article URL you want to use: ").strip()
                break
            elif choice == "2":
                article_url = input("\n✅ Paste your article URL: ").strip()
                break
            elif choice == "3":
                print("\n🔄 Searching for new viral content...")
                viral_content_results = self.search_viral_content()
                print(viral_content_results)
                continue
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

        # Step 3: Confirm the URL
        print(f"\n✅ Selected URL: {article_url}")
        confirm = input("Is this correct? (yes/no): ").strip().lower()

        if confirm not in ['yes', 'y']:
            print("❌ Operation cancelled. Please run the script again.")
            return

        # Step 4: Analyze the article
        article_summary = self.get_article_details(article_url)
        print(article_summary)

        # Step 5: Generate video creation materials
        video_package = self.generate_video_prompt(article_url, article_summary)

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
            f.write(f"Article URL: {article_url}\n")
            f.write("=" * 60 + "\n\n")
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
        print("\nMake sure you have set the ANTHROPIC_API_KEY environment variable.")
