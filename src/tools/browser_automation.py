"""
Browser Automation Tools using Selenium
"""
from typing import Dict, List
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
except ImportError:
    webdriver = None


class BrowserSession:
    """Manages browser session state"""
    driver = None
    current_url = None


def start_browser(headless: bool = False, browser: str = "chrome", use_profile: bool = False) -> Dict:
    """
    Start a browser session for automation
    
    Args:
        headless: Run browser in headless mode (no UI)
        browser: Browser to use (chrome, firefox, edge)
        use_profile: Use default Chrome profile with saved logins (Chrome only)
    """
    if not webdriver:
        return {"error": "selenium not installed. Run: pip install selenium"}
    
    try:
        if browser.lower() == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            # Use default Chrome profile if requested
            if use_profile:
                import os
                user_data_dir = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
                options.add_argument(f"--user-data-dir={user_data_dir}")
                options.add_argument("--profile-directory=Default")
            
            BrowserSession.driver = webdriver.Chrome(options=options)
        elif browser.lower() == "firefox":
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            BrowserSession.driver = webdriver.Firefox(options=options)
        elif browser.lower() == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
            BrowserSession.driver = webdriver.Edge(options=options)
        else:
            return {"error": f"Unsupported browser: {browser}"}
        
        BrowserSession.driver.maximize_window()
        
        return {
            "success": True,
            "message": f"{browser.capitalize()} browser started",
            "headless": headless
        }
        
    except Exception as e:
        return {"error": f"Failed to start browser: {str(e)}"}


def navigate_to_url(url: str) -> Dict:
    """Navigate to a URL"""
    if not BrowserSession.driver:
        return {"error": "No browser session. Call start_browser first"}
    
    try:
        BrowserSession.driver.get(url)
        BrowserSession.current_url = url
        time.sleep(2)  # Wait for page load
        
        return {
            "success": True,
            "message": f"Navigated to {url}",
            "title": BrowserSession.driver.title
        }
        
    except Exception as e:
        return {"error": str(e)}


def click_element(selector: str, by: str = "css") -> Dict:
    """
    Click an element on the page
    
    Args:
        selector: CSS selector, XPath, ID, etc.
        by: Selection method (css, xpath, id, name, class, tag)
    """
    if not BrowserSession.driver:
        return {"error": "No browser session"}
    
    try:
        by_mapping = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME
        }
        
        by_method = by_mapping.get(by.lower(), By.CSS_SELECTOR)
        
        element = WebDriverWait(BrowserSession.driver, 10).until(
            EC.element_to_be_clickable((by_method, selector))
        )
        element.click()
        
        return {
            "success": True,
            "message": f"Clicked element: {selector}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def type_text_browser(selector: str, text: str, by: str = "css") -> Dict:
    """Type text into an input field"""
    if not BrowserSession.driver:
        return {"error": "No browser session"}
    
    try:
        by_mapping = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME
        }
        
        by_method = by_mapping.get(by.lower(), By.CSS_SELECTOR)
        
        element = WebDriverWait(BrowserSession.driver, 10).until(
            EC.presence_of_element_located((by_method, selector))
        )
        element.clear()
        element.send_keys(text)
        
        return {
            "success": True,
            "message": f"Typed text into {selector}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def get_page_text() -> Dict:
    """Get all text content from current page"""
    if not BrowserSession.driver:
        return {"error": "No browser session"}
    
    try:
        text = BrowserSession.driver.find_element(By.TAG_NAME, "body").text
        
        return {
            "success": True,
            "text": text[:5000],  # Limit to 5000 chars
            "length": len(text),
            "url": BrowserSession.driver.current_url,
            "title": BrowserSession.driver.title
        }
        
    except Exception as e:
        return {"error": str(e)}


def take_browser_screenshot(filepath: str = None) -> Dict:
    """Take a screenshot of current browser page"""
    if not BrowserSession.driver:
        return {"error": "No browser session"}
    
    try:
        if not filepath:
            from pathlib import Path
            import datetime
            filepath = Path.home() / "Desktop" / f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        BrowserSession.driver.save_screenshot(str(filepath))
        
        return {
            "success": True,
            "message": f"Screenshot saved to {filepath}",
            "filepath": str(filepath)
        }
        
    except Exception as e:
        return {"error": str(e)}


def execute_javascript(script: str) -> Dict:
    """Execute JavaScript code in the browser"""
    if not BrowserSession.driver:
        return {"error": "No browser session"}
    
    try:
        result = BrowserSession.driver.execute_script(script)
        
        return {
            "success": True,
            "result": str(result) if result else "Script executed"
        }
        
    except Exception as e:
        return {"error": str(e)}


def close_browser() -> Dict:
    """Close the browser session"""
    if not BrowserSession.driver:
        return {"error": "No browser session to close"}
    
    try:
        BrowserSession.driver.quit()
        BrowserSession.driver = None
        BrowserSession.current_url = None
        
        return {
            "success": True,
            "message": "Browser closed"
        }
        
    except Exception as e:
        return {"error": str(e)}


def wait_for_element(selector: str, by: str = "css", timeout: int = 10) -> Dict:
    """Wait for an element to appear on the page"""
    if not BrowserSession.driver:
        return {"error": "No browser session"}
    
    try:
        by_mapping = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "name": By.NAME,
            "class": By.CLASS_NAME
        }
        
        by_method = by_mapping.get(by.lower(), By.CSS_SELECTOR)
        
        element = WebDriverWait(BrowserSession.driver, timeout).until(
            EC.presence_of_element_located((by_method, selector))
        )
        
        return {
            "success": True,
            "message": f"Element found: {selector}",
            "visible": element.is_displayed()
        }
        
    except Exception as e:
        return {"error": f"Element not found after {timeout}s: {str(e)}"}


# Tool definitions for Claude
def get_browser_tools() -> List[Dict]:
    """Get browser automation tool definitions"""
    return [
        {
            "name": "start_browser",
            "description": "Start a browser session for web automation. Opens Chrome, Firefox, or Edge. Use use_profile=true to open Chrome with your saved logins.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "headless": {
                        "type": "boolean",
                        "description": "Run browser without UI (default: false)"
                    },
                    "browser": {
                        "type": "string",
                        "description": "Browser to use: 'chrome', 'firefox', or 'edge' (default: chrome)"
                    },
                    "use_profile": {
                        "type": "boolean",
                        "description": "Use default Chrome profile with saved logins and sessions (Chrome only, default: false)"
                    }
                }
            }
        },
        {
            "name": "navigate_to_url",
            "description": "Navigate to a URL in the browser",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to (e.g., https://google.com)"
                    }
                },
                "required": ["url"]
            }
        },
        {
            "name": "click_element",
            "description": "Click an element on the webpage by selector",
            "input_schema": {
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "The selector to find the element (e.g., '#submit-btn', '//button[@id=\"submit\"]')"
                    },
                    "by": {
                        "type": "string",
                        "description": "Selection method: 'css', 'xpath', 'id', 'name', 'class', 'tag' (default: css)"
                    }
                },
                "required": ["selector"]
            }
        },
        {
            "name": "type_text_browser",
            "description": "Type text into an input field on the webpage",
            "input_schema": {
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "Selector for the input field"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to type"
                    },
                    "by": {
                        "type": "string",
                        "description": "Selection method (default: css)"
                    }
                },
                "required": ["selector", "text"]
            }
        },
        {
            "name": "get_page_text",
            "description": "Get all visible text content from the current webpage",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "take_browser_screenshot",
            "description": "Take a screenshot of the current browser webpage (Selenium). Use this only for capturing web content in an active browser session. For general screen capture, use take_screenshot instead.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Where to save the screenshot (default: Desktop with timestamp)"
                    }
                }
            }
        },
        {
            "name": "execute_javascript",
            "description": "Execute JavaScript code in the browser",
            "input_schema": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "JavaScript code to execute"
                    }
                },
                "required": ["script"]
            }
        },
        {
            "name": "wait_for_element",
            "description": "Wait for an element to appear on the page",
            "input_schema": {
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "Selector for the element to wait for"
                    },
                    "by": {
                        "type": "string",
                        "description": "Selection method (default: css)"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default: 10)"
                    }
                },
                "required": ["selector"]
            }
        },
        {
            "name": "close_browser",
            "description": "Close the browser session",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        }
    ]


# Map tool names to functions
BROWSER_FUNCTIONS = {
    "start_browser": start_browser,
    "navigate_to_url": navigate_to_url,
    "click_element": click_element,
    "type_text_browser": type_text_browser,
    "get_page_text": get_page_text,
    "take_browser_screenshot": take_browser_screenshot,
    "execute_javascript": execute_javascript,
    "wait_for_element": wait_for_element,
    "close_browser": close_browser
}
