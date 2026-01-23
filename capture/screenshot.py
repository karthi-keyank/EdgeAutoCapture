import os
import base64
from datetime import datetime

from selenium.common.exceptions import WebDriverException

import core.state as state
from core.logger import log


def capture_full_page(driver):
    """
    Capture full-page screenshot using Chromium DevTools
    Works for Chrome, Edge, Opera
    """

    # ==============================
    # BASIC GUARDS
    # ==============================
    if not state.CAPTURE_ENABLED:
        log("Capture paused – ignored", "WARN")
        return

    if not state.ACTIVE_FOLDER:
        log("No active folder selected", "WARN")
        return

    if driver is None:
        log("Capture ignored – browser not started", "WARN")
        return

    # ==============================
    # BROWSER VALIDATION
    # ==============================
    try:
        handles = driver.window_handles
        if not handles:
            raise WebDriverException("No browser window")
    except Exception:
        log(
            "Browser window not available – capture disabled",
            "ERROR"
        )
        state.CAPTURE_ENABLED = False
        state.BROWSER_RUNNING = False
        return

    # ==============================
    # SCREENSHOT CAPTURE
    # ==============================
    try:
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
            log("Screenshot failed – no image data", "ERROR")
            return

        image_bytes = base64.b64decode(result["data"])

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
        save_path = os.path.join(state.ACTIVE_FOLDER, filename)

        with open(save_path, "wb") as f:
            f.write(image_bytes)

        log(f"Screenshot saved: {save_path}", "CAPTURE")

    # ==============================
    # FILE / SYSTEM ERRORS
    # ==============================
    except PermissionError:
        log(
            "Permission denied while saving screenshot",
            "ERROR"
        )

    except OSError as e:
        log(
            f"File system error while saving screenshot: {e}",
            "ERROR"
        )

    except WebDriverException as e:
        log(
            f"Browser error during capture: {e}",
            "ERROR"
        )
        state.CAPTURE_ENABLED = False
        state.BROWSER_RUNNING = False

    except Exception as e:
        log(
            f"Unexpected capture error: {e}",
            "ERROR"
        )
