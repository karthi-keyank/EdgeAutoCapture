from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# ==============================
# CUSTOM ERRORS
# ==============================
class BrowserLaunchError(Exception):
    pass


def create_driver():
    """
    Create and return a Microsoft Edge WebDriver.

    Selenium Manager automatically:
    - detects installed Edge
    - downloads matching msedgedriver
    """

    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Edge(options=options)
        return driver

    except WebDriverException as e:
        raise BrowserLaunchError(
            f"Failed to start Edge browser: {e}"
        ) from e


def close_driver(driver):
    """
    Safely close Edge browser
    """
    try:
        if driver:
            driver.quit()
    except Exception:
        pass
