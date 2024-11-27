import logging
import tkinter as tk
import queue
from LogSetup import SetupLogger

class LogSender:
    def __init__(self, output_text, log_queue) -> None:
        self.output_text = output_text
        self.log_queue = log_queue
        self.process_queue()  # start processing the queue

    def print_to_gui(self, msg: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, msg + "\n")   # insert the message into the Text widget
        self.output_text.configure(state="disabled")  # disable editing the Text widget
        self.output_text.yview(tk.END)                # scroll to the end

    def process_queue(self) -> None:
        """
        Processes messages from the queue and updates the GUI.
        """
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.print_to_gui(msg)
        except queue.Empty:
            pass

        # schedule the next check
        self.output_text.after(100, self.process_queue)

    def write_log(self, msg: logging.LogRecord) -> None:
        if msg.levelno == logging.INFO:
            self.log_queue.put(f"INFO: [{msg.module}] {msg.message}")
        elif msg.levelno == logging.WARNING:
            self.log_queue.put(f"WARN: [{msg.module}] {msg.message}")
        elif msg.levelno == logging.ERROR:
            self.log_queue.put(f"ERROR: [{msg.module}] {msg.message}")

class GuiHandler(logging.Handler):
    def __init__(self, output_text) -> None:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, GuiHandler):
                logging.getLogger().removeHandler(handler)

        self.log_queue = queue.Queue()  # create a thread-safe queue
        self.sender = LogSender(output_text=output_text, log_queue=self.log_queue)
        logging.Handler.__init__(self)

    def emit(self, record) -> None:
        self.sender.write_log(record)
