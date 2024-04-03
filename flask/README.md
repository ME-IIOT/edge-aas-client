## Requirements
* MongoDB
* Docker 


## Setting Up Virtual Environment

To ensure a clean and isolated environment for this project, we recommend setting up a virtual environment using `venv`, `miniconda`, etc .

### Creating Virtual Environment

```bash
python3 -m venv venv
```

### Activating Virtual Environment (Linux) with ENV
In Linux, activate the virtual environment and set up environment variables by adding the following lines to the activation script located at venv/bin/activate:

```bash
set -a
source ./dev_aas_client.env
set +a
```

After adding these lines, you can activate the virtual environment using:

```bash
source venv/bin/activate
```

## Start Backend in python virtual env
If ENV is loaded in virtual env do the following. If not apply the virtual environment in file dev_aas_client.env

Start mongo db

Start Flask backend

```
python run.py
```

## Start in container environment

without frontend

```
cd docker_compose_package
docker-compose up
```
