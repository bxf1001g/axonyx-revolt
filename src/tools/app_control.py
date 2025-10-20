"""
Advanced Desktop Application Control using pywinauto
"""
from typing import Dict, List, Optional, Tuple
import time

try:
    from pywinauto import Application, Desktop
    from pywinauto.findwindows import ElementNotFoundError
    import pywinauto.keyboard as keyboard
    import pywinauto.mouse as mouse
except ImportError:
    Application = Desktop = None


def launch_and_control_app(exe_path: str, window_title: str = None, maximize: bool = False) -> Dict:
    """
    Launch an application and get control handle for further automation
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        # Launch application
        app = Application(backend="uia").start(exe_path)
        time.sleep(2)  # Wait for app to start
        
        # Find main window
        if window_title:
            window = app.window(title_re=f".*{window_title}.*")
        else:
            window = app.top_window()
        
        if maximize:
            window.maximize()
        
        # Get window info
        info = {
            "success": True,
            "window_title": window.window_text(),
            "handle": window.handle,
            "visible": window.is_visible(),
            "enabled": window.is_enabled()
        }
        
        return info
        
    except Exception as e:
        return {"error": str(e)}


def connect_to_app(window_title: str = None, process_id: int = None) -> Dict:
    """
    Connect to an already running application
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        if process_id:
            app = Application(backend="uia").connect(process=process_id)
        elif window_title:
            app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        else:
            return {"error": "Must provide window_title or process_id"}
        
        window = app.top_window()
        
        return {
            "success": True,
            "window_title": window.window_text(),
            "handle": window.handle,
            "process_id": window.process_id()
        }
        
    except Exception as e:
        return {"error": str(e)}


def click_button(window_title: str, button_name: str) -> Dict:
    """
    Click a button in an application window by name or automation ID
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        window = app.top_window()
        
        # Try to find button by name
        try:
            button = window.child_window(title=button_name, control_type="Button")
        except:
            # Try by automation ID
            button = window.child_window(auto_id=button_name, control_type="Button")
        
        button.click()
        
        return {
            "success": True,
            "message": f"Clicked button: {button_name}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def set_text_field(window_title: str, field_name: str, text: str) -> Dict:
    """
    Set text in a text field/input box
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        window = app.top_window()
        
        # Find edit control
        try:
            edit = window.child_window(title=field_name, control_type="Edit")
        except:
            edit = window.child_window(auto_id=field_name, control_type="Edit")
        
        edit.set_edit_text(text)
        
        return {
            "success": True,
            "message": f"Set text in {field_name}: {text}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def select_menu_item(window_title: str, menu_path: str) -> Dict:
    """
    Select a menu item (e.g., "File->Open", "Edit->Paste")
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        window = app.top_window()
        
        # Parse menu path
        menu_items = menu_path.split("->")
        
        # Navigate menu
        window.menu_select(" -> ".join(menu_items))
        
        return {
            "success": True,
            "message": f"Selected menu: {menu_path}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def get_window_controls(window_title: str) -> Dict:
    """
    List all controls/elements in a window for inspection
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        window = app.top_window()
        
        # Print control identifiers
        controls = []
        
        def traverse_controls(element, depth=0):
            try:
                controls.append({
                    "type": element.element_info.control_type,
                    "name": element.window_text(),
                    "automation_id": element.element_info.automation_id,
                    "depth": depth
                })
                
                for child in element.children():
                    traverse_controls(child, depth + 1)
            except:
                pass
        
        traverse_controls(window)
        
        return {
            "success": True,
            "controls": controls[:50],  # Limit to first 50
            "total": len(controls)
        }
        
    except Exception as e:
        return {"error": str(e)}


def close_app_window(window_title: str, force: bool = False) -> Dict:
    """
    Close an application window gracefully or forcefully
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        window = app.top_window()
        
        if force:
            window.close()  # Force close
        else:
            # Try graceful close (Alt+F4)
            window.type_keys("%{F4}")
        
        return {
            "success": True,
            "message": f"Closed window: {window_title}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def minimize_maximize_window(window_title: str, action: str) -> Dict:
    """
    Minimize, maximize, or restore a window
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        app = Application(backend="uia").connect(title_re=f".*{window_title}.*")
        window = app.top_window()
        
        if action.lower() == "minimize":
            window.minimize()
        elif action.lower() == "maximize":
            window.maximize()
        elif action.lower() == "restore":
            window.restore()
        else:
            return {"error": "Invalid action. Use: minimize, maximize, restore"}
        
        return {
            "success": True,
            "message": f"Window {action}d: {window_title}"
        }
        
    except Exception as e:
        return {"error": str(e)}


def wait_for_window(window_title: str, timeout: int = 30) -> Dict:
    """
    Wait for a window to appear (useful after launching apps)
    """
    if not Application:
        return {"error": "pywinauto not installed"}
    
    try:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                desktop = Desktop(backend="uia")
                windows = desktop.windows()
                
                for win in windows:
                    if window_title.lower() in win.window_text().lower():
                        return {
                            "success": True,
                            "message": f"Window found: {win.window_text()}",
                            "handle": win.handle
                        }
            except:
                pass
            
            time.sleep(0.5)
        
        return {"error": f"Window not found after {timeout} seconds"}
        
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_app_control_tools() -> List[Dict]:
    """Get application control tool definitions"""
    return [
        {
            "name": "launch_and_control_app",
            "description": "Launch an application and get control for automation. Returns window handle for further operations.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "exe_path": {
                        "type": "string",
                        "description": "Full path to executable or command name (e.g., 'notepad.exe', 'C:/Program Files/App/app.exe')"
                    },
                    "window_title": {
                        "type": "string",
                        "description": "Optional: Expected window title to find"
                    },
                    "maximize": {
                        "type": "boolean",
                        "description": "Whether to maximize the window on launch"
                    }
                },
                "required": ["exe_path"]
            }
        },
        {
            "name": "connect_to_app",
            "description": "Connect to an already running application for control",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title to search for"
                    },
                    "process_id": {
                        "type": "integer",
                        "description": "Process ID to connect to"
                    }
                }
            }
        },
        {
            "name": "click_button",
            "description": "Click a button in an application window by its name or automation ID",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Title of the window containing the button"
                    },
                    "button_name": {
                        "type": "string",
                        "description": "Name or automation ID of the button"
                    }
                },
                "required": ["window_title", "button_name"]
            }
        },
        {
            "name": "set_text_field",
            "description": "Set text in an input field/textbox in an application",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title"
                    },
                    "field_name": {
                        "type": "string",
                        "description": "Name or ID of the text field"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to enter"
                    }
                },
                "required": ["window_title", "field_name", "text"]
            }
        },
        {
            "name": "select_menu_item",
            "description": "Select a menu item from application menu bar (e.g., 'File->Open')",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title"
                    },
                    "menu_path": {
                        "type": "string",
                        "description": "Menu path separated by '->' (e.g., 'File->Save As')"
                    }
                },
                "required": ["window_title", "menu_path"]
            }
        },
        {
            "name": "get_window_controls",
            "description": "Inspect a window to list all its controls/elements for automation",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title to inspect"
                    }
                },
                "required": ["window_title"]
            }
        },
        {
            "name": "close_app_window",
            "description": "Close an application window gracefully or forcefully",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title to close"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force close without saving (default: false)"
                    }
                },
                "required": ["window_title"]
            }
        },
        {
            "name": "minimize_maximize_window",
            "description": "Minimize, maximize, or restore a window",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title"
                    },
                    "action": {
                        "type": "string",
                        "description": "Action: 'minimize', 'maximize', or 'restore'"
                    }
                },
                "required": ["window_title", "action"]
            }
        },
        {
            "name": "wait_for_window",
            "description": "Wait for a window to appear (useful after launching applications)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "window_title": {
                        "type": "string",
                        "description": "Window title to wait for"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default: 30)"
                    }
                },
                "required": ["window_title"]
            }
        }
    ]


# Map tool names to functions
APP_CONTROL_FUNCTIONS = {
    "launch_and_control_app": launch_and_control_app,
    "connect_to_app": connect_to_app,
    "click_button": click_button,
    "set_text_field": set_text_field,
    "select_menu_item": select_menu_item,
    "get_window_controls": get_window_controls,
    "close_app_window": close_app_window,
    "minimize_maximize_window": minimize_maximize_window,
    "wait_for_window": wait_for_window
}
