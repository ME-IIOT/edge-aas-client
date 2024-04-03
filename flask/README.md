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
If ENV is loaded in virtual env do the following. If not apply the virtual environment in file dev_aas_client.env (for windows see this https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-powershell-1.0/ff730964(v=technet.10)?redirectedfrom=MSDN)

Start mongo db

Start Flask backend

```
python run.py
```

## Start in container environment

### With published images

```
cd docker_compose_package
docker-compose up
```
### For development

1. rebuild image

docker-compose -f docker-compose.yaml build

2. run with built image

docker-compose -f docker-compose.yaml up

## Clean up everything
```
docker-compose down
```
