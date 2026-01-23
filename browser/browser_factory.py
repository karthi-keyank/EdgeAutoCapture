from browser.edge_driver import (
    create_driver as create_edge_driver,
    close_driver as close_edge_driver,
    BrowserLaunchError as EdgeLaunchError
)

from browser.chrome_driver import (
    create_driver as create_chrome_driver,
    close_driver as close_chrome_driver,
    BrowserLaunchError as ChromeLaunchError
)

from browser.opera_driver import (
    create_driver as create_opera_driver,
    close_driver as close_opera_driver,
    BrowserLaunchError as OperaLaunchError,
    BrowserNotFoundError
)

from core.logger import log


# ==============================
# UNIFIED BROWSER ERROR
# ==============================
class BrowserError(Exception):
    pass


# ==============================
# BROWSER FACTORY
# ==============================
def create_browser(browser_type="edge"):
    """
    Create browser driver safely.
    Translates low-level driver errors into user-safe BrowserError.
    """

    browser_type = browser_type.lower()
    log(f"Browser requested: {browser_type}", "BROWSER")

    try:
        if browser_type == "chrome":
            log("Launching Chrome browser", "BROWSER")
            driver = create_chrome_driver()

        elif browser_type == "opera":
            log("Launching Opera browser", "BROWSER")
            driver = create_opera_driver()

        else:
            log("Launching Edge browser", "BROWSER")
            driver = create_edge_driver()

        log(f"{browser_type.capitalize()} browser started", "BROWSER")
        return driver

    except BrowserNotFoundError as e:
        log(str(e), "ERROR")
        raise BrowserError(str(e)) from e

    except (ChromeLaunchError, EdgeLaunchError, OperaLaunchError) as e:
        log(f"Browser launch failed: {e}", "ERROR")
        raise BrowserError(
            "Failed to start browser. Please close existing browser windows and try again."
        ) from e

    except Exception as e:
        log(f"Unexpected browser error: {e}", "ERROR")
        raise BrowserError(
            "Unexpected error while starting browser."
        ) from e


def close_browser(driver, browser_type="edge"):
    """
    Safely close the browser driver
    """

    if not driver:
        log("Close browser ignored – no active browser", "WARN")
        return

    browser_type = browser_type.lower()
    log(f"Closing browser: {browser_type}", "BROWSER")

    try:
        if browser_type == "chrome":
            close_chrome_driver(driver)

        elif browser_type == "opera":
            close_opera_driver(driver)

        else:
            close_edge_driver(driver)

        log(f"{browser_type.capitalize()} browser closed", "BROWSER")

    except Exception as e:
        log(f"Error while closing browser: {e}", "ERROR")
