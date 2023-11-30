# Use Python 3.10
ARG ARCH=
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies, including ca-certificates for HTTPS communication
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev iproute2 procps ca-certificates redis-server && \
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

# Command to migrate & run the application
CMD ["bash", "entrypoint.sh"]
