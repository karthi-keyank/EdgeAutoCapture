import tkinter as tk

_log_box = None

# ======================================================
# LOG CATEGORY → COLOR MAP
# ======================================================
LOG_STYLES = {
    # Success / flow
    "CAPTURE": {"foreground": "#27ae60"},   # green
    "NAV":     {"foreground": "#2980b9"},   # blue
    "BROWSER": {"foreground": "#8e44ad"},   # purple
    "SYSTEM":  {"foreground": "#7f8c8d"},   # gray

    # Attention levels
    "WARN":    {"foreground": "#e67e22"},   # orange
    "ERROR":   {"foreground": "#e74c3c"},   # red

    # Fallback
    "INFO":    {"foreground": "#2c3e50"},   # dark default
}


def init_logger(log_box_widget):
    """
    Initialize logger with ScrolledText widget
    and configure color tags for all log categories.
    """
    global _log_box
    _log_box = log_box_widget

    for tag, style in LOG_STYLES.items():
        _log_box.tag_config(tag, **style)


def log(message, category="INFO"):
    """
    Log a message to the UI log box with category-based color.

    Categories:
    CAPTURE | NAV | BROWSER | SYSTEM | WARN | ERROR | INFO
    """
    if not _log_box:
        return

    category = category.upper()
    tag = category if category in LOG_STYLES else "INFO"

    prefix = f"[{tag}] "
    _log_box.insert(tk.END, prefix + message + "\n", tag)
    _log_box.see(tk.END)
