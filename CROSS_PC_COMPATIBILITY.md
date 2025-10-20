# Cross-PC Compatibility Guide

## Issue: Hardcoded User Paths

When code has paths like `C:\Users\Jemisha Roy JXT\Desktop`, it breaks on other PCs with different usernames.

## Solutions Implemented

### 1. ✅ Dynamic Desktop Path (OneDrive-Aware)

**File: `screen_reader.py`**

The `take_screenshot()` function now:
- Reads actual Desktop path from Windows Registry
- Handles OneDrive Desktop redirection automatically
- Works on ANY Windows PC regardless of username

**How it works:**
```python
import winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
    r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
# Expands %USERPROFILE%\OneDrive\Desktop or %USERPROFILE%\Desktop
desktop_path = os.path.expandvars(desktop_path)
```

### 2. ✅ Environment Variable Expansion

All path operations use:
- `Path.home()` → Gets current user's home directory
- `os.path.expandvars()` → Expands `%USERPROFILE%` and other variables
- `Path.expanduser()` → Expands `~` to home directory

### 3. ✅ Wait for Page Load

**File: `chrome_launcher.py`**

Added `wait_seconds` parameter (default: 3 seconds):
```python
def open_chrome_with_profile(url: str = None, wait_seconds: int = 3):
    subprocess.Popen([chrome_exe, url])
    if wait_seconds > 0:
        time.sleep(wait_seconds)  # Wait for page to load
```

**Usage:**
- Default: Waits 3 seconds (good for most pages)
- Slow connection: Increase to 5-10 seconds
- Fast page: Can reduce to 1-2 seconds

## Cross-PC Compatibility Checklist

### ✅ Desktop Path
- Uses Windows Registry to find actual Desktop
- Handles OneDrive redirection
- Works on any username

### ✅ User Home Directory
- All paths use `Path.home()` 
- Never hardcoded `C:\Users\SomeUser`

### ✅ Documents, Downloads, Pictures
- All special folders use proper resolution:
```python
# BAD (hardcoded):
path = "C:\\Users\\Jemisha Roy JXT\\Documents\\file.txt"

# GOOD (dynamic):
path = Path.home() / "Documents" / "file.txt"
```

### ✅ Chrome Installation
- Checks both Program Files locations
- Works on 32-bit and 64-bit Windows
- No hardcoded paths

### ✅ Tesseract OCR
- Checks multiple standard installation paths
- Fallback to registry/environment variables
- Graceful error if not installed

## Testing on Different PCs

### What to Test:

1. **Screenshot saving**
   ```
   Take a screenshot and save to Desktop/test.png
   ```
   Should appear on Desktop regardless of username or OneDrive

2. **File operations**
   ```
   Create a file at Documents/test.txt with content "Hello"
   ```
   Should work on any PC

3. **Chrome opening**
   ```
   Open Chrome and go to google.com
   ```
   Should find Chrome regardless of installation location

4. **Page load timing**
   ```
   Open Anthropic billing page and wait 5 seconds, then take screenshot
   ```
   Should wait for full page load

## Best Practices for Adding New Tools

### ✅ DO:
```python
from pathlib import Path
import os

# Use Path.home()
desktop = Path.home() / "Desktop"

# Use environment variables
user_folder = os.path.expandvars("%USERPROFILE%")

# Use expanduser
path = Path("~/Documents/file.txt").expanduser()

# Check registry for special folders
import winreg
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
    r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
desktop = winreg.QueryValueEx(key, "Desktop")[0]
```

### ❌ DON'T:
```python
# Hardcoded username
path = "C:\\Users\\Jemisha Roy JXT\\Desktop\\file.txt"

# Assumed path
path = "C:\\Users\\Public\\Documents\\file.txt"

# Fixed drive letter
path = "D:\\MyFiles\\file.txt"
```

## Environment Variables Reference

Common Windows environment variables that work across PCs:
- `%USERPROFILE%` → `C:\Users\CurrentUser`
- `%APPDATA%` → `C:\Users\CurrentUser\AppData\Roaming`
- `%LOCALAPPDATA%` → `C:\Users\CurrentUser\AppData\Local`
- `%TEMP%` → Temporary files directory
- `%PUBLIC%` → `C:\Users\Public`

## Windows Registry Special Folders

Located at: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`

Available folders:
- `Desktop` → User's desktop (handles OneDrive)
- `Personal` → Documents folder
- `My Pictures` → Pictures folder
- `{374DE290-123F-4565-9164-39C4925E467B}` → Downloads
- `AppData` → Roaming AppData

## Summary

✅ **All paths are now dynamic and cross-PC compatible!**

The agent will work on:
- Any Windows PC
- Any username (including spaces, special characters)
- OneDrive Desktop redirection
- Different drive configurations
- 32-bit or 64-bit Windows
- Different language versions of Windows

Just copy the project folder to another PC, install dependencies, add API key, and it works!
