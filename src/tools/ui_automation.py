"""
UI Automation Tools using pywinauto and pyautogui
"""
import time
from typing import Dict, List, Tuple

try:
    import pyautogui
    import pywinauto
    from pywinauto import Desktop
except ImportError:
    pyautogui = None
    pywinauto = None


def type_text(text: str, interval: float = 0.05) -> Dict:
    """Type text using keyboard automation"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        pyautogui.write(text, interval=interval)
        return {"success": True, "message": f"Typed: {text}"}
    except Exception as e:
        return {"error": str(e)}


def press_key(key: str, presses: int = 1) -> Dict:
    """Press a keyboard key (e.g., 'enter', 'tab', 'esc')"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        pyautogui.press(key, presses=presses)
        return {"success": True, "message": f"Pressed {key} {presses} time(s)"}
    except Exception as e:
        return {"error": str(e)}


def click_mouse(x: int = None, y: int = None, clicks: int = 1, button: str = 'left') -> Dict:
    """Click the mouse at coordinates or current position"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        if x is not None and y is not None:
            pyautogui.click(x, y, clicks=clicks, button=button)
            return {"success": True, "message": f"Clicked at ({x}, {y})"}
        else:
            pyautogui.click(clicks=clicks, button=button)
            return {"success": True, "message": "Clicked at current position"}
    except Exception as e:
        return {"error": str(e)}


def move_mouse(x: int, y: int, duration: float = 0.5) -> Dict:
    """Move the mouse to coordinates"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        pyautogui.moveTo(x, y, duration=duration)
        return {"success": True, "message": f"Moved mouse to ({x}, {y})"}
    except Exception as e:
        return {"error": str(e)}


def get_mouse_position() -> Dict:
    """Get current mouse cursor position"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        x, y = pyautogui.position()
        return {"success": True, "x": x, "y": y}
    except Exception as e:
        return {"error": str(e)}


def get_screen_size() -> Dict:
    """Get screen dimensions"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        width, height = pyautogui.size()
        return {"success": True, "width": width, "height": height}
    except Exception as e:
        return {"error": str(e)}


def find_window(title: str = None, class_name: str = None) -> Dict:
    """Find a window by title or class name"""
    if not pywinauto:
        return {"error": "pywinauto not installed"}
    
    try:
        desktop = Desktop(backend="uia")
        windows = desktop.windows()
        
        matches = []
        for win in windows:
            try:
                win_title = win.window_text()
                if title and title.lower() in win_title.lower():
                    matches.append({
                        "title": win_title,
                        "handle": win.handle
                    })
            except:
                pass
        
        return {
            "success": True,
            "windows": matches,
            "count": len(matches)
        }
    except Exception as e:
        return {"error": str(e)}


def hotkey(*keys: str) -> Dict:
    """Press a keyboard shortcut (e.g., 'ctrl', 'c' for copy)"""
    if not pyautogui:
        return {"error": "pyautogui not installed"}
    
    try:
        pyautogui.hotkey(*keys)
        return {"success": True, "message": f"Pressed hotkey: {'+'.join(keys)}"}
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_ui_tools() -> List[Dict]:
    """Get UI automation tool definitions"""
    return [
        {
            "name": "type_text",
            "description": "Type text using keyboard automation. The text will be typed wherever the cursor is currently focused.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to type"
                    },
                    "interval": {
                        "type": "number",
                        "description": "Delay between keystrokes in seconds (default 0.05)"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "press_key",
            "description": "Press a keyboard key. Useful for special keys like enter, tab, esc, backspace, delete, etc.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The key to press (e.g., 'enter', 'tab', 'esc', 'space', 'backspace')"
                    },
                    "presses": {
                        "type": "integer",
                        "description": "Number of times to press (default 1)"
                    }
                },
                "required": ["key"]
            }
        },
        {
            "name": "hotkey",
            "description": "Press a keyboard shortcut combination (e.g., Ctrl+C, Alt+Tab)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "keys": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Keys to press together (e.g., ['ctrl', 'c'] for copy)"
                    }
                },
                "required": ["keys"]
            }
        },
        {
            "name": "click_mouse",
            "description": "Click the mouse at specified coordinates or current position",
            "input_schema": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "X coordinate to click at"
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y coordinate to click at"
                    },
                    "clicks": {
                        "type": "integer",
                        "description": "Number of clicks (default 1, use 2 for double-click)"
                    },
                    "button": {
                        "type": "string",
                        "description": "Mouse button to click: 'left', 'right', or 'middle'"
                    }
                }
            }
        },
        {
            "name": "move_mouse",
            "description": "Move the mouse cursor to specific coordinates",
            "input_schema": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "integer",
                        "description": "X coordinate to move to"
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y coordinate to move to"
                    },
                    "duration": {
                        "type": "number",
                        "description": "Time in seconds for the movement (default 0.5)"
                    }
                },
                "required": ["x", "y"]
            }
        },
        {
            "name": "get_mouse_position",
            "description": "Get the current mouse cursor position",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "get_screen_size",
            "description": "Get the screen resolution/dimensions",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "find_window",
            "description": "Find open windows by title. Useful for checking if an application is running.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Part of the window title to search for"
                    }
                },
                "required": ["title"]
            }
        }
    ]


# Map tool names to functions - need to handle hotkey specially
def hotkey_wrapper(**kwargs):
    keys = kwargs.get('keys', [])
    return hotkey(*keys)


UI_FUNCTIONS = {
    "type_text": type_text,
    "press_key": press_key,
    "click_mouse": click_mouse,
    "move_mouse": move_mouse,
    "get_mouse_position": get_mouse_position,
    "get_screen_size": get_screen_size,
    "find_window": find_window,
    "hotkey": hotkey_wrapper
}
