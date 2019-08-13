import parted


class Partition(object):

    def __init__(self, partition: parted.Partition):
        self.rawPartition = partition

    def get_path(self):
        return self.rawPartition.path

    def get_capacity(self):
        return self.rawPartition.getLength()

    def get_filesystem(self):
        return .self.rawPartition.fileSystem.type
