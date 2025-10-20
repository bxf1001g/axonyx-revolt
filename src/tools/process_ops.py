"""
Process Management Tools
"""
import psutil
import subprocess
from typing import Dict, List


def list_processes() -> Dict:
    """List all running processes"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
            try:
                info = proc.info
                processes.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "username": info.get('username'),
                    "memory_percent": round(info.get('memory_percent', 0), 2),
                    "cpu_percent": round(info.get('cpu_percent', 0), 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return {
            "success": True,
            "processes": processes[:50],  # Limit to first 50
            "total_count": len(processes)
        }
    except Exception as e:
        return {"error": str(e)}


def start_process(command: str, args: List[str] = None) -> Dict:
    """Start a new process/application"""
    try:
        cmd = [command]
        if args:
            cmd.extend(args)
        
        # Start process without waiting
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        
        return {
            "success": True,
            "message": f"Started process: {command}",
            "pid": proc.pid
        }
    except Exception as e:
        return {"error": str(e)}


def kill_process(pid: int = None, name: str = None) -> Dict:
    """Terminate a process by PID or name"""
    try:
        killed = []
        
        if pid:
            proc = psutil.Process(pid)
            proc.terminate()
            killed.append(f"PID {pid}")
        elif name:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == name.lower():
                    proc.terminate()
                    killed.append(f"{name} (PID {proc.pid})")
        else:
            return {"error": "Must specify either pid or name"}
        
        return {
            "success": True,
            "message": f"Terminated: {', '.join(killed)}",
            "count": len(killed)
        }
    except psutil.NoSuchProcess:
        return {"error": f"Process not found"}
    except psutil.AccessDenied:
        return {"error": "Access denied - may need administrator privileges"}
    except Exception as e:
        return {"error": str(e)}


def get_process_info(pid: int) -> Dict:
    """Get detailed information about a process"""
    try:
        proc = psutil.Process(pid)
        info = proc.as_dict(attrs=[
            'pid', 'name', 'username', 'status', 
            'cpu_percent', 'memory_percent', 'create_time',
            'exe', 'cwd', 'cmdline'
        ])
        
        return {"success": True, "process": info}
    except psutil.NoSuchProcess:
        return {"error": f"Process {pid} not found"}
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_process_tools() -> List[Dict]:
    """Get process management tool definitions"""
    return [
        {
            "name": "list_processes",
            "description": "List all currently running processes on the system",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "start_process",
            "description": "Start a new application or process. Use for launching programs like notepad, calculator, chrome, etc.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command or application to start (e.g., 'notepad', 'calc', 'chrome')"
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional command line arguments"
                    }
                },
                "required": ["command"]
            }
        },
        {
            "name": "kill_process",
            "description": "Terminate a running process by PID or name. Use with caution!",
            "input_schema": {
                "type": "object",
                "properties": {
                    "pid": {
                        "type": "integer",
                        "description": "The process ID to terminate"
                    },
                    "name": {
                        "type": "string",
                        "description": "The process name to terminate (e.g., 'notepad.exe')"
                    }
                }
            }
        },
        {
            "name": "get_process_info",
            "description": "Get detailed information about a specific process",
            "input_schema": {
                "type": "object",
                "properties": {
                    "pid": {
                        "type": "integer",
                        "description": "The process ID to query"
                    }
                },
                "required": ["pid"]
            }
        }
    ]


# Map tool names to functions
PROCESS_FUNCTIONS = {
    "list_processes": list_processes,
    "start_process": start_process,
    "kill_process": kill_process,
    "get_process_info": get_process_info
}
