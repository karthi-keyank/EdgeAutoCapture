import os
from tkinter import filedialog, messagebox

import core.state as state
from core.logger import log

# =====================================
# UI CALLBACK (injected from UI layer)
# =====================================
_update_path_ui = None


def register_path_updater(callback):
    """
    Register a function that updates the path Entry UI
    """
    global _update_path_ui
    _update_path_ui = callback


# =====================================
# CORE FOLDER LOGIC
# =====================================
def set_active_folder(path, record_history=True):
    path = os.path.normpath(path)

    if not os.path.isdir(path):
        messagebox.showerror(
            "Invalid Folder",
            f"Folder does not exist:\n{path}"
        )
        log(f"Invalid folder path: {path}", "WARN")
        return

    if state.ACTIVE_FOLDER and record_history:
        state.BACK_STACK.append(state.ACTIVE_FOLDER)
        state.FORWARD_STACK.clear()

    state.ACTIVE_FOLDER = path
    log(f"Active folder set: {state.ACTIVE_FOLDER}", "NAV")

    # Update navigation bar UI
    if _update_path_ui:
        _update_path_ui(state.ACTIVE_FOLDER)


def go_back():
    if not state.BACK_STACK:
        log("Back navigation ignored – no history", "WARN")
        return

    state.FORWARD_STACK.append(state.ACTIVE_FOLDER)
    previous = state.BACK_STACK.pop()
    log(f"Navigating back to: {previous}", "NAV")
    set_active_folder(previous, record_history=False)


def go_forward():
    if not state.FORWARD_STACK:
        log("Forward navigation ignored – no history", "WARN")
        return

    state.BACK_STACK.append(state.ACTIVE_FOLDER)
    next_path = state.FORWARD_STACK.pop()
    log(f"Navigating forward to: {next_path}", "NAV")
    set_active_folder(next_path, record_history=False)


def choose_folder():
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        log(f"Folder selected via dialog: {folder}", "NAV")
        set_active_folder(folder)
    else:
        log("Folder selection cancelled", "SYSTEM")


def create_subfolder():
    if not state.ACTIVE_FOLDER:
        messagebox.showwarning(
            "Warning",
            "Select a folder first"
        )
        log("Subfolder creation ignored – no active folder", "WARN")
        return

    from tkinter import simpledialog

    name = simpledialog.askstring(
        "Subfolder Name",
        "Enter subfolder name:"
    )

    if not name:
        log("Subfolder creation cancelled", "SYSTEM")
        return

    path = os.path.join(state.ACTIVE_FOLDER, name)

    try:
        os.makedirs(path, exist_ok=True)
        log(f"Subfolder created: {path}", "NAV")
        set_active_folder(path)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Failed to create folder:\n{e}"
        )
        log(f"Failed to create subfolder: {e}", "ERROR")
