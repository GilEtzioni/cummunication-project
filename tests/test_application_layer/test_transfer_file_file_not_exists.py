# function: TransferFile(filepath: str)
# check the function when the file does not exist

# example: if the file path does not show to an existing file on the computer,
#          the function should print an error message

import unittest
from unittest.mock import patch
from App.ApplicationLayerFunctions import TransferFile

class TestTransferFileFileNotExists(unittest.TestCase):

    @patch("App.ApplicationLayerFunctions.logger")
    def test_transfer_file_file_not_exists(self, mock_logger):
        # mock the file does not exist
        with patch("App.ApplicationLayerFunctions.os.path.exists", return_value=False):
            TransferFile("path/to/nonexistent.txt") # this is none exist file path

        # assertions
        mock_logger.error.assert_called_with("File 'path/to/nonexistent.txt' does not exist.")

if __name__ == "__main__":
    unittest.main()
