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

### Configuring the ENV File

- Ensure that you substitute the placeholder with your actual device AAS identifier:
    ```shell
    AAS_ID_Short=<your_device_AAS>
    VENDOR_NAME=<your_company_name>
    VENDOR_LINK=<link_to_your_company_homepage>
    PRIMARY_COLOR=<color_of_header>
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

### Using your own client GUI
The AAS client exposes REST API to manage the simulated device states for your GUI with REST client or scrpting with curl command.

- LastUpdate format is '%Y-%m-%dT%H:%M:%S'

Here are JSON examples for different endpoints:

- **PUT /api/NetworkConfiguration/**:
    ```json
        {
            "NetworkSetting": {
                "InterfaceEth0": {
                    "IPv4Address": "192.168.0.1",
                    "IPv4SubnetMask": "255.255.255.0",
                    "IPv4StandardGateway": "192.168.0.0",
                    "HostName": "eth0",
                    "AddressModus": "Static",
                    "LinkSpeedReceiveTransmit": "1 Gbps",
                    "IPv4DNSServers": "8.8.8.8",
                    "PrimaryDNSSuffix": "example.com"
                },
                "InterfaceEth1": {
                    "IPv4Address": "192.168.1.100",
                    "IPv4SubnetMask": "255.255.255.0",
                    "IPv4StandardGateway": "192.168.1.0",
                    "HostName": "eth1",
                    "AddressModus": "Automatic/DHCP",
                    "LinkSpeedReceiveTransmit": "10 Gbps",
                    "IPv4DNSServers": "8.8.8.8",
                    "PrimaryDNSSuffix": "example.com"
                }
            },
            "LastUpdate": "2023-10-19T15:28:51"
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
            "LastUpdate": "2023-10-19T15:44:26" 
        }
    ```
