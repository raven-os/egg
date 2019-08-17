from typing import List

import parted

from egg.disk_management.partition import Partition


class Disk(object):
    def __init__(self, device: parted.Device = None, device_path: str = None):
        if device is not None:
            self.device: parted.Device = device
        elif device_path:
            self.device: parted.Device = parted.getDevice(device_path)
        else:
            raise parted.DiskException("no device specified")
        self.disk: parted.Disk = parted.newDisk(self.device)
        self.partitions: List[Partition] = list(map(lambda x: Partition(x), self.disk.partitions))

    def __del__(self):
        self.device.removeFromCache()

    def get_model(self) -> str:
        return str(self.device.model)

    def get_type(self) -> str:
        return self.disk.type

    def get_capacity(self) -> int:
        return self.device.getLength() * self.device.sectorSize

    def get_partitions(self) -> List[Partition]:
        return self.partitions

    def get_path(self) -> str:
        return self.device.path
