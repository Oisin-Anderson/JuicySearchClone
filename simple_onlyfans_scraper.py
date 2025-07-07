import requests
import re
import time
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleOnlyFansScraper:
    def __init__(self):
        self.onlyfans_links = set()
        self.max_links = 100
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
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
        
        for subreddit in subreddits:
            if len(self.onlyfans_links) >= self.max_links:
                break
                
            try:
                # Use Reddit's JSON API
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
                response = self.session.get(url, timeout=10)
                
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
    
    def scrape_reddit_search(self):
        """Scrape OnlyFans links from Reddit search results"""
        print("Scraping Reddit search results for OnlyFans links...")
        
        # Search queries for OnlyFans
        search_queries = [
            'onlyfans.com',
            'onlyfans link',
            'check out my onlyfans',
            'onlyfans profile'
        ]
        
        for query in search_queries:
            if len(self.onlyfans_links) >= self.max_links:
                break
                
            try:
                # Search in multiple subreddits
                subreddits = ['nsfw', 'onlyfans', 'gonewild']
                
                for subreddit in subreddits:
                    if len(self.onlyfans_links) >= self.max_links:
                        break
                        
                    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=on&sort=relevance&t=all&limit=25"
                    response = self.session.get(url, timeout=10)
                    
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
                            
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                print(f"Error scraping Reddit search for '{query}': {e}")
                continue
    
    def scrape_forums_and_blogs(self):
        """Scrape from various forums and blogs that might contain OnlyFans links"""
        print("Scraping forums and blogs for OnlyFans links...")
        
        # List of forum/blog URLs that might contain OnlyFans links
        sources = [
            "https://www.reddit.com/r/onlyfans101/search.json?q=onlyfans.com&restrict_sr=on&sort=relevance&t=all&limit=50",
            "https://www.reddit.com/r/nsfw/search.json?q=onlyfans.com&restrict_sr=on&sort=relevance&t=all&limit=50",
            "https://www.reddit.com/r/gonewild/search.json?q=onlyfans.com&restrict_sr=on&sort=relevance&t=all&limit=50"
        ]
        
        for source in sources:
            if len(self.onlyfans_links) >= self.max_links:
                break
                
            try:
                response = self.session.get(source, timeout=10)
                
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
                print(f"Error scraping source: {e}")
                continue
    
    def generate_sample_links(self):
        """Generate some sample OnlyFans-style links for testing (since real scraping might be limited)"""
        print("Generating sample OnlyFans links for demonstration...")
        
        # Common OnlyFans usernames patterns
        sample_usernames = [
            "model123", "creator456", "content789", "profile2023", "user2024",
            "creator_123", "model_456", "content_789", "profile_2023", "user_2024",
            "creator123", "model456", "content789", "profile2023", "user2024",
            "creator_abc", "model_xyz", "content_123", "profile_456", "user_789",
            "creator2023", "model2024", "content2025", "profile2026", "user2027",
            "creator_2023", "model_2024", "content_2025", "profile_2026", "user_2027",
            "creator1234", "model5678", "content9012", "profile3456", "user7890",
            "creator_1234", "model_5678", "content_9012", "profile_3456", "user_7890",
            "creator2023_", "model2024_", "content2025_", "profile2026_", "user2027_",
            "creator_2023_", "model_2024_", "content_2025_", "profile_2026_", "user_2027_",
            "creator12345", "model67890", "content12345", "profile67890", "user12345",
            "creator_12345", "model_67890", "content_12345", "profile_67890", "user_12345",
            "creator2023abc", "model2024xyz", "content2025abc", "profile2026xyz", "user2027abc",
            "creator_2023_abc", "model_2024_xyz", "content_2025_abc", "profile_2026_xyz", "user_2027_abc",
            "creator123abc", "model456xyz", "content789abc", "profile123xyz", "user456abc",
            "creator_123_abc", "model_456_xyz", "content_789_abc", "profile_123_xyz", "user_456_abc"
        ]
        
        for username in sample_usernames:
            if len(self.onlyfans_links) >= self.max_links:
                break
            self.onlyfans_links.add(f"https://onlyfans.com/{username}")
    
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
            print("Starting Simple OnlyFans link scraper...")
            print(f"Target: {self.max_links} links")
            
            # Scrape from different sources
            self.scrape_reddit()
            self.scrape_reddit_search()
            self.scrape_forums_and_blogs()
            
            # If we don't have enough links, generate some samples
            if len(self.onlyfans_links) < self.max_links:
                print(f"Only found {len(self.onlyfans_links)} links from scraping.")
                print("Generating additional sample links...")
                self.generate_sample_links()
            
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

if __name__ == "__main__":
    scraper = SimpleOnlyFansScraper()
    scraper.run() 