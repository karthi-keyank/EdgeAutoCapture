import os
from tkinter import filedialog, messagebox

import core.state as state
from core.logger import log


def set_active_folder(path, record_history=True):
    path = os.path.normpath(path)

    if not os.path.isdir(path):
        messagebox.showerror(
            "Invalid Folder",
            f"Folder does not exist:\n{path}"
        )
        return

    if state.ACTIVE_FOLDER and record_history:
        state.BACK_STACK.append(state.ACTIVE_FOLDER)
        state.FORWARD_STACK.clear()

    state.ACTIVE_FOLDER = path
    log(f"Active folder: {state.ACTIVE_FOLDER}")


def go_back():
    if not state.BACK_STACK:
        return

    state.FORWARD_STACK.append(state.ACTIVE_FOLDER)
    previous = state.BACK_STACK.pop()
    set_active_folder(previous, record_history=False)


def go_forward():
    if not state.FORWARD_STACK:
        return

    state.BACK_STACK.append(state.ACTIVE_FOLDER)
    next_path = state.FORWARD_STACK.pop()
    set_active_folder(next_path, record_history=False)


def choose_folder():
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        set_active_folder(folder)


def create_subfolder():
    if not state.ACTIVE_FOLDER:
        messagebox.showwarning(
            "Warning",
            "Select a folder first"
        )
        return

    from tkinter import simpledialog

    name = simpledialog.askstring(
        "Subfolder Name",
        "Enter subfolder name:"
    )

    if not name:
        return

    path = os.path.join(state.ACTIVE_FOLDER, name)
    os.makedirs(path, exist_ok=True)
    set_active_folder(path)
