#!/bin/sh
set -e  # Exit on error

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root. Please use sudo."
    exit 1
fi

echo "Shutting down Docker services..."

# Define the directory where the socket files are stored
SOCKET_DIRECTORY="shared"

# Stop docker-compose services
if command -v docker-compose >/dev/null 2>&1; then
    echo "Stopping services using docker-compose..."
    docker-compose down
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    echo "Stopping services using Docker Compose v2..."
    docker compose down
else
    echo "docker-compose is not installed."
    exit 1
fi

echo "Cleaning up socket directory..."
if [ -d "$SOCKET_DIRECTORY" ]; then
    # Remove the socket directory or its contents
    rm -rf "$SOCKET_DIRECTORY"/*
    echo "Socket directory cleaned."
else
    echo "Socket directory does not exist. No need to clean."
fi

echo "All services stopped and cleaned up successfully!"
