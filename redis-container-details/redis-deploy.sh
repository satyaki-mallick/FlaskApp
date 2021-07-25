#!/bin/bash

# Comments:
# This script is written with the assumption that the machine running them has aws cli and docker installed.
# Make this script executable first using $ chmod +x auto_deploy.sh

# Pull and Run Redis docker image
docker run --name redis-container -d -p 6379:6379 redis


aws lightsail create-container-service --service-name redis-service --power micro --scale 1


aws lightsail push-container-image --service-name redis-service --label redis-container --image redis-container


aws lightsail create-container-service-deployment --service-name redis-service --containers file://containers.json --public-endpoint file://public-endpoint.json


# Check status
aws lightsail get-container-services --service-name flask-service