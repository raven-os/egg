import parted


class Disk(object):
    def __init__(self, device_path):
        self.device = parted.getDevice(device_path)
        self.disk = parted.newDisk(self.device)
        self.partitions = list(map(lambda x: Partition(x), self.disk.partitions))

    def __init__(self, device):
        self.device = device
        self.disk = parted.newDisk(self.device)
        self.partitions = list(map(lambda x: Partition(x), self.disk.partitions))

    def get_model(self):
        return self.device.model

    def get_capacity(self):
        return self.device.lenght * self.device.sectorSize

    def get_partitions(self):
        return self.partitions
