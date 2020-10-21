from selenium.webdriver.common.by import By

from test_frames.pages.base_page import BasePage


class DashboardPage(BasePage):

    CS_MAIN_LOGO = (By.XPATH, "//img[contains(@src, '/static/media/ContentStatus_Basic Logo.ff7ca552.png')]")
    LOGIN_CS_WELCOME_PICTURE = (By.XPATH, "//div[contains(@class, 'login-header')]")

    user_field, password_field = None, None

    def __init__(self, driver):
        self.driver = driver
        super().__init__(driver)

    def check_is_dashboard_displayed(self):
        return self.wait_till_element_is_displayed(self.CS_MAIN_LOGO)
