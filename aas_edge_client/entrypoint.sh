# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver --noreload 0.0.0.0:18000

#!/bin/bash
set -e

# Run database migrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Start gunicorn
exec gunicorn aas_edge_client.wsgi:application --bind 0.0.0.0:18000 --log-file -
