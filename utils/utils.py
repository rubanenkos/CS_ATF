import csv
import datetime
import json
import os
import random
import string
import time
from pathlib import Path

import allure
# import objectpath
from allure_commons.types import AttachmentType


def get_location_path(my_folder):
    loc = os.getcwd()
    return os.path.join(loc, my_folder)


def get_location_based_on_root(my_folder):
    root_location = os.path.abspath('..')
    return root_location+my_folder


def join_folders(f1, f2):
    return os.path.join(f1, f2)


def get_project_root():
    return Path(__file__).parent.parent.__str__()


def concat_project_root(my_path):
    return join_folders(get_project_root(), my_path)


def get_random_string(string_length=10, uppercase=True):
    """Generate a random string of fixed length """
    if uppercase:
        letters = string.ascii_uppercase
    else:
        letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def load_json_file(file_path):
    with open(file_path, "r") as file_data:
        return json.load(file_data)


def retrieve_node_value_from_json(json_file, node_name):
    for k in json_file:
        if k == node_name:
            return json_file[k]
    return None


def current_time_in_milliseconds():
    return int(round(time.time() * 1000))


def compare_lists_entities(list_a, list_b):
    difference = list(set(list_a) ^ set(list_b))
    # logging.info(list(set(list_a) - set(list_b)))  # Can be useful to know which elements the list 'b' doesn't contain
    # logging.info(list(set(list_b) - set(list_a)))  # Can be useful to know which elements the list 'a' doesn't contain
    return difference

# @allure.step('close browser')
def close_instance(inst):
    if inst is not None and type(inst) is dict:
        try:
            inst['instance'].browser.close()
        except Exception:
            pass
        return None


def capture_screenshot(inst, screenshot_name):
    if inst is not None and type(inst) is dict:
        try:
            allure.attach(inst['instance'].get_browser().get_screenshot_as_png(),
                          name=screenshot_name,
                          attachment_type=AttachmentType.PNG)
        except Exception:
            pass


def snake_to_camel(word, delimiter='-'):
    return ''.join(x.capitalize() or delimiter for x in word.split(delimiter))


def csv_to_json(my_file):
    my_data = list()
    # with open(my_file, 'rU') as csv_file:
    # DeprecationWarning: 'U' mode is deprecated
    with open(my_file, newline = '') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='|')
        field = reader.fieldnames
        for row in reader:
            my_data.extend([{field[i]: row[field[i]] for i in range(len(field))}])
    return my_data


def str_to_bool(value):
    true_list = ['true']
    return value.lower in true_list


# def get_field_from_scenario(my_json, root_field, field):
#     """ get specific field(pair key:value) from whole tree"""
#     result = None
#     if my_json and field:
#         json_tree = objectpath.Tree(my_json)
#         result = json_tree.execute('$..' + root_field)
#         result_json_tree = objectpath.Tree(result)
#         result = tuple(result_json_tree.execute('$..' + field))
#     return result
#
#
# def get_part_from_scenario(my_json, root_field):
#     """ get part of tree """
#     result = None
#     if my_json and root_field:
#         json_tree = objectpath.Tree(my_json)
#         result = list(json_tree.execute('$.' + root_field))
#     return result
#
#
# def get_value_from_field(my_json, field):
#     """ get value from tree """
#     result = None
#     if my_json and field:
#         json_tree = objectpath.Tree(my_json)
#         result = tuple(json_tree.execute('$..' + field))
#     return result


def get_date():
    return datetime.date.today()


def convert_str_to_data_time(date_time_str, str_template='%Y-%m-%dT%H:%M:%S.%fZ'):
    return datetime.datetime.strptime(date_time_str, str_template)


def str_to_json(value):
    try:
        return json.loads(value)
    except ValueError:
        return None
