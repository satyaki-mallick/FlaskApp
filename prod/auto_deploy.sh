#!/bin/bash

# Comments:
# This script is written with the assumption that the machine running them has aws cli and docker installed.
# Make this script executable first using $ chmod +x auto_deploy.sh


# Create docker container
docker build -t flask-container .

# Run docker container
docker run -p 5000:5000 -e PYTHONUNBUFFERED=1 -d flask-container


# Run below command only first time to create container in Lightsail
#aws lightsail create-container-service --service-name flask-service --power micro --scale 1


# Push container image to lightsail
aws lightsail push-container-image --service-name flask-service --label flask-container --image flask-container


# Deploy Service
aws lightsail create-container-service-deployment --service-name flask-service --containers file://containers.json --public-endpoint file://public-endpoint.json


# After running above command, run below command to check "nextDeployment:state"(should be ACTIVE) and find the public URL
# aws lightsail get-container-services --service-name flask-service