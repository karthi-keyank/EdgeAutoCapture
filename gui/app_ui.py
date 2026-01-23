import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import core.state as state
from core.logger import init_logger, log
from folders.navigation import (
    choose_folder,
    create_subfolder,
    go_back,
    go_forward,
    set_active_folder
)
from pdf.image_pdf_scanner import scan_and_convert
from browser.browser_factory import create_browser


def build_ui(app_context):
    root = app_context["root"]

    # ==============================
    # TITLE
    # ==============================
    tk.Label(
        root,
        text="Capture Tool",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=10)

    main = tk.Frame(root)
    main.pack(fill="both", expand=True, padx=10)
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=1)

    # ==============================
    # BROWSER SELECTION
    # ==============================
    tk.Label(
        main,
        text="Browser Selection",
        font=("Segoe UI", 12, "bold")
    ).grid(row=0, column=0, columnspan=2, sticky="w")

    browser_var = tk.StringVar(value="edge")

    tk.OptionMenu(
        main,
        browser_var,
        "edge",
        "chrome"
    ).grid(row=1, column=0, sticky="ew")

    def start_browser():
        if app_context.get("driver"):
            log("Browser already running")
            return

        browser_type = browser_var.get()
        log(f"Starting browser: {browser_type}")

        driver = create_browser(browser_type)

        app_context["driver"] = driver
        app_context["browser_type"] = browser_type

        log("Browser started successfully")

    tk.Button(
        main,
        text="Start Browser",
        command=start_browser,
        bg="#2ecc71",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).grid(row=1, column=1, sticky="ew")

    # ==============================
    # FOLDER NAVIGATION
    # ==============================
    tk.Label(
        main,
        text="Folder Navigation",
        font=("Segoe UI", 12, "bold")
    ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))

    nav = tk.Frame(main)
    nav.grid(row=3, column=0, columnspan=2, sticky="ew")
    nav.columnconfigure(1, weight=1)

    tk.Button(nav, text="◀ Back", command=go_back).grid(row=0, column=0)
    tk.Button(nav, text="Forward ▶", command=go_forward).grid(row=0, column=2)

    path_var = tk.StringVar()
    path_entry = tk.Entry(nav, textvariable=path_var)
    path_entry.grid(row=0, column=1, sticky="ew", padx=5)

    path_entry.bind("<Return>", lambda e: set_active_folder(path_var.get()))

    tk.Button(
        main,
        text="Select Folder",
        command=choose_folder
    ).grid(row=4, column=0, sticky="ew", pady=5)

    tk.Button(
        main,
        text="Create Subfolder",
        command=create_subfolder
    ).grid(row=4, column=1, sticky="ew", pady=5)

    # ==============================
    # IMAGE → PDF
    # ==============================
    def convert_images():
        if not state.ACTIVE_FOLDER:
            log("Select a folder first")
            return

        log("Scanning folders for images...")
        scan_and_convert(state.ACTIVE_FOLDER, logger=log)
        log("Image to PDF conversion completed")

    tk.Button(
        main,
        text="Convert Images → PDF",
        command=convert_images,
        bg="#3498db",
        fg="white",
        font=("Segoe UI", 10, "bold")
    ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(5, 10))

    # ==============================
    # CAPTURE CONTROL
    # ==============================
    tk.Label(
        main,
        text="Capture Control",
        font=("Segoe UI", 12, "bold")
    ).grid(row=6, column=0, columnspan=2, sticky="w")

    status_lbl = tk.Label(
        main,
        text="RUNNING",
        font=("Segoe UI", 12, "bold"),
        fg="green"
    )
    status_lbl.grid(row=7, column=1)

    toggle_btn = tk.Button(
        main,
        text="Pause Capture",
        bg="#e74c3c",
        fg="white"
    )
    toggle_btn.grid(row=7, column=0, sticky="ew")

    def toggle_capture():
        state.CAPTURE_ENABLED = not state.CAPTURE_ENABLED
        if state.CAPTURE_ENABLED:
            toggle_btn.config(text="Pause Capture", bg="#e74c3c")
            status_lbl.config(text="RUNNING", fg="green")
            log("Capture resumed")
        else:
            toggle_btn.config(text="Resume Capture", bg="#2ecc71")
            status_lbl.config(text="PAUSED", fg="red")
            log("Capture paused")

    toggle_btn.config(command=toggle_capture)

    # ==============================
    # LOG BOX
    # ==============================
    tk.Label(
        main,
        text="Activity Log",
        font=("Segoe UI", 12, "bold")
    ).grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 0))

    log_box = ScrolledText(main, height=8, wrap="word")
    log_box.grid(row=9, column=0, columnspan=2, sticky="nsew")
    main.rowconfigure(9, weight=1)

    init_logger(log_box)

    log(
        "Instructions:\n"
        "- Select browser and click Start Browser\n"
        "- Select or navigate to the main/root folder\n"
        "- Capture screenshots using 'S' key\n"
        "- Images are saved in the active folder\n"
        "- Convert Images → PDF scans all subfolders\n"
        "- Each image folder gets its own PDF\n"
        "- Pause capture when typing paths\n"
        "- Press ESC or close window to exit"
    )
