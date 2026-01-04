# Viral Content Automation Tool

Automate the process of finding viral social media content, analyzing trending topics, and generating SEO-optimized YouTube video prompts with AI.

## Features

- **Reddit-Based Viral Content Discovery**: Fetches real-time trending topics from Reddit (r/all, r/news, r/trending, etc.)
- **Smart Filtering**: Only shows posts with high scores and engagement
- **Interactive Selection**: Choose from top 10 trending topics or provide your own URL
- **AI-Powered Analysis**: Uses Claude AI to analyze viral content and extract key elements
- **Complete Video Package Generation**: Creates ready-to-use prompts for AI video creators
- **SEO Optimization**: Generates titles, descriptions, and tags optimized for YouTube
- **Auto-Save Results**: Saves all generated content to timestamped files
- **No Authentication Required**: Uses Reddit's public API (no API key needed)

## Prerequisites

- Python 3.7 or higher
- Anthropic API key (Claude API)

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ViralAutomation.git
   cd ViralAutomation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:

   **Windows (Command Prompt)**:
   ```cmd
   set ANTHROPIC_API_KEY=your_api_key_here
   ```

   **Windows (PowerShell)**:
   ```powershell
   $env:ANTHROPIC_API_KEY="your_api_key_here"
   ```

   **Mac/Linux**:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

   **Or create a `.env` file** (recommended for permanent setup):
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Getting Your Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and set it as your environment variable

## Usage

Run the automation script:

```bash
python viral_content_automation.py
```

### Workflow

1. **Fetch Phase**: The tool fetches the top 10 viral posts from Reddit with:
   - High scores (1000+ upvotes)
   - Active engagement (comments)
   - External article links
2. **Selection Phase**: You'll see the top trending topics and can:
   - Select one by number (1-10)
   - Provide your own article URL
   - Refresh to fetch new viral content
3. **Confirmation**: Confirm your selected topic
4. **Analysis Phase**: Claude AI analyzes the content for viral elements
5. **Generation Phase**: Creates a complete YouTube video package including:
   - AI text-to-video prompt (30-60 seconds)
   - SEO-optimized title
   - YouTube description with emojis and hashtags
   - 20-25 relevant tags
6. **Save**: Results are displayed and saved to a timestamped file

## Output

The tool generates a text file named `video_package_YYYYMMDD_HHMMSS.txt` containing:

- Complete AI video creation prompt
- YouTube title (SEO-optimized)
- YouTube description with emojis and hashtags
- List of tags for maximum discoverability

Simply copy and paste the content into your AI video creator and YouTube upload form.

## Example Output

```
========================================
AI TEXT-TO-VIDEO PROMPT
========================================
Create a 30-60 second engaging video about [viral topic]...

========================================
SEO-OPTIMIZED YOUTUBE TITLE
========================================
[Engaging title under 60 characters]

========================================
YOUTUBE DESCRIPTION
========================================
[Description with emojis, hashtags, and CTAs]

========================================
YOUTUBE TAGS
========================================
[20-25 relevant tags]
```

## Project Structure

```
ViralAutomation/
├── viral_content_automation.py    # Main automation script
├── automation/
│   ├── __init__.py               # Package initializer
│   ├── models.py                 # Data models for trending topics
│   ├── config.py                 # Reddit API configuration
│   └── reddit_client.py          # Reddit API client
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
└── video_package_*.txt           # Generated output files (auto-created)
```

## Troubleshooting

**"ANTHROPIC_API_KEY environment variable not set"**
- Make sure you've set the API key as an environment variable
- Check that you're using the correct command for your operating system

**"Module not found" error**
- Run `pip install -r requirements.txt` to install dependencies
- Make sure you're using Python 3.7 or higher

**Reddit fetch not working**
- Ensure you have an active internet connection
- Reddit's API may have rate limits - wait a minute and try again
- Check that requests and tenacity are properly installed

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

MIT License - Feel free to use this tool for your YouTube content creation.

## Disclaimer

This tool uses the Anthropic Claude API which may incur costs. Please check [Anthropic's pricing](https://www.anthropic.com/pricing) for current rates.

## Support

For issues or questions:
- Open an issue on GitHub
- Check the Anthropic documentation at [docs.anthropic.com](https://docs.anthropic.com/)

---

Made with Claude AI
