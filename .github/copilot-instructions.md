# Axonyx Revolt - AI Coding Agent Instructions

## Project Overview
Windows 11 automation agent powered by Claude SDK using tool-calling architecture. Agent executes natural language tasks through registered Python functions for file ops, process management, UI automation, and system info.

## Architecture & Patterns

### Core Agent Pattern (agent.py)
- **Agentic loop**: Claude makes multiple tool calls per task (max 10 iterations)
- **Tool registration**: Tools defined as JSON schemas, mapped to Python functions
- **Conversation flow**: `user → claude reasoning → tool_use → tool_result → repeat → end_turn`
- Tool results passed back via `{"type": "tool_result", "tool_use_id": id, "content": json_result}`

### Tool Implementation Pattern
All tools in `src/tools/` follow this structure:
```python
def tool_function(**kwargs) -> Dict:
    """Returns {"success": bool, "data": any} or {"error": str}"""
    try:
        # Implementation
        return {"success": True, "result": value}
    except Exception as e:
        return {"error": str(e)}
```

Each tool module exports:
- `get_*_tools()` → List of Claude tool schemas
- `*_FUNCTIONS` → Dict mapping tool names to functions

### Key Files
- `src/agent.py` - Core orchestrator, manages Claude conversation loop
- `src/main.py` - CLI interface using `rich` library
- `src/tools/*.py` - Windows automation implementations
- `.env` - Configuration (API key, model, safety settings)

## Development Workflows

### Adding New Tools
1. Implement function in appropriate `tools/*.py` module
2. Add JSON schema to `get_*_tools()` list with precise `input_schema`
3. Add function mapping to `*_FUNCTIONS` dict
4. Import in `agent.py._register_tools()` and `._map_tool_functions()`

### Testing Tools
```powershell
# Run with confirmation mode for safety
python src/main.py
# Or test functions directly:
python -c "from tools.file_ops import list_directory; print(list_directory('C:/Users'))"
```

### Running the Agent
```powershell
.\venv\Scripts\Activate.ps1  # Always activate venv first
python src/main.py
```

## Dependencies & Windows Integration

### Key Libraries
- `anthropic` - Claude SDK client
- `pywinauto` - Windows UI automation (requires UIAutomation backend)
- `pyautogui` - Keyboard/mouse control (has failsafe - move mouse to corner)
- `pywin32` - Windows API bindings
- `psutil` - Cross-platform process/system utilities

### Windows-Specific Considerations
- Use `Path.expanduser()` for home directory paths
- Process killing may require admin privileges
- `pywinauto` uses UIA backend: `Desktop(backend="uia")`
- File paths: Accept both forward/back slashes, normalize internally

## Project-Specific Conventions

### Error Handling
All tools return dicts, never raise exceptions to caller. Wrap all operations in try/except and return `{"error": str(e)}` on failure.

### Path Handling
- Accept Windows paths like `Desktop`, `Documents` - expand with `Path.expanduser()`
- Use `pathlib.Path` throughout, not `os.path`
- Create parent directories automatically: `path.parent.mkdir(parents=True, exist_ok=True)`

### Safety Features
- `REQUIRE_CONFIRMATION=true` in `.env` prompts before each tool execution
- `DRY_RUN_MODE=true` simulates without actual execution (not implemented yet - opportunity!)
- Tool functions should validate inputs (e.g., don't delete system directories)

### Claude Model Configuration
Default: `claude-3-5-sonnet-20241022` (most capable for reasoning/tool use)
Alternative: `claude-3-haiku-20240307` (faster, for simpler tasks)

## Common Tasks

### Debugging Tool Execution
Check `agent.py` console output - shows tool name, inputs, and results. Enable detailed logging by setting `LOG_LEVEL=DEBUG` in `.env`.

### Extending UI Automation
See `tools/ui_automation.py` for examples. Common pattern: use `pyautogui` for simple keyboard/mouse, `pywinauto` for window management/complex UI.

### System Operations Requiring Elevation
Some operations need admin rights (killing system processes, protected files). Detect with try/except and return helpful error messages.

## Integration Points

### Claude API
- Streaming not used - single response per iteration
- `max_tokens` controls response length (default 4096)
- Tool schemas must match exact parameter types (int not string for numbers)

### Windows APIs
- File ops: Standard `pathlib` + `shutil`
- Process ops: `psutil` for cross-platform, `subprocess.Popen` for launching
- UI automation: `pyautogui` (coordinates), `pywinauto` (window objects)
- System info: `platform` + `psutil` for hardware details

## Notes for AI Agents

### When adding tools:
- Description is crucial - Claude decides tool usage from description alone
- Use specific types in `input_schema` (integer not number for coordinates)
- Required fields should be truly required - make others optional with defaults

### When debugging:
- Check tool result format - must be JSON serializable
- Verify tool name matches exactly between schema and function mapping
- Test tools independently before integrating with agent loop

### Best practices:
- Keep tool descriptions concise but complete
- Return structured data (lists of dicts) not plain text when possible
- Log tool execution for debugging: `console.print()` in `agent.py`
- Handle edge cases (empty directories, missing files, invalid PIDs) gracefully
