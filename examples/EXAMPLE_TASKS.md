# Example Tasks for Windows Agent

## Beginner Tasks

### File Operations
- "Create a folder called 'test' on my Desktop"
- "List all files in my Downloads folder"
- "Create a file called todo.txt with content 'Buy groceries'"
- "What's inside my Documents folder?"

### Process Management
- "Start Calculator"
- "Open Notepad"
- "Show me all running processes"
- "Is Chrome running?"

### System Info
- "What's my CPU usage?"
- "How much RAM do I have?"
- "Show me disk space"
- "What's my computer name?"

## Intermediate Tasks

### File Organization
- "Create a project structure: MyApp with folders src, tests, docs"
- "Copy all .txt files from Desktop to Documents/TextFiles"
- "Move readme.txt from Downloads to Desktop"
- "Delete all empty folders in my Desktop"

### Multi-Step Automation
- "Open Notepad and type 'Hello World', then press Enter twice"
- "Create a folder called 'Backup' and copy Documents/important.txt to it"
- "Check if Firefox is running, if not start it"

### UI Automation
- "Type 'test message' and press Enter"
- "Press Ctrl+C to copy"
- "What's my current screen resolution?"
- "Move mouse to center of screen"

## Advanced Tasks

### Complex Workflows
- "Create a daily notes system: folder for today's date with morning.txt, afternoon.txt, evening.txt files"
- "Organize my Downloads: create folders by file type and move files accordingly"
- "Monitor system: check CPU, RAM, disk space and tell me if anything is over 80%"

### Process Management
- "Find all Chrome processes and show their memory usage"
- "Start notepad, wait, then close it"
- "Kill all processes named 'test.exe'"

### System Administration
- "Generate a system report: OS version, CPU cores, RAM, disk space, top 5 processes"
- "Find which drive has the most free space"
- "Check network interfaces and IP addresses"

## Safety Reminders

⚠️ **Destructive Operations**
- Be careful with delete operations
- Use confirmation mode for safety
- Test in isolated environments first

⚠️ **Process Management**
- Don't kill system-critical processes
- Verify process names before termination
- Some operations need admin rights

⚠️ **UI Automation**
- Mouse/keyboard control affects active window
- Use specific coordinates carefully
- Failsafe: move mouse to corner to stop

## Tips for Better Results

### Be Specific
❌ "Open browser"
✅ "Open chrome.exe"

### Use Exact Paths
❌ "Desktop"
✅ "C:/Users/YourName/Desktop"

### Break Complex Tasks
❌ "Set up entire development environment"
✅ "Create project folders, then create config files, then install packages"

### Provide Context
❌ "List files"
✅ "List all .txt files in my Documents folder"

### Check Before Deleting
❌ "Delete everything in Downloads"
✅ "List files in Downloads" → verify → "Delete file X"
