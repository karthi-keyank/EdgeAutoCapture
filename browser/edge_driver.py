from selenium import webdriver


def create_driver():
    """
    Create and return a Microsoft Edge WebDriver.

    Selenium Manager automatically:
    - detects installed Edge version
    - downloads matching msedgedriver
    - caches it for future runs
    """
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Edge(options=options)
    return driver


def close_driver(driver):
    """
    Safely close Edge browser
    """
    try:
        if driver:
            driver.quit()
    except Exception:
        pass
