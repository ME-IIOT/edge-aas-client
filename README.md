# AASX Server & Client Guide

This document provides straightforward steps to set up and run the AASX Server (IDTA) and AAS Client using Docker. Ensure your AASX package is located under the `aasxs` folder before you begin.

## AASX Server - IDTA (Local Setup)

### Starting the AASX Server

1. Use the following command to start the server:
    ```shell
    docker-compose up aasx-server-idta
    ```
2. Verify the server status and results by navigating to the following URL in your web browser:
    [http://localhost:5001](http://localhost:5001)

## AAS Client 

### Configuring the ENV File

- Ensure that you substitute the placeholder with your actual device AAS identifier:
    ```shell
    AAS_ID_Short=<your_device_AAS>
    ```

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
