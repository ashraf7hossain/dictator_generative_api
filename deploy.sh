#!/bin/bash

# Stop the running Docker containers
cd ./generative_api
echo "Stopping running containers..."
docker-compose down

# Pull the latest changes from the GitHub repository
echo "Pulling the latest code from GitHub..."
git pull origin master

# Rebuild the Docker images and start the containers
echo "Building and starting containers..."
docker-compose up --build -d

# Check the status of the containers
echo "Checking the status of the containers..."
docker-compose ps

echo "Deployment completed successfully!"
