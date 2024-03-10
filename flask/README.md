## Setting Up Virtual Environment

To ensure a clean and isolated environment for this project, we recommend setting up a virtual environment using `venv`.

### Creating Virtual Environment

```bash
python3 -m venv venv
```

### Activating Virtual Environment (Linux)
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
