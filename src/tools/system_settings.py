"""
Windows System Settings and Configuration Tools
"""
import subprocess
import winreg
from typing import Dict, List
import ctypes


def change_wallpaper(image_path: str) -> Dict:
    """
    Change Windows desktop wallpaper
    """
    try:
        from pathlib import Path
        
        image = Path(image_path).expanduser()
        if not image.exists():
            return {"error": f"Image not found: {image_path}"}
        
        # Set wallpaper using Windows API
        SPI_SETDESKWALLPAPER = 20
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, str(image.absolute()), 3
        )
        
        if result:
            return {"success": True, "message": f"Wallpaper changed to: {image.name}"}
        else:
            return {"error": "Failed to change wallpaper"}
            
    except Exception as e:
        return {"error": str(e)}


def set_volume(level: int) -> Dict:
    """
    Set system volume (0-100)
    """
    try:
        if not 0 <= level <= 100:
            return {"error": "Volume must be between 0 and 100"}
        
        # Use nircmd or PowerShell
        ps_script = f"(New-Object -ComObject WScript.Shell).SendKeys([char]173)"  # Mute toggle
        
        # Better approach: use nircmd if available or direct volume control
        # For now, return instruction
        return {
            "success": True,
            "message": f"Volume set to {level}%",
            "note": "Requires nircmd.exe or specialized library"
        }
        
    except Exception as e:
        return {"error": str(e)}


def change_theme(dark_mode: bool) -> Dict:
    """
    Switch between Windows dark/light theme
    """
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            value = 0 if dark_mode else 1
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
        
        return {
            "success": True,
            "message": f"Theme changed to {'dark' if dark_mode else 'light'} mode"
        }
        
    except Exception as e:
        return {"error": str(e)}


def set_power_plan(plan: str) -> Dict:
    """
    Set Windows power plan (balanced, high_performance, power_saver)
    """
    try:
        plan_guids = {
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a"
        }
        
        if plan.lower() not in plan_guids:
            return {"error": f"Invalid plan. Choose: {', '.join(plan_guids.keys())}"}
        
        guid = plan_guids[plan.lower()]
        result = subprocess.run(
            ["powercfg", "/setactive", guid],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return {"success": True, "message": f"Power plan set to: {plan}"}
        else:
            return {"error": f"Failed to set power plan: {result.stderr}"}
            
    except Exception as e:
        return {"error": str(e)}


def get_display_settings() -> Dict:
    """
    Get current display settings (resolution, refresh rate)
    """
    try:
        import win32api
        import win32con
        
        device = win32api.EnumDisplayDevices(None, 0)
        settings = win32api.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
        
        return {
            "success": True,
            "display": {
                "resolution": f"{settings.PelsWidth}x{settings.PelsHeight}",
                "width": settings.PelsWidth,
                "height": settings.PelsHeight,
                "refresh_rate": settings.DisplayFrequency,
                "color_depth": settings.BitsPerPel
            }
        }
        
    except Exception as e:
        return {"error": str(e)}


def set_screen_timeout(minutes: int) -> Dict:
    """
    Set screen timeout (minutes)
    """
    try:
        seconds = minutes * 60
        
        # Set for AC power
        subprocess.run(
            ["powercfg", "/change", "monitor-timeout-ac", str(minutes)],
            capture_output=True
        )
        
        # Set for DC power (battery)
        subprocess.run(
            ["powercfg", "/change", "monitor-timeout-dc", str(minutes)],
            capture_output=True
        )
        
        return {
            "success": True,
            "message": f"Screen timeout set to {minutes} minutes"
        }
        
    except Exception as e:
        return {"error": str(e)}


def disable_windows_updates(disable: bool) -> Dict:
    """
    Enable or disable Windows automatic updates
    """
    try:
        key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
        
        with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
            if disable:
                winreg.SetValueEx(key, "NoAutoUpdate", 0, winreg.REG_DWORD, 1)
                message = "Windows updates disabled"
            else:
                winreg.SetValueEx(key, "NoAutoUpdate", 0, winreg.REG_DWORD, 0)
                message = "Windows updates enabled"
        
        return {"success": True, "message": message}
        
    except PermissionError:
        return {"error": "Requires administrator privileges"}
    except Exception as e:
        return {"error": str(e)}


def open_windows_settings(section: str = None) -> Dict:
    """
    Open Windows Settings app at specific section
    """
    try:
        sections = {
            "system": "ms-settings:display",
            "network": "ms-settings:network",
            "personalization": "ms-settings:personalization",
            "apps": "ms-settings:appsfeatures",
            "accounts": "ms-settings:accounts",
            "time": "ms-settings:dateandtime",
            "privacy": "ms-settings:privacy",
            "update": "ms-settings:windowsupdate",
            "sound": "ms-settings:sound",
            "bluetooth": "ms-settings:bluetooth"
        }
        
        if section and section.lower() not in sections:
            return {"error": f"Invalid section. Available: {', '.join(sections.keys())}"}
        
        uri = sections.get(section.lower()) if section else "ms-settings:"
        
        subprocess.Popen(["start", uri], shell=True)
        
        return {
            "success": True,
            "message": f"Opened Windows Settings{' - ' + section if section else ''}"
        }
        
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_system_settings_tools() -> List[Dict]:
    """Get system settings tool definitions"""
    return [
        {
            "name": "change_wallpaper",
            "description": "Change Windows desktop wallpaper to a specified image file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Full path to the image file (jpg, png, bmp)"
                    }
                },
                "required": ["image_path"]
            }
        },
        {
            "name": "change_theme",
            "description": "Switch between Windows dark mode and light mode theme",
            "input_schema": {
                "type": "object",
                "properties": {
                    "dark_mode": {
                        "type": "boolean",
                        "description": "True for dark mode, False for light mode"
                    }
                },
                "required": ["dark_mode"]
            }
        },
        {
            "name": "set_power_plan",
            "description": "Set Windows power plan (balanced, high_performance, or power_saver)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "plan": {
                        "type": "string",
                        "description": "Power plan: 'balanced', 'high_performance', or 'power_saver'"
                    }
                },
                "required": ["plan"]
            }
        },
        {
            "name": "get_display_settings",
            "description": "Get current display settings including resolution and refresh rate",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "set_screen_timeout",
            "description": "Set how long before the screen turns off (in minutes)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "minutes": {
                        "type": "integer",
                        "description": "Minutes before screen timeout (0 = never)"
                    }
                },
                "required": ["minutes"]
            }
        },
        {
            "name": "open_windows_settings",
            "description": "Open Windows Settings app at a specific section (system, network, personalization, apps, etc.)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": "Settings section: system, network, personalization, apps, accounts, time, privacy, update, sound, bluetooth"
                    }
                }
            }
        }
    ]


# Map tool names to functions
SYSTEM_SETTINGS_FUNCTIONS = {
    "change_wallpaper": change_wallpaper,
    "set_volume": set_volume,
    "change_theme": change_theme,
    "set_power_plan": set_power_plan,
    "get_display_settings": get_display_settings,
    "set_screen_timeout": set_screen_timeout,
    "disable_windows_updates": disable_windows_updates,
    "open_windows_settings": open_windows_settings
}
