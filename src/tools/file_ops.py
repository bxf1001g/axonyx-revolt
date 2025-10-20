"""
File System Operations Tools
"""
import os
import shutil
from pathlib import Path
from typing import Dict, List


def list_directory(path: str) -> Dict:
    """List contents of a directory"""
    try:
        path_obj = Path(path).expanduser()
        if not path_obj.exists():
            return {"error": f"Path does not exist: {path}"}
        
        items = []
        for item in path_obj.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            })
        
        return {"success": True, "items": items, "count": len(items)}
    except Exception as e:
        return {"error": str(e)}


def create_directory(path: str) -> Dict:
    """Create a new directory"""
    try:
        path_obj = Path(path).expanduser()
        path_obj.mkdir(parents=True, exist_ok=True)
        return {"success": True, "message": f"Created directory: {path}"}
    except Exception as e:
        return {"error": str(e)}


def create_file(path: str, content: str = "") -> Dict:
    """Create a new file with optional content"""
    try:
        path_obj = Path(path).expanduser()
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        path_obj.write_text(content, encoding='utf-8')
        return {"success": True, "message": f"Created file: {path}"}
    except Exception as e:
        return {"error": str(e)}


def read_file(path: str) -> Dict:
    """Read contents of a file"""
    try:
        path_obj = Path(path).expanduser()
        if not path_obj.exists():
            return {"error": f"File does not exist: {path}"}
        
        content = path_obj.read_text(encoding='utf-8')
        return {"success": True, "content": content, "size": len(content)}
    except Exception as e:
        return {"error": str(e)}


def delete_path(path: str) -> Dict:
    """Delete a file or directory"""
    try:
        path_obj = Path(path).expanduser()
        if not path_obj.exists():
            return {"error": f"Path does not exist: {path}"}
        
        if path_obj.is_dir():
            shutil.rmtree(path_obj)
            return {"success": True, "message": f"Deleted directory: {path}"}
        else:
            path_obj.unlink()
            return {"success": True, "message": f"Deleted file: {path}"}
    except Exception as e:
        return {"error": str(e)}


def move_path(source: str, destination: str) -> Dict:
    """Move/rename a file or directory"""
    try:
        src = Path(source).expanduser()
        dst = Path(destination).expanduser()
        
        if not src.exists():
            return {"error": f"Source does not exist: {source}"}
        
        shutil.move(str(src), str(dst))
        return {"success": True, "message": f"Moved {source} to {destination}"}
    except Exception as e:
        return {"error": str(e)}


def copy_path(source: str, destination: str) -> Dict:
    """Copy a file or directory"""
    try:
        src = Path(source).expanduser()
        dst = Path(destination).expanduser()
        
        if not src.exists():
            return {"error": f"Source does not exist: {source}"}
        
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        
        return {"success": True, "message": f"Copied {source} to {destination}"}
    except Exception as e:
        return {"error": str(e)}


# Tool definitions for Claude
def get_file_tools() -> List[Dict]:
    """Get file operation tool definitions"""
    return [
        {
            "name": "list_directory",
            "description": "List all files and folders in a directory. Use for browsing file system.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list. Use special paths like 'Desktop' or 'Documents'"
                    }
                },
                "required": ["path"]
            }
        },
        {
            "name": "create_directory",
            "description": "Create a new directory/folder at the specified path",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The full path where the directory should be created"
                    }
                },
                "required": ["path"]
            }
        },
        {
            "name": "create_file",
            "description": "Create a new file with optional text content",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The full path where the file should be created"
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to write to the file"
                    }
                },
                "required": ["path"]
            }
        },
        {
            "name": "read_file",
            "description": "Read the contents of a text file",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["path"]
            }
        },
        {
            "name": "delete_path",
            "description": "Delete a file or directory. Use with caution!",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to delete"
                    }
                },
                "required": ["path"]
            }
        },
        {
            "name": "move_path",
            "description": "Move or rename a file or directory",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "The current path"
                    },
                    "destination": {
                        "type": "string",
                        "description": "The new path"
                    }
                },
                "required": ["source", "destination"]
            }
        },
        {
            "name": "copy_path",
            "description": "Copy a file or directory to a new location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "The path to copy"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Where to copy it"
                    }
                },
                "required": ["source", "destination"]
            }
        }
    ]


# Map tool names to functions
FILE_FUNCTIONS = {
    "list_directory": list_directory,
    "create_directory": create_directory,
    "create_file": create_file,
    "read_file": read_file,
    "delete_path": delete_path,
    "move_path": move_path,
    "copy_path": copy_path
}
