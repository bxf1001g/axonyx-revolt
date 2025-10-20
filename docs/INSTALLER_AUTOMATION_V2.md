# Installer Automation V2 - Robust Edition

## What's New in V2?

### Problems Solved
1. **Multiple Window Matches** - V1 used regex matching that found multiple windows (e.g., Chrome + Python installer both match "Python")
2. **Exact Window Titles** - V2 returns and uses exact window titles to avoid ambiguity
3. **Multi-Strategy Checkbox Detection** - V2 tries 3 different approaches before giving up
4. **Known Position Fallback** - For Python installer, V2 knows common checkbox positions
5. **Detailed Step Results** - V2 returns complete information about what worked/failed

## Key Differences

### V1 (Old) vs V2 (New)

| Feature | V1 | V2 |
|---------|----|----|
| Window matching | Regex partial match | Priority-based exact match |
| Window focusing | Basic set_focus() | Explicit focus step |
| Checkbox detection | 1 strategy | 3 strategies + fallback |
| Button clicking | Text search only | Text + alternatives |
| Error reporting | Generic errors | Detailed step results |
| Multiple windows | Fails with error | Smart prioritization |

## Tool Usage

### 1. Wait for Installer Window (V2)
```python
wait_for_installer_window_v2(
    window_title_contains="Python",
    timeout=15
)

# Returns:
{
    "success": True,
    "found": True,
    "window_title": "Python 3.13.9 (64-bit) Setup",  # EXACT TITLE
    "exact_title": "Python 3.13.9 (64-bit) Setup",
    "all_matches": ["Python 3.13.9 (64-bit) Setup", "Python.org - Chrome"]
}
```

**Key Feature**: Returns EXACT window title to use in subsequent operations

### 2. Click Checkbox (V2)
```python
click_checkbox_in_window_v2(
    exact_window_title="Python 3.13.9 (64-bit) Setup",  # Use exact title from step 1
    checkbox_text="Add Python to PATH"
)

# Strategies tried (in order):
# 1. pywinauto checkbox control (exact match)
# 2. pywinauto checkbox control (partial match)
# 3. Find text element, click 25px to the left
# 4. Known Python installer positions (bottom-left area)

# Returns:
{
    "success": True,
    "message": "Checked: Add Python to PATH",
    "method": "text_offset_click",
    "position": {"x": 45, "y": 520}
}
```

### 3. Click Button (V2)
```python
click_button_in_window_v2(
    exact_window_title="Python 3.13.9 (64-bit) Setup",
    button_text="Install Now",
    button_alternatives=["Install", "Next", "Continue"]
)

# Tries each text (exact, then partial) before moving to next
```

### 4. Full Python Installer Automation (V2)
```python
automate_python_installer_v2(
    installer_path="C:\\Users\\...\\python-3.13.9-amd64.exe",
    add_to_path=True
)

# Returns detailed step results:
{
    "success": True,
    "message": "Installation started successfully",
    "exact_window_title": "Python 3.13.9 (64-bit) Setup",
    "steps": {
        "launch": {"success": True, "message": "Installer launched"},
        "wait_window": {"success": True, "found": True, "exact_title": "..."},
        "focus": {"success": True, "message": "Focused window: ..."},
        "checkbox": {"success": True, "method": "text_offset_click"},
        "install_button": {"success": True, "method": "pywinauto_exact"}
    }
}
```

### 5. Monitor Installation Progress (V2)
```python
check_installation_complete_v2(
    expected_window_title="Python 3.13.9 (64-bit) Setup",
    check_interval=3,
    max_checks=60
)

# Polls every 3 seconds, returns when window closes
```

## Multi-Strategy Checkbox Detection

### Strategy 1: PyWinAuto Checkbox Control
- Searches for CheckBox controls by exact title
- Tries partial match if exact fails
- Uses `get_toggle_state()` to check status

### Strategy 2: Text Element + Offset Click
- Finds Text elements containing checkbox label
- Calculates checkbox position (25px left of text)
- Uses pyautogui to click coordinates

### Strategy 3: Known Position Fallback
- For Python installer: tries common bottom-left positions
- Clicks multiple possible positions (60px, 80px, 100px from bottom)
- Uses installer window dimensions to calculate

### Strategy 4: OCR (not implemented in V2 yet)
- Can be added as Strategy 4
- Take screenshot, find text with Tesseract, click offset

## Complete Workflow Example

```python
# 1. Wait for download (if needed)
result = wait_for_download("python*.exe", timeout=120)
installer_path = result["file_path"]

# 2. Launch and automate installer
result = automate_python_installer_v2(
    installer_path=installer_path,
    add_to_path=True
)

# 3. Monitor until complete
exact_title = result["exact_window_title"]
check_installation_complete_v2(
    expected_window_title=exact_title,
    check_interval=3,
    max_checks=60
)
```

## When to Use V1 vs V2?

### Use V2 (Robust) When:
- ✅ Installing Python (or similar installers with known layout)
- ✅ Multiple windows might have similar titles
- ✅ Need detailed step-by-step results
- ✅ Checkbox detection is critical
- ✅ Previous automation failed

### Use V1 (Simple) When:
- ⚠️ Simple installers with unique window titles
- ⚠️ No checkbox detection needed
- ⚠️ Quick one-off installations
- ⚠️ Testing/development

## Debugging Failed Installations

### Check Step Results
```python
result = automate_python_installer_v2(...)
print(result["steps"])

# Shows exactly which step failed:
{
    "launch": {"success": True},
    "wait_window": {"success": True},
    "checkbox": {"error": "Could not find checkbox"},  # ← Failed here
    "install_button": {"success": True}
}
```

### Common Issues

**Multiple Windows Match:**
```
Error: "Found 2 windows matching 'Python'"
Solution: Close Chrome/other apps with "Python" in title before running installer
```

**Checkbox Not Found:**
```
Error: "Could not find checkbox for 'Add Python to PATH'"
Solution: V2 should handle this with fallback strategies, check if installer layout changed
```

**Button Click Failed:**
```
Error: "Could not find button in 'Python 3.13.9 Setup'"
Solution: Try alternative button texts, or check if installer requires admin rights
```

## Tool Count
**Total tools registered: 74**
- V1 tools: 5
- V2 tools: 5 (additional)
- All other tools: 64

## Migration from V1

No code changes needed! V2 tools have "_v2" suffix, so both versions coexist.

Agent will automatically prefer V2 tools when available due to better descriptions.

## Future Enhancements

1. **OCR Integration** - Add as Strategy 4 in checkbox detection
2. **Screenshot Debugging** - Capture screenshots when steps fail
3. **UAC Handling** - Detect and handle User Account Control prompts
4. **Progress Bar Reading** - Monitor actual installation percentage
5. **Generic Installer Support** - Extend patterns to work with any installer type
