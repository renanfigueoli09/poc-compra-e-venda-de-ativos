# Base image
FROM python:3.9.0
# Define environment variables
ENV PYTHONUNBUFFERED=1

# Define the working directory inside the container
WORKDIR /code

# Copy the entire application code into the container
COPY . /code

# Copy requirements file separately for caching
COPY requirements.txt /code/

# Upgrade pip to the specified version
RUN pip install pip==24.0

# Install Flower (monitoring tool for Celery)
RUN pip install flower

# Install project dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ntp
# Expose the Flower port (default is 5555, adjust if needed)
EXPOSE 5555
EXPOSE 5672
EXPOSE 15672

# Default command (can be overridden in docker-compose.yml)
CMD ["bash", "start.sh"]
