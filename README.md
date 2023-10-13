# AASX Server & Client Guide

This document provides straightforward steps to set up and run the AASX Server (IDTA) and AAS Client using Docker. Ensure your AASX package is located under the `aasxs` folder before you begin.
TODO Demo aasx file v004 is provided in this repo aasx folder.
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
    ```
TODO **If cloud server is used**, also update the env var for server URL

### Starting the AAS Client

1. Start the client using the following command:
    ```shell
    docker-compose up web
    ```
2. Check the client's functionality through the following URLs:

   - For NetworkConfiguration/NetworkSetting SMC, visit:
     [http://localhost:18000/api/interfaces/](http://localhost:18000/api/interfaces/)
   
   **OR**
   
   - For SystemInformation/Hardware SMC, visit:
     [http://localhost:18000/api/hardware/](http://localhost:18000/api/hardware/)

### Using your own client GUI
The AAS client exposes REST API to manage the simulated device states for your GUI with REST client or scrpting with curl command.

- Get/Set IP: TODO
- TODO
