from pynput import keyboard

from capture.screenshot import capture_full_page


def start_keyboard_listener(app_context):
    """
    Start global keyboard listener
    S   -> capture screenshot
    ESC -> exit app
    """

    driver = app_context["driver"]
    root = app_context["root"]

    def on_press(key):
        try:
            if key.char and key.char.lower() == "s":
                capture_full_page(driver)

        except AttributeError:
            if key == keyboard.Key.esc:
                root.after(0, root.destroy)
                return False

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
