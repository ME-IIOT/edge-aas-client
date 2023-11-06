# AASX Server & Client Guide

This document provides straightforward steps to set up and run the AASX Server (IDTA) and AAS Client using Docker. Ensure your AASX package is located under the `aasxs` folder before you begin.

## AASX Server - IDTA (Local Setup)
The demo server support AAS v2. 

### Starting the AASX Server

1. Use the following command to start the server:
    ```shell
    docker-compose up aasx-server-idta
    ```
2. Verify the server status and results by navigating to the following URL in your web browser:
    [http://localhost:5001](http://localhost:5001)

## AAS Client 
The client **simulates** gateway edge device configuration with internal Database and sync with AAS server.

### Configuring the Docker Image for Your Architecture

To set up the client image tailored for your system's architecture, update the `docker-compose.yaml` file. You have three architectural options to select from:

- **amd64**: `manhlinh210/aas_edge_client-web:amd64-1.0.2`
  
- **arm32v7**: `manhlinh210/aas_edge_client-web:arm32v7-1.0.2`
  
- **arm64v8**: `manhlinh210/aas_edge_client-web:arm64v8-1.0.2`

### Configuring the ENV File

- Ensure that you substitute the placeholder with your variable (leave it as empty string if you dont want any text there)
    ```shell
    AAS_ID_Short=<your_device_AAS>

    SERVER_URL=<url_of_aasx_server>
    CLIENT_POLLING_INTERVAL=<seconds_between_each_poll_from_client>
    SERVER_POLLING_INTERVAL=<seconds_between_each_poll_from_server> 


    VENDOR_NAME=<your_company_name>
    VENDOR_LINK=<link_to_your_company_homepage>
    PRIMARY_COLOR=<color_of_header>
    TEXT_COLOR=<text_color>
    BUTTON_COLOR=<color_of_the_button>
    ```

- To update your logo, place your company's `logo.png` in the `vendor_images` folder and rename it to `vendorImages.png`.

TODO **If cloud server is used**, also update the env var for server URL

### Starting the AAS Client

1. Start the client using the following command:
    ```shell
    docker-compose up web
    ```
2. Check the client's functionality through the following URLs:

   - For NetworkConfiguration, visit:
     [http://localhost:18000/api/NetworkConfiguration/](http://localhost:18000/api/NetworkConfiguration/)
   
   **OR**
   
   - For SystemInformation, visit:
     [http://localhost:18000/api/SystemInformation/](http://localhost:18000/api/SystemInformation/)

3. Mounted script

There are mounted bash scripts to read device information (sysInfo.sh). Change the bash script if it is not working with your device.

### Using your own client GUI
The AAS client exposes REST API to manage the simulated device states for your GUI with REST client or scrpting with curl command.

- LastUpdate format is '%Y-%m-%dT%H:%M:%SZ'

Here are JSON examples for different endpoints:

- **PUT /api/NetworkConfiguration/**:
    ```json
        {
            "NetworkSetting": {
                "InterfaceEth0": {
                    "IPv4Address": "192.168.0.1",
                    "IPv4SubnetMask": "255.255.255.0",
                    "IPv4StandardGateway": "192.168.0.0",
                    "Name": "eth0",
                    "AddressMode": "Static",
                    "LinkSpeedReceiveTransmit": "1 Gbps",
                    "IPv4DNSServers": "8.8.8.8",
                    "PrimaryDNSSuffix": "example.com"
                },
                "InterfaceEth1": {
                    "IPv4Address": "192.168.1.100",
                    "IPv4SubnetMask": "255.255.255.0",
                    "IPv4StandardGateway": "192.168.1.0",
                    "Name": "eth1",
                    "AddressMode": "Automatic/DHCP",
                    "LinkSpeedReceiveTransmit": "10 Gbps",
                    "IPv4DNSServers": "8.8.8.8",
                    "PrimaryDNSSuffix": "example.com"
                }
            },
            "LastUpdate": "2023-10-19T15:28:51Z"
        }
    ```

- **PUT /api/SystemInformation/:**
    ```json
        {
            "Hardware": {
                "Processor": {
                    "CpuType": "ARMv8",
                    "CpuCores": "4",
                    "CpuClock": "1.8 GHz",
                    "CpuUsage": "17 %",
                    "CpuTemperature": "55 °C"
                },
                "Memory": {
                    "RAMInstalled": "2 GB",
                    "RAMFree": "729 MB",
                    "DiskInstalled": "17 GB",
                    "DiskFree": "14.3 GB"
                },
                "BoardTemperature": "42 °C"
            },
            "HealthStatus": "NORMAL",
            "LastUpdate": "2023-10-19T15:44:26Z" 
        }
    ```

### Logging

There are 2 logging files: django_access.log and django_error.log

Access these files through docker exec: 

```bash
docker exec -it <image_id> /bin/bash

tail -f logging/django_access.log

tail -f logging/django_error.log

```