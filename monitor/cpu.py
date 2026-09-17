import os
import psutil


def _get_cpu_model():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass

    return "Unknown CPU"


def get_cpu_info():
    usage = psutil.cpu_percent(interval=0.15)
    per_core = psutil.cpu_percent(interval=None, percpu=True)
    frequency = psutil.cpu_freq()

    try:
        load1, load5, load15 = os.getloadavg()
    except OSError:
        load1 = load5 = load15 = 0

    return {
        "model": _get_cpu_model(),
        "usage": round(usage, 1),
        "physical_cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),

        "frequency_mhz": (
            round(frequency.current, 0)
            if frequency else None
        ),

        "frequency_ghz": (
            round(frequency.current / 1000, 2)
            if frequency else None
        ),

        "max_frequency_ghz": (
            round(frequency.max / 1000, 2)
            if frequency and frequency.max
            else None
        ),

        "per_core": [
            round(value, 1)
            for value in per_core
        ],

        "load": {
            "1m": round(load1, 2),
            "5m": round(load5, 2),
            "15m": round(load15, 2)
        }
    }
