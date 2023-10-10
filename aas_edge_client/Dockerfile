# Use Python 3.10.9
FROM python:3.10.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose port
EXPOSE 18000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:18000", "aas_edge_client.wsgi:application"]
