import psutil


def get_top_processes(limit=8):
    processes = []

    for proc in psutil.process_iter([
        "pid",
        "name",
        "username",
        "cpu_percent",
        "memory_percent",
        "memory_info"
    ]):

        try:
            info = proc.info

            rss = (
                info["memory_info"].rss
                if info["memory_info"]
                else 0
            )

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "username": info["username"],

                "cpu_percent": round(
                    info["cpu_percent"] or 0,
                    1
                ),

                "memory_percent": round(
                    info["memory_percent"] or 0,
                    1
                ),

                "memory_mb": round(
                    rss / (1024 ** 2),
                    1
                )
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            continue

    processes.sort(
        key=lambda x: (
            x["cpu_percent"],
            x["memory_percent"]
        ),
        reverse=True
    )

    return processes[:limit]
