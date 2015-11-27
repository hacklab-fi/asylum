#!/bin/sh

# Force rebuild from start
# This will destroy ALL DOCKER CONTAINERS and remove intermediate images

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images | grep "^<none>" | awk '{ print $3 }')

