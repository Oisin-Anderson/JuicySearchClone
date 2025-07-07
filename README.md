# OnlyFans Link Scraper

A Python script that automatically scrapes OnlyFans profile links from Reddit and Twitter, collecting up to 100 unique links.

## Features

- **Multi-source scraping**: Collects links from Reddit and Twitter
- **Automatic deduplication**: Ensures no duplicate links
- **Rate limiting**: Respects website rate limits to avoid being blocked
- **Headless browser**: Uses Selenium with Chrome in headless mode
- **Multiple output formats**: Saves results as both TXT and JSON files
- **Link validation**: Cleans and validates OnlyFans URLs

## Requirements

- Python 3.7+
- Chrome browser installed
- Internet connection

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Chrome browser is installed** on your system

## Usage

Simply run the script:

```bash
python onlyfans_scraper.py
```

The script will:
1. Scrape OnlyFans links from Reddit subreddits
2. Scrape OnlyFans links from Twitter searches
3. Clean and validate all found links
4. Save results to `onlyfans_links.txt` and `onlyfans_links.json`
5. Display a summary of found links

## Output Files

- **`onlyfans_links.txt`**: Plain text file with one link per line
- **`onlyfans_links.json`**: JSON file with links and metadata

## How It Works

### Reddit Scraping
- Searches through multiple NSFW subreddits
- Uses Reddit's JSON API for efficient data extraction
- Searches post titles, content, and URLs for OnlyFans links

### Twitter Scraping
- Uses Selenium WebDriver to navigate Twitter search
- Searches for various OnlyFans-related keywords
- Scrolls through results to load more content

### Link Processing
- Extracts OnlyFans URLs using regex patterns
- Removes duplicates and invalid links
- Cleans URLs by removing query parameters
- Validates that links point to valid OnlyFans profiles

## Configuration

You can modify the following parameters in the script:

- `max_links`: Change the target number of links (default: 100)
- `subreddits`: Add or remove subreddits to search
- `search_queries`: Modify Twitter search terms
- Rate limiting delays: Adjust sleep times between requests

## Notes

- The script includes rate limiting to avoid being blocked by websites
- Some websites may block automated access; the script handles these errors gracefully
- Results may vary depending on current content availability
- Always respect website terms of service and robots.txt files

## Troubleshooting

**Chrome driver issues**: The script automatically downloads the appropriate Chrome driver version. If you encounter issues, ensure Chrome is installed and up to date.

**Rate limiting**: If you're getting blocked, increase the sleep times in the script.

**No links found**: This can happen if websites change their structure or block automated access. Try running the script again later.

## Legal Disclaimer

This tool is for educational purposes only. Users are responsible for complying with all applicable laws and website terms of service. The authors are not responsible for any misuse of this software. 