from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
# from test_frames.locators.map.map_locators import MapLocators
from utils import scope_utils


class BaseError(Exception):
    pass


class BasePage:

    delay = 0.5
    double_delay = 1
    TAB = "//nav//a[contains(text(),'{}')]"
    BUTTON ="//button[contains(text(),'{}')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.mouse = ActionChains(self.driver)
        # self.map_locators = MapLocators()

    def click_on_element(self, *locator):
        found_element = self.wait.until(ec.visibility_of_element_located(*locator))
        time.sleep(self.delay)
        found_element.click()

    # def click(self, element):
    #     time.sleep(self.delay)
    #     element.click()

    def click_with_mouse_on_element(self, *locator):
        element = self.wait.until(ec.visibility_of_element_located(*locator))
        action = self.mouse.move_to_element(element)
        action.click(element).perform()

    def click_by_execute_script_on_element(self, element, sleep=0.5):
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(sleep)

    def click_on_element_with_custom_locator(self, locator, title, timeout=15, js_click=True, sleep_in_the_end=0.5):
        link = locator.format(title)
        element = (By.XPATH, link)
        if self.wait_till_element_is_displayed(element, timeout):
            try:
                web_element = self.find_element_with_locator(element)
                if js_click:
                    self.click_by_execute_script_on_element(web_element, sleep=sleep_in_the_end)
                else:
                    web_element.click()
                    time.sleep(sleep_in_the_end)
            except NoSuchElementException:
                logging.error("Not found element with following locator %s", link)

    def click_on_element_with_any_locator_multi(self, locator, timeout=1, counter=30):
        web_element = None
        for i in range(counter):
            try:
                web_element = self.find_element_with_locator(locator)
                try:
                    self.click_by_execute_script_on_element(web_element)
                    break
                except StaleElementReferenceException:
                    logging.debug("Element is not attached to the page document %s", locator)
                    time.sleep(timeout)
            except NoSuchElementException:
                logging.error("Not found element with following locator %s", web_element)

    def click_on_element_with_any_locator(self, locator, timeout=30, check_is_displayed=True, js_click=True):
        web_element = None
        if not check_is_displayed:
            try:
                web_element = self.find_element_with_locator(locator)
                if js_click:
                    self.click_by_execute_script_on_element(web_element)
                else:
                    web_element.click()
            except NoSuchElementException:
                logging.error("Not found element with following locator %s", web_element)
        else:
            if self.wait_till_element_is_displayed(locator, timeout):
                try:
                    web_element = self.find_element_with_locator(locator)
                    if js_click:
                        self.click_by_execute_script_on_element(web_element)
                    else:
                        web_element.click()
                except NoSuchElementException:
                    logging.error("Not found element with following locator %s", web_element)

    def find_elements_by_xpath(self, element_locator, counter=20):
        try:
            for i in range(counter):
                elements = self.driver.find_elements(*element_locator)
                if elements:
                    return elements
                else:
                    time.sleep(self.delay)
        except NoSuchElementException:
            logging.error("Not found element with following locator %s", element_locator)

    def find_element_with_locator(self, element_locator, counter=60):
        element = None
        for i in range(counter):
            try:
                element = self.driver.find_element(*element_locator)
                if element:
                    return element
                # else:
                #     raise BaseError("Not found element with following locator: {}".format(element_locator))
            except NoSuchElementException:
                logging.debug("Try to found element with locator %s", element_locator)
                time.sleep(self.double_delay)
        raise BaseError("Not found element with following locator: {}".format(element_locator))

    def insert_text_to_field(self, element, text):
        try:
            if element:
                # self.wait_till_element_is_clickable(element, timeout=30)
                element.click()
                element.clear()
                time.sleep(1)
                element.clear()
                element.send_keys(text)
                time.sleep(1)
            else:
                return False
        except NoSuchElementException:
            logging.error("Not found element with following locator %s", element)


    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(self.delay)

    def scroll_to_element_full_cycle(self, text_locator, modify_with=None, timeout=0.5):
        if modify_with:
            apply_element = (By.XPATH, text_locator.format(modify_with))
        else:
            apply_element = (By.XPATH, text_locator)
        web_element = self.find_element_with_locator(apply_element)
        self.driver.execute_script("arguments[0].scrollIntoView();", web_element)
        time.sleep(timeout)




    # def click_on_element_with_locator(self, element_locator, sleep_in_the_end=0.5):
    #     try:
    #         element = self.wait.until(ec.element_to_be_clickable(element_locator))
    #         if element:
    #             time.sleep(sleep_in_the_end)
    #             element.click()
    #         else:
    #             return False
    #     except NoSuchElementException:
    #         logging.error("Not found element with following locator %s", element_locator)


    def wait_till_element_is_displayed(self, *locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout=int(timeout),
                             ignored_exceptions=(StaleElementReferenceException, NoSuchElementException))
        try:
            return wait.until(ec.visibility_of_element_located(*locator))
            # return True
        except TimeoutException:
            return False

    def wait_till_element_is_disabled(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout=int(timeout),
                             ignored_exceptions=(StaleElementReferenceException, NoSuchElementException))
        try:
            wait.until(ec.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_till_element_becomes_clickable(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout=int(timeout))
        try:
            wait.until(ec.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    # def wait_map_loading(self):
    #     self.wait_till_element_is_displayed(self.map_locators.search_field, timeout=60)

    def update_locator_with_data(self, locator, data):
        temp = list(locator)
        temp[1] = temp[1] % data
        return tuple(temp)

    def create_locator_from_data(self, xpath, value):
        xpath_locator = (By.XPATH, xpath.format(value))
        return xpath_locator

    def refresh_page(self):
        currentURL = self.driver.current_url
        self.driver.get(currentURL)

    def approve_alert(self):
        elem = self.driver.find_elements_by_xpath("//span[contains(.,'ok')]")
        if len(elem) > 0:
            elem[0].click()

    def get_value_via_attribute(self, xpath, attribute_name):
        # example attribute_name can be "outerText" or "value" or "textContent" etc
        element = self.driver.find_element_by_xpath(xpath)
        value = element.get_attribute(attribute_name)
        return value

    def open_tab(self, tab_name):
        tab_locator = (By.XPATH, self.TAB.format(tab_name))
        tab = self.find_element_with_locator(tab_locator)
        tab.click()



    # def is_loading_media_finished(self, element_xpath, source="src", timeout=1):
    #     result = False
    #     s3_link = "......amazonaws.com"
    #     while not result:
    #         value = self.get_value_via_attribute(element_xpath, source)
    #         if s3_link in value:
    #             result = True
    #         else:
    #             time.sleep(timeout)
