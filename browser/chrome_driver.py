from selenium import webdriver


def create_driver():
    """
    Create and return a Chrome WebDriver.

    Selenium Manager automatically:
    - detects installed Chrome version
    - downloads matching chromedriver
    - caches and reuses it
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver


def close_driver(driver):
    """
    Safely close Chrome browser
    """
    try:
        if driver:
            driver.quit()
    except Exception:
        pass
