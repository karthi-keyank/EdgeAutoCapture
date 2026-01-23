import os
import base64
from datetime import datetime

import core.state as state
from core.logger import log


def capture_full_page(driver):
    """
    Capture full-page screenshot using Chrome DevTools
    """

    if not state.CAPTURE_ENABLED:
        log("Capture paused – ignored")
        return

    if not state.ACTIVE_FOLDER:
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

        image_bytes = base64.b64decode(result["data"])

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
        save_path = os.path.join(state.ACTIVE_FOLDER, filename)

        with open(save_path, "wb") as f:
            f.write(image_bytes)

        log(f"Saved: {save_path}")

    except Exception as e:
        log(f"Capture error: {e}")
