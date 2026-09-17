import psutil


GB = 1024 ** 3


def get_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "ram": {
            "total_gb": round(memory.total / GB, 2),
            "used_gb": round(memory.used / GB, 2),
            "available_gb": round(memory.available / GB, 2),
            "percent": round(memory.percent, 1)
        },

        "swap": {
            "total_gb": round(swap.total / GB, 2),
            "used_gb": round(swap.used / GB, 2),
            "free_gb": round(swap.free / GB, 2),
            "percent": round(swap.percent, 1)
        }
    }
