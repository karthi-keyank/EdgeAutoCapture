from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# ==============================
# CUSTOM ERRORS
# ==============================
class BrowserLaunchError(Exception):
    pass


def create_driver():
    """
    Create and return a Chrome WebDriver.

    Selenium Manager automatically:
    - detects installed Chrome
    - downloads matching chromedriver
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(options=options)
        return driver

    except WebDriverException as e:
        raise BrowserLaunchError(
            f"Failed to start Chrome browser: {e}"
        ) from e


def close_driver(driver):
    """
    Safely close Chrome browser
    """
    try:
        if driver:
            driver.quit()
    except Exception:
        pass
