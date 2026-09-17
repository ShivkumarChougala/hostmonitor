from flask import Flask, jsonify, render_template

from monitor.system import get_system_info
from monitor.cpu import get_cpu_info
from monitor.memory import get_memory_info
from monitor.thermal import get_thermal_info
from monitor.storage import get_storage_info
from monitor.network import get_network_info
from monitor.docker import get_docker_info
from monitor.virtualization import get_virtualization_info
from monitor.processes import get_top_processes
from monitor.health import get_health_info
from monitor.capacity import get_capacity_info


app = Flask(__name__)


def collect_all():

    system = get_system_info()
    cpu = get_cpu_info()
    memory = get_memory_info()
    thermal = get_thermal_info()
    storage = get_storage_info()
    network = get_network_info()

    virtualization = (
        get_virtualization_info()
    )

    docker = get_docker_info()

    processes = get_top_processes()

    health = get_health_info(
        cpu,
        memory,
        storage,
        thermal
    )

    capacity = get_capacity_info(
        cpu,
        memory,
        storage,
        thermal
    )

    return {
        "system": system,
        "cpu": cpu,
        "memory": memory,
        "thermal": thermal,
        "storage": storage,
        "network": network,
        "virtualization": virtualization,
        "docker": docker,
        "processes": processes,
        "health": health,
        "capacity": capacity
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/overview")
def api_overview():
    return jsonify(collect_all())


@app.route("/api/system")
def api_system():
    return jsonify(get_system_info())


@app.route("/api/cpu")
def api_cpu():
    return jsonify(get_cpu_info())


@app.route("/api/memory")
def api_memory():
    return jsonify(get_memory_info())


@app.route("/api/thermal")
def api_thermal():
    return jsonify(get_thermal_info())


@app.route("/api/storage")
def api_storage():
    return jsonify(get_storage_info())


@app.route("/api/network")
def api_network():
    return jsonify(get_network_info())


@app.route("/api/docker")
def api_docker():
    return jsonify(get_docker_info())


@app.route("/api/vms")
def api_vms():
    return jsonify(
        get_virtualization_info()
    )


@app.route("/api/processes")
def api_processes():
    return jsonify(
        get_top_processes()
    )


if __name__ == "__main__":

    print()
    print("VM Host Monitor")
    print("----------------------------")
    print("Dashboard : http://127.0.0.1:5000")
    print("API       : http://127.0.0.1:5000/api/overview")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
