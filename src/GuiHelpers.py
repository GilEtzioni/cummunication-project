import logging
import tkinter as tk
import LogSetup
from LogSetup import  SetupLogger

class LogSender:
    def __init__(self,output_text) -> None:
        self.output_text = output_text
        pass
    def printToGui(self, msg: str) -> None:
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, msg+"\n")  # Insert the message into the Text widget
        self.output_text.configure(state="disabled")  # Disable editing the Text widget
        self.output_text.yview(tk.END) 

    def writeLog(self, msg: logging.LogRecord) -> None:
        # not printing debug
        if msg.levelno == logging.INFO:
            self.printToGui(f"INFO: [{msg.module}] {msg.message}")
        if msg.levelno == logging.WARNING:
            self.printToGui(f"WARN: [{msg.module}] {msg.message}")
        if msg.levelno == logging.ERROR:
            self.printToGui(f"ERROR: [{msg.module}] {msg.message}")

class GuiHandler(logging.Handler):

    def __init__(self,output_text )-> None:
        self.sender = LogSender(output_text=output_text)
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        self.sender.writeLog(record)
