from browser.edge_driver import (
    create_driver as create_edge_driver,
    close_driver as close_edge_driver
)

from browser.chrome_driver import (
    create_driver as create_chrome_driver,
    close_driver as close_chrome_driver
)


def create_browser(browser_type="edge"):
    """
    Create a browser driver based on browser type.

    browser_type:
        - "edge"
        - "chrome"
    """
    browser_type = browser_type.lower()

    if browser_type == "chrome":
        return create_chrome_driver()

    # default → Edge
    return create_edge_driver()


def close_browser(driver, browser_type="edge"):
    """
    Safely close the browser driver
    """
    browser_type = browser_type.lower()

    if browser_type == "chrome":
        close_chrome_driver(driver)
    else:
        close_edge_driver(driver)
