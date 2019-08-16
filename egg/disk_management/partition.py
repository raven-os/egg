import parted


class Partition(object):

    def __init__(self, partition: parted.Partition) -> None:
        self.rawPartition = partition

    def get_path(self) -> str:
        return self.rawPartition.path

    def get_capacity(self) -> int:
        return self.rawPartition.getLength()

    def get_filesystem(self) -> parted.FileSystem:
        return self.rawPartition.fileSystem

    def get_start(self) -> int:
        return self.rawPartition.geometry.start

    def get_end(self) -> int:
        return self.rawPartition.geometry.end
