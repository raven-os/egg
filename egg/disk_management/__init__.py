from typing import List

import parted

__all__ = ['Disk', 'Partition']

from egg.disk_management.disk import Disk
from egg.disk_management.partition import Partition


def get_disk(device_path: str) -> Disk:
    return Disk(device_path=device_path)


def get_disks() -> List[Disk]:
    return list(map(lambda x: Disk(x), parted.getAllDevices()))
