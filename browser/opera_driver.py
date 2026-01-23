import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# ==============================
# CUSTOM ERRORS
# ==============================
class BrowserNotFoundError(Exception):
    pass


class BrowserLaunchError(Exception):
    pass


# ==============================
# OPERA PATH DETECTION
# ==============================
def _find_opera_path():
    """
    Try to locate Opera or Opera GX executable on Windows
    Returns full path if found, else None
    """

    possible_paths = [
        # Opera Stable
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs", "Opera", "opera.exe"
        ),
        # Opera GX
        os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs", "Opera GX", "opera.exe"
        ),
        # System-wide installs (rare but possible)
        r"C:\Program Files\Opera\opera.exe",
        r"C:\Program Files\Opera GX\opera.exe",
        r"C:\Program Files (x86)\Opera\opera.exe",
        r"C:\Program Files (x86)\Opera GX\opera.exe",
    ]

    for path in possible_paths:
        if path and os.path.isfile(path):
            return path

    return None


# ==============================
# DRIVER CREATION
# ==============================
def create_driver():
    """
    Create and return an Opera WebDriver using ChromeDriver
    """

    opera_path = _find_opera_path()

    if not opera_path:
        raise BrowserNotFoundError(
            "Opera browser not found. Please install Opera or Opera GX."
        )

    options = webdriver.ChromeOptions()
    options.binary_location = opera_path
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(options=options)
        return driver

    except WebDriverException as e:
        raise BrowserLaunchError(
            f"Failed to start Opera browser: {e}"
        ) from e


# ==============================
# DRIVER SHUTDOWN
# ==============================
def close_driver(driver):
    """
    Safely close Opera browser
    """
    try:
        if driver:
            driver.quit()
    except Exception:
        pass
