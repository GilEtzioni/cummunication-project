# function: the ReceiveAndSaveFile
# check if the function raise an exception during file reception.

# example: if an error occurs while receiving the file, the function should raise an error and return None

import unittest
from unittest.mock import patch
from App.ApplicationLayerFunctions import ReceiveAndSaveFile

class TestReceiveAndSaveFileException(unittest.TestCase):

    @patch("App.ApplicationLayerFunctions.ReceiveFile", side_effect=Exception("Mocked exception"))
    @patch("App.ApplicationLayerFunctions.logger")
    def test_receive_and_save_file_exception(self, mock_logger, mock_receivefile):

        result = ReceiveAndSaveFile("path/to/output") # call the function

        self.assertIsNone(result)                     # assertions
        mock_logger.error.assert_called_with("Error during file reception: Mocked exception. try again.")

if __name__ == "__main__":
    unittest.main()
