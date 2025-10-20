"""
Hybrid Installer Automation
Combines pywinauto, pyautogui, and OCR for robust installer automation
"""

import time
from typing import Dict, List, Optional
from pathlib import Path

try:
    import pyautogui
    import pywinauto
    from pywinauto import Desktop
    from pywinauto.findwindows import ElementNotFoundError
except ImportError as e:
    print(f"Warning: installer_automation dependencies not available: {e}")


def wait_for_installer_window(window_title_contains: str, timeout: int = 30) -> Dict:
    """
    Wait for installer window to appear and return window info
    
    Args:
        window_title_contains: Text that appears in window title
        timeout: Maximum seconds to wait
    
    Returns:
        Dict with window info or error
    """
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                desktop = Desktop(backend="uia")
                windows = desktop.windows()
                
                for window in windows:
                    title = window.window_text()
                    if window_title_contains.lower() in title.lower():
                        return {
                            "success": True,
                            "window_title": title,
                            "found": True,
                            "message": f"Found installer window: {title}"
                        }
            except:
                pass
            
            time.sleep(1)
        
        return {
            "success": True,
            "found": False,
            "message": f"No window containing '{window_title_contains}' found after {timeout}s"
        }
    except Exception as e:
        return {"error": f"Failed to wait for window: {str(e)}"}


def find_and_click_checkbox_by_text(window_title: str, checkbox_text: str) -> Dict:
    """
    Find checkbox near specific text and click it using pywinauto
    
    Args:
        window_title: Window title to search in
        checkbox_text: Text near the checkbox
    
    Returns:
        Dict with success status
    """
    try:
        desktop = Desktop(backend="uia")
        window = desktop.window(title_re=f".*{window_title}.*")
        window.set_focus()
        
        # Try to find checkbox by label
        try:
            checkbox = window.child_window(title=checkbox_text, control_type="CheckBox")
            if not checkbox.get_toggle_state():
                checkbox.click_input()
                return {
                    "success": True,
                    "message": f"Checked checkbox: {checkbox_text}",
                    "method": "pywinauto"
                }
            else:
                return {
                    "success": True,
                    "message": f"Checkbox already checked: {checkbox_text}",
                    "method": "pywinauto"
                }
        except:
            # Try to find text and click nearby
            try:
                text_elem = window.child_window(title=checkbox_text, control_type="Text")
                rect = text_elem.rectangle()
                # Click to the left of the text (where checkbox usually is)
                pyautogui.click(rect.left - 20, rect.top + rect.height() // 2)
                return {
                    "success": True,
                    "message": f"Clicked near text: {checkbox_text}",
                    "method": "pyautogui_coordinates"
                }
            except:
                return {"error": f"Could not find checkbox or text: {checkbox_text}"}
                
    except Exception as e:
        return {"error": f"Failed to find/click checkbox: {str(e)}"}


def find_and_click_button_by_text(window_title: str, button_text: str) -> Dict:
    """
    Find and click button with specific text using pywinauto
    
    Args:
        window_title: Window title to search in
        button_text: Text on the button
    
    Returns:
        Dict with success status
    """
    try:
        desktop = Desktop(backend="uia")
        window = desktop.window(title_re=f".*{window_title}.*")
        window.set_focus()
        
        # Try to find button by exact title
        try:
            button = window.child_window(title=button_text, control_type="Button")
            button.click_input()
            return {
                "success": True,
                "message": f"Clicked button: {button_text}",
                "method": "pywinauto"
            }
        except:
            # Try partial match
            try:
                button = window.child_window(title_re=f".*{button_text}.*", control_type="Button")
                button.click_input()
                return {
                    "success": True,
                    "message": f"Clicked button (partial match): {button_text}",
                    "method": "pywinauto_partial"
                }
            except:
                return {"error": f"Could not find button: {button_text}"}
                
    except Exception as e:
        return {"error": f"Failed to find/click button: {str(e)}"}


def find_text_on_screen_and_click_nearby(text: str, offset_x: int = 0, offset_y: int = 0) -> Dict:
    """
    Use OCR to find text on screen and click at offset position
    Useful when UI elements aren't accessible via pywinauto
    
    Args:
        text: Text to find on screen
        offset_x: Horizontal offset from text position (negative = left, positive = right)
        offset_y: Vertical offset from text position
    
    Returns:
        Dict with success status
    """
    try:
        # This requires the OCR tools from screen_reader
        from tools.screen_reader import find_text_on_screen
        
        result = find_text_on_screen(text, case_sensitive=False)
        
        if result.get("found"):
            # Take screenshot and get text position
            screenshot = pyautogui.screenshot()
            
            # Use pytesseract to get bounding boxes
            try:
                import pytesseract
                from PIL import Image
                
                data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
                
                # Find text position
                for i, word in enumerate(data['text']):
                    if text.lower() in word.lower():
                        x = data['left'][i] + offset_x
                        y = data['top'][i] + data['height'][i] // 2 + offset_y
                        
                        pyautogui.click(x, y)
                        return {
                            "success": True,
                            "message": f"Clicked at offset ({offset_x}, {offset_y}) from text '{text}'",
                            "position": {"x": x, "y": y},
                            "method": "ocr_click"
                        }
                        
                return {"error": f"Found text '{text}' but could not determine position"}
            except ImportError:
                return {"error": "OCR (pytesseract) not installed"}
        else:
            return {"error": f"Text '{text}' not found on screen"}
            
    except Exception as e:
        return {"error": f"Failed OCR click: {str(e)}"}


def automate_python_installer(installer_path: str, add_to_path: bool = True) -> Dict:
    """
    Automate Python installer with proper PATH checkbox handling
    
    Args:
        installer_path: Path to python installer exe
        add_to_path: Whether to check "Add Python to PATH"
    
    Returns:
        Dict with installation status
    """
    try:
        import subprocess
        
        installer_path = Path(installer_path).expanduser()
        if not installer_path.exists():
            return {"error": f"Installer not found: {installer_path}"}
        
        # Launch installer
        subprocess.Popen([str(installer_path)])
        
        # Wait for installer window
        time.sleep(2)
        wait_result = wait_for_installer_window("Python", timeout=10)
        
        if not wait_result.get("found"):
            return {"error": "Installer window did not appear"}
        
        window_title = wait_result.get("window_title", "Python")
        
        # Check "Add Python to PATH" if requested
        if add_to_path:
            time.sleep(1)
            checkbox_result = find_and_click_checkbox_by_text(
                window_title, 
                "Add Python"  # Partial match for "Add Python to PATH"
            )
            
            if not checkbox_result.get("success"):
                # Fallback: Try OCR approach
                checkbox_result = find_text_on_screen_and_click_nearby(
                    "Add Python to PATH",
                    offset_x=-20,  # Click 20 pixels to the left of text (checkbox position)
                    offset_y=0
                )
        
        # Click "Install Now" button
        time.sleep(1)
        install_result = find_and_click_button_by_text(window_title, "Install Now")
        
        if not install_result.get("success"):
            # Try alternative button texts
            for button_text in ["Install", "Next", "Continue"]:
                install_result = find_and_click_button_by_text(window_title, button_text)
                if install_result.get("success"):
                    break
        
        return {
            "success": True,
            "message": "Python installer automated",
            "checkbox_result": checkbox_result if add_to_path else None,
            "install_click": install_result,
            "note": "Installation is running. It may take a few minutes."
        }
        
    except Exception as e:
        return {"error": f"Failed to automate installer: {str(e)}"}


def check_installation_progress(window_title_contains: str = "Python") -> Dict:
    """
    Check if installation window is still open (indicates ongoing installation)
    
    Returns:
        Dict with installation status
    """
    try:
        desktop = Desktop(backend="uia")
        windows = desktop.windows()
        
        for window in windows:
            title = window.window_text()
            if window_title_contains.lower() in title.lower():
                # Try to find progress bar or "Installing" text
                try:
                    # Check for progress indicators
                    controls = window.descendants()
                    for ctrl in controls:
                        ctrl_text = ctrl.window_text()
                        if any(word in ctrl_text.lower() for word in ["installing", "please wait", "progress"]):
                            return {
                                "success": True,
                                "installing": True,
                                "message": f"Installation in progress: {ctrl_text}"
                            }
                except:
                    pass
                
                return {
                    "success": True,
                    "installing": True,
                    "message": f"Installer window still open: {title}"
                }
        
        return {
            "success": True,
            "installing": False,
            "message": "No installer window found - installation may be complete"
        }
        
    except Exception as e:
        return {"error": f"Failed to check installation progress: {str(e)}"}


# Tool definitions
def get_installer_automation_tools() -> List[Dict]:
    """Get installer automation tool definitions"""
    return [
        {
            "name": "wait_for_installer_window",
            "description": "Wait for installer window to appear. Use after launching an installer to detect when UI is ready.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title_contains": {
                        "type": "string",
                        "description": "Text that appears in window title (e.g., 'Python', 'Setup', 'Install')"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum seconds to wait (default: 30)",
                        "default": 30
                    }
                },
                "required": ["window_title_contains"]
            }
        },
        {
            "name": "find_and_click_checkbox_by_text",
            "description": "Find and check a checkbox near specific text in installer window. Uses pywinauto + fallback to pyautogui.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title or partial title"
                    },
                    "checkbox_text": {
                        "type": "string",
                        "description": "Text label near checkbox (e.g., 'Add Python to PATH')"
                    }
                },
                "required": ["window_title", "checkbox_text"]
            }
        },
        {
            "name": "find_and_click_button_by_text",
            "description": "Find and click button with specific text in installer window. Uses pywinauto.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title or partial title"
                    },
                    "button_text": {
                        "type": "string",
                        "description": "Button text (e.g., 'Install Now', 'Next', 'Finish')"
                    }
                },
                "required": ["window_title", "button_text"]
            }
        },
        {
            "name": "automate_python_installer",
            "description": "Fully automate Python installer: launch, check 'Add to PATH', click Install. Hybrid approach using pywinauto + OCR fallback.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "installer_path": {
                        "type": "string",
                        "description": "Path to python installer .exe file"
                    },
                    "add_to_path": {
                        "type": "boolean",
                        "description": "Check 'Add Python to PATH' checkbox (default: true)",
                        "default": True
                    }
                },
                "required": ["installer_path"]
            }
        },
        {
            "name": "check_installation_progress",
            "description": "Check if installation is still running. Returns true if installer window is open.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title_contains": {
                        "type": "string",
                        "description": "Text in installer window title (default: 'Python')",
                        "default": "Python"
                    }
                },
                "required": []
            }
        }
    ]


# Function mapping
INSTALLER_AUTOMATION_FUNCTIONS = {
    "wait_for_installer_window": wait_for_installer_window,
    "find_and_click_checkbox_by_text": find_and_click_checkbox_by_text,
    "find_and_click_button_by_text": find_and_click_button_by_text,
    "automate_python_installer": automate_python_installer,
    "check_installation_progress": check_installation_progress
}
