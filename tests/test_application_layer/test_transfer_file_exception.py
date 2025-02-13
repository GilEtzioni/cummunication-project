# function: TransferFile(filepath: str)
# check the function when an exception occurs during file transfer

# example: if we get an unexpected error while sending a file (e.g., network error),
#          the function should print the error message and handle the exception.

import unittest
from unittest.mock import patch
from App.ApplicationLayerFunctions import TransferFile

class TestTransferFileException(unittest.TestCase):

    @patch("App.ApplicationLayerFunctions.os.path.getsize", return_value=100)
    @patch("App.ApplicationLayerFunctions.os.path.basename", return_value="example.txt")
    @patch("App.ApplicationLayerFunctions.SendFile")
    @patch("App.ApplicationLayerFunctions.os.path.exists", return_value=True)
    @patch("App.ApplicationLayerFunctions.logger")
    def test_transfer_file_exception(self, mock_logger, mock_exists, mock_sendfile, mock_getsize, mock_basename):
        # mock SendFile() to raise an exception
        mock_sendfile.side_effect = Exception("Mocked exception")

        TransferFile("path/to/example.txt")  # call the function

        # assertions
        mock_logger.error.assert_called_with("Error during file transfer: Mocked exception")  # Verify the error log

if __name__ == "__main__":
    unittest.main()
