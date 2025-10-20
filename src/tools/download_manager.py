"""
Download Manager - Monitor and detect file downloads
"""

import time
import os
from typing import Dict, List
from pathlib import Path


def get_downloads_folder() -> Path:
    """Get the actual Downloads folder path (OneDrive-aware)"""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        downloads_path = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]
        winreg.CloseKey(key)
        return Path(os.path.expandvars(downloads_path))
    except:
        # Fallback
        return Path.home() / "Downloads"


def wait_for_download(file_pattern: str, timeout: int = 120, check_interval: int = 2) -> Dict:
    """
    Wait for a file matching pattern to appear and finish downloading
    
    Args:
        file_pattern: Filename pattern (e.g., "python*.exe", "setup.msi")
        timeout: Maximum seconds to wait
        check_interval: Seconds between checks
    
    Returns:
        Dict with downloaded file path or error
    """
    try:
        downloads_folder = get_downloads_folder()
        start_time = time.time()
        found_files = {}
        
        while time.time() - start_time < timeout:
            # Find matching files
            matching_files = list(downloads_folder.glob(file_pattern))
            
            for file_path in matching_files:
                # Skip .crdownload and .tmp files (incomplete downloads)
                if file_path.suffix.lower() in ['.crdownload', '.tmp', '.partial']:
                    continue
                
                # Check if file size is stable (download complete)
                file_size = file_path.stat().st_size
                
                if str(file_path) not in found_files:
                    found_files[str(file_path)] = file_size
                    continue
                
                # If size hasn't changed, download is complete
                if found_files[str(file_path)] == file_size and file_size > 0:
                    return {
                        "success": True,
                        "file_path": str(file_path),
                        "file_name": file_path.name,
                        "file_size": file_size,
                        "message": f"Download complete: {file_path.name}",
                        "waited_seconds": int(time.time() - start_time)
                    }
                
                # Update size for next check
                found_files[str(file_path)] = file_size
            
            time.sleep(check_interval)
        
        return {
            "success": False,
            "error": f"No matching file found after {timeout}s",
            "pattern": file_pattern,
            "downloads_folder": str(downloads_folder),
            "note": "Make sure you clicked the download button in the browser"
        }
        
    except Exception as e:
        return {"error": f"Failed to wait for download: {str(e)}"}


def list_recent_downloads(count: int = 10, file_extension: str = None) -> Dict:
    """
    List most recent downloads
    
    Args:
        count: Number of files to return
        file_extension: Optional filter by extension (e.g., ".exe", ".msi")
    
    Returns:
        Dict with list of recent downloads
    """
    try:
        downloads_folder = get_downloads_folder()
        
        # Get all files
        all_files = []
        for file_path in downloads_folder.iterdir():
            if file_path.is_file():
                # Skip incomplete downloads
                if file_path.suffix.lower() in ['.crdownload', '.tmp', '.partial']:
                    continue
                
                # Apply extension filter
                if file_extension and not file_path.suffix.lower() == file_extension.lower():
                    continue
                
                all_files.append(file_path)
        
        # Sort by modification time (most recent first)
        all_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Take top N
        recent_files = all_files[:count]
        
        result = []
        for file_path in recent_files:
            stat = file_path.stat()
            result.append({
                "name": file_path.name,
                "path": str(file_path),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
                "modified": time.ctime(stat.st_mtime)
            })
        
        return {
            "success": True,
            "downloads_folder": str(downloads_folder),
            "files": result,
            "count": len(result)
        }
        
    except Exception as e:
        return {"error": f"Failed to list downloads: {str(e)}"}


def find_latest_download(file_pattern: str) -> Dict:
    """
    Find the most recent file matching pattern in Downloads
    
    Args:
        file_pattern: Filename pattern (e.g., "python*.exe")
    
    Returns:
        Dict with file path or error
    """
    try:
        downloads_folder = get_downloads_folder()
        
        # Find matching files
        matching_files = list(downloads_folder.glob(file_pattern))
        
        if not matching_files:
            return {
                "success": False,
                "found": False,
                "pattern": file_pattern,
                "downloads_folder": str(downloads_folder),
                "message": f"No files matching '{file_pattern}' found in Downloads"
            }
        
        # Skip incomplete downloads
        complete_files = [f for f in matching_files 
                         if f.suffix.lower() not in ['.crdownload', '.tmp', '.partial']]
        
        if not complete_files:
            return {
                "success": False,
                "found": False,
                "message": f"Found {len(matching_files)} file(s) but all are incomplete downloads",
                "incomplete_files": [f.name for f in matching_files]
            }
        
        # Get most recent
        latest_file = max(complete_files, key=lambda p: p.stat().st_mtime)
        stat = latest_file.stat()
        
        return {
            "success": True,
            "found": True,
            "file_path": str(latest_file),
            "file_name": latest_file.name,
            "file_size": stat.st_size,
            "size_mb": round(stat.st_size / 1024 / 1024, 2),
            "modified": time.ctime(stat.st_mtime)
        }
        
    except Exception as e:
        return {"error": f"Failed to find download: {str(e)}"}


def check_download_in_progress(file_pattern: str = None) -> Dict:
    """
    Check if any downloads are currently in progress
    
    Args:
        file_pattern: Optional pattern to check specific download
    
    Returns:
        Dict with download status
    """
    try:
        downloads_folder = get_downloads_folder()
        
        # Look for incomplete download files
        incomplete_extensions = ['.crdownload', '.tmp', '.partial']
        
        if file_pattern:
            # Check specific pattern
            all_matches = list(downloads_folder.glob(file_pattern))
            incomplete = [f for f in all_matches if f.suffix.lower() in incomplete_extensions]
        else:
            # Check all downloads
            incomplete = [f for f in downloads_folder.iterdir() 
                         if f.is_file() and f.suffix.lower() in incomplete_extensions]
        
        if incomplete:
            return {
                "success": True,
                "downloading": True,
                "count": len(incomplete),
                "files": [f.name for f in incomplete],
                "message": f"{len(incomplete)} download(s) in progress"
            }
        else:
            return {
                "success": True,
                "downloading": False,
                "message": "No downloads in progress"
            }
            
    except Exception as e:
        return {"error": f"Failed to check downloads: {str(e)}"}


# Tool definitions
def get_download_manager_tools() -> List[Dict]:
    """Get download manager tool definitions"""
    return [
        {
            "name": "wait_for_download",
            "description": "Wait for a file to finish downloading. Monitors Downloads folder for file matching pattern and waits until download completes. Use after user clicks download button in browser. Example: 'wait for python*.exe to download'",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_pattern": {
                        "type": "string",
                        "description": "Filename pattern with wildcards (e.g., 'python*.exe', 'setup*.msi', '*.pdf')"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum seconds to wait (default: 120)",
                        "default": 120
                    },
                    "check_interval": {
                        "type": "integer",
                        "description": "Seconds between checks (default: 2)",
                        "default": 2
                    }
                },
                "required": ["file_pattern"]
            }
        },
        {
            "name": "list_recent_downloads",
            "description": "List most recent files in Downloads folder. Useful to see what was downloaded recently or find installer files.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "description": "Number of files to return (default: 10)",
                        "default": 10
                    },
                    "file_extension": {
                        "type": "string",
                        "description": "Optional: Filter by extension (e.g., '.exe', '.msi', '.pdf')"
                    }
                },
                "required": []
            }
        },
        {
            "name": "find_latest_download",
            "description": "Find the most recent file matching pattern in Downloads. Returns immediately (doesn't wait). Use to check if file already downloaded.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_pattern": {
                        "type": "string",
                        "description": "Filename pattern with wildcards (e.g., 'python*.exe')"
                    }
                },
                "required": ["file_pattern"]
            }
        },
        {
            "name": "check_download_in_progress",
            "description": "Check if downloads are currently in progress (looks for .crdownload files). Useful to know if user is still downloading.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_pattern": {
                        "type": "string",
                        "description": "Optional: Check specific download pattern"
                    }
                },
                "required": []
            }
        }
    ]


# Function mapping
DOWNLOAD_MANAGER_FUNCTIONS = {
    "wait_for_download": wait_for_download,
    "list_recent_downloads": list_recent_downloads,
    "find_latest_download": find_latest_download,
    "check_download_in_progress": check_download_in_progress
}
