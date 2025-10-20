# Quick Model Switcher Commands

Copy-paste these into PowerShell terminal to switch models instantly:

## Switch to Haiku (Fast & Cheap) ⚡
```powershell
(Get-Content .env) -replace '^CLAUDE_MODEL=.*', 'CLAUDE_MODEL=claude-3-5-haiku-20241022' | Set-Content .env; Write-Host "✅ Switched to Haiku 3.5" -ForegroundColor Green
```

## Switch to Sonnet 3.5 (Balanced) 🎯
```powershell
(Get-Content .env) -replace '^CLAUDE_MODEL=.*', 'CLAUDE_MODEL=claude-3-5-sonnet-20241022' | Set-Content .env; Write-Host "✅ Switched to Sonnet 3.5" -ForegroundColor Green
```

## Switch to Sonnet 4 (Most Powerful) 🚀
```powershell
(Get-Content .env) -replace '^CLAUDE_MODEL=.*', 'CLAUDE_MODEL=claude-sonnet-4-20250514' | Set-Content .env; Write-Host "✅ Switched to Sonnet 4" -ForegroundColor Green
```

## Check Current Model 🔍
```powershell
$model = (Get-Content .env | Select-String '^CLAUDE_MODEL=').ToString().Split('=')[1].Trim(); Write-Host "Current model: $model" -ForegroundColor Cyan
```

## After Switching
Always restart the agent for changes to take effect:
```powershell
python src/main.py
```

## Model Pricing Reference (as of Oct 2025)
- **Haiku 3.5**: ~$0.25 per million input tokens, ~$1.25 per million output
- **Sonnet 3.5**: ~$3 per million input, ~$15 per million output  
- **Sonnet 4**: ~$3 per million input, ~$15 per million output (similar to 3.5 but more capable)

## When to Use Each Model

### Haiku (Current) ✅
- General automation tasks
- File operations
- Simple installations
- UI automation
- Browser control
- **Cost-effective for most work**

### Sonnet 3.5
- Complex reasoning
- Multi-step planning
- Debugging difficult issues
- Code analysis
- **When Haiku struggles**

### Sonnet 4
- Very complex problems
- Advanced reasoning
- Research tasks
- **When Sonnet 3.5 isn't enough**

## Pro Tip 💡
Start with Haiku for everything. Only upgrade if you see:
- "I don't understand the task"
- Repeated failures
- Need for complex reasoning

Most tasks (including the Python installer automation we just built) work perfectly fine with Haiku!
