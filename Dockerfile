# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    g++ \
    clang \
    libopenblas-dev

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install llama-cpp-python
RUN pip install llama-cpp-python
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application runs on (if applicable)
EXPOSE 8000

# Command to run your application
CMD ["python", "app.py"]