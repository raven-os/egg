import subprocess
import unittest
import os

from tests.disk_management import load_expected


class DiskRead(unittest.TestCase):
    VHD_DIR: str = os.path.dirname(os.path.abspath(__file__)) + '/virtual_hard_disk/'
    VHD_TABLE: str = VHD_DIR + 'gpt_512M_4p/vhd.table'

    def setUp(self) -> None:
        os.system(self.VHD_DIR + 'gpt_512M_4p/setup.sh ' + self.VHD_TABLE)
        self.expected = load_expected('gpt_512M_4p')
        self.loop_path: str = subprocess.check_output('cat ./loop_path.tmp', shell=True).rstrip().decode("utf-8")

    @unittest.skipUnless(os.getuid() == 0, None)
    def test_something(self) -> None:
        pass

    def tearDown(self) -> None:
        os.system(self.VHD_DIR + 'gpt_512M_4p/tear_down.sh')


if __name__ == '__main__':
    unittest.main()
