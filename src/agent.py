"""
Windows Agent - Core orchestrator using Claude SDK with tool use
"""
import os
import json
from typing import Any, Dict, List, Optional
from anthropic import Anthropic
from rich.console import Console

from tools.file_ops import get_file_tools
from tools.process_ops import get_process_tools
from tools.ui_automation import get_ui_tools
from tools.system_info import get_system_tools
from tools.app_installation import get_installation_tools
from tools.system_settings import get_system_settings_tools
from tools.app_control import get_app_control_tools
from tools.browser_automation import get_browser_tools
from tools.chrome_launcher import get_chrome_launcher_tools
from tools.screen_reader import get_screen_reader_tools
from tools.installer_automation import get_installer_automation_tools
from tools.installer_automation_v2 import get_installer_automation_v2_tools
from tools.download_manager import get_download_manager_tools

console = Console()


class WindowsAgent:
    """
    Agentic AI that uses Claude with tool calling to automate Windows tasks
    """
    
    def __init__(self, api_key: str, model: str = None):
        self.client = Anthropic(api_key=api_key)
        self.model = model or os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.require_confirmation = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
        self.allow_all = False  # "Yes to all" flag for current task
        
        # Register all available tools
        self.tools = self._register_tools()
        self.tool_functions = self._map_tool_functions()
        
        console.print(f"[dim]Initialized agent with {len(self.tools)} tools[/dim]")
    
    def _register_tools(self) -> List[Dict]:
        """Register all available tools for Claude"""
        tools = []
        tools.extend(get_file_tools())
        tools.extend(get_process_tools())
        tools.extend(get_ui_tools())
        tools.extend(get_system_tools())
        tools.extend(get_installation_tools())
        tools.extend(get_system_settings_tools())
        tools.extend(get_app_control_tools())
        tools.extend(get_browser_tools())
        tools.extend(get_chrome_launcher_tools())
        tools.extend(get_screen_reader_tools())
        tools.extend(get_installer_automation_tools())
        tools.extend(get_installer_automation_v2_tools())  # NEW: Robust installer automation
        tools.extend(get_download_manager_tools())
        
        from tools.image_downloader import get_image_download_tools
        tools.extend(get_image_download_tools())
        
        return tools
    
    def _map_tool_functions(self) -> Dict:
        """Map tool names to their implementation functions"""
        from tools.file_ops import FILE_FUNCTIONS
        from tools.process_ops import PROCESS_FUNCTIONS
        from tools.ui_automation import UI_FUNCTIONS
        from tools.system_info import SYSTEM_FUNCTIONS
        from tools.app_installation import INSTALLATION_FUNCTIONS
        from tools.system_settings import SYSTEM_SETTINGS_FUNCTIONS
        from tools.app_control import APP_CONTROL_FUNCTIONS
        from tools.browser_automation import BROWSER_FUNCTIONS
        from tools.chrome_launcher import CHROME_LAUNCHER_FUNCTIONS
        from tools.screen_reader import SCREEN_READER_FUNCTIONS
        from tools.installer_automation import INSTALLER_AUTOMATION_FUNCTIONS
        from tools.installer_automation_v2 import INSTALLER_AUTOMATION_V2_FUNCTIONS
        from tools.download_manager import DOWNLOAD_MANAGER_FUNCTIONS
        from tools.image_downloader import IMAGE_DOWNLOAD_FUNCTIONS
        
        return {
            **FILE_FUNCTIONS,
            **PROCESS_FUNCTIONS,
            **UI_FUNCTIONS,
            **SYSTEM_FUNCTIONS,
            **INSTALLATION_FUNCTIONS,
            **SYSTEM_SETTINGS_FUNCTIONS,
            **APP_CONTROL_FUNCTIONS,
            **BROWSER_FUNCTIONS,
            **CHROME_LAUNCHER_FUNCTIONS,
            **SCREEN_READER_FUNCTIONS,
            **INSTALLER_AUTOMATION_FUNCTIONS,
            **INSTALLER_AUTOMATION_V2_FUNCTIONS,
            **DOWNLOAD_MANAGER_FUNCTIONS,
            **IMAGE_DOWNLOAD_FUNCTIONS
        }
    
    def execute_task(self, task: str) -> Dict[str, Any]:
        """
        Execute a task using the agentic workflow
        
        Args:
            task: Natural language description of the task
            
        Returns:
            Dictionary with success status and result/error
        """
        # Reset "allow all" for new task
        self.allow_all = False
        
        messages = [
            {
                "role": "user",
                "content": task
            }
        ]
        
        try:
            # Agentic loop - Claude can call tools multiple times
            max_iterations = 10
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                # Get Claude's response
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    tools=self.tools,
                    messages=messages
                )
                
                # Check if Claude wants to use tools
                if response.stop_reason == "tool_use":
                    # Process tool calls
                    tool_results = []
                    
                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_input = block.input
                            
                            console.print(f"[yellow]🔧 Using tool: {tool_name}[/yellow]")
                            console.print(f"[dim]   Input: {json.dumps(tool_input, indent=2)}[/dim]")
                            
                            # Confirm with user if required
                            if self.require_confirmation and not self.allow_all:
                                from rich.prompt import Prompt
                                response_text = Prompt.ask(
                                    f"Execute {tool_name}?",
                                    choices=["y", "n", "a", "yes", "no", "all"],
                                    default="y",
                                    show_choices=True,
                                    show_default=True
                                ).lower()
                                
                                if response_text in ["a", "all"]:
                                    console.print("[green]✓ Allowing all subsequent operations for this task[/green]")
                                    self.allow_all = True
                                elif response_text in ["n", "no"]:
                                    console.print("[red]✗ Operation cancelled by user[/red]")
                                    return {
                                        "success": False,
                                        "error": "User cancelled operation"
                                    }
                            
                            # Execute the tool
                            result = self._execute_tool(tool_name, tool_input)
                            
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result)
                            })
                    
                    # Add assistant response and tool results to conversation
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({"role": "user", "content": tool_results})
                    
                else:
                    # Claude is done, extract final response
                    final_text = ""
                    for block in response.content:
                        if hasattr(block, "text"):
                            final_text += block.text
                    
                    return {
                        "success": True,
                        "message": final_text,
                        "iterations": iteration
                    }
            
            return {
                "success": False,
                "error": "Max iterations reached"
            }
            
        except Exception as e:
            console.print(f"[red]Agent error: {str(e)}[/red]")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_tool(self, tool_name: str, tool_input: Dict) -> Dict:
        """Execute a tool function"""
        try:
            if tool_name not in self.tool_functions:
                return {"error": f"Unknown tool: {tool_name}"}
            
            func = self.tool_functions[tool_name]
            result = func(**tool_input)
            
            console.print(f"[green]✓ Tool result: {json.dumps(result, indent=2)[:200]}...[/green]")
            
            return result
            
        except Exception as e:
            error_msg = f"Tool execution error: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            return {"error": error_msg}
