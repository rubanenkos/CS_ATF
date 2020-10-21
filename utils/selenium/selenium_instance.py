import pytest
from selenium import webdriver

from utils import scope_utils
from utils.const_params import ProjectPaths
from os.path import dirname
from selenium.webdriver.chrome.options import Options
import logging
# from utils import scope_utils

@pytest.mark.usefixtures("get_settings")
class CreateSeleniumInstance:

    def __init__(self, headless=False):
        try:
            main_directory = dirname(dirname(dirname(__file__)))

            headless = scope_utils.get_key("headless")
            chrome_options = Options()
            if headless == 'YES':
                chrome_options.add_argument("--headless")
                #allow notifications the argument 1 to allow and 2 to block
            # chrome_options.add_argument("--headless")
            chrome_options.add_experimental_option("prefs",
                                                       {"profile.default_content_setting_values.notifications": 1})
            self.browser = webdriver.Chrome(options=chrome_options,
                                            executable_path=main_directory + "/" + ProjectPaths.CHROME_DRIVER.value)
            self.browser.maximize_window()
        except Exception as e:
            logging.error('Failed to do something: ' + str(e))
            self.browser = webdriver.Chrome(options=chrome_options,
                                            executable_path=main_directory + "/" + ProjectPaths.CHROME_DRIVER.value)
            self.browser.maximize_window()

    def get_browser(self):
        return self.browser

    def close_browser(self):
        self.browser.close()

