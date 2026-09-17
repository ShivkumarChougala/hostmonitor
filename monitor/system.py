import platform
import socket
import time
from datetime import datetime

import psutil


def _format_uptime(seconds):
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m"


def get_system_info():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time

    try:
        distro = platform.freedesktop_os_release().get(
            "PRETTY_NAME", "Linux"
        )
    except Exception:
        distro = "Linux"

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "distribution": distro,
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "uptime": _format_uptime(uptime_seconds),
        "uptime_seconds": int(uptime_seconds),
        "boot_time": datetime.fromtimestamp(boot_time).isoformat()
    }
