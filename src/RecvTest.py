from App.ApplicationLayerFunctions import ReceiveAndSaveFile

OUTPUT_DIRECTORY = "./received_files"

def Recv():
    file_name = ReceiveAndSaveFile(OUTPUT_DIRECTORY)

    if file_name.endswith('.txt'):                      # .txt file
        print(f"Received a text file: {file_name}")
    elif file_name.endswith('.pdf'):                    # .pdf file
        print(f"Received a PDF file: {file_name}")
    else:                                               # another file
        print(f"Received an unsupported file type: {file_name}")

if __name__ == "__main__":
    Recv()