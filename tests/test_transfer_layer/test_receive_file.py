# function: ReceiveFile(output_dir: str)
# check receive and save a file successfully and handle exception

import unittest
from unittest.mock import patch, mock_open
from Transports.AudioTransport.DataLayer.AudioTransport import RecvFrame
from App.TransportLayerFunctions import ReceiveFile

class TestReceiveFile(unittest.TestCase):

    @patch("App.TransportLayerFunctions.logger")
    @patch("App.TransportLayerFunctions.RecvFrame")
    @patch("builtins.open", new_callable=mock_open)
    def test_receive_file_success(self, mock_file, mock_recvframe, mock_logger):
        output_dir = "/path/to/output"
        mock_recvframe.side_effect = [
            b"\x00\x00\x00\x08" + b"test.txt".ljust(32, b"\x00") + b"\x00\x00\x00\x08",  # Valid header (40 bytes)
            b"test data"  # File chunk
        ]

        filename = ReceiveFile(output_dir)

        # Assertions
        self.assertEqual(filename, "test.txt")
        mock_logger.info.assert_any_call("File 'test.txt' has been processed.")

    @patch("App.TransportLayerFunctions.logger")
    @patch("App.TransportLayerFunctions.RecvFrame")
    def test_receive_file_invalid_header(self, mock_recvframe, mock_logger):
        mock_recvframe.return_value = b"invalid header"  # Incorrect header size

        with self.assertRaises(ValueError):
            ReceiveFile("/path/to/output")

        # Match the actual logged error message
        mock_logger.error.assert_called_with("Error in ReceiveFile: Invalid header size.")

if __name__ == "__main__":
    unittest.main()
