#!/bin/bash

# navigate to the project directory
cd ./dictator_generative_api
echo "Changing directory to dictator_generative_api...$PWD"

# Pull the latest changes from the GitHub repository
echo "Pulling the latest code from GitHub..."
git pull origin master

# Stop the running Docker containers
cd ./generative_api
echo "Stopping running containers..."
docker-compose down

# Rebuild the Docker images and start the containers
echo "Building and starting containers..."
docker-compose up --build -d

# Check the status of the containers
echo "Checking the status of the containers..."
docker-compose ps

echo "Deployment completed successfully!"
