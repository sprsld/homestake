# Use the official Python image from the Docker Hub
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY homestake/ ./homestake/
COPY tests/ ./tests/

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["fastapi", "run", "homestake/main.py"]
