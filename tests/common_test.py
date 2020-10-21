
import allure
import pytest
import os.path
import json

from utils.utils import concat_project_root
from utils.const_params import ProjectPaths
from test_frames.pages.login_page import LoginPage
from utils import scope_utils


@pytest.mark.usefixtures("driver_init")
class CommonTest:
    user = {}
    scenario_dict = {}
    driver = None

    @allure.step
    def initialize_users(self, user):
        user_path = concat_project_root(ProjectPaths.FILES_USERS.value) + user
        if os.path.exists(user_path):
            with open(user_path, 'r') as usr:
                self.user = json.load(usr)
        else:
            return False

    @allure.step
    def initialize_scenario(self, scenario):
        scenario_path = concat_project_root(ProjectPaths.FLOW_SCENARIO.value) + scenario
        if os.path.exists(scenario_path):
            with open(scenario_path, 'r') as flow:
                self.scenario_dict = json.load(flow)
                return self.scenario_dict
        else:
            return False

    @allure.step
    def log_in(self):
        login = LoginPage(self.driver, self.user)
        env = scope_utils.get_key("env_settings")
        login.open_url(env.get("env_url"))
        login.fill_login_password()
        login.submit_login()
        return self.scenario_dict

    @allure.step
    def log_in_with_user(self, driver, user, update_url=True):
        login = LoginPage(driver, user)
        env = scope_utils.get_key("env_settings")
        if update_url is True:
            login.open_url(env.get("env_url"))
        login.fill_login_password()
        login.submit_login()
        return True

    def get_user(self, user_id):
        for usr in self.user:
            if user_id in usr:
                value = self.user[user_id][0]
                return value
        return None
