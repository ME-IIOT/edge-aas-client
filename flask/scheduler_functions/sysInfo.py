# import subprocess
# import json
from datetime import datetime
import os
# import sys
from pymongo import MongoClient

# Add the path to the sys.path list
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utility.submodels import update_submodel, async_update_submodel
from utility.utility import run_command, run_bash_script
# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI')
AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
AAS_IDENTIFIER = os.environ.get('AAS_IDENTIFIER')
AASX_SERVER = os.environ.get('AASX_SERVER')

client = MongoClient(MONGO_URI)
db = client['aas_edge_database']
shells_collection = db['shells']
submodels_collection = db['submodels']

# def display_system_info():
#     # Processor Information
#     CPU_TYPE = "ARMv8"  # Assuming a static value
#     cpu_cores = run_command("lscpu | grep '^CPU(s):' | awk '{print $2}'")
#     cpu_clock = run_command("lscpu | grep 'Model name' | awk -F '@' '{print $2}' | xargs")
#     cpu_usage = run_command("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\\1/' | awk '{print 100 - $1\"%\"}'")
#     temp = run_command("cat /sys/class/thermal/thermal_zone*/temp")
#     # cpu_temperature = "{:.1f}°C".format(float(temp) / 1000) if temp else None

#     cpu_temperature = "42°C"

#     # Memory Information
#     ram_info = run_command("free -h")
#     ram_installed = ram_info.splitlines()[1].split()[1] if ram_info else None
#     ram_free = ram_info.splitlines()[1].split()[3] if ram_info else None
#     disk_info = run_command("df -H --output=size,avail /")
#     disk_installed = disk_info.splitlines()[1].split()[0] if disk_info else None
#     disk_free = disk_info.splitlines()[1].split()[1] if disk_info else None

#     # Board Temperature - Assuming a static value
#     board_temperature = "42°C"

#     # Output as JSON
#     system_info = {
#         "Hardware": {
#             "Processor": {
#                 "CpuType": CPU_TYPE,
#                 "CpuCores": cpu_cores,
#                 "CpuClock": cpu_clock,
#                 "CpuUsage": cpu_usage,
#                 "CpuTemperature": cpu_temperature
#             },
#             "Memory": {
#                 "RAMInstalled": ram_installed,
#                 "RAMFree": ram_free,
#                 "DiskInstalled": disk_installed,
#                 "DiskFree": disk_free
#             },
#             "BoardTemperature": board_temperature
#         },
#         "HealthStatus": "NORMAL",
#         "LastUpdate": datetime.now().isoformat()
#     }
#     return system_info

# Call the function to display the information and print the JSON output
# print(display_system_info())

# def update_system_info():
#     try:
#         update_submodel(collectionName=submodels_collection,
#                     aas_id_short= AAS_ID_SHORT,
#                     submodel_id_short= "SystemInformation",
#                     aas_uid=AAS_IDENTIFIER,
#                     aasx_server=AASX_SERVER,
#                     updated_data=display_system_info(),
#                     sync_with_server=True
#                     )
#     except Exception as e:
#         raise e

# async def display_system_info_wrapper():
#     # Here, you can switch between different implementations
#     # or modify the behavior before calling the actual function.
#     return display_system_info()  # This could be a call to the original or a modified version

import asyncio
async def update_system_info_async():
    try:
        print("update sysInfo")
        import os
        import json
        current_directory = os.getcwd()
        update_data = await run_bash_script(f"{current_directory}/scheduler_functions/mounted_script/sysInfo.sh")
        update_data = json.loads(update_data)
        # print("Current Working Directory:", current_directory)
        # print("Updating System Information")
        await async_update_submodel(collectionName=submodels_collection,
                        aas_id_short= AAS_ID_SHORT,
                        submodel_id_short= "SystemInformation",
                        aas_uid=AAS_IDENTIFIER,
                        aasx_server=AASX_SERVER,
                        # updated_data= await asyncio.to_thread(display_system_info()),
                        # updated_data= display_system_info(),
                        updated_data= update_data,
                        sync_with_server=True
                        )
    except Exception as e:
        print(f"Error executing update_system_info_async: {e}")

# def update_system_info_async():
#     try:
#         print("Updating System Information")
#         asyncio.run(async_update_submodel(collectionName=submodels_collection,
#                         aas_id_short= AAS_ID_SHORT,
#                         submodel_id_short= "SystemInformation",
#                         aas_uid=AAS_IDENTIFIER,
#                         aasx_server=AASX_SERVER,
#                         updated_data= display_system_info(),
#                         sync_with_server=True
#                         ))
#     except Exception as e:
#         print(f"Error executing update_system_info_async: {e}")
