import logging
from time import sleep

import allure

from test_frames.pages.dashboard_page import DashboardPage
from test_frames.pages.jobs_page import JobsPage
from utils.utils import get_random_string, retrieve_node_value_from_json


class MainFlow:

    def __init__(self, driver):
        self.driver = driver
        self.dashboard = DashboardPage(self.driver)
        self.jobs = JobsPage(self.driver)

    def go_to_tab(self, tab_name):
        logging.info("Go to tab - '{}'".format(tab_name))
        self.dashboard.open_tab(tab_name)

    def add_new_job(self, retailer, skus_id):
        job_name = get_random_string()
        logging.info("Add new job - '{}'".format(job_name))
        self.jobs.press_new_job()
        self.jobs.fill_job_name(job_name)
        self.jobs.select_retailer(retailer)
        self.jobs.press_button_on_active_tab('Next')
        self.jobs.enter_skus(skus_id)
        self.jobs.press_button_on_active_tab('Load')
        self.jobs.press_button_on_active_tab('Next')
        self.jobs.press_button_on_active_tab('Next')
        self.jobs.approve_submit()
        self.jobs.press_button_on_active_tab('Submit')
        self.jobs.accept_alert()
        return job_name

    # @allure.step
    def validate_if_dashboard_is_displayed(self):
        logging.info("Validate if 'Dashboard' page is displayed")
        assert self.dashboard.check_is_dashboard_displayed()

    def validate_if_jobs_tab_is_displayed(self):
        logging.info("Validate if 'Jobs' page is displayed")
        assert self.jobs.check_is_jobs_displayed()

    def get_test_param(self, test_data, param):
        return retrieve_node_value_from_json(test_data, param)

    def validate_if_job_exists(self, new_job):
        logging.info("Validate if '{}' job exists". format(new_job))
        result = self.jobs.find_job(job_name=new_job)
        assert result

    def validate_if_skus_is_loaded(self, new_job, skus_id):
        logging.info("Validate if '{}' sku was loaded".format(skus_id))
        self.jobs.press_jobs_eye_button(new_job)
        result = self.jobs.check_if_skus_is_displayed(skus_id)
        assert result

    def validate_if_jobs_are_displayed(self):
        logging.info("Validate if jobs exist")
        self.jobs.wait_table_is_loaded('One-Time Jobs')
        jobs_list = self.jobs.check_if_jobs_are_displayed()
        assert len(jobs_list) > 0, 'There are no jobs to delete'
        return jobs_list

    def delete_first_job(self, jobs_list):
        first_job = jobs_list[0]
        logging.info("Delete '{}' job".format(first_job))
        self.jobs.press_jobs_bin_button(first_job)
        sleep(3)
        return first_job

    def validate_if_job_is_missing(self, deleted_job):
        logging.info("Validate if '{}' job is missing".format(deleted_job))
        result = self.jobs.check_if_job_exist(job_name=deleted_job)
        assert result is False

