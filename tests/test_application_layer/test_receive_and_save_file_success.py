# function: the ReceiveAndSaveFile
# check if the function get the file successful

# example: when a file is received, it should be saved in the correct path.
#          then, the function should return the full path of the file.

import unittest
from unittest.mock import patch
from App.ApplicationLayerFunctions import ReceiveAndSaveFile

class TestReceiveAndSaveFileSuccess(unittest.TestCase):

    @patch("App.ApplicationLayerFunctions.ReceiveFile")
    @patch("App.ApplicationLayerFunctions.os.path.join")
    @patch("App.ApplicationLayerFunctions.logger")
    def test_receive_and_save_file_success(self, mock_logger, mock_join, mock_receivefile):

        # mock values
        mock_receivefile.return_value = "example.txt"
        mock_join.return_value = "path/to/output/example.txt"

        # call the function
        result = ReceiveAndSaveFile("path/to/output")

        # assertions
        self.assertEqual(result, "path/to/output/example.txt")
        mock_logger.info.assert_any_call("Waiting to receive file...")
        mock_logger.info.assert_any_call("File received and saved as 'path/to/output/example.txt'.")

if __name__ == "__main__":
    unittest.main()
