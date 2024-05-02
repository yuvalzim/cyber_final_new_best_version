import psutil
import os


def get_disk_names():
    disk_names = []
    for partition in psutil.disk_partitions(all=True):
        disk_names.append(partition.device)
    return disk_names


def move_to_quarantine(path):
    try:
        os.replace(path, f"Quarantine\\{os.path.basename(path)}")
    except OSError as e:
        print(e)
