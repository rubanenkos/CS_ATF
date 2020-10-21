from enum import Enum

Enviroments = ['PROD', 'STAGE', 'QA', 'DEV']
Tabs = ['Dashboard', 'Jobs']


class CS_ATF_Env(Enum):
    pass
    # PROD = "10.0.0.1:27017"
    # STAGE = "10.0.3.202:27017"
    # QA = "10.0.3.202:27017"


class ProjectPaths(Enum):
    CHROME_DRIVER = 'drivers/linux_chromedriver'
    FILES_USERS = 'settings/'
    FLOW_SCENARIO = 'test_data/scenarios/'
    # API_TEST_CSV = 'data/files/test_api_files/'

