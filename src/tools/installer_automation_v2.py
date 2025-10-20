"""
Installer Automation V2 - More Robust with Better Window Handling
"""

import time
from typing import Dict
from pathlib import Path
import subprocess
from pywinauto import Desktop
import pyautogui


def wait_for_installer_window_v2(window_title_contains: str, timeout: int = 15) -> Dict:
    """
    Wait for installer window to appear - returns exact title to avoid multiple matches
    
    Args:
        window_title_contains: Partial text to match in window title
        timeout: Maximum seconds to wait
    
    Returns:
        Dict with exact window title or error
    """
    try:
        desktop = Desktop(backend="uia")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            windows = desktop.windows()
            
            # Find windows matching criteria, prefer "Setup" windows
            matching_windows = []
            for window in windows:
                try:
                    title = window.window_text()
                    if window_title_contains.lower() in title.lower():
                        # Prioritize setup/installer windows
                        priority = 0
                        if "setup" in title.lower():
                            priority += 10
                        if any(char.isdigit() for char in title):  # Has version number
                            priority += 5
                        if "chrome" in title.lower() or "browser" in title.lower():
                            priority -= 20  # Deprioritize browser windows
                            
                        matching_windows.append((priority, title, window))
                except:
                    pass
            
            if matching_windows:
                # Sort by priority and return highest
                matching_windows.sort(reverse=True, key=lambda x: x[0])
                best_match = matching_windows[0]
                
                return {
                    "success": True,
                    "found": True,
                    "window_title": best_match[1],
                    "exact_title": best_match[1],
                    "message": f"Found installer: {best_match[1]}",
                    "all_matches": [m[1] for m in matching_windows] if len(matching_windows) > 1 else None
                }
            
            time.sleep(1)
        
        return {
            "success": False,
            "found": False,
            "message": f"No installer window found after {timeout}s"
        }
    except Exception as e:
        return {"error": f"Failed to wait for window: {str(e)}"}


def focus_window_by_exact_title(exact_title: str) -> Dict:
    """
    Focus a specific window by exact title
    
    Args:
        exact_title: Exact window title
    
    Returns:
        Dict with success status
    """
    try:
        desktop = Desktop(backend="uia")
        app = desktop.window(title=exact_title, top_level_only=True)
        app.set_focus()
        time.sleep(0.5)
        
        return {
            "success": True,
            "message": f"Focused window: {exact_title}"
        }
    except Exception as e:
        return {"error": f"Failed to focus window: {str(e)}"}


def click_checkbox_in_window_v2(exact_window_title: str, checkbox_text: str) -> Dict:
    """
    Click checkbox by text - robust multi-strategy approach
    
    Strategy:
    1. Try pywinauto checkbox control
    2. Try pywinauto text element + coordinate offset
    3. Try screen coordinates with pyautogui
    
    Args:
        exact_window_title: Exact window title from wait_for_installer_window_v2
        checkbox_text: Text to search for (e.g., "Add Python to PATH")
    
    Returns:
        Dict with success status and method used
    """
    try:
        desktop = Desktop(backend="uia")
        app = desktop.window(title=exact_window_title, top_level_only=True)
        app.set_focus()
        time.sleep(0.3)
        
        # STRATEGY 1: Try to find checkbox control directly
        try:
            # Try exact match
            checkbox = app.child_window(title=checkbox_text, control_type="CheckBox")
            if checkbox.exists(timeout=2):
                is_checked = checkbox.get_toggle_state()
                if is_checked == 0:  # Not checked
                    checkbox.click_input()
                    return {
                        "success": True,
                        "message": f"Checked: {checkbox_text}",
                        "method": "pywinauto_checkbox_exact"
                    }
                else:
                    return {
                        "success": True,
                        "message": f"Already checked: {checkbox_text}",
                        "method": "pywinauto_checkbox_exact"
                    }
        except:
            pass
        
        # Try partial match
        try:
            checkboxes = app.descendants(control_type="CheckBox")
            for cb in checkboxes:
                cb_text = cb.window_text()
                if checkbox_text.lower() in cb_text.lower() or cb_text.lower() in checkbox_text.lower():
                    is_checked = cb.get_toggle_state()
                    if is_checked == 0:
                        cb.click_input()
                        return {
                            "success": True,
                            "message": f"Checked: {cb_text}",
                            "method": "pywinauto_checkbox_partial"
                        }
                    else:
                        return {
                            "success": True,
                            "message": f"Already checked: {cb_text}",
                            "method": "pywinauto_checkbox_partial"
                        }
        except:
            pass
        
        # STRATEGY 2: Find text and click at offset
        try:
            # Get all text elements
            texts = app.descendants(control_type="Text")
            for text_elem in texts:
                text_val = text_elem.window_text()
                if checkbox_text.lower() in text_val.lower():
                    # Found the text, get its rectangle
                    rect = text_elem.rectangle()
                    # Checkbox is usually 20-30 pixels to the left of text
                    checkbox_x = rect.left - 25
                    checkbox_y = rect.top + (rect.height() // 2)
                    
                    pyautogui.click(checkbox_x, checkbox_y)
                    return {
                        "success": True,
                        "message": f"Clicked checkbox near text: {text_val}",
                        "method": "text_offset_click",
                        "position": {"x": checkbox_x, "y": checkbox_y}
                    }
        except Exception as e:
            pass
        
        # STRATEGY 3: Try known positions for Python installer
        if "python" in exact_window_title.lower():
            try:
                # Python installer checkbox is typically in bottom-left area
                rect = app.rectangle()
                
                # Try bottom-left area (where "Add to PATH" usually is)
                possible_positions = [
                    (rect.left + 30, rect.bottom - 60),  # Bottom-left
                    (rect.left + 30, rect.bottom - 80),
                    (rect.left + 30, rect.bottom - 100),
                ]
                
                for x, y in possible_positions:
                    pyautogui.click(x, y)
                    time.sleep(0.2)
                    
                return {
                    "success": True,
                    "message": "Clicked checkbox at common Python installer position",
                    "method": "known_position",
                    "note": "Using typical Python installer layout"
                }
            except:
                pass
        
        return {
            "error": f"Could not find checkbox for '{checkbox_text}' in window '{exact_window_title}'",
            "strategies_tried": ["pywinauto_exact", "pywinauto_partial", "text_offset", "known_position"]
        }
        
    except Exception as e:
        return {"error": f"Failed to click checkbox: {str(e)}"}


def click_button_in_window_v2(exact_window_title: str, button_text: str, button_alternatives: list = None) -> Dict:
    """
    Click button by text - tries exact match then alternatives
    
    Args:
        exact_window_title: Exact window title
        button_text: Primary button text to find
        button_alternatives: List of alternative button texts to try
    
    Returns:
        Dict with success status
    """
    try:
        desktop = Desktop(backend="uia")
        app = desktop.window(title=exact_window_title, top_level_only=True)
        app.set_focus()
        time.sleep(0.3)
        
        # Build list of texts to try
        texts_to_try = [button_text]
        if button_alternatives:
            texts_to_try.extend(button_alternatives)
        
        for text in texts_to_try:
            try:
                # Try exact button match
                button = app.child_window(title=text, control_type="Button")
                if button.exists(timeout=2):
                    button.click_input()
                    return {
                        "success": True,
                        "message": f"Clicked button: {text}",
                        "method": "pywinauto_exact"
                    }
            except:
                pass
            
            try:
                # Try partial match
                buttons = app.descendants(control_type="Button")
                for btn in buttons:
                    btn_text = btn.window_text()
                    if text.lower() in btn_text.lower():
                        btn.click_input()
                        return {
                            "success": True,
                            "message": f"Clicked button: {btn_text}",
                            "method": "pywinauto_partial"
                        }
            except:
                pass
        
        return {
            "error": f"Could not find button in '{exact_window_title}'",
            "tried": texts_to_try
        }
        
    except Exception as e:
        return {"error": f"Failed to click button: {str(e)}"}


def automate_python_installer_v2(installer_path: str, add_to_path: bool = True) -> Dict:
    """
    Automate Python installer - ROBUST VERSION
    
    Args:
        installer_path: Full path to python installer exe
        add_to_path: Whether to check "Add Python to PATH"
    
    Returns:
        Dict with detailed results of each step
    """
    try:
        installer_path = Path(installer_path).expanduser()
        if not installer_path.exists():
            return {"error": f"Installer not found: {installer_path}"}
        
        results = {
            "success": False,
            "steps": {}
        }
        
        # STEP 1: Launch installer
        try:
            subprocess.Popen([str(installer_path)])
            results["steps"]["launch"] = {"success": True, "message": "Installer launched"}
        except Exception as e:
            return {"error": f"Failed to launch installer: {str(e)}"}
        
        # STEP 2: Wait for installer window
        time.sleep(2)
        wait_result = wait_for_installer_window_v2("Python", timeout=15)
        results["steps"]["wait_window"] = wait_result
        
        if not wait_result.get("found"):
            return {"error": "Installer window did not appear", "results": results}
        
        exact_title = wait_result["exact_title"]
        results["exact_window_title"] = exact_title
        
        # STEP 3: Focus the installer window
        time.sleep(1)
        focus_result = focus_window_by_exact_title(exact_title)
        results["steps"]["focus"] = focus_result
        
        # STEP 4: Check "Add to PATH" checkbox if requested
        if add_to_path:
            time.sleep(0.5)
            checkbox_result = click_checkbox_in_window_v2(exact_title, "Add Python to PATH")
            results["steps"]["checkbox"] = checkbox_result
        
        # STEP 5: Click Install Now button
        time.sleep(0.5)
        button_result = click_button_in_window_v2(
            exact_title, 
            "Install Now",
            button_alternatives=["Install", "Next", "Continue"]
        )
        results["steps"]["install_button"] = button_result
        
        # Determine overall success
        checkbox_ok = results["steps"].get("checkbox", {}).get("success", True)
        button_ok = results["steps"]["install_button"].get("success", False)
        
        results["success"] = button_ok
        results["message"] = "Installation started successfully" if button_ok else "Failed to start installation"
        
        return results
        
    except Exception as e:
        return {"error": f"Automation failed: {str(e)}"}


def check_installation_complete_v2(expected_window_title: str, check_interval: int = 3, max_checks: int = 60) -> Dict:
    """
    Monitor installation progress by checking if window still exists
    
    Args:
        expected_window_title: Exact installer window title
        check_interval: Seconds between checks
        max_checks: Maximum number of checks before giving up
    
    Returns:
        Dict with completion status
    """
    try:
        desktop = Desktop(backend="uia")
        checks_done = 0
        
        while checks_done < max_checks:
            try:
                # Check if installer window still exists
                app = desktop.window(title=expected_window_title, top_level_only=True)
                if app.exists(timeout=1):
                    checks_done += 1
                    time.sleep(check_interval)
                else:
                    return {
                        "success": True,
                        "complete": True,
                        "message": "Installation completed (window closed)",
                        "checks": checks_done
                    }
            except:
                # Window not found - installation complete
                return {
                    "success": True,
                    "complete": True,
                    "message": "Installation completed (window closed)",
                    "checks": checks_done
                }
        
        return {
            "success": False,
            "complete": False,
            "message": f"Installation still running after {checks_done * check_interval} seconds",
            "checks": checks_done
        }
        
    except Exception as e:
        return {"error": f"Failed to check installation: {str(e)}"}


# Tool schemas for Claude
def get_installer_automation_v2_tools():
    """Return tool schemas for robust installer automation"""
    return [
        {
            "name": "wait_for_installer_window_v2",
            "description": "Wait for installer window to appear and get its EXACT title (avoids multiple window matches). Returns exact window title to use in subsequent operations.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title_contains": {
                        "type": "string",
                        "description": "Partial text that should be in the window title (e.g., 'Python', 'Setup', 'Installer')"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum seconds to wait for window to appear",
                        "default": 15
                    }
                },
                "required": ["window_title_contains"]
            }
        },
        {
            "name": "click_checkbox_in_window_v2",
            "description": "Click a checkbox in an installer window using exact window title. Uses multi-strategy approach: pywinauto controls → text position offset → known installer positions. Much more robust than v1.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "exact_window_title": {
                        "type": "string",
                        "description": "EXACT window title from wait_for_installer_window_v2 (e.g., 'Python 3.13.9 (64-bit) Setup')"
                    },
                    "checkbox_text": {
                        "type": "string",
                        "description": "Text near the checkbox (e.g., 'Add Python to PATH', 'I accept', 'Create shortcut')"
                    }
                },
                "required": ["exact_window_title", "checkbox_text"]
            }
        },
        {
            "name": "click_button_in_window_v2",
            "description": "Click a button in installer window by text. Tries exact match, then alternatives. Uses exact window title to avoid multiple matches.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "exact_window_title": {
                        "type": "string",
                        "description": "EXACT window title from wait_for_installer_window_v2"
                    },
                    "button_text": {
                        "type": "string",
                        "description": "Primary button text (e.g., 'Install Now', 'Next', 'Finish')"
                    },
                    "button_alternatives": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Alternative button texts to try if primary not found",
                        "default": []
                    }
                },
                "required": ["exact_window_title", "button_text"]
            }
        },
        {
            "name": "automate_python_installer_v2",
            "description": "ROBUST Python installer automation - uses exact window titles and multi-strategy checkbox/button detection. Launches installer, checks 'Add to PATH', clicks Install Now. Returns detailed step-by-step results.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "installer_path": {
                        "type": "string",
                        "description": "Full path to Python installer .exe file"
                    },
                    "add_to_path": {
                        "type": "boolean",
                        "description": "Whether to check the 'Add Python to PATH' checkbox",
                        "default": True
                    }
                },
                "required": ["installer_path"]
            }
        },
        {
            "name": "check_installation_complete_v2",
            "description": "Monitor installation progress by checking if installer window still exists. Returns when window closes (installation complete).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expected_window_title": {
                        "type": "string",
                        "description": "Exact installer window title to monitor"
                    },
                    "check_interval": {
                        "type": "integer",
                        "description": "Seconds between checks",
                        "default": 3
                    },
                    "max_checks": {
                        "type": "integer",
                        "description": "Maximum checks before giving up",
                        "default": 60
                    }
                },
                "required": ["expected_window_title"]
            }
        }
    ]


# Function mapping for agent
INSTALLER_AUTOMATION_V2_FUNCTIONS = {
    "wait_for_installer_window_v2": wait_for_installer_window_v2,
    "click_checkbox_in_window_v2": click_checkbox_in_window_v2,
    "click_button_in_window_v2": click_button_in_window_v2,
    "automate_python_installer_v2": automate_python_installer_v2,
    "check_installation_complete_v2": check_installation_complete_v2
}
