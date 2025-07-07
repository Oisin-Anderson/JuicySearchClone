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

class ValidatedOnlyFansScraper:
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
        """Validate if an OnlyFans profile is real and active"""
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
            
            # Look for strong indicators that this is a real OnlyFans profile
            text_content = soup.get_text().lower()
            
            # Check for OnlyFans-specific elements
            onlyfans_indicators = [
                soup.find('meta', {'property': 'og:site_name', 'content': 'OnlyFans'}),
                soup.find('meta', {'name': 'twitter:site', 'content': '@OnlyFans'}),
                soup.find('link', {'rel': 'canonical', 'href': lambda x: 'onlyfans.com' in x}),
            ]
            
            # Check title separately
            title_tag = soup.find('title')
            if title_tag and title_tag.get_text() and 'onlyfans' in title_tag.get_text().lower():
                onlyfans_indicators.append(title_tag)
            
            # Check for profile-specific content
            profile_indicators = [
                soup.find('div', {'class': lambda x: x and 'profile' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'creator' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'user' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'account' in x.lower()}),
            ]
            
            # Check for content indicators
            content_indicators = [
                soup.find('div', {'class': lambda x: x and 'posts' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'media' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'content' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'gallery' in x.lower()}),
            ]
            
            # Check for subscription elements
            subscription_indicators = [
                soup.find('button', {'class': lambda x: x and 'subscribe' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'price' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'subscription' in x.lower()}),
                soup.find('span', {'class': lambda x: x and 'price' in x.lower()}),
            ]
            
            # Check for OnlyFans branding
            branding_indicators = [
                soup.find('img', {'src': lambda x: x and 'onlyfans' in x.lower()}),
                soup.find('img', {'alt': lambda x: x and 'onlyfans' in x.lower()}),
                soup.find('svg', {'class': lambda x: x and 'onlyfans' in x.lower()}),
            ]
            
            # Count how many indicator categories we have
            indicator_counts = {
                'onlyfans': sum(1 for i in onlyfans_indicators if i is not None),
                'profile': sum(1 for i in profile_indicators if i is not None),
                'content': sum(1 for i in content_indicators if i is not None),
                'subscription': sum(1 for i in subscription_indicators if i is not None),
                'branding': sum(1 for i in branding_indicators if i is not None),
            }
            
            # Check for content keywords in text
            content_keywords = [
                'onlyfans', 'subscribe', 'posts', 'media', 'content', 'videos', 
                'photos', 'exclusive', 'premium', 'subscription', 'creator'
            ]
            
            keyword_matches = sum(1 for keyword in content_keywords if keyword in text_content)
            
            # Check for common error/invalid page indicators
            error_indicators = [
                'page not found', 'profile not found', 'user not found', 'account suspended',
                'this page is not available', 'access denied', 'forbidden', 'not found',
                'does not exist', 'no longer available', 'account deleted'
            ]
            
            has_errors = any(error in text_content for error in error_indicators)
            
            # Determine if profile is valid (more strict criteria)
            if has_errors:
                return False, "Error page detected"
            
            # Calculate total indicator score
            total_indicators = sum(indicator_counts.values()) + keyword_matches
            
            # Require multiple strong indicators to consider it valid
            if total_indicators >= 3:
                content_count = self.extract_content_count(soup)
                if content_count > 0:
                    return True, f"Valid profile with {content_count} posts (score: {total_indicators})"
                else:
                    return True, f"Valid profile (score: {total_indicators})"
            elif total_indicators >= 2 and keyword_matches >= 2:
                return True, f"Valid profile (score: {total_indicators})"
            
            return False, f"No OnlyFans indicators found (score: {total_indicators})"
            
        except Exception as e:
            return False, f"Error validating: {str(e)}"
    
    def extract_content_count(self, soup):
        """Extract content count from profile page"""
        try:
            # Look for post count indicators
            text = soup.get_text()
            
            # Common patterns for post counts
            patterns = [
                r'(\d+)\s*posts?',
                r'(\d+)\s*photos?',
                r'(\d+)\s*videos?',
                r'(\d+)\s*media',
                r'(\d+)\s*items?'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            
            return 0
        except:
            return 0
    
    def scrape_reddit_with_validation(self):
        """Scrape OnlyFans links from Reddit and validate them immediately"""
        print("Scraping Reddit for OnlyFans links and validating profiles immediately...")
        
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
            if len(self.valid_onlyfans_links) >= self.max_links:
                break
                
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
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
                                
                            print(f"Validating: {link}")
                            is_valid, reason = self.validate_onlyfans_profile(link)
                            
                            if is_valid:
                                self.valid_onlyfans_links.add(link)
                                print(f"✓ Added to list: {reason}")
                            else:
                                print(f"✗ Rejected: {reason}")
                            
                            # Rate limiting between validations
                            time.sleep(random.uniform(1, 3))
                        
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping r/{subreddit}: {e}")
                continue
    

    
    def scrape_reddit_search_with_validation(self):
        """Scrape OnlyFans links from Reddit search and validate them immediately"""
        print("Scraping Reddit search results for OnlyFans links and validating immediately...")
        
        search_queries = [
            'onlyfans.com',
            'onlyfans link',
            'check out my onlyfans',
            'onlyfans profile'
        ]
        
        for query in search_queries:
            if len(self.valid_onlyfans_links) >= self.max_links:
                break
                
            try:
                subreddits = ['nsfw', 'onlyfans', 'gonewild']
                
                for subreddit in subreddits:
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
                                    
                                print(f"Validating: {link}")
                                is_valid, reason = self.validate_onlyfans_profile(link)
                                
                                if is_valid:
                                    self.valid_onlyfans_links.add(link)
                                    print(f"✓ Added to list: {reason}")
                                else:
                                    print(f"✗ Rejected: {reason}")
                                
                                # Rate limiting between validations
                                time.sleep(random.uniform(1, 3))
                            
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Error scraping Reddit search for '{query}': {e}")
                continue
    
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
        with open('validated_onlyfans_links.txt', 'w') as f:
            for link in links:
                f.write(f"{link}\n")
        
        with open('validated_onlyfans_links.json', 'w') as f:
            json.dump({
                'links': links, 
                'count': len(links),
                'validation_info': 'All links have been validated as real, active OnlyFans profiles'
            }, f, indent=2)
    
    def run(self):
        """Main method to run the validated scraper"""
        try:
            print("Starting Validated OnlyFans Link Scraper...")
            print(f"Target: {self.max_links} validated links")
            print("This will take longer as each profile is validated individually.")
            print()
            
            # Scrape and validate from different sources
            self.scrape_reddit_with_validation()
            
            if len(self.valid_onlyfans_links) < self.max_links:
                self.scrape_reddit_search_with_validation()
            
            # Clean and validate links
            final_links = self.clean_and_validate_links()
            
            # Save results
            self.save_links(final_links)
            
            print(f"\nValidation completed!")
            print(f"Total validated OnlyFans links found: {len(final_links)}")
            print(f"Links saved to: validated_onlyfans_links.txt and validated_onlyfans_links.json")
            
            # Display first 10 links as preview
            if final_links:
                print("\nFirst 10 validated links:")
                for i, link in enumerate(final_links[:10], 1):
                    print(f"{i}. {link}")
            
        except Exception as e:
            print(f"Error during scraping: {e}")

if __name__ == "__main__":
    scraper = ValidatedOnlyFansScraper()
    scraper.run() 