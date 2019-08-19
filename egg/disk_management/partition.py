import parted


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
