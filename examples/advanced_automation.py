"""
Advanced automation examples for power users
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from agent import WindowsAgent


def install_dev_environment():
    """
    Example: Automated development environment setup
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Set up my development environment:
    1. Check if Visual Studio Code is installed
    2. Check if Git is installed
    3. If any are missing, list what needs to be installed
    4. Switch Windows to dark mode
    5. Set power plan to high performance for better build times
    """
    
    result = agent.execute_task(task)
    print(result)


def automated_app_installation():
    """
    Example: Install and verify application
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Replace with your actual installer path
    task = """
    Automated installation workflow:
    1. Check if '7-Zip' is installed
    2. If not installed, tell me where I should place the installer
    3. List all currently installed applications for reference
    """
    
    result = agent.execute_task(task)
    print(result)


def system_maintenance():
    """
    Example: System health check and cleanup
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Perform system maintenance check:
    1. Check CPU usage
    2. Check memory usage
    3. Check disk space on all drives
    4. List top 10 processes by memory usage
    5. Summarize the health status
    """
    
    result = agent.execute_task(task)
    print(result)


def desktop_app_automation():
    """
    Example: Advanced desktop app control
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Notepad automation demo:
    1. Launch notepad.exe
    2. Wait for the window to appear
    3. Type 'Automated Text Entry Test'
    4. Press Enter twice
    5. Type '- Line 1'
    6. Press Enter
    7. Type '- Line 2'
    """
    
    result = agent.execute_task(task)
    print(result)


def configure_system_settings():
    """
    Example: System configuration
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Configure system for presentation mode:
    1. Get current display resolution
    2. Set screen timeout to never (0 minutes)
    3. Set power plan to high performance
    4. Switch to dark mode
    """
    
    result = agent.execute_task(task)
    print(result)


def application_testing_workflow():
    """
    Example: Automated application testing
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Test Calculator application:
    1. Launch Calculator
    2. Wait for window to appear
    3. Maximize the window
    4. Find window and report its controls (for inspection)
    """
    
    result = agent.execute_task(task)
    print(result)


def batch_app_management():
    """
    Example: Manage multiple applications
    """
    load_dotenv()
    agent = WindowsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    task = """
    Application management:
    1. List all installed applications
    2. Find applications with 'Microsoft' in the name
    3. Check if Chrome is running
    4. Show me system information
    """
    
    result = agent.execute_task(task)
    print(result)


if __name__ == "__main__":
    print("=" * 60)
    print("ADVANCED WINDOWS AUTOMATION EXAMPLES")
    print("=" * 60)
    print("\nChoose an example:")
    print("1. Install development environment")
    print("2. Automated app installation")
    print("3. System maintenance check")
    print("4. Desktop app automation (Notepad demo)")
    print("5. Configure system settings")
    print("6. Application testing workflow")
    print("7. Batch application management")
    print()
    
    choice = input("Enter number (1-7): ")
    
    examples = {
        "1": install_dev_environment,
        "2": automated_app_installation,
        "3": system_maintenance,
        "4": desktop_app_automation,
        "5": configure_system_settings,
        "6": application_testing_workflow,
        "7": batch_app_management
    }
    
    if choice in examples:
        print(f"\n{'='*60}\nRunning example...\n{'='*60}\n")
        examples[choice]()
    else:
        print("Invalid choice")
