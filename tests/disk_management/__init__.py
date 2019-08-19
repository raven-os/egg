import json
import os

VHD_DIR: str = f'{os.path.dirname(os.path.abspath(__file__))}/virtual_hard_disk'


def create_disk_test_case(testcase_type, scenario_data: dict = None):

    class ScenarioTestCase(testcase_type):
        @classmethod
        def setUpClass(cls):
            cls.fillClassVariables(scenario_data)

    return_class = ScenarioTestCase
    return_class.__name__ = testcase_type.__name__
    return return_class


def load_expected_results(vhd_name: str) -> dict:
    expected_file_path = f'{VHD_DIR}/{vhd_name}/expected.json'
    with open(expected_file_path, 'r') as expected_file:
        expected_dict = json.load(expected_file)
    return expected_dict
