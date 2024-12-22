FROM python:3.13-slim

# Set the working directory
WORKDIR /workspaceFS

# Switch to root user to install packages
USER root

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    git \
    sudo \
    curl \
    cmake \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set root password (not recommended for production)
RUN echo 'root:1234567' | chpasswd

# Create non-root user and set password
RUN useradd -m vscode && \
    echo 'vscode:123456' | chpasswd && \
    adduser vscode sudo

# Switch to the non-root user
USER vscode

# Copy requirements and install Python packages
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Expose the application port
EXPOSE 8000

# Copy the application code
COPY . /workspaceFS

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]