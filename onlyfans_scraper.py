import requests
import re
import time
import json
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OnlyFansScraper:
    def __init__(self):
        self.onlyfans_links = set()
        self.max_links = 100
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with headless mode"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        
        try:
            # Try with webdriver-manager first
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Failed to setup Chrome driver with webdriver-manager: {e}")
            print("Trying alternative setup...")
            
            try:
                # Try without webdriver-manager (uses system Chrome driver)
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                print(f"Failed to setup Chrome driver: {e2}")
                print("Please ensure Chrome browser is installed and ChromeDriver is in your PATH")
                print("You can download ChromeDriver from: https://chromedriver.chromium.org/")
                raise e2
        
    def extract_onlyfans_links(self, text):
        """Extract OnlyFans links from text using regex"""
        # Pattern to match OnlyFans URLs
        patterns = [
            r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+',
            r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+/\?',
            r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+/posts',
            r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+/videos',
            r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+/photos'
        ]
        
        links = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            links.update(matches)
        
        return links
    
    def scrape_reddit(self):
        """Scrape OnlyFans links from Reddit"""
        print("Scraping Reddit for OnlyFans links...")
        
        # Subreddits that might contain OnlyFans links
        subreddits = [
            'onlyfans',
            'onlyfans101',
            'onlyfanspromotions',
            'onlyfansgirls',
            'onlyfansleaks',
            'nsfw',
            'nsfw_gifs',
            'gonewild'
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for subreddit in subreddits:
            if len(self.onlyfans_links) >= self.max_links:
                break
                
            try:
                # Use Reddit's JSON API
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for post in data['data']['children']:
                        if len(self.onlyfans_links) >= self.max_links:
                            break
                            
                        post_data = post['data']
                        title = post_data.get('title', '')
                        selftext = post_data.get('selftext', '')
                        url = post_data.get('url', '')
                        
                        # Extract links from title, selftext, and URL
                        text_to_search = f"{title} {selftext} {url}"
                        links = self.extract_onlyfans_links(text_to_search)
                        
                        self.onlyfans_links.update(links)
                        print(f"Found {len(links)} OnlyFans links from r/{subreddit}")
                        
                time.sleep(2)  # Rate limiting
                
            except Exception as e:
                print(f"Error scraping r/{subreddit}: {e}")
                continue
    
    def scrape_twitter(self):
        """Scrape OnlyFans links from Twitter using Selenium"""
        print("Scraping Twitter for OnlyFans links...")
        
        # Twitter search queries
        search_queries = [
            'onlyfans',
            'onlyfans link',
            'onlyfans.com',
            'check out my onlyfans',
            'onlyfans profile'
        ]
        
        for query in search_queries:
            if len(self.onlyfans_links) >= self.max_links:
                break
                
            try:
                # Navigate to Twitter search
                search_url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
                self.driver.get(search_url)
                
                # Wait for content to load
                time.sleep(5)
                
                # Scroll a few times to load more content
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                
                # Get page source and extract links
                page_source = self.driver.page_source
                links = self.extract_onlyfans_links(page_source)
                
                self.onlyfans_links.update(links)
                print(f"Found {len(links)} OnlyFans links from Twitter search: {query}")
                
                time.sleep(3)  # Rate limiting
                
            except Exception as e:
                print(f"Error scraping Twitter for query '{query}': {e}")
                continue
    
    def scrape_additional_sources(self):
        """Scrape from additional sources like forums and blogs"""
        print("Scraping additional sources for OnlyFans links...")
        
        # Additional sources to check
        sources = [
            "https://www.reddit.com/r/onlyfans101/search.json?q=onlyfans.com&restrict_sr=on&sort=relevance&t=all",
            "https://www.reddit.com/r/nsfw/search.json?q=onlyfans.com&restrict_sr=on&sort=relevance&t=all"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        for source in sources:
            if len(self.onlyfans_links) >= self.max_links:
                break
                
            try:
                response = requests.get(source, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for post in data['data']['children']:
                        if len(self.onlyfans_links) >= self.max_links:
                            break
                            
                        post_data = post['data']
                        title = post_data.get('title', '')
                        selftext = post_data.get('selftext', '')
                        
                        text_to_search = f"{title} {selftext}"
                        links = self.extract_onlyfans_links(text_to_search)
                        
                        self.onlyfans_links.update(links)
                        
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping additional source: {e}")
                continue
    
    def clean_and_validate_links(self):
        """Clean and validate the collected links"""
        cleaned_links = set()
        
        for link in self.onlyfans_links:
            # Basic validation
            if 'onlyfans.com' in link.lower():
                # Remove query parameters and fragments
                parsed = urlparse(link)
                clean_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                
                # Ensure it's a valid OnlyFans profile URL
                if re.match(r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+/?$', clean_link):
                    cleaned_links.add(clean_link)
        
        return list(cleaned_links)[:self.max_links]
    
    def save_links(self, links):
        """Save links to a file"""
        with open('onlyfans_links.txt', 'w') as f:
            for link in links:
                f.write(f"{link}\n")
        
        with open('onlyfans_links.json', 'w') as f:
            json.dump({'links': links, 'count': len(links)}, f, indent=2)
    
    def run(self):
        """Main method to run the scraper"""
        try:
            print("Starting OnlyFans link scraper...")
            print(f"Target: {self.max_links} links")
            
            # Scrape from different sources
            self.scrape_reddit()
            self.scrape_twitter()
            self.scrape_additional_sources()
            
            # Clean and validate links
            final_links = self.clean_and_validate_links()
            
            # Save results
            self.save_links(final_links)
            
            print(f"\nScraping completed!")
            print(f"Total OnlyFans links found: {len(final_links)}")
            print(f"Links saved to: onlyfans_links.txt and onlyfans_links.json")
            
            # Display first 10 links as preview
            if final_links:
                print("\nFirst 10 links found:")
                for i, link in enumerate(final_links[:10], 1):
                    print(f"{i}. {link}")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    scraper = OnlyFansScraper()
    scraper.run() 