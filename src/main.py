import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time
# from  Transports.SocketTransport.SocketTransport import SendFrame,RecvFrame
from  Transports.AudioTransport.AudioTransport import SendFrame,RecvFrame

# server GUI
class FileReceiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Receiver")
        
        self.text_area = scrolledtext.ScrolledText(root, width=50, height=15)
        self.text_area.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Waiting for incoming files...")
        self.status_label.pack(pady=5)

    def update_text_area(self, message):
        self.root.after(0, self._update_text_area, message)

    def _update_text_area(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)  # Scroll to the end

# server functionality
def start_server(app, host='127.0.0.1', port=12345):
    while True:
        data = RecvFrame()
        print("received: ",data)
        # app.update_text_area(f"Received data: {data.decode()}")
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind((host, port))
    #     s.listen(1)
    #     app.update_text_area(f"Server listening on {host}:{port}")
    #     conn, addr = s.accept()
    #     app.update_text_area(f"Connected by {addr}")
    #     with conn:
    #         while True:
    #             data = conn.recv(1024)
    #             if not data:
    #                 break
    #             

# client functionality
class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Transfer")
        self.label = tk.Label(root, text="Select a file to send:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.send_button = tk.Button(root, text="Send", command=self.send_file)
        self.send_button.pack(pady=5)

        self.file_path = ""

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.label.config(text=f"Selected file: {self.file_path}")

    def send_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        attempt = 0
        while attempt < 5:  
            # try:
            with open(self.file_path, 'rb') as f:
                data = f.read(40)  
                while data:
                    SendFrame(data)
                    data = f.read(40)
            #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #         s.connect(('127.0.0.1', 12345))

            #         messagebox.showinfo("Success", "File sent successfully!")
            #     return  
            # except ConnectionRefusedError as e:
            #     messagebox.showwarning("Warning", f"Attempt {attempt + 1}: Connection refused. Retrying...")
            #     attempt += 1
            #     time.sleep(1)  
            # except Exception as e:
            #     messagebox.showerror("Error", f"An error occurred: {e}")
            #     return

        messagebox.showerror("Error", "Failed to send file after multiple attempts.")

def run_server(app):
    start_server(app)

if __name__ == "__main__":
    # create a Tkinter root for the receiver
    receiver_root = tk.Tk()
    receiver_app = FileReceiverApp(receiver_root)

    # start the server in a separate thread with the receiver app
    server_thread = threading.Thread(target=run_server, args=(receiver_app,), daemon=True)
    server_thread.start()

    # give the server a moment to start
    time.sleep(2) 

    # create a separate Tkinter root for the sender
    sender_root = tk.Tk()
    sender_app = FileTransferApp(sender_root)

    # start the sender GUI
    sender_root.mainloop()