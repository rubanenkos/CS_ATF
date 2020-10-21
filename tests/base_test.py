import random

import allure
import logging

from tests.common_test import CommonTest
from utils.selenium.selenium_instance import CreateSeleniumInstance


class BaseTest:

    # @allure.step('open browser and login')
    def create_instance_of_browser_and_login(self, users, get_user):
        instance = CreateSeleniumInstance()
        browser = instance.get_browser()
        if browser:
            common_test = CommonTest()
            common_test.initialize_users(users)
            user = common_test.get_user(get_user)
            logging.info("Login with User: '{}'".format(user['email']))
            common_test.log_in_with_user(browser, user)
            return dict(instance=instance, user=user)
        else:
            return None
    #
    # # @allure.step('get test data')
    # def get_test_data(self, scenario_name):
    #     user_scenarios = self.get_data_scenario(scenario_name)

    # @allure.step('get data scenario')
    def get_data_scenario(self, scenario_name):
        common_test = CommonTest()
        dict_scenario = common_test.initialize_scenario(scenario_name)
        if dict_scenario:
            return dict_scenario
        else:
            return None
