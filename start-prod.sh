#!/bin/bash
# Start script for production deployment of Fuelix

# Exit on any error
set -e

echo "Fuelix Production Deployment Script"
echo "-----------------------------------"

# Check if docker and docker-compose exist
if ! command -v docker >/dev/null 2>&1; then
    echo "Error: docker is required but not installed."
    exit 1
fi

if ! command -v docker-compose >/dev/null 2>&1; then
    echo "Error: docker-compose is required but not installed."
    exit 1
fi

# Determine if .env file exists. Provide warning if not.
if [ ! -f ".env" ]; then
    echo "Warning: .env file missing in production. We will use defaults or .env.example values if applicable."
    echo "Copying .env.example to .env for you. PLEASE CHANGE THESE CREDENTIALS."
    cp .env.example .env
fi

# Stop existing containers just in case
echo "Bringing down any existing containers..."
docker-compose -f docker-compose.prod.yml down

# Run the build
echo "Building full production stack..."
docker-compose -f docker-compose.prod.yml build

# Start the stack
echo "Starting application..."
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "Deployment successful."
echo "Application running on:"
echo "Frontend: http://localhost"
echo "API Backend: http://localhost/api/v1 (Proxied)"
echo ""
echo "If running on a VPS or cloud droplet, replace localhost with your public IP/domain."
