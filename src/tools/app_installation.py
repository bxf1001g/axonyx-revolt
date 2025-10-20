"""
Application Installation and Management Tools
"""
import subprocess
import winreg
from pathlib import Path
from typing import Dict, List, Optional
import os

try:
    import psutil
except ImportError:
    psutil = None


def install_application(installer_path: str, args: List[str] = None, silent: bool = True) -> Dict:
    """
    Install an application from an installer file
    
    Supports: .exe, .msi installers
    """
    try:
        installer = Path(installer_path).expanduser()
        if not installer.exists():
            return {"error": f"Installer not found: {installer_path}"}
        
        # Build command based on installer type
        cmd = [str(installer)]
        
        if installer.suffix.lower() == '.msi':
            # MSI installer
            cmd = ['msiexec', '/i', str(installer)]
            if silent:
                cmd.extend(['/quiet', '/norestart'])
            if args:
                cmd.extend(args)
        else:
            # EXE installer
            if silent:
                # Common silent install flags
                if args:
                    cmd.extend(args)
                else:
                    cmd.extend(['/S', '/silent', '/VERYSILENT'])
            elif args:
                cmd.extend(args)
        
        # Run installer
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": f"Installation completed: {installer.name}",
                "stdout": result.stdout
            }
        else:
            return {
                "error": f"Installation failed with code {result.returncode}",
                "stderr": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        return {"error": "Installation timeout (5 minutes)"}
    except Exception as e:
        return {"error": str(e)}


def uninstall_application(app_name: str, silent: bool = True) -> Dict:
    """
    Uninstall an application by name
    """
    try:
        # Search for uninstall string in registry
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        
        uninstall_cmd = None
        
        # Check 64-bit registry
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if app_name.lower() in display_name.lower():
                                    uninstall_cmd = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                    break
                            except FileNotFoundError:
                                continue
                    except Exception:
                        continue
        except Exception:
            pass
        
        if not uninstall_cmd:
            return {"error": f"Application not found: {app_name}"}
        
        # Execute uninstall
        cmd = uninstall_cmd
        if silent and '/I' in cmd:
            # MSI uninstaller
            cmd = cmd.replace('/I', '/X') + ' /quiet /norestart'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
        
        return {
            "success": True,
            "message": f"Uninstalled: {app_name}",
            "output": result.stdout
        }
        
    except Exception as e:
        return {"error": str(e)}


def list_installed_applications() -> Dict:
    """
    List all installed applications from Windows registry
    """
    try:
        apps = []
        uninstall_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        for hkey, path in uninstall_keys:
            try:
                with winreg.OpenKey(hkey, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    try:
                                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    except FileNotFoundError:
                                        version = "Unknown"
                                    try:
                                        publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                                    except FileNotFoundError:
                                        publisher = "Unknown"
                                    
                                    apps.append({
                                        "name": name,
                                        "version": version,
                                        "publisher": publisher
                                    })
                                except FileNotFoundError:
                                    continue
                        except Exception:
                            continue
            except Exception:
                continue
        
        # Remove duplicates
        seen = set()
        unique_apps = []
        for app in apps:
            if app["name"] not in seen:
                seen.add(app["name"])
                unique_apps.append(app)
        
        return {
            "success": True,
            "applications": sorted(unique_apps, key=lambda x: x["name"]),
            "count": len(unique_apps)
        }
        
    except Exception as e:
        return {"error": str(e)}


def download_and_install(url: str, installer_name: str = None, silent: bool = True) -> Dict:
    """
    Download an installer from URL and install it
    """
    try:
        import urllib.request
        
        # Determine filename
        if not installer_name:
            installer_name = url.split('/')[-1]
        
        # Download to temp directory
        temp_dir = Path(os.environ.get('TEMP', '/tmp'))
        installer_path = temp_dir / installer_name
        
        # Download
        urllib.request.urlretrieve(url, installer_path)
        
        if not installer_path.exists():
            return {"error": "Download failed"}
        
        # Install
        install_result = install_application(str(installer_path), silent=silent)
        
        # Cleanup
        try:
            installer_path.unlink()
        except:
            pass
        
        return install_result
        
    except Exception as e:
        return {"error": str(e)}


def check_application_installed(app_name: str) -> Dict:
    """
    Check if an application is installed
    """
    try:
        result = list_installed_applications()
        if "error" in result:
            return result
        
        apps = result.get("applications", [])
        matches = [app for app in apps if app_name.lower() in app["name"].lower()]
        
        return {
            "success": True,
            "installed": len(matches) > 0,
            "matches": matches
        }
        
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_installation_tools() -> List[Dict]:
    """Get application installation tool definitions"""
    return [
        {
            "name": "install_application",
            "description": "Install an application from an installer file (.exe or .msi). Supports silent installation.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "installer_path": {
                        "type": "string",
                        "description": "Path to the installer file (e.g., 'C:/Downloads/setup.exe')"
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional installer arguments"
                    },
                    "silent": {
                        "type": "boolean",
                        "description": "Install silently without user interaction (default: true)"
                    }
                },
                "required": ["installer_path"]
            }
        },
        {
            "name": "uninstall_application",
            "description": "Uninstall an application by name. Searches Windows registry for uninstaller.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Name of the application to uninstall"
                    },
                    "silent": {
                        "type": "boolean",
                        "description": "Uninstall silently (default: true)"
                    }
                },
                "required": ["app_name"]
            }
        },
        {
            "name": "list_installed_applications",
            "description": "Get a list of all installed applications from Windows registry with versions and publishers",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "check_application_installed",
            "description": "Check if a specific application is installed on the system",
            "input_schema": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Name of the application to check"
                    }
                },
                "required": ["app_name"]
            }
        },
        {
            "name": "download_and_install",
            "description": "Download an installer from a URL and install it automatically",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Direct download URL for the installer"
                    },
                    "installer_name": {
                        "type": "string",
                        "description": "Optional filename for the downloaded installer"
                    },
                    "silent": {
                        "type": "boolean",
                        "description": "Install silently (default: true)"
                    }
                },
                "required": ["url"]
            }
        }
    ]


# Map tool names to functions
INSTALLATION_FUNCTIONS = {
    "install_application": install_application,
    "uninstall_application": uninstall_application,
    "list_installed_applications": list_installed_applications,
    "check_application_installed": check_application_installed,
    "download_and_install": download_and_install
}
