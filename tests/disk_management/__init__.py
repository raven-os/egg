import json
import os


def load_expected(vhd_name: str) -> dict:
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/virtual_hard_disk/' + vhd_name + '/expected.json'
    file = open(file_path, 'r')
    expected_dict = json.load(file)
    file.close()
    return expected_dict
