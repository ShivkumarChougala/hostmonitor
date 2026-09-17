import shutil
import subprocess


def _run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return ""


def get_docker_info():
    if shutil.which("docker") is None:
        return {
            "available": False,
            "running": 0,
            "containers": []
        }

    output = _run([
        "docker",
        "stats",
        "--no-stream",
        "--format",
        "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|"
        "{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}|{{.PIDs}}"
    ])

    containers = []

    if output:
        for line in output.splitlines():

            parts = line.split("|")

            if len(parts) != 7:
                continue

            containers.append({
                "name": parts[0],
                "cpu": parts[1],
                "memory": parts[2],
                "memory_percent": parts[3],
                "network_io": parts[4],
                "block_io": parts[5],
                "pids": parts[6]
            })

    return {
        "available": True,
        "running": len(containers),
        "containers": containers
    }
