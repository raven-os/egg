class disk_service(object):

    def get_disk_list():
        return list(map(lambda x: Disk(x), parted.getAllDevices()))

    def get_disk(device_path):
        return Disk(device_path)
