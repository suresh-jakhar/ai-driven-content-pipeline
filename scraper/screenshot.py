from playwright.sync_api import sync_playwright
from config import SCREENSHOTS_DIR
import hashlib
from datetime import datetime
import subprocess
from utils.helpers import print_error, print_info, print_success

def capture_screenshot(url):
    """Capture full-page screenshot with automatic browser installation"""
    try:
        url_hash = hashlib.md5(url.encode()).hexdigest()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{url_hash}_{timestamp}.png"
        screenshot_path = SCREENSHOTS_DIR / filename

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception as e:
                print_info("Installing required browsers...")
                result = subprocess.run(["playwright", "install"], capture_output=True, text=True)
                if result.returncode != 0:
                    print_error("Failed to install browsers automatically")
                    print_error(result.stderr)
                    return None
                print_success("Browsers installed successfully")
                browser = p.chromium.launch()

            try:
                page = browser.new_page()
                page.goto(url)
                page.screenshot(path=screenshot_path, full_page=True)
                print_success(f"Screenshot saved to: {screenshot_path}")
                return str(screenshot_path)
            except Exception as e:
                print_error(f"Failed to capture screenshot: {str(e)}")
                return None
            finally:
                browser.close()
                
    except Exception as e:
        print_error(f"Screenshot error: {str(e)}")
        return None