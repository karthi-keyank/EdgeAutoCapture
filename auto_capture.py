import os
import base64
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText

from selenium import webdriver
from pynput import keyboard

from image_pdf_scanner import scan_and_convert


# ======================================================
# GLOBAL STATE
# ======================================================
ACTIVE_FOLDER = None
CAPTURE_ENABLED = True

BACK_STACK = []
FORWARD_STACK = []

# ======================================================
# SELENIUM (EDGE) – Selenium Manager handles driver
# ======================================================
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Edge(options=options)

# ======================================================
# LOGGING
# ======================================================
def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# ======================================================
# FOLDER NAVIGATION
# ======================================================
def set_active_folder(path, record_history=True):
    global ACTIVE_FOLDER
    path = os.path.normpath(path)

    if not os.path.isdir(path):
        messagebox.showerror("Invalid Folder", f"Folder does not exist:\n{path}")
        return

    if ACTIVE_FOLDER and record_history:
        BACK_STACK.append(ACTIVE_FOLDER)
        FORWARD_STACK.clear()

    ACTIVE_FOLDER = path
    path_var.set(ACTIVE_FOLDER)
    log(f"Active folder: {ACTIVE_FOLDER}")

def go_back():
    if BACK_STACK:
        FORWARD_STACK.append(ACTIVE_FOLDER)
        set_active_folder(BACK_STACK.pop(), record_history=False)

def go_forward():
    if FORWARD_STACK:
        BACK_STACK.append(ACTIVE_FOLDER)
        set_active_folder(FORWARD_STACK.pop(), record_history=False)

# ======================================================
# FULL PAGE SCREENSHOT (DevTools – SAFE)
# ======================================================
def capture_full_page():
    if not CAPTURE_ENABLED:
        log("Capture paused – ignored")
        return

    if not ACTIVE_FOLDER:
        log("No active folder selected")
        return

    try:
        handles = driver.window_handles
        if not handles:
            log("Edge window closed")
            return

        driver.switch_to.window(handles[0])

        result = driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "format": "png",
                "captureBeyondViewport": True,
                "fromSurface": True
            }
        )

        if not result or "data" not in result:
            log("Screenshot failed (no data)")
            return

        image = base64.b64decode(result["data"])
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
        path = os.path.join(ACTIVE_FOLDER, filename)

        with open(path, "wb") as f:
            f.write(image)

        log(f"Saved: {path}")

    except Exception as e:
        log(f"Capture error: {e}")

# ======================================================
# KEYBOARD HOTKEY
# ======================================================
def on_press(key):
    try:
        if key.char.lower() == 's':
            capture_full_page()
    except AttributeError:
        if key == keyboard.Key.esc:
            on_close()
            return False

keyboard.Listener(on_press=on_press).start()

# ======================================================
# FOLDER ACTIONS
# ======================================================
def choose_folder():
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        set_active_folder(folder)

def create_subfolder():
    if not ACTIVE_FOLDER:
        messagebox.showwarning("Warning", "Select a folder first")
        return

    name = simpledialog.askstring("Subfolder Name", "Enter subfolder name:")
    if name:
        path = os.path.join(ACTIVE_FOLDER, name)
        os.makedirs(path, exist_ok=True)
        set_active_folder(path)

def on_path_enter(event):
    set_active_folder(path_var.get())

# ======================================================
# CAPTURE TOGGLE
# ======================================================
def toggle_capture():
    global CAPTURE_ENABLED
    CAPTURE_ENABLED = not CAPTURE_ENABLED

    if CAPTURE_ENABLED:
        toggle_btn.config(text="Pause Capture", bg="#e74c3c")
        status_lbl.config(text="RUNNING", fg="green")
        log("Capture resumed")
    else:
        toggle_btn.config(text="Resume Capture", bg="#2ecc71")
        status_lbl.config(text="PAUSED", fg="red")
        log("Capture paused")

# ======================================================
# IMAGE TO PDF CONVERSION
# ======================================================

def convert_all_images_to_pdf():
    if not ACTIVE_FOLDER:
        messagebox.showwarning("Warning", "Select a folder first")
        return

    log("Scanning folders for images...")
    scan_and_convert(ACTIVE_FOLDER, logger=log)
    log("Image to PDF conversion completed")


# ======================================================
# GUI
# ======================================================
root = tk.Tk()
root.title("SkillRack Capture Tool")
root.geometry("720x560")
root.minsize(650, 520)

tk.Label(
    root,
    text="SkillRack Capture Tool",
    font=("Segoe UI", 16, "bold")
).pack(pady=10)

main = tk.Frame(root)
main.pack(fill="both", expand=True, padx=10)
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)

# ---- Navigation Bar ----
tk.Label(main, text="Folder Navigation", font=("Segoe UI", 12, "bold")) \
    .grid(row=0, column=0, columnspan=2, sticky="w")

nav = tk.Frame(main)
nav.grid(row=1, column=0, columnspan=2, sticky="ew")
nav.columnconfigure(1, weight=1)

tk.Button(nav, text="◀ Back", command=go_back).grid(row=0, column=0)
tk.Button(nav, text="Forward ▶", command=go_forward).grid(row=0, column=2)

path_var = tk.StringVar()
path_entry = tk.Entry(nav, textvariable=path_var)
path_entry.grid(row=0, column=1, sticky="ew", padx=5)
path_entry.bind("<Return>", on_path_enter)

tk.Button(main, text="Select Folder", command=choose_folder)\
    .grid(row=2, column=0, sticky="ew", pady=5)

tk.Button(main, text="Create Subfolder", command=create_subfolder)\
    .grid(row=2, column=1, sticky="ew", pady=5)

# ===== Image → PDF (Folder Operation) =====
tk.Button(
    main,
    text="Convert Images → PDF",
    command=convert_all_images_to_pdf,
    bg="#3498db",
    fg="white",
    font=("Segoe UI", 10, "bold")
).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(5, 10))

# ---- Capture Controls ----
tk.Label(main, text="Capture Control", font=("Segoe UI", 12, "bold")) \
    .grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))

toggle_btn = tk.Button(
    main,
    text="Pause Capture",
    bg="#e74c3c",
    fg="white",
    command=toggle_capture
)
toggle_btn.grid(row=5, column=0, sticky="ew")

status_lbl = tk.Label(
    main,
    text="RUNNING",
    font=("Segoe UI", 12, "bold"),
    fg="green"
)
status_lbl.grid(row=5, column=1)

# ---- Log ----
tk.Label(main, text="Activity Log", font=("Segoe UI", 12, "bold")) \
    .grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))

log_box = ScrolledText(main, height=8, wrap="word")
log_box.grid(row=7, column=0, columnspan=2, sticky="nsew")
main.rowconfigure(7, weight=1)

log(
    "Instructions:\n"
    "- Select or navigate to the main/root folder\n"
    "- Capture screenshots using 'S' key as usual\n"
    "- Images are saved in the active folder\n"
    "- Click 'Convert Images → PDF' to scan all subfolders\n"
    "- Each folder containing images will get its own PDF\n"
    "- PDFs are saved inside the same image folders\n"
    "- Pause capture when typing paths manually\n"
    "- Press ESC or close window to exit"
)


# ======================================================
# EXIT
# ======================================================
def on_close():
    try:
        driver.quit()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
