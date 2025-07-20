import hashlib
import logging
from colorama import Fore, Style, init
import re

# Initialize colorama
init()

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger("utils.helpers")

def clean_text(text):
    """Basic text cleaning: strip, remove extra spaces, normalize newlines."""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")

def generate_chapter_id(url):
    """Generate a unique chapter ID from the URL."""
    return hashlib.md5(url.encode()).hexdigest()[:12]