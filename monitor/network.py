import time
import psutil
import threading


MB = 1024 ** 2

_lock = threading.Lock()
_previous = {}
_previous_time = {}


def _primary_interface():
    stats = psutil.net_if_stats()

    preferred = [
        "wlan0",
        "eth0",
        "enp0s31f6"
    ]

    for interface in preferred:
        if (
            interface in stats
            and stats[interface].isup
        ):
            return interface

    for interface, info in stats.items():
        if interface != "lo" and info.isup:
            return interface

    return None


def get_network_info():
    interface = _primary_interface()

    if interface is None:
        return {
            "interface": None,
            "connected": False
        }

    counters = psutil.net_io_counters(
        pernic=True
    )

    if interface not in counters:
        return {
            "interface": interface,
            "connected": False
        }

    current = counters[interface]
    now = time.monotonic()

    download = 0
    upload = 0

    with _lock:
        previous = _previous.get(interface)
        previous_time = _previous_time.get(interface)

        if previous and previous_time:
            elapsed = now - previous_time

            if elapsed > 0:
                download = (
                    current.bytes_recv -
                    previous.bytes_recv
                ) / elapsed

                upload = (
                    current.bytes_sent -
                    previous.bytes_sent
                ) / elapsed

        _previous[interface] = current
        _previous_time[interface] = now

    return {
        "interface": interface,
        "connected": True,

        "download_mb_s":
            round(download / MB, 2),

        "upload_mb_s":
            round(upload / MB, 2),

        "total_received_gb":
            round(
                current.bytes_recv /
                (1024 ** 3),
                2
            ),

        "total_sent_gb":
            round(
                current.bytes_sent /
                (1024 ** 3),
                2
            ),

        "packets_received":
            current.packets_recv,

        "packets_sent":
            current.packets_sent,

        "errors_in":
            current.errin,

        "errors_out":
            current.errout
    }
