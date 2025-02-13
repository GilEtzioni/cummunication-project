# function: SendFile(filepath, filelen, filename)
# check if the function sends the file successfully and handles exceptions

import unittest
from unittest.mock import patch, mock_open
from Transports.AudioTransport.DataLayer.AudioTransport import SendFrame
from App.TransportLayerFunctions import SendFile

class TestSendFile(unittest.TestCase):

    @patch("App.TransportLayerFunctions.time.sleep")
    @patch("App.TransportLayerFunctions.SendFrame")
    @patch("App.TransportLayerFunctions.logger")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test data")

    # send succes file
    def test_send_file_success(self, mock_file, mock_logger, mock_sendframe, mock_sleep):
        filepath = "test.txt"
        filelen = 8
        filename = "test.txt"

        SendFile(filepath, filelen, filename)

        # assertions
        mock_logger.debug.assert_any_call(f"File details: Name='{filename}', Length={filelen} bytes, filepath={filepath}")
        mock_logger.info.assert_any_call("Sending file content in chunks of 40 bytes...")
        mock_logger.info.assert_any_call(f"File '{filename}' sent successfully.")
        mock_sendframe.assert_called()

    @patch("App.TransportLayerFunctions.logger")
    @patch("builtins.open", new_callable=mock_open)
    @patch("App.TransportLayerFunctions.SendFrame")

    def test_send_file_exception(self, mock_sendframe, mock_file, mock_logger):
        # mock file opening --> raise an exception
        mock_file.side_effect = Exception("File error")

        filepath = "test.txt"
        filelen = 8
        filename = "test.txt"

        with self.assertRaises(Exception):
            SendFile(filepath, filelen, filename)

        mock_logger.error.assert_any_call("Error in SendFile: File error") # assert


if __name__ == "__main__":
    unittest.main()
