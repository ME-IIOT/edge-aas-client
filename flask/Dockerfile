# Use Python 3.10
ARG ARCH=
FROM python:3.10-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install system dependencies, including ca-certificates for HTTPS communication
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc ca-certificates build-essential python3-dev libffi-dev bc sysstat procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire project directory into the container
COPY . .

# Expose the port the app runs on
EXPOSE 18000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=18000"]
