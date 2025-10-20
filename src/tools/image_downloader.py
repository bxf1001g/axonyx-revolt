"""
Google Images Download Tool - Automated image search and download
"""

import time
from typing import Dict, List
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui


def search_and_download_images(query: str, count: int = 10, download_folder: str = None) -> Dict:
    """
    Search Google Images and download specified number of images
    
    Args:
        query: Search query (e.g., "cars", "dogs", "sunset")
        count: Number of images to download (default: 10)
        download_folder: Where to save images (default: Downloads/google_images/{query})
    
    Returns:
        Dict with success status and list of downloaded files
    """
    try:
        from tools.browser_automation import BrowserSession, start_browser
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
        
        # Setup download folder
        if download_folder is None:
            downloads = Path.home() / "Downloads" / "google_images" / query.replace(" ", "_")
        else:
            downloads = Path(download_folder)
        
        downloads.mkdir(parents=True, exist_ok=True)
        
        # Start browser if not already started
        if not BrowserSession.driver:
            result = start_browser(browser="chrome", use_profile=False)
            if "error" in result:
                return result
        
        driver = BrowserSession.driver
        
        # Go directly to Google Images search
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
        driver.get(search_url)
        time.sleep(3)
        
        downloaded_images = []
        attempts = 0
        max_attempts = count * 3  # Try up to 3x the count to account for failures
        
        # Scroll to load more images
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(0.5)
        
        while len(downloaded_images) < count and attempts < max_attempts:
            try:
                attempts += 1
                
                # Re-find thumbnails each iteration to avoid stale elements
                thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf, img.Q4LuWd, img[data-src]")
                
                if not thumbnails:
                    break
                
                # Skip already processed images
                if attempts - 1 >= len(thumbnails):
                    # Scroll more to load additional images
                    driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(1)
                    continue
                
                thumbnail = thumbnails[min(attempts - 1, len(thumbnails) - 1)]
                
                # Scroll thumbnail into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thumbnail)
                time.sleep(0.5)
                
                # Try to click with JavaScript if regular click fails
                try:
                    thumbnail.click()
                except (ElementClickInterceptedException, Exception):
                    driver.execute_script("arguments[0].click();", thumbnail)
                
                time.sleep(2)  # Wait for full image to load
                
                # Find full-size image with multiple strategies
                full_image = None
                selectors = [
                    "img.sFlh5c.pT0Scc.iPVvYb",
                    "img.n3VNCb",
                    "img.iPVvYb",
                    "img[jsname]",
                    "div.p7sI2 img"
                ]
                
                for selector in selectors:
                    try:
                        images = driver.find_elements(By.CSS_SELECTOR, selector)
                        for img in images:
                            src = img.get_attribute("src")
                            if src and src.startswith("http") and "gstatic.com" not in src:
                                full_image = img
                                break
                        if full_image:
                            break
                    except:
                        continue
                
                if full_image:
                    img_url = full_image.get_attribute("src")
                    
                    if img_url and img_url.startswith("http"):
                        try:
                            # Download image
                            response = requests.get(img_url, timeout=10, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            })
                            if response.status_code == 200 and len(response.content) > 5000:  # Skip tiny images
                                file_path = downloads / f"{query.replace(' ', '_')}_{len(downloaded_images) + 1}.jpg"
                                file_path.write_bytes(response.content)
                                downloaded_images.append(str(file_path))
                                print(f"✓ Downloaded image {len(downloaded_images)}/{count}")
                        except Exception as e:
                            print(f"Download error: {e}")
                
                # Close preview
                try:
                    driver.execute_script("document.body.click();")
                    pyautogui.press('escape')
                    time.sleep(0.3)
                except:
                    pass
                    
            except (StaleElementReferenceException, Exception) as e:
                # Just continue to next image on any error
                continue
        
        return {
            "success": True if len(downloaded_images) > 0 else False,
            "message": f"Downloaded {len(downloaded_images)} of {count} requested images for '{query}'",
            "images": downloaded_images,
            "download_folder": str(downloads),
            "note": f"Successfully saved {len(downloaded_images)} images. Some images may have failed due to loading issues."
        }
        
    except Exception as e:
        return {"error": f"Failed to download images: {str(e)}"}


def quick_google_images_search(query: str) -> Dict:
    """
    Quick way to open Google Images search results
    
    Args:
        query: Search query
    
    Returns:
        Dict with success status
    """
    try:
        from tools.browser_automation import BrowserSession, start_browser
        
        # Start browser if not already started
        if not BrowserSession.driver:
            result = start_browser(browser="chrome", use_profile=False)
            if "error" in result:
                return result
        
        # Go directly to Google Images with tbm=isch parameter
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
        BrowserSession.driver.get(search_url)
        
        return {
            "success": True,
            "message": f"Opened Google Images search for '{query}'",
            "url": search_url
        }
        
    except Exception as e:
        return {"error": f"Failed to open Google Images: {str(e)}"}


def download_image_from_url(url: str, save_path: str = None) -> Dict:
    """
    Download a single image from URL
    
    Args:
        url: Image URL
        save_path: Where to save (default: Downloads/image_{timestamp}.jpg)
    
    Returns:
        Dict with success status and file path
    """
    try:
        import requests
        from datetime import datetime
        
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = Path.home() / "Downloads" / f"image_{timestamp}.jpg"
        else:
            save_path = Path(save_path)
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            save_path.write_bytes(response.content)
            return {
                "success": True,
                "file_path": str(save_path),
                "message": f"Image downloaded to {save_path}"
            }
        else:
            return {"error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Failed to download image: {str(e)}"}


# Tool schemas for Claude
def get_image_download_tools():
    """Return tool schemas for image downloading"""
    return [
        {
            "name": "search_and_download_images",
            "description": "Search Google Images and automatically download multiple images. Best for bulk image downloads. Saves to Downloads/google_images/{query}/ folder.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'cars', 'sunset', 'dogs playing')"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of images to download (1-50)",
                        "default": 10
                    },
                    "download_folder": {
                        "type": "string",
                        "description": "Custom download folder path (optional)"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "quick_google_images_search",
            "description": "Quickly open Google Images search results for a query. Use this first before downloading, or when you just want to show images without downloading.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "download_image_from_url",
            "description": "Download a single image from a direct URL. Use when you have a specific image URL.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Direct image URL (http:// or https://)"
                    },
                    "save_path": {
                        "type": "string",
                        "description": "Where to save the image (optional)"
                    }
                },
                "required": ["url"]
            }
        }
    ]


# Function mapping for agent
IMAGE_DOWNLOAD_FUNCTIONS = {
    "search_and_download_images": search_and_download_images,
    "quick_google_images_search": quick_google_images_search,
    "download_image_from_url": download_image_from_url
}
