"""
Example automation scripts showing how to use the agent programmatically
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agent import WindowsAgent


def example_file_automation():
    """Example: Automated file organization"""
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Create a folder structure for a new project:
    1. Create a folder called 'MyProject' on the Desktop
    2. Inside it, create folders: 'docs', 'src', 'tests'
    3. Create a README.txt file in MyProject with content 'Project started'
    """
    
    result = agent.execute_task(task)
    print(result)


def example_system_monitoring():
    """Example: System health check"""
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Give me a system health report:
    1. CPU usage
    2. Memory usage
    3. Disk space on C drive
    4. Top 5 processes by memory
    """
    
    result = agent.execute_task(task)
    print(result)


def example_productivity_automation():
    """Example: Daily productivity setup"""
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Set up my work environment:
    1. Open Notepad
    2. Type 'Daily Tasks:\n- \n- \n- '
    3. Check if Chrome is running, if not start it
    """
    
    result = agent.execute_task(task)
    print(result)


if __name__ == "__main__":
    print("Choose an example:")
    print("1. File automation")
    print("2. System monitoring")
    print("3. Productivity automation")
    
    choice = input("Enter number (1-3): ")
    
    if choice == "1":
        example_file_automation()
    elif choice == "2":
        example_system_monitoring()
    elif choice == "3":
        example_productivity_automation()
    else:
        print("Invalid choice")
