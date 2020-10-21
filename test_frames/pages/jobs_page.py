import logging

from selenium.webdriver.common.by import By

from test_frames.pages.base_page import BasePage


class JobsPage(BasePage):

    JOBS_CONTENT = (By.XPATH, "//div[@class='myjobs-wrapper']")
    JOB_NAME_FIELD = (By.XPATH, "//input[@name='jobName']")
    TEXTAREA = (By.XPATH, "//textarea[@id='newJobStep3Textarea']")
    ALERT_CLOSE_BUTTON = (By.XPATH, "//div[@class='cs-success-dialog']//button")

    TABLE = "//div[@class='card csui_segment' and contains(.,'{}')]"
    JOBS_TABLE = TABLE + "//div[@class='rt-table']"
    JOBS_TABLE_ROWS = TABLE + "//div[@class='rt-tr-group']"
    JOBS_NAME_ROW = TABLE + "//div[@class='rt-tr-group']/div/div[5]"

    SKUS_ID = "//div[@class='catalog-table']//tr//span[contains(text(),'{}')]"
    ACTIVE_TAB_PANEL = "//div[@class='tab-pane active']"
    # COMPLETE_JOB = "(//div[@class='card csui_segment'])[3]//div[@class='rt-tr-group']//div[div[text()= '{}'] " \
    #                "and div[contains(., 'Complete')]]"
    COMPLETE_JOB = "//div[@class='card csui_segment' and contains(.,'One-Time Jobs')]//div[@class='rt-tr-group']" \
                   "//div[div[text()= '{}'] and div[contains(., 'Complete')]]"

    EYE_ICON = "(" + COMPLETE_JOB + "//a)[2]"
    BIN_ICON = COMPLETE_JOB + "//button"
    CONFIRM_DELETE_BUTTON = "//div[@class='delete-job-confirmation-dialog']//div[@class='options']/button"

    user_field, password_field = None, None

    def __init__(self, driver):

        self.driver = driver
        super().__init__(driver)

    def check_is_jobs_displayed(self):
        return self.wait_till_element_is_displayed(self.JOBS_CONTENT)

    def press_button_on_active_tab(self, button_name):
        next_button = (By.XPATH, self.ACTIVE_TAB_PANEL + self.BUTTON.format(button_name))
        self.click_on_element(next_button)

    def press_new_job(self):
        add_new_job_button = (By.XPATH, self.BUTTON.format("Add New Job"))
        self.click_on_element(add_new_job_button)

    def select_retailer(self, retailer):
        retailer_button = (By.XPATH, self.BUTTON.format(retailer))
        self.click_on_element(retailer_button)

    def fill_job_name(self, job_name):
        job_name_field = self.wait_till_element_is_displayed(self.JOB_NAME_FIELD)
        job_name_field.send_keys(job_name)

    def enter_skus(self, skus_id):
        job_name_field = self.wait_till_element_is_displayed(self.TEXTAREA)
        job_name_field.send_keys(skus_id)

    def approve_submit(self):
        approve_checkbox = self.ACTIVE_TAB_PANEL+"//input"
        checkbox_list = [x for x in self.driver.find_elements_by_xpath(approve_checkbox)]
        for checkbox in checkbox_list:
            self.click_by_execute_script_on_element(checkbox)

    def accept_alert(self):
        # close_button = (By.XPATH, self.ALERT_CLOSE_BUTTON)
        self.click_on_element(self.ALERT_CLOSE_BUTTON)
        # elem = self.driver.find_elements_by_xpath(self.incident_locators.ok_button)
        # # logging.debug(len(elem))
        # if len(elem) > 0:
        #     elem[0].click()

    def find_job(self, job_name, attempts_amount=60):
        job_locator = (By.XPATH, self.COMPLETE_JOB.format(job_name))
        return self.find_element_with_locator(job_locator, counter=attempts_amount)

    def press_jobs_eye_button(self, new_job):
        eye_button = (By.XPATH, self.EYE_ICON.format(new_job))
        self.click_on_element(eye_button)

    def check_if_skus_is_displayed(self, skus_id):
        skus = (By.XPATH, self.SKUS_ID.format(skus_id))
        return self.find_element_with_locator(skus)

    def check_if_jobs_are_displayed(self):
        list_of_rows = []
        rows_of_one_time_jobs = self.JOBS_NAME_ROW.format('One-Time Jobs')
        total = self.driver.find_elements_by_xpath(rows_of_one_time_jobs)
        for row in total:
            list_of_rows.append(row.get_attribute("outerText"))
        logging.info("There are {} jobs available to delete".format(len(total)))
        return list_of_rows

    def wait_table_is_loaded(self, table_name):
        table = (By.XPATH, self.JOBS_TABLE.format(table_name))
        self.wait_till_element_is_displayed(table, timeout=30)

    def press_jobs_bin_button(self, job_name):
        bin_button = (By.XPATH, self.BIN_ICON.format(job_name))
        self.click_on_element(bin_button)
        self.__confirm_delete_job()
        self.__confirm_delete_job()

    def __confirm_delete_job(self, option=1):
        # delete_button = self.CONFIRM_DELETE_BUTTON + "[" + str(option) + "]"
        delete_button = (By.XPATH, "{}[{}]".format(self.CONFIRM_DELETE_BUTTON, str(option)))
        self.click_on_element(delete_button)

    def check_if_job_exist(self, job_name, delay=3):
        job_locator = (By.XPATH, self.COMPLETE_JOB.format(job_name))
        return self.wait_till_element_is_displayed(job_locator, timeout=delay)

