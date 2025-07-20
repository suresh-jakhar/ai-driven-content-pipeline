import requests
from utils.helpers import print_error, print_success, print_warning
from readability import Document
from bs4 import BeautifulSoup
from config import DATA_DIR
from .screenshot import capture_screenshot
import re
from urllib.parse import urlparse
from tqdm import tqdm

def validate_url(url):
    """Validate the URL structure"""
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError("Invalid URL structure")
    return True

def extract_main_content(html):
    """Extract main content with progress feedback"""
    print("  Analyzing page structure...")
    doc = Document(html)
    with tqdm(total=100, desc="Extracting content", leave=False) as pbar:
        content = doc.summary()
        pbar.update(100)
    return content

def clean_html_content(html):
    """Clean HTML content with progress feedback"""
    print("  Cleaning extracted content...")
    with tqdm(total=100, desc="Cleaning HTML", leave=False) as pbar:
        soup = BeautifulSoup(html, 'lxml')
        pbar.update(20)
        
        for tag in soup(['script', 'style', 'footer', 'nav', 'aside', 'meta']):
            tag.decompose()
        pbar.update(30)
        
        text = soup.get_text()
        pbar.update(20)
        
        text = re.sub(r'\n\s*\n', '\n\n', text)
        pbar.update(20)
        
        text = text.strip()
        pbar.update(10)
    
    return text

def scrape_url(url):
    """Main scraping function"""
    try:
        print(f"\nScraping URL: {url}")
        validate_url(url)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        print("  Downloading page content...")
        with tqdm(total=100, desc="Downloading", leave=False) as pbar:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            pbar.update(100)
        
        article_html = extract_main_content(response.text)
        clean_text = clean_html_content(article_html)
        
        if not clean_text or len(clean_text) < 100:
            raise ValueError("Insufficient content extracted - possible scraping issue")
        
        print("  Capturing page screenshot...")
        screenshot_path = capture_screenshot(url)
        
        return {
            "original_text": clean_text,
            "screenshot_path": str(screenshot_path),
            "content_length": len(clean_text),
            "scrape_success": True
        }
    except Exception as e:
        print_error(f"Scraping failed: {str(e)}")
        return {
            "error": str(e),
            "scrape_success": False
        }