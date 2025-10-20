# Windows 11 Agentic AI - Complete Setup Guide

## 🚀 Quick Start

### Step 1: Install Python
Make sure you have Python 3.10+ installed:
```powershell
python --version
```

### Step 2: Create Virtual Environment
```powershell
cd d:\Git\Axonyx_Revolt
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude SDK
- `pywinauto` - Windows UI automation
- `pyautogui` - Keyboard/mouse control
- `pywin32` - Windows API access
- `psutil` - System/process information
- `python-dotenv` - Environment configuration
- `rich` - Beautiful terminal output

### Step 4: Configure API Key
1. Get your API key from https://console.anthropic.com/
2. Copy the example config:
   ```powershell
   Copy-Item .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

### Step 5: Run the Agent
```powershell
python src/main.py
```

## 📖 Usage Examples

Once running, try these natural language commands:

### File Operations
- "Create a folder called 'MyProject' on my Desktop"
- "List all files in my Documents folder"
- "Create a text file called notes.txt with the content 'Hello World'"
- "Copy all files from Desktop to Documents/Backup"

### Process Management
- "Show me all running processes"
- "Start Calculator"
- "Open Notepad"
- "Close all Chrome windows"

### UI Automation
- "Open Notepad and type 'Hello from AI'"
- "Press Ctrl+S to save"
- "Click at position 500, 300"
- "What's my current mouse position?"

### System Information
- "What's my CPU usage?"
- "How much RAM is available?"
- "Show me disk space on C drive"
- "What's my battery status?"

### Combined Workflows
- "Open Notepad, type 'Meeting Notes', press Enter twice, then type 'Attendees:'"
- "Create a folder called 'Reports' on Desktop, then create 3 text files inside it"
- "Check if Chrome is running, if not, start it"

## 🛠️ Architecture Overview

### Agent Flow
```
User Input → Claude (reasoning) → Tool Selection → Tool Execution → Result → Claude (synthesis) → Output
```

### Key Components

1. **agent.py** - Core orchestrator
   - Manages conversation with Claude
   - Handles tool calling loop
   - Coordinates tool execution

2. **tools/** - Windows automation capabilities
   - `file_ops.py` - File system operations
   - `process_ops.py` - Process management
   - `ui_automation.py` - Keyboard/mouse control
   - `system_info.py` - System queries

3. **main.py** - User interface
   - Terminal interaction
   - Input/output formatting
   - Error handling

### How Tool Calling Works

1. User gives natural language task
2. Claude analyzes and decides which tools to use
3. Agent executes tools with parameters Claude provides
4. Results go back to Claude
5. Claude continues or provides final answer

Example flow for "Open Notepad and type Hello":
```
User: "Open Notepad and type Hello"
↓
Claude: "I'll use start_process to open notepad"
Tool: start_process(command="notepad")
↓
Claude: "Now I'll type the text"
Tool: type_text(text="Hello")
↓
Claude: "Done! Notepad is open with 'Hello' typed"
```

## 🔧 Customization

### Adding New Tools

1. Create function in appropriate `tools/*.py` file:
```python
def my_new_tool(param: str) -> Dict:
    try:
        # Your implementation
        return {"success": True, "result": "..."}
    except Exception as e:
        return {"error": str(e)}
```

2. Add tool definition:
```python
{
    "name": "my_new_tool",
    "description": "What this tool does",
    "input_schema": {
        "type": "object",
        "properties": {
            "param": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param"]
    }
}
```

3. Map to function:
```python
MY_FUNCTIONS = {
    "my_new_tool": my_new_tool
}
```

### Adjusting Safety Settings

In `.env`:
- `REQUIRE_CONFIRMATION=true` - Ask before each tool execution
- `DRY_RUN_MODE=true` - Simulate without actual execution
- `MAX_TOKENS=4096` - Control response length

### Using Different Claude Models

In `.env`, change:
```
CLAUDE_MODEL=claude-3-5-sonnet-20241022  # Most capable
# CLAUDE_MODEL=claude-3-haiku-20240307  # Faster, cheaper
```

## 🔒 Security & Safety

### Important Warnings
⚠️ This agent can:
- Delete files
- Kill processes
- Control your keyboard/mouse
- Modify system settings

### Best Practices
1. **Always use confirmation mode** (`REQUIRE_CONFIRMATION=true`)
2. **Test in isolated environment** first
3. **Review tool permissions** before deployment
4. **Monitor agent actions** closely
5. **Use specific commands** to avoid ambiguity
6. **Keep API keys secure** (never commit `.env`)

### Windows Permissions
Some operations require administrator privileges:
- Killing system processes
- Accessing protected directories
- Installing software

Run PowerShell as Administrator if needed:
```powershell
Start-Process powershell -Verb RunAs
```

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Make sure `.env` file exists (copy from `.env.example`)
- Check that API key is valid
- Restart terminal after creating `.env`

### "Import could not be resolved"
- Activate virtual environment: `.\venv\Scripts\Activate.ps1`
- Reinstall packages: `pip install -r requirements.txt`

### "pyautogui failsafe triggered"
- Move mouse to corner to cancel
- Adjust failsafe: `pyautogui.FAILSAFE = False` (use carefully)

### "Access Denied" errors
- Run as Administrator for system operations
- Check Windows permissions
- Some processes are protected by Windows

### Agent not understanding commands
- Be more specific: "Open notepad.exe" vs "Open Notepad"
- Provide exact paths: "C:/Users/YourName/Desktop" vs "Desktop"
- Break complex tasks into steps

## 🎯 Advanced Features

### Computer Vision (Optional)
Uncomment in `requirements.txt`:
```
pillow>=10.0.0
opencv-python>=4.8.0
```

Then add screenshot/image analysis tools.

### Web Browser Automation
Install Selenium:
```powershell
pip install selenium
```

Create `tools/browser_ops.py` for web automation.

### Email Integration
Add email tools with `smtplib` or Microsoft Graph API.

### Voice Control
Integrate with `speech_recognition` and `pyttsx3`.

## 📚 Resources

- [Claude API Docs](https://docs.anthropic.com/)
- [Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [pywinauto Docs](https://pywinauto.readthedocs.io/)
- [pyautogui Docs](https://pyautogui.readthedocs.io/)

## 🤝 Contributing

To extend this agent:
1. Add new tools in `src/tools/`
2. Update tool registrations in `agent.py`
3. Test thoroughly in safe environment
4. Document new capabilities in README

## 📝 License

MIT License - Feel free to modify and extend!

---

**Happy Automating! 🤖**

For questions or issues, consult the troubleshooting section or Claude API documentation.
