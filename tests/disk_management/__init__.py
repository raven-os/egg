import json
import os

VHD_DIR: str = os.path.dirname(os.path.abspath(__file__)) + '/virtual_hard_disk/'


def create_disk_test_case(testcase_klass, scenario_data: dict = None):

    class ScenarioTestCase(testcase_klass):
        @classmethod
        def setUpClass(cls):
            cls.fillClassVariables(scenario_data)

    return_class = ScenarioTestCase
    return_class.__name__ = testcase_klass.__name__
    return return_class


def load_expected_results(vhd_name: str) -> dict:
    file_path = VHD_DIR + vhd_name + '/expected.json'
    file = open(file_path, 'r')
    expected_dict = json.load(file)
    file.close()
    return expected_dict
