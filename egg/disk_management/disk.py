import parted
from parted import Device

from egg.disk_management.partition import Partition


class Disk(object):
    def __init__(self, device: Device = None, device_path: str = None) -> None:
        if device is not None:
            self.device: parted.Device = device
        elif device_path:
            self.device: parted.Device = parted.getDevice(device_path)
        else:
            raise parted.DiskException("no device specified")
        self.disk: Disk = parted.newDisk(self.device)
        self.partitions: list = list(map(lambda x: Partition(x), self.disk.partitions))

    def __del__(self) -> None:
        self.device.removeFromCache()

    def get_model(self) -> str:
        return self.device.model.__str__()

    def get_capacity(self) -> int:
        return self.device.getLength() * self.device.sectorSize

    def get_partitions(self) -> list:
        return self.partitions

    def get_path(self) -> str:
        return self.device.path
