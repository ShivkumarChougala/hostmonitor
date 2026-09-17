const $ = id => document.getElementById(id);


function setText(id, value) {
    const el = $(id);

    if (el) {
        el.textContent = value;
    }
}


function setBar(id, value) {
    const el = $(id);

    if (!el) return;

    const percent = Math.max(
        0,
        Math.min(100, Number(value) || 0)
    );

    el.style.width = `${percent}%`;

    if (percent >= 90) {
        el.style.background = "var(--red)";
    } else if (percent >= 80) {
        el.style.background = "var(--yellow)";
    } else {
        el.style.background = "var(--accent)";
    }
}


function statusForPercent(value) {
    if (value >= 90) {
        return ["CRITICAL", "critical"];
    }

    if (value >= 80) {
        return ["HIGH", "warning"];
    }

    return ["GOOD", "good"];
}


function setBadge(id, text, type = "") {
    const el = $(id);

    if (!el) return;

    el.textContent = text;

    el.className = "badge";

    if (type) {
        el.classList.add(type);
    }
}


function recommendation(value) {
    if (value === "safe") {
        return ["SAFE", "good"];
    }

    if (value === "check") {
        return ["CHECK", "warning"];
    }

    return ["NOT ADVISED", "critical"];
}


function renderCPU(cpu) {

    setText("cpu-usage", cpu.usage.toFixed(1));

    setBar(
        "cpu-bar",
        cpu.usage
    );

    const cpuStatus = statusForPercent(
        cpu.usage
    );

    setBadge(
        "cpu-state",
        cpuStatus[0],
        cpuStatus[1]
    );

    setText(
        "cpu-model",
        cpu.model
    );

    setText(
        "cpu-cores",
        cpu.physical_cores
    );

    setText(
        "cpu-threads",
        cpu.threads
    );

    setText(
        "cpu-clock",
        cpu.frequency_ghz !== null
            ? `${cpu.frequency_ghz} GHz`
            : "--"
    );

    setText(
        "cpu-max",
        cpu.max_frequency_ghz !== null
            ? `${cpu.max_frequency_ghz} GHz`
            : "--"
    );

    setText(
        "load-1",
        cpu.load["1m"]
    );

    setText(
        "load-5",
        cpu.load["5m"]
    );

    setText(
        "load-15",
        cpu.load["15m"]
    );


    const coreList = $("core-list");

    coreList.innerHTML = "";

    cpu.per_core.forEach(
        (usage, index) => {

            const row =
                document.createElement("div");

            row.className = "core-row";

            row.innerHTML = `
                <span>CPU${index}</span>

                <div class="core-bar">
                    <div
                        class="core-fill"
                        style="width:${usage}%">
                    </div>
                </div>

                <span>${usage.toFixed(1)}%</span>
            `;

            coreList.appendChild(row);
        }
    );
}


function renderMemory(memory) {

    const ram = memory.ram;
    const swap = memory.swap;

    setText(
        "ram-percent",
        ram.percent.toFixed(1)
    );

    setBar(
        "ram-bar",
        ram.percent
    );

    const status = statusForPercent(
        ram.percent
    );

    setBadge(
        "ram-state",
        status[0],
        status[1]
    );

    setText(
        "ram-used",
        `${ram.used_gb} GB`
    );

    setText(
        "ram-available",
        `${ram.available_gb} GB`
    );

    setText(
        "ram-total",
        `${ram.total_gb} GB`
    );

    setText(
        "swap",
        `${swap.used_gb} / ${swap.total_gb} GB`
    );
}


function renderStorage(storage) {

    setText(
        "disk-percent",
        storage.percent.toFixed(1)
    );

    setBar(
        "disk-bar",
        storage.percent
    );

    const status = statusForPercent(
        storage.percent
    );

    setBadge(
        "disk-state",
        status[0],
        status[1]
    );

    setText(
        "disk-model",
        storage.model
    );

    setText(
        "disk-used",
        `${storage.used_gb} GB`
    );

    setText(
        "disk-free",
        `${storage.free_gb} GB`
    );

    setText(
        "disk-read",
        `${storage.read_mb_s} MB/s`
    );

    setText(
        "disk-write",
        `${storage.write_mb_s} MB/s`
    );
}


function renderThermals(thermal) {

    if (thermal.cpu_package) {

        const temp =
            thermal.cpu_package.temperature;

        setText(
            "cpu-temp",
            temp.toFixed(0)
        );

        let state = "NORMAL";
        let type = "good";

        if (temp >= 95) {
            state = "CRITICAL";
            type = "critical";
        } else if (temp >= 85) {
            state = "HOT";
            type = "critical";
        } else if (temp >= 70) {
            state = "WARM";
            type = "warning";
        }

        setBadge(
            "temp-state",
            state,
            type
        );
    }


    const list = $("thermal-list");

    list.innerHTML = "";


    thermal.cores.forEach(sensor => {

        const row =
            document.createElement("div");

        row.className = "thermal-row";

        row.innerHTML = `
            <span class="thermal-name">
                ${sensor.name}
            </span>

            <strong>
                ${sensor.temperature}°C
            </strong>

            <span class="${sensor.status === "normal"
                ? "good"
                : "warning"}">
                ${sensor.status.toUpperCase()}
            </span>
        `;

        list.appendChild(row);
    });


    const extras = [
        ["NVMe", thermal.nvme],
        ["PCH", thermal.pch],
        ["Wi-Fi", thermal.wifi]
    ];


    extras.forEach(([name, sensor]) => {

        if (!sensor) return;

        const row =
            document.createElement("div");

        row.className = "thermal-row";

        row.innerHTML = `
            <span class="thermal-name">
                ${name}
            </span>

            <strong>
                ${sensor.temperature}°C
            </strong>

            <span class="${sensor.status === "normal"
                ? "good"
                : "warning"}">
                ${sensor.status.toUpperCase()}
            </span>
        `;

        list.appendChild(row);
    });


    const fans = $("fan-list");

    fans.innerHTML = "";

    thermal.fans.forEach(fan => {

        const row =
            document.createElement("div");

        row.className = "fan-row";

        row.innerHTML = `
            <span class="thermal-name">
                ${fan.name}
            </span>

            <strong>
                ${fan.rpm} RPM
            </strong>

            <span></span>
        `;

        fans.appendChild(row);
    });
}


function renderNetwork(network) {

    setBadge(
        "network-state",
        network.connected
            ? "CONNECTED"
            : "OFFLINE",
        network.connected
            ? "good"
            : "critical"
    );

    setText(
        "network-interface",
        network.interface || "--"
    );

    setText(
        "download",
        network.download_mb_s ?? 0
    );

    setText(
        "upload",
        network.upload_mb_s ?? 0
    );

    setText(
        "total-rx",
        `${network.total_received_gb ?? 0} GB`
    );

    setText(
        "total-tx",
        `${network.total_sent_gb ?? 0} GB`
    );

    setText(
        "rx-errors",
        network.errors_in ?? 0
    );

    setText(
        "tx-errors",
        network.errors_out ?? 0
    );
}


function renderVirtualization(v) {

    setText(
        "kvm",
        v.kvm_available
            ? "AVAILABLE"
            : "UNAVAILABLE"
    );

    setText(
        "libvirt",
        v.libvirt_available
            ? "AVAILABLE"
            : "UNAVAILABLE"
    );

    setText(
        "libvirt-uri",
        v.uri || "--"
    );

    setText(
        "vm-running",
        v.running_vms
    );

    setText(
        "vm-stopped",
        v.stopped_vms
    );

    setText(
        "vm-total",
        v.total_vms
    );


    const list = $("vm-list");

    list.innerHTML = "";


    if (!v.vms.length) {

        list.innerHTML = `
            <div class="muted"
                 style="padding-top:18px;
                        font-family:monospace;
                        font-size:10px;">
                No virtual machines defined.
            </div>
        `;

        return;
    }


    v.vms.forEach(vm => {

        const row =
            document.createElement("div");

        row.className = "vm-item";

        row.innerHTML = `
            <span>${vm.name}</span>
            <span>${vm.state}</span>
        `;

        list.appendChild(row);
    });
}


function renderDocker(docker) {

    setBadge(
        "docker-count",
        `${docker.running} RUNNING`,
        docker.running > 0
            ? "good"
            : ""
    );


    const list = $("docker-list");

    list.innerHTML = "";


    if (!docker.containers.length) {

        list.innerHTML = `
            <div class="muted">
                No running containers.
            </div>
        `;

        return;
    }


    docker.containers.forEach(container => {

        const row =
            document.createElement("div");

        row.className = "docker-container";

        row.innerHTML = `
            <div>
                <small>CONTAINER</small>
                <strong>${container.name}</strong>
            </div>

            <div>
                <small>CPU</small>
                ${container.cpu}
            </div>

            <div>
                <small>MEMORY</small>
                ${container.memory}
            </div>

            <div>
                <small>NETWORK</small>
                ${container.network_io}
            </div>

            <div>
                <small>PIDS</small>
                ${container.pids}
            </div>
        `;

        list.appendChild(row);
    });
}


function renderCapacity(capacity) {

    setText(
        "capacity-cpu",
        `${capacity.cpu_headroom_percent}%`
    );

    setText(
        "capacity-ram",
        `${capacity.available_ram_gb} GB`
    );

    setText(
        "capacity-storage",
        `${capacity.free_storage_gb} GB`
    );


    if (capacity.main_constraint) {

        setBadge(
            "constraint-badge",
            `LIMIT: ${capacity.main_constraint.toUpperCase()}`,
            "warning"
        );

    } else {

        setBadge(
            "constraint-badge",
            "NO CONSTRAINT",
            "good"
        );
    }


    const mappings = [
        ["vm-2gb", capacity.recommendations["2gb_vm"]],
        ["vm-4gb", capacity.recommendations["4gb_vm"]],
        ["vm-8gb", capacity.recommendations["8gb_vm"]]
    ];


    mappings.forEach(([id, value]) => {

        const [text, type] =
            recommendation(value);

        const element = $(id);

        element.textContent = text;
        element.className = type;
    });
}


function renderHealth(health) {

    setText(
        "health-score",
        `${health.score}/100`
    );

    const type =
        health.status === "good"
            ? "good"
            : health.status === "critical"
            ? "critical"
            : "warning";

    const hostStatus =
        $("host-status");

    hostStatus.textContent =
        health.status.toUpperCase();

    hostStatus.className = type;


    setBadge(
        "warning-count",
        health.warnings.length.toString(),
        health.warnings.length
            ? "warning"
            : "good"
    );


    const container =
        $("warnings");

    container.innerHTML = "";


    if (!health.warnings.length) {

        container.innerHTML = `
            <div class="no-warning">
                No active host warnings.
            </div>
        `;

        return;
    }


    health.warnings.forEach(warning => {

        const div =
            document.createElement("div");

        div.className = "warning-item";

        div.textContent =
            `${warning.type.toUpperCase()} / ${warning.message}`;

        container.appendChild(div);
    });
}


function renderProcesses(processes) {

    const tbody =
        $("process-table");

    tbody.innerHTML = "";


    processes.forEach(process => {

        const row =
            document.createElement("tr");

        row.innerHTML = `
            <td>${process.pid}</td>
            <td>${process.name}</td>
            <td>${process.username}</td>
            <td>${process.cpu_percent}%</td>
            <td>${process.memory_percent}%</td>
            <td>${process.memory_mb} MB</td>
        `;

        tbody.appendChild(row);
    });
}


function renderSystem(system) {

    setText(
        "hostname",
        system.hostname
    );

    setText(
        "distribution",
        system.distribution
    );

    setText(
        "uptime",
        system.uptime
    );

    setText(
        "kernel",
        system.kernel
    );

    setText(
        "architecture",
        system.architecture
    );
}


async function updateDashboard() {

    try {

        const response =
            await fetch(
                "/api/overview",
                {
                    cache: "no-store"
                }
            );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();


        renderSystem(data.system);
        renderCPU(data.cpu);
        renderMemory(data.memory);
        renderStorage(data.storage);
        renderThermals(data.thermal);
        renderNetwork(data.network);
        renderVirtualization(
            data.virtualization
        );
        renderDocker(data.docker);
        renderCapacity(data.capacity);
        renderHealth(data.health);
        renderProcesses(data.processes);


        setText(
            "refresh-time",
            new Date().toLocaleTimeString()
        );

    } catch (error) {

        console.error(
            "Dashboard update failed:",
            error
        );

        const live =
            document.querySelector(".live");

        if (live) {
            live.textContent =
                "● CONNECTION LOST";

            live.style.color =
                "var(--red)";
        }
    }
}


function updateClock() {

    setText(
        "clock",
        new Date().toLocaleTimeString()
    );
}


updateClock();

setInterval(
    updateClock,
    1000
);


updateDashboard();

setInterval(
    updateDashboard,
    2000
);
