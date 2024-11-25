# function: TransferFile(filepath: str)
# create new temp file, and check if the file transfer successful

# example: the function should process the file correctly, and call SendFile() with the right params,
#          and print success messages.

import unittest
from unittest.mock import patch
from App.ApplicationLayerFunctions import TransferFile
import tempfile
import os

class TestTransferFileSuccess(unittest.TestCase):

    @patch("App.ApplicationLayerFunctions.SendFile")
    @patch("App.ApplicationLayerFunctions.os.path.getsize")
    @patch("App.ApplicationLayerFunctions.os.path.basename")
    @patch("App.ApplicationLayerFunctions.os.path.exists")
    @patch("App.ApplicationLayerFunctions.logger")
    def test_transfer_file_success(self, mock_logger, mock_exists, mock_basename, mock_getsize, mock_sendfile):
    # create a temporary file to simulate the file being sent
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"This is a test file.")  # Write content to simulate a file
            temp_file.flush()
            temp_file_path = temp_file.name

        try:
            # mock values
            mock_exists.return_value = True
            mock_basename.return_value = os.path.basename(temp_file_path)
            mock_getsize.return_value = os.path.getsize(temp_file_path)

            TransferFile(temp_file_path) # call the function

            # assertions
            mock_logger.debug.assert_called_with(f"Preparing to send file: {temp_file_path}")
            mock_logger.info.assert_any_call(f"Starting SendFile from {temp_file_path}")
            mock_logger.info.assert_any_call(f"File '{temp_file_path}' sent successfully.")
            mock_sendfile.assert_called_once_with(temp_file_path, os.path.getsize(temp_file_path), os.path.basename(temp_file_path))

        finally:
            # clean up the temporary file
            os.remove(temp_file_path)

if __name__ == "__main__":
    unittest.main()