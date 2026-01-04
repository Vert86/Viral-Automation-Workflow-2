# Viral Content Automation Tool

Automate the process of finding viral social media content, analyzing trending topics, and generating SEO-optimized YouTube video prompts with AI.

## Features

- **Automated Viral Content Discovery**: Searches the web for current trending topics and viral social media content
- **Interactive Link Selection**: Choose from suggested articles or provide your own
- **AI-Powered Analysis**: Analyzes articles to extract key viral elements
- **Complete Video Package Generation**: Creates ready-to-use prompts for AI video creators
- **SEO Optimization**: Generates titles, descriptions, and tags optimized for YouTube
- **Auto-Save Results**: Saves all generated content to timestamped files

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

1. **Search Phase**: The tool automatically searches for current viral content and trending topics
2. **Selection Phase**: You'll see 3 article options and can:
   - Choose one of the suggested articles
   - Provide your own article URL
   - Search for different viral content
3. **Confirmation**: Confirm the URL you want to use
4. **Analysis Phase**: The tool analyzes the article content
5. **Generation Phase**: Creates a complete YouTube video package including:
   - AI text-to-video prompt
   - SEO-optimized title
   - YouTube description with hashtags
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
├── requirements.txt               # Python dependencies
├── README.md                      # This file
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

**Web search not working**
- Ensure you have an active internet connection
- Check that your API key has sufficient credits

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
