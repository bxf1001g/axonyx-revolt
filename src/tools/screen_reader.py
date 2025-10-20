"""
Screen Reading and OCR Tools
Extract text from screen using OCR, take screenshots
"""

import os
from typing import Dict, List
from pathlib import Path
from datetime import datetime

try:
    import pyautogui
    import pytesseract
    from PIL import Image
    import re
    
    # Try to set Tesseract path if installed
    try:
        # Common Tesseract installation paths
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
        ]
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
    except:
        pass
except ImportError as e:
    print(f"Warning: Some screen_reader dependencies not available: {e}")

def take_screenshot(save_path: str = None, region: tuple = None) -> Dict:
    """
    Take a screenshot of the entire screen or a specific region
    
    Args:
        save_path: Optional path to save screenshot (default: screenshots/screenshot_TIMESTAMP.png)
        region: Optional tuple (x, y, width, height) to capture specific area
    
    Returns:
        Dict with success status and file path
    """
    try:
        # Default save location - use actual Desktop (handles OneDrive redirection)
        if not save_path:
            # Get the real Desktop path (handles OneDrive Desktop redirection)
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
                desktop_path = Path(winreg.QueryValueEx(key, "Desktop")[0])
                winreg.CloseKey(key)
                # Expand environment variables
                desktop_path = Path(os.path.expandvars(str(desktop_path)))
            except:
                # Fallback to standard Desktop
                desktop_path = Path.home() / "Desktop"
            
            screenshots_dir = desktop_path / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = str(screenshots_dir / f"screenshot_{timestamp}.png")
        else:
            # Handle relative paths like "Desktop/file.png"
            save_path = str(Path(save_path).expanduser())
            if not Path(save_path).is_absolute():
                # If starts with Desktop, use actual Desktop path (OneDrive-aware)
                if save_path.lower().startswith('desktop'):
                    try:
                        import winreg
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
                        desktop_path = Path(winreg.QueryValueEx(key, "Desktop")[0])
                        winreg.CloseKey(key)
                        desktop_path = Path(os.path.expandvars(str(desktop_path)))
                        # Remove "Desktop/" or "Desktop\" from start
                        relative_part = save_path[8:] if len(save_path) > 8 else ""
                        save_path = str(desktop_path / relative_part) if relative_part else str(desktop_path)
                    except:
                        save_path = str(Path.home() / save_path)
                elif save_path.lower().startswith(('documents', 'downloads', 'pictures')):
                    save_path = str(Path.home() / save_path)
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Take screenshot
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Save
        screenshot.save(save_path)
        
        return {
            "success": True,
            "file_path": save_path,
            "message": f"Screenshot saved to {save_path}",
            "size": f"{screenshot.width}x{screenshot.height}"
        }
    except Exception as e:
        return {"error": f"Failed to take screenshot: {str(e)}"}


def extract_text_from_screen(region: tuple = None, language: str = "eng") -> Dict:
    """
    Extract text from screen using OCR
    
    Args:
        region: Optional tuple (x, y, width, height) to read specific area
        language: OCR language (default: eng)
    
    Returns:
        Dict with extracted text
    """
    try:
        # Take screenshot
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Check if Tesseract is available
        try:
            # Perform OCR
            text = pytesseract.image_to_string(screenshot, lang=language)
            
            return {
                "success": True,
                "text": text.strip(),
                "length": len(text.strip()),
                "message": "Text extracted successfully"
            }
        except pytesseract.TesseractNotFoundError:
            return {
                "error": "Tesseract OCR not installed. Please install from: https://github.com/UB-Mannheim/tesseract/wiki or run as admin: choco install tesseract",
                "screenshot_saved": False,
                "note": "Screenshot capability works, but OCR requires Tesseract installation"
            }
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}


def find_text_on_screen(search_text: str, case_sensitive: bool = False) -> Dict:
    """
    Take screenshot and search for specific text using OCR
    
    Args:
        search_text: Text to search for
        case_sensitive: Whether search is case sensitive
    
    Returns:
        Dict with found status and context
    """
    try:
        # Take screenshot and extract text
        screenshot = pyautogui.screenshot()
        full_text = pytesseract.image_to_string(screenshot)
        
        # Search
        if not case_sensitive:
            found = search_text.lower() in full_text.lower()
            search_in = full_text.lower()
            search_for = search_text.lower()
        else:
            found = search_text in full_text
            search_in = full_text
            search_for = search_text
        
        if found:
            # Get context around found text
            index = search_in.find(search_for)
            start = max(0, index - 50)
            end = min(len(full_text), index + len(search_text) + 50)
            context = full_text[start:end].strip()
            
            return {
                "success": True,
                "found": True,
                "search_text": search_text,
                "context": context,
                "message": f"Found '{search_text}' on screen"
            }
        else:
            return {
                "success": True,
                "found": False,
                "search_text": search_text,
                "message": f"Text '{search_text}' not found on screen"
            }
    except Exception as e:
        return {"error": f"Failed to search text: {str(e)}"}


def extract_currency_from_screen(region: tuple = None) -> Dict:
    """
    Extract currency values from screen (like $4.61, €100.00)
    
    Args:
        region: Optional tuple (x, y, width, height) to search specific area
    
    Returns:
        Dict with found currency values
    """
    try:
        # Take screenshot and extract text
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        text = pytesseract.image_to_string(screenshot)
        
        # Find currency patterns: $123.45, €123.45, £123.45, 123.45 USD
        patterns = [
            r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?',  # $1,234.56
            r'€\s*\d+(?:,\d{3})*(?:\.\d{2})?',   # €1,234.56
            r'£\s*\d+(?:,\d{3})*(?:\.\d{2})?',   # £1,234.56
            r'\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP)',  # 1,234.56 USD
        ]
        
        found_values = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            found_values.extend(matches)
        
        # Remove duplicates while preserving order
        unique_values = []
        for val in found_values:
            if val not in unique_values:
                unique_values.append(val)
        
        if unique_values:
            return {
                "success": True,
                "currency_values": unique_values,
                "count": len(unique_values),
                "message": f"Found {len(unique_values)} currency value(s)",
                "full_text_context": text[:200]  # First 200 chars for context
            }
        else:
            return {
                "success": True,
                "currency_values": [],
                "count": 0,
                "message": "No currency values found",
                "full_text_context": text[:200]
            }
    except Exception as e:
        return {"error": f"Failed to extract currency: {str(e)}"}


def locate_image_on_screen(image_path: str, confidence: float = 0.8) -> Dict:
    """
    Find an image on the screen (useful for finding buttons, icons)
    
    Args:
        image_path: Path to image file to find
        confidence: Match confidence (0.0 to 1.0)
    
    Returns:
        Dict with location if found
    """
    try:
        image_path = str(Path(image_path).expanduser())
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        
        if location:
            center = pyautogui.center(location)
            return {
                "success": True,
                "found": True,
                "x": location.left,
                "y": location.top,
                "width": location.width,
                "height": location.height,
                "center_x": center.x,
                "center_y": center.y,
                "message": f"Image found at ({location.left}, {location.top})"
            }
        else:
            return {
                "success": True,
                "found": False,
                "message": "Image not found on screen"
            }
    except Exception as e:
        return {"error": f"Failed to locate image: {str(e)}"}


# Tool definitions for Claude
def get_screen_reader_tools() -> List[Dict]:
    """Return screen reader tool definitions"""
    return [
        {
            "name": "take_screenshot",
            "description": "Take a screenshot of the entire screen or specific region. Saves to Desktop/screenshots by default. Use this when user asks to 'take a screenshot', 'capture screen', 'grab a picture of my screen'",
            "input_schema": {
                "type": "object",
                "properties": {
                    "save_path": {
                        "type": "string",
                        "description": "Optional: Path to save screenshot (e.g., 'Desktop/myshot.png'). If not provided, saves to Desktop/screenshots/screenshot_TIMESTAMP.png"
                    },
                    "region": {
                        "type": "array",
                        "description": "Optional: Capture specific area as [x, y, width, height]. Example: [0, 0, 800, 600] for top-left 800x600 area",
                        "items": {"type": "integer"},
                        "minItems": 4,
                        "maxItems": 4
                    }
                },
                "required": []
            }
        },
        {
            "name": "extract_text_from_screen",
            "description": "Read all text visible on screen using OCR (Optical Character Recognition). Useful for reading content from any application, browser, PDF viewer, etc. Use when user asks to 'read what's on screen', 'extract text from screen', 'what does my screen say'",
            "input_schema": {
                "type": "object",
                "properties": {
                    "region": {
                        "type": "array",
                        "description": "Optional: Read specific area as [x, y, width, height]. If not provided, reads entire screen",
                        "items": {"type": "integer"},
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "language": {
                        "type": "string",
                        "description": "OCR language code (default: 'eng'). Examples: 'eng' for English, 'fra' for French, 'deu' for German",
                        "default": "eng"
                    }
                },
                "required": []
            }
        },
        {
            "name": "find_text_on_screen",
            "description": "Search for specific text on screen using OCR. Returns whether text was found and surrounding context. Use when user asks 'is [text] visible?', 'find [text] on screen', 'do you see [text]?'",
            "input_schema": {
                "type": "object",
                "properties": {
                    "search_text": {
                        "type": "string",
                        "description": "Text to search for on screen"
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Whether search should be case sensitive (default: false)",
                        "default": False
                    }
                },
                "required": ["search_text"]
            }
        },
        {
            "name": "extract_currency_from_screen",
            "description": "Extract currency values from screen (like $4.61, €100.00, £50.00). Perfect for reading balances, prices, bills. Use when user asks 'what's my balance?', 'get the price', 'how much does it cost?', 'extract the amount'",
            "input_schema": {
                "type": "object",
                "properties": {
                    "region": {
                        "type": "array",
                        "description": "Optional: Search specific area as [x, y, width, height]. If not provided, searches entire screen",
                        "items": {"type": "integer"},
                        "minItems": 4,
                        "maxItems": 4
                    }
                },
                "required": []
            }
        },
        {
            "name": "locate_image_on_screen",
            "description": "Find a specific image (button, icon, logo) on screen. Useful for locating UI elements. User must provide path to reference image file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to image file to find on screen"
                    },
                    "confidence": {
                        "type": "number",
                        "description": "Match confidence from 0.0 to 1.0 (default: 0.8). Lower = more lenient",
                        "default": 0.8
                    }
                },
                "required": ["image_path"]
            }
        }
    ]


# Function mapping
SCREEN_READER_FUNCTIONS = {
    "take_screenshot": take_screenshot,
    "extract_text_from_screen": extract_text_from_screen,
    "find_text_on_screen": find_text_on_screen,
    "extract_currency_from_screen": extract_currency_from_screen,
    "locate_image_on_screen": locate_image_on_screen
}
