"""
Launch default Chrome browser with user profile (simpler than Selenium)
"""
import subprocess
import time
from typing import Dict, List


def open_chrome_with_profile(url: str = None, wait_seconds: int = 3) -> Dict:
    """
    Open default Chrome browser with your saved logins and profile
    
    This opens your normal Chrome (not Selenium) so all your accounts work!
    
    Args:
        url: Optional URL to open
        wait_seconds: How long to wait for page to load (default: 3)
    """
    try:
        # Chrome executable paths
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        # Find Chrome
        chrome_exe = None
        for path in chrome_paths:
            from pathlib import Path
            if Path(path).exists():
                chrome_exe = path
                break
        
        if not chrome_exe:
            return {"error": "Chrome not found. Please install Google Chrome"}
        
        # Launch Chrome with URL
        if url:
            subprocess.Popen([chrome_exe, url])
            
            # Wait for page to load
            if wait_seconds > 0:
                time.sleep(wait_seconds)
            
            return {
                "success": True,
                "message": f"Opened Chrome with your profile at {url}",
                "note": f"Waited {wait_seconds} seconds for page to load. This is your regular Chrome with all saved logins!",
                "wait_seconds": wait_seconds
            }
        else:
            subprocess.Popen([chrome_exe])
            return {
                "success": True,
                "message": "Opened Chrome with your profile"
            }
            
    except Exception as e:
        return {"error": str(e)}


# Tool definitions
def get_chrome_launcher_tools() -> List[Dict]:
    """Get Chrome launcher tool definitions"""
    return [
        {
            "name": "open_chrome_with_profile",
            "description": "Open your DEFAULT Chrome browser with all your saved logins and Google accounts. Use this when you need to access sites where you're already logged in (like Anthropic Console, Gmail, etc). This opens your regular Chrome, not a new automated session. Waits for page to load before returning.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Optional URL to open (e.g., 'https://console.anthropic.com/settings/billing')"
                    },
                    "wait_seconds": {
                        "type": "integer",
                        "description": "Seconds to wait for page to load (default: 3). Increase for slow connections or complex pages.",
                        "default": 3
                    }
                }
            }
        }
    ]


# Map tool names to functions
CHROME_LAUNCHER_FUNCTIONS = {
    "open_chrome_with_profile": open_chrome_with_profile
}
