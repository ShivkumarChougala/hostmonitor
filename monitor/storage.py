import os
import time
import psutil
import threading


GB = 1024 ** 3
MB = 1024 ** 2

_lock = threading.Lock()
_previous_io = None
_previous_time = None


def get_storage_info():
    global _previous_io, _previous_time

    usage = psutil.disk_usage("/")
    current_io = psutil.disk_io_counters()
    now = time.monotonic()

    read_speed = 0.0
    write_speed = 0.0

    with _lock:
        if _previous_io is not None and _previous_time is not None:
            elapsed = now - _previous_time

            if elapsed > 0:
                read_speed = (
                    current_io.read_bytes -
                    _previous_io.read_bytes
                ) / elapsed

                write_speed = (
                    current_io.write_bytes -
                    _previous_io.write_bytes
                ) / elapsed

        _previous_io = current_io
        _previous_time = now

    device = "Unknown"
    model = "Unknown"

    try:
        root_device = os.stat("/").st_dev

        for partition in psutil.disk_partitions():
            try:
                if os.stat(partition.mountpoint).st_dev == root_device:
                    device = partition.device
                    break
            except OSError:
                continue
    except Exception:
        pass

    # Your host currently uses nvme0n1.
    try:
        with open(
            "/sys/block/nvme0n1/device/model",
            "r"
        ) as f:
            model = f.read().strip()
    except OSError:
        pass

    return {
        "device": device,
        "model": model,

        "total_gb": round(usage.total / GB, 2),
        "used_gb": round(usage.used / GB, 2),
        "free_gb": round(usage.free / GB, 2),
        "percent": round(usage.percent, 1),

        "read_mb_s": round(read_speed / MB, 2),
        "write_mb_s": round(write_speed / MB, 2)
    }
