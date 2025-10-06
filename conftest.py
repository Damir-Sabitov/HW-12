import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config


from utils.attach import add_screenshot, add_logs, add_html, add_video

def pytest_addoption(parser):
    parser.addoption('--browser-version',  default='128.0')


@pytest.fixture(scope="function", autouse=True)
def configuring_browser(setup_browser):
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10

@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser_version=request.config.getoption('--browser-version')
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )
    browser.config.driver = driver
    yield browser

    add_screenshot(browser)
    add_logs(browser)
    add_html(browser)
    add_video(browser)

    browser.quit()