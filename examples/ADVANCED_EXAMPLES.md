# Advanced Windows Automation Examples

## Application Installation & Management

### Install Applications
```python
# Install from downloaded installer
"Install 7-Zip from C:/Downloads/7z-installer.exe silently"

# Check if app is installed
"Is Google Chrome installed on this system?"

# List all installed applications
"Show me all installed applications"

# Uninstall an application
"Uninstall Adobe Reader"

# Download and install (if you have direct URL)
"Download and install VLC from https://example.com/vlc.exe"
```

### Complex Installation Workflows
```python
# Check, install if missing, then launch
"Check if Notepad++ is installed. If not, install it from C:/Downloads/npp-installer.exe, then launch it"

# Batch install multiple apps
"Install these applications from my Downloads folder: setup1.exe, setup2.msi, setup3.exe"

# Verify installation
"After installing, verify that the app 'VideoEditor' appears in installed programs"
```

## Desktop Application Control (pywinauto)

### Launch and Control Applications
```python
# Launch and maximize
"Launch Calculator and maximize the window"

# Launch notepad and automate input
"Launch notepad.exe, wait for window to appear, then type 'Meeting Notes' and press Enter twice"

# Connect to running app
"Connect to the Chrome window and inspect available controls"
```

### Advanced UI Automation
```python
# Menu navigation
"In Notepad window, select File->Save As"

# Button clicking
"In the 'Save As' dialog, click the 'Save' button"

# Form filling
"In the 'Settings' window, set the 'Username' field to 'JohnDoe' and click 'Apply'"

# Inspect controls
"Show me all buttons and text fields in the Calculator window"
```

### Window Management
```python
# Minimize/Maximize
"Minimize all Chrome windows"
"Maximize the Visual Studio Code window"

# Wait for windows
"Launch installer.exe and wait for the 'Setup' window to appear"

# Close windows
"Close all Notepad windows without saving"

# Multi-window workflow
"Open Notepad, maximize it, type 'Hello', then open Calculator and minimize Notepad"
```

## System Settings & Configuration

### Theme & Appearance
```python
# Dark mode
"Switch to dark mode"
"Enable Windows dark theme"

# Wallpaper
"Change my wallpaper to C:/Pictures/nature.jpg"

# Display settings
"What's my current screen resolution?"
```

### Power Management
```python
# Power plans
"Set power plan to high performance"
"Switch to balanced power mode"

# Screen timeout
"Set screen timeout to 15 minutes"
"Never turn off my display"
```

### System Configuration
```python
# Open settings
"Open Windows Settings at the Network section"
"Open Bluetooth settings"

# Display info
"Show me my display resolution and refresh rate"
```

## Real-World Automation Scenarios

### Developer Setup
```python
"""
Set up my development environment:
1. Check if Visual Studio Code is installed
2. If not, install it from C:/Downloads/VSCode-Setup.exe
3. Check if Git is installed
4. Launch VS Code
5. Switch to dark mode
6. Set power plan to high performance
"""
```

### Application Deployment
```python
"""
Deploy application to test machine:
1. Copy installer from Desktop to C:/Temp
2. Run installer silently
3. Wait for installation to complete
4. Verify app appears in installed programs
5. Launch the application
6. Maximize the window
"""
```

### System Maintenance
```python
"""
Perform system cleanup:
1. List all installed applications
2. Check disk space on C: drive
3. Show CPU and memory usage
4. List top 10 processes by memory
5. Create a report file with findings
"""
```

### Automated Testing Workflow
```python
"""
Test application installation:
1. Install app from C:/Test/app-setup.exe
2. Wait for 'AppName' window to appear
3. Click 'Next' button 3 times
4. Click 'Finish' button
5. Verify app window opens
6. Close the app
7. Uninstall the app
"""
```

### Conference Call Setup
```python
"""
Prepare for meeting:
1. Close all unnecessary applications
2. Launch Teams
3. Maximize Teams window
4. Set power plan to high performance
5. Set screen timeout to never
6. Open Notepad for notes
"""
```

### Software Update Workflow
```python
"""
Update applications:
1. List all installed applications
2. Check if Adobe Reader is installed
3. If version is old, uninstall it
4. Install new version from C:/Downloads/reader-new.exe
5. Verify installation
6. Launch to confirm it works
"""
```

## Advanced pywinauto Techniques

### Working with Dialogs
```python
# Handle file dialogs
"In Notepad, select File->Open, then in the file dialog set filename to 'test.txt' and click Open"

# Handle confirmations
"Click 'Yes' in the confirmation dialog"

# Navigate complex UIs
"In the Settings window, click 'Advanced' tab, then enable 'Developer Mode' checkbox"
```

### Form Automation
```python
"""
Fill out registration form in MyApp:
1. Connect to 'Registration' window
2. Set 'First Name' field to 'John'
3. Set 'Last Name' field to 'Doe'
4. Set 'Email' field to 'john@example.com'
5. Click 'Submit' button
6. Wait for 'Success' message
"""
```

### Application Testing
```python
"""
Test calculator functionality:
1. Launch Calculator
2. Click '5' button
3. Click '+' button
4. Click '3' button
5. Click '=' button
6. Verify result shows '8'
"""
```

## Installation from Package Managers

### Using winget (Windows Package Manager)
```python
# Note: Can be extended with custom tool
"Run command: winget install --id Google.Chrome -e --silent"
"Run command: winget uninstall 'Adobe Reader'"
```

### Using Chocolatey
```python
# If chocolatey is installed
"Run command: choco install 7zip -y"
"Run command: choco upgrade all -y"
```

## Safety & Best Practices

### Always Use Confirmation Mode
```python
# In .env file
REQUIRE_CONFIRMATION=true
```

### Test Installations in VM First
- Use virtual machine for testing destructive operations
- Take snapshots before major changes
- Test silent install flags before deployment

### Error Handling
```python
"""
Robust installation:
1. Check if installer exists at path
2. Verify checksum if available
3. Check if app is already installed
4. Install with error handling
5. Verify installation success
6. Log results
"""
```

### Admin Privileges
Some operations require elevation:
- Run PowerShell as Administrator
- Or right-click script and "Run as Administrator"

## Tips for Success

### Finding Control Names
1. Use `get_window_controls()` to inspect
2. Use Windows Spy tools (inspect.exe)
3. Use pywinauto's `print_control_identifiers()`

### Silent Installation Flags
Common flags:
- `/S` or `/silent` - Silent install
- `/quiet` - MSI quiet mode
- `/norestart` - Don't restart
- `/D=C:\path` - Install directory

### Timing Issues
- Always wait after launching apps
- Use `wait_for_window()` for reliability
- Add delays between operations if needed

### Window Title Matching
- Use partial matches: "Notepad" matches "Untitled - Notepad"
- Case-insensitive by default
- Use regex for complex patterns
