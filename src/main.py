"""
Windows 11 Agentic AI - Main Entry Point
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from agent import WindowsAgent

console = Console()


def main():
    """Main entry point for the Windows Agent"""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        console.print("[red]Error: ANTHROPIC_API_KEY not set in .env file[/red]")
        console.print("Please copy .env.example to .env and add your API key")
        return
    
    # Get model selection
    model = os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022")
    require_confirmation = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
    
    # Display welcome message with model info
    model_display = {
        "claude-sonnet-4-20250514": "Sonnet 4 (Most Capable)",
        "claude-3-5-haiku-20241022": "Haiku 3.5 (Fast & Cheap)",
        "claude-3-5-sonnet-20241022": "Sonnet 3.5 (Balanced)",
        "claude-3-opus-20240229": "Opus 3 (Very Capable)"
    }.get(model, model)
    
    confirmation_mode = "[yellow]Ask before each action[/yellow]" if require_confirmation else "[green]Auto-execute all actions[/green]"
    
    console.print(Panel.fit(
        f"[bold cyan]Windows 11 Agentic AI[/bold cyan]\n"
        f"Powered by Claude SDK\n"
        f"Model: [yellow]{model_display}[/yellow]\n"
        f"Mode: {confirmation_mode}\n\n"
        "[dim]Type your task in natural language, or 'quit' to exit\n"
        "When prompted: [y]es, [n]o, [a]ll (yes to all for this task)[/dim]",
        title="🤖 Axonyx Revolt Agent"
    ))
    
    # Initialize agent
    agent = WindowsAgent(api_key=api_key)
    
    # Main loop
    while True:
        try:
            # Get user input
            task = Prompt.ask("\n[bold green]What would you like me to do?[/bold green]")
            
            if task.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            
            if not task.strip():
                continue
            
            # Execute task
            console.print(f"\n[cyan]🤔 Thinking about: {task}[/cyan]\n")
            result = agent.execute_task(task)
            
            # Display result
            if result.get("success"):
                console.print(f"[green]✓ {result.get('message', 'Task completed')}[/green]")
                if result.get("output"):
                    console.print(Panel(str(result["output"]), title="Output"))
            else:
                console.print(f"[red]✗ {result.get('error', 'Task failed')}[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    main()
