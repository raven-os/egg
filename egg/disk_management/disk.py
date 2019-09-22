import copy
from typing import List

import parted

from egg.disk_management.partition import Partition
from egg.install_queue.install_event import InstallEvent
from egg.install_queue.install_queue import InstallQueue


class Disk(object):

    def __init__(self, device: parted.Device = None, device_path: str = None, is_managed: bool = True):
        if device is not None:
            self.device: parted.Device = device
        elif device_path:
            self.device: parted.Device = parted.getDevice(device_path)
        else:
            raise parted.DiskException("no device specified")
        self.disk: parted.Disk = parted.newDisk(self.device)
        self.partitions: List[Partition] = list(map(lambda x: Partition(x), self.disk.partitions))
        self.is_managed: bool = is_managed

    def __del__(self):
        self.device.removeFromCache()

    def write_table(self, table_name: str):
        if self.is_managed:
            self.disk = parted.freshDisk(self.device, table_name)
        else:
            event = DiskInstallEvent(self.path, self.write_table.__name__, table_name=table_name)
            InstallQueue().add(event)

    def to_unmanaged(self):
        unmanaged_disk = copy.copy(self)
        unmanaged_disk.is_managed = False
        return unmanaged_disk

    @property
    def model(self) -> str:
        return str(self.device.model)

    @property
    def type(self) -> str:
        return self.disk.type

    @property
    def capacity(self) -> int:
        return self.device.getLength() * self.device.sectorSize

    @property
    def path(self) -> str:
        return self.device.path


class DiskInstallEvent(InstallEvent):

    def __init__(self, device_path: str, method_name: str, **kwargs):
        super().__init__(InstallEvent.EventType.DISK, method_name, **kwargs)
        self.device_path = device_path

    def exec(self):
        disk = Disk(device_path=self.device_path)
        getattr(disk, self.method_name)(**self.kwargs)
