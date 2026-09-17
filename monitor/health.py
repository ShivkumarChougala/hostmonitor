def get_health_info(
    cpu,
    memory,
    storage,
    thermal
):
    warnings = []
    score = 100

    cpu_usage = cpu["usage"]
    ram_usage = memory["ram"]["percent"]
    disk_usage = storage["percent"]

    cpu_temp = None

    if thermal["cpu_package"]:
        cpu_temp = thermal[
            "cpu_package"
        ]["temperature"]

    # CPU
    if cpu_usage >= 90:
        warnings.append({
            "type": "cpu",
            "severity": "critical",
            "message": "CPU usage is extremely high."
        })
        score -= 25

    elif cpu_usage >= 75:
        warnings.append({
            "type": "cpu",
            "severity": "warning",
            "message": "CPU usage is high."
        })
        score -= 10

    # RAM
    if ram_usage >= 90:
        warnings.append({
            "type": "memory",
            "severity": "critical",
            "message": "RAM pressure is critical."
        })
        score -= 25

    elif ram_usage >= 80:
        warnings.append({
            "type": "memory",
            "severity": "warning",
            "message": "RAM usage is high."
        })
        score -= 10

    # STORAGE
    if disk_usage >= 95:
        warnings.append({
            "type": "storage",
            "severity": "critical",
            "message": "Storage is almost full."
        })
        score -= 30

    elif disk_usage >= 85:
        warnings.append({
            "type": "storage",
            "severity": "warning",
            "message": "Storage space is running low."
        })
        score -= 15

    # TEMPERATURE
    if cpu_temp is not None:

        if cpu_temp >= 95:
            warnings.append({
                "type": "temperature",
                "severity": "critical",
                "message": "CPU temperature is critical."
            })
            score -= 30

        elif cpu_temp >= 85:
            warnings.append({
                "type": "temperature",
                "severity": "warning",
                "message": "CPU temperature is high."
            })
            score -= 15

    score = max(score, 0)

    if score >= 90:
        status = "good"

    elif score >= 70:
        status = "moderate"

    elif score >= 50:
        status = "constrained"

    else:
        status = "critical"

    return {
        "score": score,
        "status": status,
        "warnings": warnings
    }
