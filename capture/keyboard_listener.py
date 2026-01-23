from pynput import keyboard
from capture.screenshot import capture_full_page
from core.logger import log


def start_keyboard_listener(app_context):
    """
    Start global keyboard listener

    S   -> capture screenshot
    ESC -> exit app
    """

    root = app_context["root"]

    def on_press(key):
        try:
            # Handle 'S' key
            if key.char and key.char.lower() == "s":
                driver = app_context.get("driver")

                if not driver:
                    log("Capture ignored – browser not started")
                    return

                capture_full_page(driver)

        except AttributeError:
            # Handle special keys (ESC)
            if key == keyboard.Key.esc:
                log("Exiting application")
                root.after(0, root.destroy)
                return False

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
