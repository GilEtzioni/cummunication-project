from App.ApplicationLayerFunctions import TransferFile

FILE_TO_SEND = "./pytest.ini"

def Send():
    TransferFile(FILE_TO_SEND)

if __name__ == "__main__":
    Send()