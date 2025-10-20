# Getting Started with Axonyx Revolt

## Welcome! 🎉
You're about to set up an AI agent that can automate Windows 11 through natural language. This guide will get you up and running in 10 minutes.

## Prerequisites ✅

### Required
- ✅ **Windows 11**
- ✅ **Python 3.12+** ([Download](https://www.python.org/downloads/))
- ✅ **Anthropic API key** ([Get one here](https://console.anthropic.com/))

### Optional (for GUI)
- ✅ **Flutter 3.35+** ([Installation Guide](https://docs.flutter.dev/get-started/install/windows))
  - Download Flutter SDK
  - Extract to `C:\flutter`
  - Add `C:\flutter\bin` to PATH
  - Run `flutter doctor` to verify

## Installation Steps

### Quick Start (CLI Agent)

#### Step 1: Get Python Ready

Open PowerShell and verify Python:
```powershell
python --version
```

You should see Python 3.12 or higher. If not, install Python first.

#### Step 2: Clone Repository

```powershell
git clone https://github.com/YOUR_USERNAME/axonyx-revolt.git
cd axonyx-revolt
```

#### Step 3: Run Automated Setup

```powershell
.\start.ps1
```

This script will:
1. ✅ Create Python virtual environment (.venv)
2. ✅ Install all required packages
3. ✅ Create .env configuration file
4. ✅ Launch the CLI agent

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Step 4: Add Your API Key

When prompted, you'll need to:
1. Open the `.env` file that was created
2. Replace `your_anthropic_api_key_here` with your actual API key
3. Save the file

Your `.env` should look like:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-3-5-haiku-20241022
REQUIRE_CONFIRMATION=true
```

#### Step 5: Start Automating! 🚀

The agent will launch automatically. Try these starter commands:

**Beginner Tasks:**
```
"Create a folder called 'test' on my Desktop"
"What's my CPU usage?"
"List all files in my Downloads folder"
"Open Notepad"
```

**Intermediate Tasks:**
```
"Is Google Chrome installed?"
"Launch Calculator and maximize it"
"Switch to dark mode"
"Set power plan to high performance"
```

**Advanced Tasks:**
```
"Install 7-Zip from C:/Downloads/7zip-installer.exe silently"
"Launch Notepad, type 'Hello World', and press Enter"
"Check if VS Code is installed, if not, tell me how to install it"
```

## Understanding the Agent

## Flutter GUI Setup (Optional)

### Prerequisites
- ✅ Flutter 3.35+ installed and in PATH
- ✅ Python agent already setup (above steps completed)

### Step 1: Run GUI Setup
```powershell
.\setup_gui.ps1
```

This will:
1. ✅ Verify Flutter installation
2. ✅ Check Python virtual environment
3. ✅ Install FastAPI and Uvicorn (backend)
4. ✅ Download Flutter dependencies
5. ✅ Enable Windows desktop support
6. ✅ Generate Windows runner files

### Step 2: Launch GUI + Backend
```powershell
# Launch both (recommended)
.\launch_gui.ps1 -Both

# OR launch separately:
.\launch_gui.ps1 -Backend  # Start API server
.\launch_gui.ps1 -GUI      # Start Flutter app
```

### Step 3: Use the GUI
- 🎨 **Frameless design** with purple/cyan gradient
- 💬 **Chat interface** - type commands naturally
- 🎛️ **Model selector** - switch between models
- 🟢 **Connection status** - shows backend connectivity
- 🔧 **Tool badges** - see what tools executed

### GUI Features
- Message history with timestamps
- Tool execution tracking (success/error badges)
- Model selection dropdown (Haiku/Sonnet/Opus)
- Empty state with suggestion chips
- Drag-to-move frameless window
- Custom title bar with window controls

---

## Understanding the Agent

### How It Works

1. **You ask** in natural language: "Install app X and launch it"
2. **Claude thinks**: Breaks down into: check if installed → install → launch
3. **Agent executes**: Calls appropriate Windows automation tools (77 total)
4. **You get results**: Success message or detailed output

### Safety Features

- **Confirmation Mode** (CLI only): Asks before each action
- **Error Handling**: Tools won't crash your system
- **Validation**: Checks paths, file existence, etc.
- **GUI Mode**: Auto-execute (no confirmations)

To change confirmation setting for CLI, edit `.env`:
```env
REQUIRE_CONFIRMATION=true   # Ask before each action (CLI default)
REQUIRE_CONFIRMATION=false  # Auto-execute (GUI mode)
```

## What Can You Automate?

### � 77 Tools Available

### �📦 Application Management (5 tools)
- Check if apps are installed
- Install applications silently (.exe, .msi)
- Uninstall applications by name
- List all installed software with versions
- Download and install from URLs

### 🖥️ Desktop Control (10 tools)
- Launch applications
- Control windows (minimize, maximize, close)
- Click buttons in dialogs
- Fill form fields
- Navigate application menus
- Take screenshots
- Keyboard shortcuts (hotkeys)
- Mouse clicks at coordinates
- Type text with intervals

### 🌐 Browser Automation (17 tools)
- **Chrome launcher** (2 tools) - native Chrome with profiles
- **Selenium** (12 tools) - full browser control
- **Image downloader** (3 tools) - Google Images bulk download
  - Search and download images
  - Quick Google Images search
  - Download from direct URLs

### 📸 OCR & Screen Reading (6 tools)
- Take screenshots
- Extract text from screen regions
- Find text on screen (coordinates)
- Read specific screen areas
- OCR from images
- OneDrive-aware paths

### 🔧 Advanced Installer Automation (10 tools)
- **V1** (5 tools) - Basic installer automation
- **V2** (5 tools) - Robust multi-strategy automation
  - Exact window title matching
  - 4 fallback strategies
  - Checkbox detection (multiple methods)
  - Progress monitoring
  - Works with: Python, Chrome, Node.js, Git, etc.

### 📥 Download Management (4 tools)
- List recent downloads
- Filter by file extension
- Find specific downloaded files
- OneDrive-aware Downloads folder

### ⚙️ System Settings (3 tools)
- Switch dark/light mode
- Change wallpaper
- Set power plans
- Configure screen timeout
- Open Windows Settings sections

### 📁 File Operations (8 tools)
- Create/delete files and folders
- Copy/move files
- Read file contents
- List directory contents
- Search for files
- Check file existence
- Get file info (size, modified date)

### 🔄 Process Management (6 tools)
- List running processes
- Kill processes by name/PID
- Check if process is running
- Get process details (memory, CPU)
- Monitor resource usage

### 💻 System Information (4 tools)
- Get hardware details
- Check disk space
- Network information
- System specifications

### 💻 System Control
- Start/stop processes
- Check system resources (CPU, RAM, disk)
- Get network information
- Monitor running applications
- Type text and control mouse

## Common Scenarios

### Setting Up Development Environment
```
"Check if VS Code is installed. Also check for Git. Then switch to dark mode and set power plan to high performance."
```

### Batch Installation
```
"Is Chrome installed? What about 7-Zip? List all installed applications."
```

### System Maintenance
```
"Show me CPU usage, memory usage, and disk space. Then list the top 10 processes by memory."
```

### Application Testing
```
"Launch Notepad, wait for it to open, type 'Test', press Enter, then close without saving."
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Make sure `.env` file exists in the project root
- Check that you've added your API key
- Restart the agent after editing `.env`

### "Import could not be resolved" errors
- These are just IDE warnings before packages are installed
- Run `.\start.ps1` or manually install: `pip install -r requirements.txt`
- Make sure virtual environment is activated: `.\venv\Scripts\Activate.ps1`

### "Access Denied" errors
- Some operations need administrator privileges
- Right-click PowerShell → "Run as Administrator"
- Try again

### Agent doesn't understand commands
- Be specific: "Launch notepad.exe" not "open notepad"
- Use full paths: "C:/Users/YourName/Desktop" not "Desktop"
- Break complex tasks into steps

### pyautogui failsafe triggered
- You moved mouse to corner (safety feature)
- Disable if needed (not recommended): Edit `ui_automation.py`

## Tips for Success

### 1. Start Simple
Begin with basic tasks to understand how the agent works:
- File operations
- Opening applications
- System information queries

### 2. Use Confirmation Mode
Keep `REQUIRE_CONFIRMATION=true` until you're comfortable with what the agent does.

### 3. Be Specific
Good: "Install 7-Zip from C:/Downloads/7z1900-x64.exe silently"
Bad: "install something"

### 4. Test in Safe Environment
- Use a test folder for file operations
- Test installations in VM if possible
- Don't automate critical system operations until confident

### 5. Learn the Capabilities
- Read `examples/EXAMPLE_TASKS.md` for inspiration
- Check `examples/ADVANCED_EXAMPLES.md` for complex workflows
- Review the tool documentation in each `tools/*.py` file

## Next Steps

### Explore Examples
```powershell
# Run example scripts
python examples/automation_examples.py
python examples/advanced_automation.py
```

### Read Documentation
- `SETUP_GUIDE.md` - Detailed technical setup
- `examples/EXAMPLE_TASKS.md` - Task library
- `examples/ADVANCED_EXAMPLES.md` - Advanced patterns
- `.github/copilot-instructions.md` - Developer guide

### Customize
- Add your own tools in `src/tools/`
- Modify existing tools for your needs
- Create workflow scripts for repetitive tasks

### Join the Automation

This is a powerful tool. Use it responsibly:
- ⚠️ Always review destructive operations
- 🧪 Test new workflows in safe environments
- 📝 Document your automation scripts
- 🔒 Keep your API key secure

## Getting Help

### Check Console Output
The agent shows detailed information about:
- Which tools it's using
- Input parameters
- Results and errors

### Enable Debug Logging
In `.env`:
```env
LOG_LEVEL=DEBUG
```

### Test Tools Directly
```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Test a tool
python -c "from tools.file_ops import list_directory; print(list_directory('C:/'))"
```

## Ready to Automate! 🎉

You now have a powerful Windows automation agent at your fingertips. Start with simple tasks, build confidence, then create amazing automation workflows.

**Remember:** The agent is as smart as Claude, but you're still in control. Use confirmation mode, start small, and gradually build up to complex automations.

Happy automating! 🚀

---

**Need more help?** Check out the detailed guides in the `examples/` directory or review the source code in `src/tools/` to understand what each tool can do.
