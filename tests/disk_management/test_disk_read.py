import subprocess
import unittest
import os
import egg.disk_management

from tests.disk_management import load_expected_results, VHD_DIR


@unittest.skipUnless(os.getuid() == 0, None)
class TestDiskRead(unittest.TestCase):

    scenario_data: dict
    vhd_name: str
    vhd_table: str
    loop_path: str

    @classmethod
    def fillClassVariables(cls, scenario_data):
        cls.vhd_name = scenario_data.get('vhd_name')
        cls.vhd_table = VHD_DIR + cls.vhd_name + '/vhd.table'
        os.system(VHD_DIR + cls.vhd_name + '/setup.sh ' + cls.vhd_table)
        cls.expected = load_expected_results(cls.vhd_name)
        cls.loop_path = subprocess.check_output('cat ./loop_path.tmp', shell=True).rstrip().decode("utf-8")

    def test_disk(self) -> None:
        disk = egg.disk_management.get_disk(self.loop_path)
        self.assertEqual(disk.get_model(), self.expected.get('model'))
        self.assertEqual(disk.get_type(), self.expected.get('type'))
        self.assertEqual(disk.get_capacity(), self.expected.get('size'))
        self.assertEqual(disk.get_path(), self.loop_path)

    def test_partitions(self) -> None:
        partitions = egg.disk_management.get_disk(self.loop_path).get_partitions()
        self.assertEqual(len(partitions), self.expected.get('number_of_partition'))

    def test_each_partitions(self) -> None:
        partitions = egg.disk_management.get_disk(self.loop_path).get_partitions()
        partitions_expected: list = self.expected.get('partitions')
        for i in range(0, len(partitions)):
            with self.subTest(partitions[i]):
                self.assertEqual(partitions[i].get_capacity(), partitions_expected[i].get('size'))
                self.assertEqual(partitions[i].get_filesystem().type, partitions_expected[i].get('filesystem'))
                self.assertEqual(partitions[i].get_path(), self.loop_path + 'p' + str(i + 1))
                self.assertEqual(partitions[i].get_start(), partitions_expected[i].get('start'))
                self.assertEqual(partitions[i].get_end(), partitions_expected[i].get('end'))

    @classmethod
    def tearDownClass(cls) -> None:
        os.system(VHD_DIR + cls.vhd_name + '/tear_down.sh')
