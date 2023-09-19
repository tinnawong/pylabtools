import unittest
from unittest.mock import mock_open, patch
from pylabtools import file_wrapper as fw

class TestFileFunctions(unittest.TestCase):

    def test_read_file_all_text(self):
        m = mock_open(read_data="test content")
        with patch("builtins.open", m):
            content = fw.read_file_all_text("fakepath.txt")
        self.assertEqual(content, "test content")

    def test_stream_file_by_line(self):
        m = mock_open(read_data="line1\nline2\nline3")
        with patch("builtins.open", m):
            lines = list(fw.stream_file_by_line("fakepath.txt"))
        self.assertEqual(lines, ["line1", "line2", "line3"])

    def test_write_text_to_file(self):
        m = mock_open()
        with patch("builtins.open", m):
            fw.write_text_to_file("fakepath.txt", "test content")
        m.assert_called_once_with("fakepath.txt", "w", encoding="utf-8")
        handle = m()
        handle.write.assert_called_once_with("test content")

    def test_read_json_config(self):
        mock_json_content = '{"key": "value"}'
        m = mock_open(read_data=mock_json_content)
        with patch("builtins.open", m), patch("json.load", return_value={"key": "value"}) as mock_json:
            result = fw.read_json_config("fakepath.json")
        self.assertEqual(result, {"key": "value"})
        mock_json.assert_called_once()

    def test_get_file_name_without_extension(self):
        result = fw.get_file_name_without_extension("directory/filename.extension")
        self.assertEqual(result, "filename")

    def test_get_file_name(self):
        result = fw.get_file_name("directory/filename.extension", tail="_tail", set_extension=".newext")
        self.assertEqual(result, "filename_tail.newext")

        result_no_ext = fw.get_file_name("directory/filename.extension", without_extension=True)
        self.assertEqual(result_no_ext, "filename")

        result_original_ext = fw.get_file_name("directory/filename.extension", tail="_tail")
        self.assertEqual(result_original_ext, "filename_tail.extension")

if __name__ == "__main__":
    unittest.main()
