import subprocess
import json
from datetime import datetime
import os
import sys
from pymongo import MongoClient

# Add the path to the sys.path list
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utility.submodels import update_submodel
# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result.check_returncode()  # Check if the command ran successfully
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def display_system_info():
    # Processor Information
    CPU_TYPE = "ARMv8"  # Assuming a static value
    cpu_cores = run_command("lscpu | grep '^CPU(s):' | awk '{print $2}'")
    cpu_clock = run_command("lscpu | grep 'Model name' | awk -F '@' '{print $2}' | xargs")
    cpu_usage = run_command("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\\1/' | awk '{print 100 - $1\"%\"}'")
    temp = run_command("cat /sys/class/thermal/thermal_zone*/temp")
    # cpu_temperature = "{:.1f}°C".format(float(temp) / 1000) if temp else None
    cpu_temperature = "42°C"

    # Memory Information
    ram_info = run_command("free -h")
    ram_installed = ram_info.splitlines()[1].split()[1] if ram_info else None
    ram_free = ram_info.splitlines()[1].split()[3] if ram_info else None
    disk_info = run_command("df -H --output=size,avail /")
    disk_installed = disk_info.splitlines()[1].split()[0] if disk_info else None
    disk_free = disk_info.splitlines()[1].split()[1] if disk_info else None

    # Board Temperature - Assuming a static value
    board_temperature = "42°C"

    # Output as JSON
    system_info = {
        "Hardware": {
            "Processor": {
                "CpuType": CPU_TYPE,
                "CpuCores": cpu_cores,
                "CpuClock": cpu_clock,
                "CpuUsage": cpu_usage,
                "CpuTemperature": cpu_temperature
            },
            "Memory": {
                "RAMInstalled": ram_installed,
                "RAMFree": ram_free,
                "DiskInstalled": disk_installed,
                "DiskFree": disk_free
            },
            "BoardTemperature": board_temperature
        },
        "HealthStatus": "NORMAL",
        "LastUpdate": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    return system_info

# Call the function to display the information and print the JSON output
# print(display_system_info())

def update_system_info():
    update_submodel(collectionName=submodels_collection,
                    aas_id_short= AAS_ID_SHORT,
                    submodel_id_short= "SystemInformation",
                    aas_uid=AAS_IDENTIFIER,
                    aasx_server=AASX_SERVER,
                    updated_data=display_system_info(),
                    sync_with_server=True
                    )
    


