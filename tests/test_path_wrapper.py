import os
import tempfile
import unittest
from pylabtools import path_wrapper as pw
class TestFileOperations(unittest.TestCase):

    def setUp(self):
        # Creating a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()

        # Test file and directory
        self.test_file_path = os.path.join(self.test_dir.name, "test.txt")
        with open(self.test_file_path, 'w') as f:
            f.write("test content")

        self.test_subdir = os.path.join(self.test_dir.name, "subdir")
        os.makedirs(self.test_subdir)
    
    def tearDown(self):
        # Cleaning up the temporary directory
        self.test_dir.cleanup()

    def test_get_all_files(self):
        # Recursive search
        files = pw.get_all_files(self.test_dir.name, recursive=True)
        self.assertIn(self.test_file_path, files)

        # Non-recursive search
        files = pw.get_all_files(self.test_dir.name, recursive=False)
        self.assertIn(self.test_file_path, files)
        self.assertNotIn(self.test_subdir, files)

        # Filter by extension
        files = pw.get_all_files(self.test_dir.name, endswith=".txt", recursive=False)
        self.assertIn(self.test_file_path, files)

    def test_get_current_folder_name(self):
        folder_name = pw.get_current_folder_name(self.test_file_path)
        self.assertEqual(folder_name, os.path.basename(self.test_dir.name))

    def test_get_previous_path(self):
        prev_path = pw.get_previous_path(self.test_file_path)
        self.assertEqual(prev_path, self.test_dir.name)

    def test_get_all_directories(self):
        dirs = pw.get_all_directories(self.test_dir.name)
        self.assertIn(self.test_subdir, dirs)

if __name__ == "__main__":
    unittest.main()
