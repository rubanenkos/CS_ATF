import pytest

from utils import scope_utils
from utils.selenium.selenium_instance import CreateSeleniumInstance
from utils.const_params import Enviroments


def pytest_addoption(parser):
    parser.addoption('--environment', action="store", help='environment name', default="STAS")
    parser.addoption('--headless', action="store", help='mode to run test', default="NO")


@pytest.fixture(autouse=True, scope="session")
def set_settings(pytestconfig):
    required_environment, settings = None, None
    if pytestconfig.getoption("environment"):
        required_environment = '{}'.format(pytestconfig.getoption("environment"))
    for env in Enviroments:
        if env.upper() == required_environment.upper():
            settings = scope_utils.get_env_settings(required_environment.upper())
            break
    scope_utils.set_key("env_settings", settings)
    scope_utils.set_key("headless", pytestconfig.getoption("headless"))


@pytest.fixture()
def get_settings():
    return scope_utils.get_key("env_settings")


@pytest.fixture(scope="function")
def driver_init(request):
    instance = CreateSeleniumInstance()
    browser = instance.get_browser()
    request.cls.driver = browser
    yield
    browser.close()
