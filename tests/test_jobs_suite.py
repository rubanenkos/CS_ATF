import pytest

from test_frames.flow.main_flow import MainFlow
from tests.base_test import BaseTest


class TestJobsSuite(BaseTest):
    @pytest.mark.test1
    @pytest.mark.parametrize("scenario, users", [("test1.json", "users.json")])
    def test_job1(self, scenario, users):
        instance = self.create_instance_of_browser_and_login(users, "test_user2")
        browser = instance['instance'].get_browser()
        test = MainFlow(browser)
        test.validate_if_dashboard_is_displayed()

    @pytest.mark.test2
    @pytest.mark.parametrize("scenario, users", [("test1.json", "users.json")])
    def test_add_new_job(self, scenario, users):
        data_scenario = self.get_data_scenario(scenario)
        instance = self.create_instance_of_browser_and_login(users, "test_user2")
        browser = instance['instance'].get_browser()
        test = MainFlow(browser)
        test.validate_if_dashboard_is_displayed()
        skus_id = test.get_test_param(data_scenario, 'skus_id')
        test.go_to_tab('Jobs')
        test.validate_if_jobs_tab_is_displayed()
        new_job = test.add_new_job('Amazon.com', skus_id)
        test.validate_if_job_exists(new_job)
        test.validate_if_skus_is_loaded(new_job, skus_id)

    @pytest.mark.test3
    @pytest.mark.parametrize("scenario, users", [("test1.json", "users.json")])
    def test_delete_job(self, scenario, users):
        data_scenario = self.get_data_scenario(scenario)
        instance = self.create_instance_of_browser_and_login(users, "test_user2")
        browser = instance['instance'].get_browser()
        test = MainFlow(browser)
        test.validate_if_dashboard_is_displayed()
        # skus_id = test.get_test_param(data_scenario, 'skus_id')
        test.go_to_tab('Jobs')
        jobs_list = test.validate_if_jobs_are_displayed()
        deleted_job = test.delete_first_job(jobs_list)
        test.validate_if_job_is_missing(deleted_job)
