"""
Unit tests for file operations tools
"""
import unittest
from pathlib import Path
import tempfile
import shutil
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools.file_ops import (
    list_directory, create_directory, create_file,
    read_file, delete_path, move_path, copy_path
)


class TestFileOperations(unittest.TestCase):
    """Test file operation tools"""
    
    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up temporary directory"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_create_directory(self):
        """Test directory creation"""
        new_dir = self.test_dir / "test_folder"
        result = create_directory(str(new_dir))
        
        self.assertTrue(result.get("success"))
        self.assertTrue(new_dir.exists())
    
    def test_create_file(self):
        """Test file creation with content"""
        test_file = self.test_dir / "test.txt"
        content = "Hello World"
        result = create_file(str(test_file), content)
        
        self.assertTrue(result.get("success"))
        self.assertTrue(test_file.exists())
        self.assertEqual(test_file.read_text(), content)
    
    def test_read_file(self):
        """Test file reading"""
        test_file = self.test_dir / "read_test.txt"
        content = "Test content"
        test_file.write_text(content)
        
        result = read_file(str(test_file))
        
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("content"), content)
    
    def test_list_directory(self):
        """Test directory listing"""
        # Create some test files
        (self.test_dir / "file1.txt").touch()
        (self.test_dir / "file2.txt").touch()
        (self.test_dir / "subdir").mkdir()
        
        result = list_directory(str(self.test_dir))
        
        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("count"), 3)
    
    def test_delete_path(self):
        """Test file deletion"""
        test_file = self.test_dir / "delete_me.txt"
        test_file.touch()
        
        result = delete_path(str(test_file))
        
        self.assertTrue(result.get("success"))
        self.assertFalse(test_file.exists())
    
    def test_move_path(self):
        """Test file moving"""
        source = self.test_dir / "source.txt"
        source.write_text("content")
        dest = self.test_dir / "dest.txt"
        
        result = move_path(str(source), str(dest))
        
        self.assertTrue(result.get("success"))
        self.assertFalse(source.exists())
        self.assertTrue(dest.exists())
    
    def test_copy_path(self):
        """Test file copying"""
        source = self.test_dir / "original.txt"
        source.write_text("content")
        dest = self.test_dir / "copy.txt"
        
        result = copy_path(str(source), str(dest))
        
        self.assertTrue(result.get("success"))
        self.assertTrue(source.exists())
        self.assertTrue(dest.exists())


if __name__ == "__main__":
    unittest.main()
