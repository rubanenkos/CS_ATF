from test_frames.pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

import time


class LoginPage(BasePage):
    email = "1-email"
    password = "//input[@name='password']"
    cs_logo = "//img[contains(@src, 'https://contentstatus.com/wp-content/uploads/2020/01/Logo-Rectangle-2.png')]"
    login_cs_welcome_picture = (By.XPATH, "//div[contains(@class, 'login-header')]")

    user_field, password_field = None, None

    def __init__(self, driver, user):
        self.driver = driver
        super().__init__(driver)
        self.mouse = ActionChains(self.driver)
        self.user = user

    def open_url(self, url):
        self.driver.get(url)

    def fill_login_password(self):
        self.user_field = self.wait_till_element_is_displayed((By.ID, self.email))
        self.user_field.send_keys(self.user['email'])

        self.password_field = self.wait_till_element_is_displayed((By.XPATH, self.password))
        self.password_field.send_keys(self.user['password'])

    def submit_login(self):
        self.password_field.send_keys(Keys.ENTER)
        # time.sleep(12)

    def validate_if_is_it_login_page(self):
        result = self.wait_till_element_is_displayed(self.login_cs_welcome_picture)
        assert result is True

