import os
import shutil
import subprocess


def _run(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=4,
            check=False
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return ""


def get_virtualization_info():
    kvm_available = os.path.exists("/dev/kvm")
    virsh_available = shutil.which("virsh") is not None

    result = {
        "kvm_available": kvm_available,
        "libvirt_available": virsh_available,
        "uri": None,
        "total_vms": 0,
        "running_vms": 0,
        "stopped_vms": 0,
        "vms": []
    }

    if not virsh_available:
        return result

    result["uri"] = _run([
        "virsh",
        "uri"
    ])

    names = _run([
        "virsh",
        "list",
        "--all",
        "--name"
    ])

    if not names:
        return result

    for name in names.splitlines():

        name = name.strip()

        if not name:
            continue

        state = _run([
            "virsh",
            "domstate",
            name
        ])

        info = _run([
            "virsh",
            "dominfo",
            name
        ])

        vm = {
            "name": name,
            "state": state,
            "vcpu": None,
            "max_memory": None
        }

        for line in info.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(
                ":",
                1
            )

            key = key.strip()
            value = value.strip()

            if key == "CPU(s)":
                try:
                    vm["vcpu"] = int(value)
                except ValueError:
                    pass

            elif key == "Max memory":
                vm["max_memory"] = value

        result["vms"].append(vm)

    result["total_vms"] = len(
        result["vms"]
    )

    result["running_vms"] = sum(
        1
        for vm in result["vms"]
        if vm["state"].lower() == "running"
    )

    result["stopped_vms"] = (
        result["total_vms"] -
        result["running_vms"]
    )

    return result
