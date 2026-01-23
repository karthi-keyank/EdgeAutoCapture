import tkinter as tk

_log_box = None


def init_logger(log_box_widget):
    """
    Initialize logger with ScrolledText widget
    """
    global _log_box
    _log_box = log_box_widget


def log(message):
    """
    Write a message to the log box
    """
    if not _log_box:
        return

    _log_box.insert(tk.END, message + "\n")
    _log_box.see(tk.END)
