#!/bin/sh
set -e  # Exit on error

echo "Starting up..."
echo "Setting up directories..."

# Define path
DIRECTORY="domain" 

if [ -d "$DIRECTORY" ]; then
    chmod -R 755 "$DIRECTORY"
    chown -R 100:100 "$DIRECTORY"
else
    echo "Directory $DIRECTORY does not exist."
    exit 1
fi

echo "Running docker-compose..."

# Ensure docker-compose is available and run it
if command -v docker-compose >/dev/null 2>&1; then
    docker-compose up -d --build --force-recreate
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    docker compose up -d --build --force-recreate
else
    echo "docker-compose is not installed."
    exit 1
fi

echo "Done!"
