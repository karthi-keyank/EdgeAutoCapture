import tkinter as tk

from browser.browser_factory import close_browser
from capture.keyboard_listener import start_keyboard_listener
from gui.app_ui import build_ui


def main():
    root = tk.Tk()
    root.title("Capture Tool")
    root.geometry("720x560")
    root.minsize(650, 520)

    # shared app context
    app_context = {
        "root": root,
        "driver": None,
        "browser_type": None
    }

    build_ui(app_context)

    start_keyboard_listener(app_context)

    def on_close():
        if app_context["driver"]:
            close_browser(
                app_context["driver"],
                app_context["browser_type"]
            )
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
