def get_capacity_info(
    cpu,
    memory,
    storage,
    thermal
):
    available_ram = memory[
        "ram"
    ]["available_gb"]

    free_storage = storage[
        "free_gb"
    ]

    cpu_usage = cpu["usage"]

    cpu_headroom = max(
        0,
        100 - cpu_usage
    )

    cpu_temp = None

    if thermal["cpu_package"]:
        cpu_temp = thermal[
            "cpu_package"
        ]["temperature"]

    constraints = []

    if available_ram < 8:
        constraints.append("memory")

    if free_storage < 80:
        constraints.append("storage")

    if cpu_headroom < 30:
        constraints.append("cpu")

    if (
        cpu_temp is not None
        and cpu_temp >= 85
    ):
        constraints.append("thermal")

    def evaluate_vm(
        ram_required,
        storage_required
    ):
        # Keep RAM reserve for host.
        ram_safe = (
            available_ram -
            ram_required
        ) >= 4

        # Keep storage reserve.
        disk_safe = (
            free_storage -
            storage_required
        ) >= 30

        cpu_safe = cpu_headroom >= 30

        thermal_safe = (
            cpu_temp is None
            or cpu_temp < 85
        )

        if (
            ram_safe
            and disk_safe
            and cpu_safe
            and thermal_safe
        ):
            return "safe"

        if (
            available_ram >= ram_required
            and free_storage >= storage_required
        ):
            return "check"

        return "not_advised"

    recommendations = {
        "2gb_vm": evaluate_vm(
            ram_required=2,
            storage_required=20
        ),

        "4gb_vm": evaluate_vm(
            ram_required=4,
            storage_required=30
        ),

        "8gb_vm": evaluate_vm(
            ram_required=8,
            storage_required=50
        )
    }

    return {
        "available_ram_gb":
            available_ram,

        "free_storage_gb":
            free_storage,

        "cpu_headroom_percent":
            round(cpu_headroom, 1),

        "constraints":
            constraints,

        "main_constraint":
            constraints[0]
            if constraints
            else None,

        "recommendations":
            recommendations
    }
