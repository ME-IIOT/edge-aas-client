#!/bin/bash

# Function to display system information
display_system_info() {
    # Processor Information
    # CPU_TYPE="ARMv8"  # Assuming a static value
    CPU_TYPE=$(lscpu | grep "Architecture" | awk '{print $2}')
    CPU_CORES=$(lscpu | grep "^CPU(s):" | awk '{print $2}')
    CPU_CLOCK=$(lscpu | grep "Model name" | awk -F '@' '{print $2}' | xargs)
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')
    TEMP=$(cat /sys/class/thermal/thermal_zone*/temp)
    CPU_TEMPERATURE=$(awk "BEGIN {printf \"%.1f°C\n\", $TEMP/1000}")

    # Memory Information
    RAM_INSTALLED=$(free -h | awk '/Mem:/ {print $2}')
    RAM_FREE=$(free -h | awk '/Mem:/ {print $4}')
    DISK_INSTALLED=$(df -H --output=size / | tail -n 1 | awk '{print $1}')
    DISK_FREE=$(df -H --output=avail / | tail -n 1 | awk '{print $1}')

    # Board Temperature - Assuming a static value
    BOARD_TEMPERATURE=$(vxsensors_lib_test humTemp | grep "Temperatur" | awk '{print $2}') 

    # Output as JSON
    echo -e "{
    \"Hardware\": {
        \"Processor\": {
            \"CpuType\": \"$CPU_TYPE\",
            \"CpuCores\": \"$CPU_CORES\",
            \"CpuClock\": \"$CPU_CLOCK\",
            \"CpuUsage\": \"$CPU_USAGE\",
            \"CpuTemperature\": \"$CPU_TEMPERATURE\"
        },
        \"Memory\": {
            \"RAMInstalled\": \"$RAM_INSTALLED\",
            \"RAMFree\": \"$RAM_FREE\",
            \"DiskInstalled\": \"$DISK_INSTALLED\",
            \"DiskFree\": \"$DISK_FREE\"
        },
        \"BoardTemperature\": \"$BOARD_TEMPERATURE\"
    },
    \"HealthStatus\": \"NORMAL\",
    \"LastUpdate\": \"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\"
}"
}

# Call the function to display the information
display_system_info
