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
    curl \
    libopenblas-dev

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install llama-cpp-python
RUN pip install --no-cache-dir llama-cpp-python==0.2.85 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu122
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama serve & sleep 5 && ollama pull qwen2.5 # Wait a few seconds for Ollama to start
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application runs on (if applicable)
EXPOSE 8000

# Command to run your application
CMD ollama serve & python app.py