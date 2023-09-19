import unittest
from unittest.mock import patch, mock_open
import logging
from pylabtools import log_wrapper as lw

class TestLoggerSetup(unittest.TestCase):

    def setUp(self):
        # Clear existing handlers
        logging.getLogger().handlers = []

        # Initialize a logger setup instance before each test
        self.logger_setup = lw.LoggerSetup()

    def test_initialization(self):
        self.assertEqual(self.logger_setup.logger.level, logging.DEBUG)
        self.assertIsInstance(self.logger_setup.formatter, lw.JSONFormatter)

    @patch('logging.FileHandler._open', mock_open())
    def test_add_file_handler(self):
        self.logger_setup.add_file_handler(log_file_path="test.log")
        self.assertEqual(len(self.logger_setup.logger.handlers), 1)
        self.assertIsInstance(self.logger_setup.logger.handlers[0], logging.FileHandler)

    @patch.object(logging.StreamHandler, 'emit')
    def test_add_console_handler(self, mock_emit):
        self.logger_setup.add_console_handler()
        log_message = "This is a test message."
        logger = self.logger_setup.get_logger()
        logger.info(log_message)  # Make sure to log a message!

        mock_emit.assert_called()
        # The emit method takes a LogRecord as argument. So, you should access its `msg` attribute.
        self.assertIn(log_message, mock_emit.call_args[0][0].msg)
    
    def test_set_custom_format(self):
        custom_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.logger_setup.add_console_handler()
        self.logger_setup.set_custom_format(custom_format)

        for handler in self.logger_setup.logger.handlers:
            self.assertEqual(handler.formatter, custom_format)

    def test_get_logger(self):
        logger = self.logger_setup.get_logger()
        self.assertEqual(logger, self.logger_setup.logger)

if __name__ == "__main__":
    unittest.main()
