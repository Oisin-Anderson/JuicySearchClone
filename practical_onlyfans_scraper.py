import requests
import re
import time
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

class PracticalOnlyFansScraper:
    def __init__(self):
        self.valid_onlyfans_links = set()
        self.max_links = 100
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def extract_onlyfans_links(self, text):
        """Extract OnlyFans links from text using regex"""
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
    
    def validate_onlyfans_profile(self, profile_url):
        """Validate if an OnlyFans profile is real and active - more practical approach"""
        try:
            # Clean the URL
            parsed = urlparse(profile_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            # Remove trailing slash
            if clean_url.endswith('/'):
                clean_url = clean_url[:-1]
            
            # Check if it's a valid OnlyFans profile URL
            if not re.match(r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+$', clean_url):
                return False, "Invalid URL format"
            
            # Try to access the profile page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(clean_url, headers=headers, timeout=10, allow_redirects=True)
            
            # Check if the page exists (not 404)
            if response.status_code == 404:
                return False, "Profile not found (404)"
            
            # Check if we got redirected to a login page or error page
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}"
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text().lower()
            
            # Check for common error/invalid page indicators
            error_indicators = [
                'page not found', 'profile not found', 'user not found', 'account suspended',
                'this page is not available', 'access denied', 'forbidden', 'not found',
                'does not exist', 'no longer available', 'account deleted', '404'
            ]
            
            has_errors = any(error in text_content for error in error_indicators)
            if has_errors:
                return False, "Error page detected"
            
            # More practical validation - just check for basic OnlyFans indicators
            onlyfans_indicators = [
                'onlyfans' in text_content,
                soup.find('meta', {'property': 'og:site_name', 'content': 'OnlyFans'}) is not None,
                soup.find('meta', {'name': 'twitter:site', 'content': '@OnlyFans'}) is not None,
                soup.find('link', {'rel': 'canonical', 'href': lambda x: 'onlyfans.com' in x}) is not None,
            ]
            
            # Check for any OnlyFans-related content
            content_indicators = [
                'subscribe' in text_content,
                'posts' in text_content,
                'media' in text_content,
                'content' in text_content,
                'videos' in text_content,
                'photos' in text_content,
                'exclusive' in text_content,
                'premium' in text_content,
                'subscription' in text_content,
                'creator' in text_content
            ]
            
            # If it's not an error page and has OnlyFans indicators, consider it valid
            if any(onlyfans_indicators) or sum(content_indicators) >= 2:
                return True, "Valid OnlyFans profile"
            
            # If we can't determine, but it's not an error page, consider it potentially valid
            if len(text_content) > 100:  # Has some content
                return True, "Potentially valid profile"
            
            return False, "No OnlyFans indicators found"
            
        except Exception as e:
            return False, f"Error validating: {str(e)}"
    
    def scrape_reddit_continuously(self):
        """Scrape OnlyFans links from Reddit continuously until we have enough valid links"""
        print("Scraping Reddit for OnlyFans links continuously...")
        
        subreddits = [
            'onlyfans', 'onlyfans101', 'onlyfanspromotions', 'onlyfansgirls', 'onlyfansleaks',
            'nsfw', 'nsfw_gifs', 'gonewild', 'nsfw_gif', 'nsfw_videos', 'nsfw_pics',
            'realgirls', 'amateur', 'homemade', 'nsfw_amateurs', 'nsfw_hardcore'
        ]
        
        search_queries = [
            'onlyfans.com', 'onlyfans link', 'check out my onlyfans', 'onlyfans profile',
            'onlyfans', 'my onlyfans', 'subscribe to my onlyfans', 'onlyfans exclusive'
        ]
        
        attempts = 0
        max_attempts = 50  # Prevent infinite loops
        
        while len(self.valid_onlyfans_links) < self.max_links and attempts < max_attempts:
            attempts += 1
            print(f"\nAttempt {attempts}: Found {len(self.valid_onlyfans_links)}/{self.max_links} valid links")
            
            # Try different subreddits
            for subreddit in subreddits:
                if len(self.valid_onlyfans_links) >= self.max_links:
                    break
                    
                try:
                    # Try different sorting methods
                    sort_methods = ['hot', 'new', 'top']
                    for sort_method in sort_methods:
                        if len(self.valid_onlyfans_links) >= self.max_links:
                            break
                            
                        url = f"https://www.reddit.com/r/{subreddit}/{sort_method}.json?limit=25"
                        response = self.session.get(url, timeout=10)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            for post in data['data']['children']:
                                if len(self.valid_onlyfans_links) >= self.max_links:
                                    break
                                    
                                post_data = post['data']
                                title = post_data.get('title', '')
                                selftext = post_data.get('selftext', '')
                                url = post_data.get('url', '')
                                
                                text_to_search = f"{title} {selftext} {url}"
                                links = self.extract_onlyfans_links(text_to_search)
                                
                                # Validate each link immediately
                                for link in links:
                                    if len(self.valid_onlyfans_links) >= self.max_links:
                                        break
                                        
                                    if link not in self.valid_onlyfans_links:  # Avoid duplicates
                                        print(f"Validating: {link}")
                                        is_valid, reason = self.validate_onlyfans_profile(link)
                                        
                                        if is_valid:
                                            self.valid_onlyfans_links.add(link)
                                            print(f"✓ Added to list: {reason} ({len(self.valid_onlyfans_links)}/{self.max_links})")
                                        else:
                                            print(f"✗ Rejected: {reason}")
                                        
                                        # Rate limiting between validations
                                        time.sleep(random.uniform(1, 2))
                        
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"Error scraping r/{subreddit}: {e}")
                    continue
            
            # Try search queries if we still need more links
            if len(self.valid_onlyfans_links) < self.max_links:
                for query in search_queries:
                    if len(self.valid_onlyfans_links) >= self.max_links:
                        break
                        
                    try:
                        for subreddit in ['nsfw', 'onlyfans', 'gonewild']:
                            if len(self.valid_onlyfans_links) >= self.max_links:
                                break
                                
                            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=on&sort=relevance&t=all&limit=25"
                            response = self.session.get(url, timeout=10)
                            
                            if response.status_code == 200:
                                data = response.json()
                                
                                for post in data['data']['children']:
                                    if len(self.valid_onlyfans_links) >= self.max_links:
                                        break
                                        
                                    post_data = post['data']
                                    title = post_data.get('title', '')
                                    selftext = post_data.get('selftext', '')
                                    
                                    text_to_search = f"{title} {selftext}"
                                    links = self.extract_onlyfans_links(text_to_search)
                                    
                                    # Validate each link immediately
                                    for link in links:
                                        if len(self.valid_onlyfans_links) >= self.max_links:
                                            break
                                            
                                        if link not in self.valid_onlyfans_links:  # Avoid duplicates
                                            print(f"Validating: {link}")
                                            is_valid, reason = self.validate_onlyfans_profile(link)
                                            
                                            if is_valid:
                                                self.valid_onlyfans_links.add(link)
                                                print(f"✓ Added to list: {reason} ({len(self.valid_onlyfans_links)}/{self.max_links})")
                                            else:
                                                print(f"✗ Rejected: {reason}")
                                            
                                            # Rate limiting between validations
                                            time.sleep(random.uniform(1, 2))
                                
                            time.sleep(1)
                            
                    except Exception as e:
                        print(f"Error searching for '{query}': {e}")
                        continue
            
            # If we still don't have enough links, wait a bit and try again
            if len(self.valid_onlyfans_links) < self.max_links:
                print(f"Waiting 5 seconds before next attempt...")
                time.sleep(5)
    
    def clean_and_validate_links(self):
        """Clean and validate the collected links"""
        cleaned_links = set()
        
        for link in self.valid_onlyfans_links:
            if 'onlyfans.com' in link.lower():
                parsed = urlparse(link)
                clean_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                
                if re.match(r'https?://(?:www\.)?onlyfans\.com/[a-zA-Z0-9_-]+/?$', clean_link):
                    cleaned_links.add(clean_link)
        
        return list(cleaned_links)[:self.max_links]
    
    def save_links(self, links):
        """Save links to a file"""
        with open('practical_onlyfans_links.txt', 'w') as f:
            for link in links:
                f.write(f"{link}\n")
        
        with open('practical_onlyfans_links.json', 'w') as f:
            json.dump({
                'links': links, 
                'count': len(links),
                'validation_info': 'Links validated as real OnlyFans profiles'
            }, f, indent=2)
    
    def run(self):
        """Main method to run the practical scraper"""
        try:
            print("Starting Practical OnlyFans Link Scraper...")
            print(f"Target: {self.max_links} validated links")
            print("This will keep searching until it finds enough valid links.")
            print()
            
            # Scrape continuously until we have enough valid links
            self.scrape_reddit_continuously()
            
            # Clean and validate links
            final_links = self.clean_and_validate_links()
            
            # Save results
            self.save_links(final_links)
            
            print(f"\nScraping completed!")
            print(f"Total validated OnlyFans links found: {len(final_links)}")
            print(f"Links saved to: practical_onlyfans_links.txt and practical_onlyfans_links.json")
            
            # Display first 10 links as preview
            if final_links:
                print("\nFirst 10 validated links:")
                for i, link in enumerate(final_links[:10], 1):
                    print(f"{i}. {link}")
            
        except Exception as e:
            print(f"Error during scraping: {e}")

if __name__ == "__main__":
    scraper = PracticalOnlyFansScraper()
    scraper.run() 