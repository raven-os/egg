import parted

from egg.install_queue.install_event import InstallEvent


class Partition(object):

    def __init__(self, partition: parted.Partition):
        self.rawPartition = partition

    @property
    def path(self) -> str:
        return self.rawPartition.path

    @property
    def capacity(self) -> int:
        return self.rawPartition.getLength()

    @property
    def filesystem(self) -> parted.FileSystem:
        return self.rawPartition.fileSystem

    @property
    def start(self) -> int:
        return self.rawPartition.geometry.start

    @property
    def end(self) -> int:
        return self.rawPartition.geometry.end


class PartitionInstallEvent(InstallEvent):

    def __init__(self, disk_path: str, partition_number: int, method_name: str, **kwargs):
        super().__init__(InstallEvent.EventType.PARTITION, method_name, **kwargs)
        self.disk_path = disk_path
        self.partition_number = partition_number

    def exec(self):
        from egg.disk_management import Disk
        partition = Partition(Disk(device_path=self.disk_path).partitions[self.partition_number])
        getattr(partition, self.method_name)(**self.kwargs)
