# Confirmation Mode Guide

## How It Works

When `REQUIRE_CONFIRMATION=true` in `.env`, the agent asks before executing each tool.

### Available Responses

When prompted: `Execute tool_name? [y/n/a] (y):`

- **`y` or `yes`** - Execute this one tool, ask again for the next one
- **`n` or `no`** - Cancel this tool (stops the current task)
- **`a` or `all`** - Execute this tool AND all remaining tools for this task without asking again

### Examples

#### Scenario 1: One-by-one approval
```
What would you like me to do?: Install Chrome and take a screenshot

🔧 Using tool: install_application
Execute install_application? [y/n/a] (y): y
✓ Tool executed

🔧 Using tool: take_screenshot
Execute take_screenshot? [y/n/a] (y): y
✓ Tool executed
```

#### Scenario 2: "Yes to All" for multi-step tasks
```
What would you like me to do?: Copy 5 files from Downloads to Desktop

🔧 Using tool: copy_path
Execute copy_path? [y/n/a] (y): a
✓ Allowing all subsequent operations for this task

🔧 Using tool: copy_path
[auto-executed, no prompt]

🔧 Using tool: copy_path
[auto-executed, no prompt]
...
```

#### Scenario 3: Cancelling
```
What would you like me to do?: Delete all files in C:\Windows

🔧 Using tool: delete_path
Execute delete_path? [y/n/a] (y): n
✗ Operation cancelled by user
```

## Disable Confirmations Entirely

### Option 1: Edit .env file
```bash
# In .env, change:
REQUIRE_CONFIRMATION=false
```

Then restart the agent. All tools will execute automatically without prompting.

### Option 2: Use "a" (all) for each task
Keep `REQUIRE_CONFIRMATION=true` but type `a` on the first prompt of each task.

## When to Use Each Mode

### ✅ Use Confirmations (`true`) When:
- Testing new automation workflows
- Working with sensitive operations (file deletion, system changes)
- Learning what the agent does
- Want control over each step
- Don't fully trust the task description

### ⚠️ Disable Confirmations (`false`) When:
- Running trusted, well-tested workflows
- Batch processing many items
- Time-sensitive automation
- You're confident in what the agent will do
- Want maximum speed

## Pro Tips

1. **Start with confirmations ON** - Learn what the agent does first
2. **Use "a" for repetitive tasks** - Like copying multiple files
3. **Check the input** - The agent shows tool inputs before executing
4. **Reset per task** - "Yes to all" only applies to current task, resets for next one
5. **Safety first** - When in doubt, review each step

## Keyboard Shortcuts

- **Enter** - Same as `y` (default)
- **Ctrl+C** - Interrupt (shows "Type 'quit' to exit")
- Just type `quit` - Clean exit

## Example Workflows

### Safe Mode (Confirmations ON, review each)
```bash
REQUIRE_CONFIRMATION=true
```
Best for: First-time tasks, system modifications, learning

### Semi-Auto Mode (Confirmations ON, use "a")
```bash
REQUIRE_CONFIRMATION=true
# Then type "a" on first prompt
```
Best for: Multi-step tasks, batch operations you trust

### Full Auto Mode (No confirmations)
```bash
REQUIRE_CONFIRMATION=false
```
Best for: Production workflows, scheduled tasks, speed

## Changing Modes

### Temporary (one session)
Just use `a` (all) when prompted - applies to current task only

### Permanent
Edit `.env` file:
```bash
REQUIRE_CONFIRMATION=false  # Auto-execute everything
# or
REQUIRE_CONFIRMATION=true   # Ask before each tool
```

Then restart the agent:
```powershell
python src/main.py
```

The startup screen will show your current mode:
```
Mode: Ask before each action       # Confirmations ON
# or
Mode: Auto-execute all actions     # Confirmations OFF
```
