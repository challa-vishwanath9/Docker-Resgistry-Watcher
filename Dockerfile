FROM python:3.10-slim
# Install dependencies
RUN apt-get update && apt-get install -y curl

# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin

# Set working directory
WORKDIR /app

# Copy code
COPY docker_watcher.py .
COPY last_tag.json .

# Install Python dependencies
RUN pip install requests

# Command to run
CMD ["python", "docker_watcher.py"]
