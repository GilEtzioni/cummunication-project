# function: CreateHeader(header: dict)
# test convert:     header --> byte array

from unittest.mock import patch, mock_open
import unittest
from App.TransportLayerFunctions import CreateHeader

class TestCreateHeader(unittest.TestCase):

    @patch("App.TransportLayerFunctions.logger")
    def test_create_header_success(self, mock_logger):
        header = {
            "FileNamelen": 8,
            "FileName": "test.txt",
            "FileLen": 100
        }
        header_bytes = CreateHeader(header)

        self.assertEqual(len(header_bytes), 40)
        mock_logger.info.assert_called_with(f"header bytes: {header_bytes}")

    @patch("App.TransportLayerFunctions.logger")
    def test_create_header_exception(self, mock_logger):
        header = {"FileName": "test.txt"} 

        with self.assertRaises(KeyError):
            CreateHeader(header)

        mock_logger.error.assert_called()

if __name__ == "__main__":
    unittest.main()
