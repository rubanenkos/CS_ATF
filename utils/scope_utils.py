from pathlib import Path
from utils.const_params import CS_ATF_Env
from utils.utils import get_location_path
import json


my_data = {'project_root_path': Path(__file__).parent.parent.__str__(),
           'agencies': {}}


def set_key(key, value):
    my_data[key] = value


def get_key(key):
    return my_data[key]


def get_env_settings(env):
    settings_full_path = get_location_path('../settings/env_settings.json')
    with open(settings_full_path) as json_file:
        data = json.load(json_file)
    return data.get(env)



