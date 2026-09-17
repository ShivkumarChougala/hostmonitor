import psutil


def _temp_status(temp):
    if temp >= 95:
        return "critical"
    if temp >= 85:
        return "hot"
    if temp >= 70:
        return "warm"

    return "normal"


def get_thermal_info():
    result = {
        "cpu_package": None,
        "cores": [],
        "nvme": None,
        "pch": None,
        "wifi": None,
        "fans": []
    }

    try:
        temperatures = psutil.sensors_temperatures()
    except Exception:
        temperatures = {}

    for chip, entries in temperatures.items():
        chip_lower = chip.lower()

        for entry in entries:
            label = entry.label or chip
            label_lower = label.lower()

            if "coretemp" in chip_lower:

                if "package" in label_lower:
                    result["cpu_package"] = {
                        "temperature": round(entry.current, 1),
                        "status": _temp_status(entry.current)
                    }

                elif "core" in label_lower:
                    result["cores"].append({
                        "name": label,
                        "temperature": round(entry.current, 1),
                        "status": _temp_status(entry.current)
                    })

            elif "nvme" in chip_lower and result["nvme"] is None:
                result["nvme"] = {
                    "temperature": round(entry.current, 1),
                    "status": _temp_status(entry.current)
                }

            elif "pch" in chip_lower:
                result["pch"] = {
                    "temperature": round(entry.current, 1),
                    "status": _temp_status(entry.current)
                }

            elif "iwlwifi" in chip_lower:
                result["wifi"] = {
                    "temperature": round(entry.current, 1),
                    "status": _temp_status(entry.current)
                }

    try:
        fans = psutil.sensors_fans()
    except Exception:
        fans = {}

    for chip, entries in fans.items():
        for index, entry in enumerate(entries, start=1):
            result["fans"].append({
                "name": entry.label or f"Fan {index}",
                "rpm": round(entry.current)
            })

    return result
